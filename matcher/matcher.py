from loguru import logger
from .event import Event
from plugin.plugin import Plugin
from typing import Optional, List, Callable, Any, DefaultDict

class Matcher:
    def __init__(self,
                 type_: str,
                 disposable: bool = False,
                 plugin: Plugin = None) -> None:

        self._type_: str = type_
        """事件响应器类型"""
        self._handlers: DefaultDict[int, List] = {}
        """事件响应器拥有的事件处理函数列表"""
        """事件响应器优先级"""
        self._disposable: bool = disposable
        """事件响应器是否为临时"""
        self._plugin: Optional["Plugin"] = plugin
        """事件响应器所在插件"""

    @property
    def disposable(self):
        return self._disposable


    def _append_handler(self, priority, handle) -> None:
        """添加事件处理"""
        if priority in self._handlers.keys():
            self._handlers[priority].append(handle)
        else:
            self._handlers[priority] = [handle]
        logger.info(f'register a new handle on Matcher {self._type_}')


    def _remove_handler(self, handle) -> None:
        """移除事件处理"""
        if handle not in self._handlers:
            raise RuntimeError(f"Event {handle.__name__} doesn't exist!")
        self._handlers.remove(handle)
    
    def handle(self, priority: int = 1) -> Callable[..., Any]:
        """事件装饰器, 将handle添加到事件处理器中"""      
        def wrap(func)-> Callable[..., Any]:
            self._append_handler(priority, func)
            def inner(*args, **kwargs):
                return func(*args, **kwargs)
            return inner
        return wrap

    async def run(self, event: Event) -> None:
        for handles in self._handlers.values():
            try:
                [await handle(event) for handle in handles]
            except Exception as e:
                print(e)
                logger.error(f"there are problems when handling the event on matcher {self._type_}")