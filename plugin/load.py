from pathlib import Path
from plugin.manager import BaseManager
from plugin.utils import path_to_module_name
from plugin.plugin import Plugin
from typing import Set, Dict, Type, Optional,Union


class PluginManager(BaseManager):
    def __init__(self):
        super().__init__()

    def load_plugin(self, module_path: Union[str, Path]) -> Optional[Plugin]:
        """加载单个插件
        """
        module_path = (
            path_to_module_name(module_path)
            if isinstance(module_path, Path)
            else module_path
        )
        return self._load_plugin(module_path)


    def load_plugins(self) -> Set[Plugin]:
        """导入文件夹下多个插件，以 `_` 开头的插件不会被导入!
        参数:
            plugin_dir: 文件夹路径
        """
        return self.load_all_plugins()
