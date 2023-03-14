"""本模块定义插件对象。

FrontMatter:
    sidebar_position: 3
    description: nonebot.plugin.plugin 模块
"""
from types import ModuleType
from dataclasses import field, dataclass



@dataclass(eq=False)
class Plugin:
    """插件元信息，由插件编写者提供"""

    name: str
    """插件可阅读名称"""
    description: str
    """插件功能介绍"""
    usage: str
    """插件使用方法"""
    config: list
    """插件配置项"""