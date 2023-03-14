import asyncio
from .process import apiProcess
from .download import *
from plugin import Plugin
from matcher import *

__name__ = ''
__plugin__ = Plugin(
    name='ncmApi',
    description='运行 NeteaseCloudMusicApi 的插件',
    usage='',
    config=None
)

boot = on_app(mode=True, plugin=__plugin__)
shut = on_app(mode=False, plugin=__plugin__)
api = apiProcess()

@boot.handle(priority=2)
async def run(event):
    await api.start()

@shut.handle(priority=2)
async def stop(event):
    await api.stop()