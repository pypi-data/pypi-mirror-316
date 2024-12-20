import asyncio
import logging
import signal
import time
import traceback
import uuid
import os
from concurrent.futures import ThreadPoolExecutor
from functools import wraps
from multiprocessing import current_process, Pool
from typing import Callable, Dict

import math
import redis
from croniter import croniter
from flask import Flask, current_app
from werkzeug.utils import import_string, find_modules
from redis import asyncio as aioredis

from flask_redis_stream_pubsub import util

RESET = '\033[0m'

logger = logging.getLogger("pubsub")
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logger.level)

formatter = logging.Formatter(f"[%(asctime)s] PUBSUB %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)

SCHEDULER_PIPE_BUFFER_SIZE = 20
SCHEDULER_INTERVAL = 0.2
SCHEDULER_JOB_STREAM_MAX_LEN = 256
SCHEDULER_LOCK_EX = 7

CONSUMER_RETRY_LOOP_INTERVAL = 3
CONSUMER_TASK_SPLIT_THRESHOLD = 20


def _thread_excute(fc, msg):
    if current_process().thread_pool is None:
        fc(msg)
    else:
        current_process().thread_pool.submit(fc, msg)


class Msg:
    __slots__ = ['stream_name', 'id', 'group_name', 'payload', 'consumer_name', 'retry_count']

    def __init__(self, stream_name, id, group_name, payload: Dict, consumer_name, retry_count=0):
        self.stream_name = stream_name
        self.id = id
        self.group_name = group_name
        self.payload: dict = payload
        self.consumer_name = consumer_name
        self.retry_count = retry_count

    def __str__(self):
        return f"Msg({self.consumer_name}-{self.id}-{self.stream_name}-{self.payload}-{self.group_name}-{self.retry_count})"

    @property
    def source(self) -> str:
        if '__SOURCE' in self.payload:
            return self.payload['__SOURCE']
        return ''

    @property
    def publish_time(self) -> int:
        if '__PUBLISH_TIME' in self.payload:
            return int(self.payload['__PUBLISH_TIME'])
        return 0


class Consumer:

    def __init__(self,
                 consumer_name: str,
                 group='',
                 processes=1,
                 threads=1,
                 retry_count=64,
                 timeout_second=300,
                 block_second=6,
                 read_count=16,
                 noack=False,
                 config_prefix='PUBSUB_REDIS',
                 app_factory: str | Callable = None):

        self.app_factory = app_factory
        self.group = group
        self.timeout_mill = timeout_second * 1000
        self.block_mill = block_second * 1000
        self.read_count = read_count
        self.rcli = None
        self.processes = processes
        self.threads = threads
        self.retry_count = retry_count
        self.consumer_name = consumer_name
        self.noack = noack

        self.__runing = True
        self.__call_map = {}
        self.xgroup_check = None
        self.process_pool = None

        self.config_prefix = config_prefix
        self.redis_url = ''

    def init_obj(self, obj):
        if isinstance(obj, str):
            obj = import_string(obj)

        cfg = {}
        for key in dir(obj):
            if key.isupper():
                cfg[key] = getattr(obj, key)

        redis_url = cfg.get(
            "{0}_URL".format(self.config_prefix), "redis://localhost:6379/0"
        )
        self.redis_url = redis_url
        self.__init_config(cfg)

    def init_app(self, app: Flask):
        redis_url = app.config.get(
            "{0}_URL".format(self.config_prefix), "redis://localhost:6379/0"
        )
        self.redis_url = redis_url

        cfg = app.config.get(f'{self.config_prefix}_OPTION')

        if not cfg:
            return

        self.__init_config(cfg)

    def __init_config(self, cfg):
        if 'group' in cfg:
            self.group = cfg['group']
        if 'processes' in cfg:
            self.processes = cfg['processes']
        if 'threads' in cfg:
            self.threads = cfg['threads']
        if 'retry_count' in cfg:
            self.retry_count = cfg['retry_count']
        if 'timeout_second' in cfg:
            self.timeout_mill = int(cfg['timeout_second']) * 1000
        if 'block_second' in cfg:
            self.block_mill = int(cfg['block_second']) * 1000
        if 'read_count' in cfg:
            self.read_count = cfg['read_count']
        if 'noack' in cfg:
            self.noack = cfg['noack']

        if 'app_factory' in cfg:
            self.app_factory = cfg['app_factory']

    def import_module(self, module: str):
        for name in find_modules(module, recursive=True, include_packages=False):
            import_string(name)

    def subscribe(self, stream: str, timeout: float = None, retry_count: int = None, cron: str = None):
        if retry_count is None:
            retry_count = self.retry_count

        def decoration(f):
            if stream in self.__call_map:
                raise RuntimeError(f'{stream} Already exists of subscribes')

            module = __import__(f.__module__, fromlist=[''])
            name = f.__name__

            if cron is None:
                self.__call_map[stream] = {
                    'module': module,
                    'name': name,
                    'type': 'subscribe',
                    'timeout': timeout,
                    'retry_count': retry_count,
                }
            else:
                if not croniter.is_valid(cron):
                    raise RuntimeError(f'{stream} cron It is invalid by {cron}')

                self.__call_map[stream] = {
                    'module': module,
                    'name': name,
                    'type': 'cron',
                    'cron': cron,
                    'iter': croniter(cron, second_at_beginning=True),
                    'stream': stream,
                    'timeout': timeout,
                    'retry_count': retry_count,
                }

            @wraps(f)
            def wrapper(*args, **kwargs):
                with current_process().app.app_context():
                    ack = False
                    try:
                        msg = args[0]
                        f(*args, **kwargs)
                        ack = True
                    except Exception as e:
                        ack = False
                        current_app.logger.error(f'\033[91m{traceback.format_exc()}')
                        raise e
                    finally:
                        if current_process().noack:
                            return

                        cli = current_process().rcli
                        if retry_count <= 0:
                            ack = True
                        if ack:
                            cli.xack(msg.stream_name, msg.group_name, msg.id)

            return wrapper

        return decoration

    def run(self, app_factory: str | Callable = None, **kwargs):
        try:
            from uvloop import run
            logger.info(f'PID({os.getpid()}) {'\033[1m'}uvloop runing...{RESET}')
        except ImportError:
            from asyncio import run
            logger.info(f'PID({os.getpid()}) {'\033[1m'}eventloop runing...{RESET}')

        run(self.run_async(app_factory, **kwargs))

    async def run_async(self, app_factory: str | Callable = None, **kwargs):
        redis_url = kwargs.get('redis_url')
        group = kwargs.get('group')
        processes = kwargs.get("processes")
        threads = kwargs.get("threads")
        retry_count = kwargs.get("retry_count")
        timeout_second = kwargs.get("timeout_second")
        block_second = kwargs.get("block_second")
        read_count = kwargs.get("read_count")
        noack = kwargs.get("noack")
        config_prefix = kwargs.get("config_prefix")

        if redis_url:
            self.redis_url = redis_url
        if group:
            self.group = group
        if processes:
            self.processes = processes
        if threads:
            self.threads = threads
        if retry_count:
            self.read_count = retry_count
        if timeout_second:
            self.timeout_mill = int(timeout_second) * 1000
        if block_second:
            self.block_mill = int(block_second) * 1000
        if read_count:
            self.read_count = read_count
        if config_prefix:
            self.config_prefix = config_prefix
        if noack is not None:
            self.noack = noack

        if app_factory is None:
            app_factory = self.app_factory

        self.process_pool = Pool(processes=self.processes,
                                 initializer=self.__init_process, initargs=(app_factory, self.threads, self.noack))
        self.rcli = aioredis.from_url(self.redis_url, decode_responses=True)

        __fix_call_map = {}
        job_list = []

        for k, v in self.__call_map.items():
            __fix_call_map[k] = {
                'fc': getattr(v['module'], v['name']),
                'timeout': v['timeout'],
                'retry_count': v['retry_count'],
            }

            try:
                await self.rcli.xgroup_create(name=k, groupname=self.group, id='0', mkstream=True)
            except redis.exceptions.ResponseError:
                pass

            if v['type'] == 'cron':
                job_list.append(v)

        if not __fix_call_map:
            raise RuntimeError('Not subscribe')

        parts = math.ceil(len(__fix_call_map) / CONSUMER_TASK_SPLIT_THRESHOLD)
        call_map_groups = util.split_dict(__fix_call_map, parts)

        tasks = []
        for __call_map in call_map_groups:
            tasks.append(self.__xread(__call_map))

            if self.noack == False:
                tasks.append(self.__retry(__call_map))

        if job_list:
            tasks.append(self.__scheduler(job_list))

        logger.info(
            f"PID({os.getpid()}) {'\033[94m'}Parameters: processes={self.processes},threads={self.threads},consumer_name={self.consumer_name},group_id={self.group}{RESET}")
        logger.info(
            f"PID({os.getpid()}) {'\033[96m'}Discovery of subscribers: {",".join(__fix_call_map.keys())}{RESET}")

        def __shutdown(signum, frame):
            self.__runing = False
            logger.warning(
                f"PID({os.getpid()}) {'\033[93m'}Listen signum:{signum}, Start to shutdown...PID({os.getpid()}){RESET}")

        signal.signal(signal.SIGINT, __shutdown)
        signal.signal(signal.SIGTERM, __shutdown)

        await asyncio.gather(*tasks)

        self.process_pool.terminate()
        self.process_pool.join()

        logger.info(f"PID({os.getpid()}) {'\033[92m'}Shutting down consumer successfully PID({os.getpid()}){RESET}")

    async def __retry(self, fix_call_map):
        while self.__runing:
            async with self.rcli.pipeline() as pipe:
                stream_list = []
                for k, val in fix_call_map.items():
                    _timeout_mill = self.timeout_mill
                    _opt_timeout = val['timeout']

                    if _opt_timeout:
                        _timeout_mill = int(float(_opt_timeout) * 1000)

                    _retry_count = val['retry_count']
                    stream_list.append({
                        'name': k,
                        'retry_count': _retry_count,
                        'timeout_mill': _timeout_mill,
                    })
                    await pipe.xpending_range(k, self.group, "0", "+",
                                              count=self.read_count, idle=_timeout_mill)

                res = await pipe.execute()

            call_count = 0
            for i in range(len(res)):
                message_ids = []
                message_del_ids = []
                times_delivered_map = {}

                stream_dict = stream_list[i]
                name = stream_dict['name']
                retry_count = stream_dict['retry_count']
                timeout_mill = stream_dict['timeout_mill']

                for d in res[i]:
                    if d['times_delivered'] > retry_count:
                        message_del_ids.append(d['message_id'])
                    else:
                        mid = d['message_id']
                        message_ids.append(mid)
                        times_delivered_map[mid] = d['times_delivered']

                if message_del_ids:
                    await self.rcli.xack(name, self.group, *message_del_ids)

                if message_ids and name in fix_call_map:
                    call = fix_call_map[name]['fc']
                    xmsgs = await self.rcli.xclaim(name, self.group,
                                                   self.consumer_name, timeout_mill, message_ids)

                    for msg in xmsgs:
                        id = msg[0]
                        payload = msg[1]
                        times_delivered = times_delivered_map[id]

                        _msg = Msg(name, id, self.group, payload,
                                   self.consumer_name, retry_count=times_delivered)

                        self.process_pool.apply_async(_thread_excute, (call, _msg,))

                        call_count += 1

            if call_count > 0:
                await asyncio.sleep(0)
            else:
                await asyncio.sleep(CONSUMER_RETRY_LOOP_INTERVAL)

    async def __xread(self, fix_call_map):
        streams = {key: ">" for key in fix_call_map.keys()}

        while self.__runing:
            rets = await self.rcli.xreadgroup(self.group, self.consumer_name, streams,
                                              count=self.read_count, block=self.block_mill,
                                              noack=self.noack)
            for ret in rets:
                stream = ret[0]
                if stream not in fix_call_map:
                    current_app.logger.error(f'{stream} not in call funcs')
                    continue

                for msg in ret[1]:
                    id = msg[0]
                    payload = msg[1]

                    _msg = Msg(stream, id, self.group, payload, self.consumer_name)

                    call = fix_call_map[stream]['fc']

                    self.process_pool.apply_async(_thread_excute, (call, _msg,))

    async def __job_pipe_xadds(self, jobs):
        async with self.rcli.pipeline() as pipe:
            for j in jobs:
                key = f'{j["stream"]}_{j["next_time"]}'
                uid = str(uuid.uuid4()).replace("-", "").upper()
                await pipe.set(f'{key}', uid, ex=SCHEDULER_LOCK_EX, nx=True)

            res = await pipe.execute()

            xcount = 0
            for i in range(len(jobs)):
                if res[i]:
                    job = jobs[i]
                    payload = {
                        '__PUBLISH_TIME': int(time.time() * 1000),
                        '__SOURCE': 'cron',
                    }
                    await pipe.xadd(job['stream'], payload, maxlen=SCHEDULER_JOB_STREAM_MAX_LEN)
                    xcount += 1

            if xcount > 0:
                await pipe.execute()

            return xcount

    async def __scheduler(self, jobs):
        __jobs = []

        start_time = time.time()
        for job in jobs:
            __jobs.append({
                'iter': job['iter'],
                'stream': job['stream'],
                'last_time': int(job['iter'].get_next(start_time=start_time)),
            })

        while self.__runing:
            current_time = time.time()
            zjobs = []

            for job in __jobs:
                _next_time = int(job['iter'].get_next(start_time=current_time))

                if job['last_time'] != _next_time:
                    zjobs.append({
                        'stream': job["stream"],
                        'next_time': _next_time,
                    })
                    job['last_time'] = _next_time

            if zjobs:
                chunkd_jobs = util.chunk_array(zjobs, SCHEDULER_PIPE_BUFFER_SIZE)
                await asyncio.gather(*map(self.__job_pipe_xadds, chunkd_jobs))

            await asyncio.sleep(SCHEDULER_INTERVAL)

    def __init_process(self, app_factory: str | Callable, threads: int, noack: bool):
        app: Flask
        if isinstance(app_factory, str):
            app = import_string(app_factory)
        elif callable(app_factory):
            app = app_factory()
        else:
            raise RuntimeError("flask app is not initialization")

        if app is None:
            raise RuntimeError("flask app is not initialization")

        redis_url = app.config.get(
            "{0}_URL".format(self.config_prefix), "redis://localhost:6379/0"
        )

        rcli = redis.from_url(redis_url, decode_responses=True)

        current_process().rcli = rcli
        current_process().app = app
        current_process().noack = noack

        thread_pool = None
        if threads > 1:
            thread_pool = ThreadPoolExecutor(max_workers=threads, thread_name_prefix='PUBSUB')
            current_process().thread_pool = thread_pool

        def shutdown(signum, frame):
            if thread_pool is not None:
                thread_pool.shutdown()

        signal.signal(signal.SIGTERM, shutdown)


def runs(*consumers: Consumer, app_factory: str | Callable = None):
    if len(consumers) == 0:
        raise RuntimeError("consumers cannot be empty")

    plist = []

    from multiprocessing import Process

    for c in consumers:
        p = Process(target=c.run, args=(app_factory,))
        plist.append(p)
        p.start()

    def shutdown(signum, frame):
        for p in plist:
            p.terminate()

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    for p in plist:
        p.join()
