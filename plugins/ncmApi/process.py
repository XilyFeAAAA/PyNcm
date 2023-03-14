import os
import sys
import asyncio
import subprocess
import time
import psutil
from loguru import logger
from pathlib import Path
from itertools import count
from threading import Thread
from matcher import Event, matchers

class apiProcess(object):
    def __init__(
            self,
            port: int = 3000,
            kill_timeout: float = 5,
            stop_timeout: float = 6,
            restart_interval: float = 4,
            max_restart_count: int = 2,
            print_process_log: bool = True,
            post_delay: float = 3) -> None:
        self.port:int = port
        self.login_state: bool = False
        # self.logger: Logger = Logger()
        self.restart_interval: float = restart_interval  # 重启间隔时间
        self.kill_timeout: float = kill_timeout  # kill的超时
        self.stop_timeout: float = stop_timeout  # stop的超时
        self.print_process_log: bool = print_process_log  # 是否打印日志
        self.post_delay: float = post_delay  # post的延迟
        self.max_restart_count: int = max_restart_count  # 最大重连次数
        self.thread_running: bool = False  # 线程是否在运行
        self.cwd: Path = Path(__file__).parent / 'NeteaseCloudMusicApi-4.8.9'  # cwd路径
        # self.DATA_PATH: Path = self.cwd / "app.js"  # app.js路径
        self.process: subprocess.Popen = None

    def _process_executor(self) :
        # 子进程运行api
        st = subprocess.STARTUPINFO()
        st.dwFlags = subprocess.STARTF_USESHOWWINDOW
        st.wShowWindow = subprocess.SW_HIDE
        self.process = subprocess.Popen(
            ['node', 'app.js'],
            cwd=self.cwd.absolute(),
            text=False,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            startupinfo=st,
        )
        out = self.process.stdout.read()
        print('out:',out)
        if self.process.poll() is None:
            self._terminate_process(self.process, timeout=self.post_delay)
        return self.process.returncode

    def _process_worker(self):
        for restart in count():
            if not self.thread_running:
                break  # 如果没进入进程，退出
            if self.max_restart_count >= 0 and restart > self.max_restart_count:
                break  # 不是无限重连切超过次数，退出
            code = None
            try:
                code = self._process_executor()
            except Exception as e:
                # log
                logger.error(f"Thread {self.thread!r} raised an unknown exception: {e}")
            logger.warning(f"Process for ncm api exited with code {code}")
            logger.warning("retrying to restart...")
            logger.warning(f"{restart}/{self.max_restart_count}")
            # 重连间隔
            time.sleep(self.restart_interval)

    def _terminate_process(self, process: subprocess.Popen, timeout: float):
        process.terminate()
        try:
            return process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            # 超时直接kill
            process.kill()

    def _find_duplicate_process(self):
        net_con = psutil.net_connections()
        for con_info in net_con:
            if con_info.laddr.port == self.port:
                puuid = con_info.pid
                if puuid: psutil.Process(puuid).terminate()
                break
        return
    
    async def start(self) -> bool:
        # 服务已经在运行
        logger.info('Loading NeteaseMusicApi.')
        if self.thread_running:
            return False
        # 判断进程是否打开
        self._find_duplicate_process()
        self.thread_running = True
        self.thread = Thread(target=self._process_worker, daemon=True)
        self.thread.name = "daemon-thread-ncm"
        self.thread.start()
        await asyncio.sleep(self.post_delay)
        logger.success('NeteaseMusicApi loaded successfully!')
        matchers.send(Event(
            name='NeteaseMusicApi Loaded',
            type_='apiRun',
            keep=True
        ))
        # logger.info('Event NcmApiStart broadcasting.')
        return self.login_state and self.thread_running

    async def stop(self):
        logger.info('Closing NeteaseMusicApi.')
        self.thread_running = False
        self.login_state = False
        if self.process is not None:
            self._terminate_process(self.process, self.post_delay)
        if self.thread and self.thread.is_alive():
            self.thread.join(self.stop_timeout)
            self.thread = None
        logger.success('NeteaseMusicApi closed successfully!')
        matchers.send(Event(
            name='NeteaseMusicApi closed',
            type_='apiClose',
            keep=True
        ))
        # logger.info('Event NcmApiStart broadcasting.')