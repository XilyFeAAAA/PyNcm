from enum import Enum
from plugin import Plugin


class Event:
    """事件类"""
    def __init__(self,  
                 name, 
                 type_,
                 keep=False, 
                 data=None) -> None:

        self.name: str = name
        """事件名称"""

        self.type_: str = type_
        """事件类型"""
        
        self.data: list = data
        """事件信息"""
        
        self.keep = keep
        """保留"""

    def __str__(self) -> str:
        return f"{self.name} - {self.priority}"

