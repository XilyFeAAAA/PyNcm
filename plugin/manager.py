import importlib
import threading
import time

from loguru import logger
from pathlib import Path
from typing import TYPE_CHECKING, Any, Set, Dict, Type, Optional, List
from plugin.plugin import Plugin


class BaseManager:
    """插件管理器"""

    def __init__(self):
        super().__init__()
        self.plugins: list = []
        self.search_path = Path(__file__).parent.parent / 'plugins'

        # cache plugins
        self._available_plugin_names: Dict[str, Path] = {}

    def __repr__(self) -> str:
        return f"PluginManager(plugins={self.plugins}, search_path={self.search_path})"

    def init(self):
        for module in self.search_path.iterdir():
            if module.is_dir():
                self._available_plugin_names[module.name] = module

    @property
    def available_plugins(self) -> Set[str]:
        """返回当前插件管理器中可用的插件名称。"""
        return self._available_plugin_names

    def _load_plugin(self, name: str) -> Optional[Plugin]:
        """加载指定插件。
        对于独立插件，可以使用完整插件模块名或者插件名称。
        参数:
            name: 插件名称。
        """
        # try:
        if name in self._available_plugin_names:
            module = importlib.import_module(f'plugins.{name}')
        else:
            raise RuntimeError(f"Plugin not found: {name}! Check your plugin name")

        if (
                plugin := getattr(module, "__plugin__", None)
        ) is None or not isinstance(plugin, Plugin):
            raise RuntimeError(
                f"Module {module.__name__} is not loaded as a plugin! "
                "Make sure not to import it before loading."
            )
        logger.success(f'Succeeded to load plugin {plugin.name}')
        self.plugins.append(module)
        return plugin
        # except Exception as e:
        #     logger.error(f'Failed to import {name} raised an unknown exception: {e}')

    def load_all_plugins(self) -> Set[Plugin]:
        """加载所有可用插件。"""

        return set(
            filter(None, (self._load_plugin(name) for name in self.available_plugins))
        )

