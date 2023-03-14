import asyncio
import time
from .event import Event
from .matcher import Matcher
from threading import Thread
from queue import Queue, Empty
from loguru import logger
from collections import defaultdict
from plugin.plugin import Plugin
from typing import Type, Optional, KeysView, ValuesView, ItemsView, Iterator, List

class matcherManager:
    def __init__(self) -> None:
        
        self._eventQueue = Queue()
        """存放事件队列"""
        
        self._thread = Thread(target=self._Run)
        """事件处理线程"""
            
        self._active = False
        """事件开关"""

        self._provider: defaultdict[int,List[Type[Matcher]]] = {}
        """存放字典：事件 => 处理函数"""

        self._delay = 0.1
        """分发事件延迟"""

    def __repr__(self) -> str:
        return f"MatcherManager"

    def __contains__(self, _o) -> bool:
        return _o in self._provider
    
    def __iter__(self) -> Iterator:
        return iter(self._provider)
    
    def __len__(self) -> int:
        return len(self._provider)
    
    def __getitem__(self, key: int) ->  List[Type["Matcher"]]:
        return self._provider[key]
    
    def __setitem__(self, key: int, value: List[Type['Matcher']]) -> None:
        self._provider[key] = value

    def __delitem__(self, key: int) -> None:
        del self._provider[key]
    
    def keys(self) -> KeysView[int]:
        return self._provider.keys()

    def values(self) -> ValuesView[List[Type["Matcher"]]]:
        return self._provider.values()

    def items(self) -> ItemsView[int, List[Type["Matcher"]]]:
        return self._provider.items()

    def clear(self) -> None:
        self._provider.clear()

    def _Run(self) -> None:
        """分发事件函数"""
        while self._active:
            try:
                event = self._eventQueue.get(block = True, timeout = 1)
                # logger.info(f'检索到新事件 {event.name}')
                self._EventProcess(event)
            except Empty:
                pass
            time.sleep(self._delay)
    
    def _EventProcess(self, event) -> None:
        """事件处理函数"""
        if event.type_ in self._provider.keys():
            """取出对应事件的每一个Matcher类"""
            for matcher in self._provider[event.type_]:
                """临时响应器,使用后删除"""
                asyncio.run(matcher.run())
                if matcher.disposable:
                    self._provider[event.type_].remove(matcher)

            return
        """如果没有对应Matcher且event.keep=True则保留事件""" 
        if event.keep:
            self._eventQueue.put(event)

    def run(self) -> None:
        """启动"""
        self._active = True
        self._thread.start()

    def stop(self) -> None:
        """停止"""
        self._active = False
        self._thread.join()

    def new(
        self,
        type_: str = "",
        disposable: bool = False,
        priority: int = 1,
        plugin: Optional["Plugin"] = None,
    ) -> Type["Matcher"]:
        """
        创建一个新的事件响应器，并存储至 `matchers <#matchers>`_
        参数:
            type_: 事件响应器类型
            disposable: 是否为临时事件响应器，即触发一次后删除
            priority: 响应优先级
            plugin: 事件响应器所在插件
        """
        """存在Matcher则返回"""
        NewMatcher = Matcher(
                plugin = plugin,
                type_ =  type_,
                disposable = disposable,
                priority = priority,
        )
        if priority in self._provider.keys():
            self._provider[priority].append(NewMatcher)
        else:
            self._provider[priority] = [NewMatcher]
        logger.info(f'created a new matcher {type_} in matchers')
        return NewMatcher

    def destory(self, type_) -> None:
        """删除事件"""
        if type_ not in self._provider:
            raise RuntimeError(f'The event type={type_} has existed.')
        self._provider.pop(type_)


    def send(self, event: Event) -> None:
        """发送事件"""
        self._eventQueue.put(event)


