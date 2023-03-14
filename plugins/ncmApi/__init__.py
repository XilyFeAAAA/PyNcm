import asyncio
from .process import apiProcess
from .download import *
from plugin import Plugin

__name__ = ''
__plugin__ = Plugin(
    name='ncmApi',
    description='运行 NeteaseCloudMusicApi 的插件',
    usage='',
    config=None
)
