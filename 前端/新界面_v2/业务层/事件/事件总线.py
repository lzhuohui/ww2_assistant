# -*- coding: utf-8 -*-
"""
模块名称：EventBus
设计思路: 提供模块间通信的事件机制
模块隔离: 事件层独立，支持松耦合通信
"""

from typing import Dict, Any, Callable, List
from dataclasses import dataclass
from enum import Enum


# *** 用户指定变量 - AI不得修改, 变量值必须生效 ***
# （用户未指定变量）
# *********************************


class EventType(Enum):
    """事件类型枚举"""
    CONFIG_CHANGED = "config_changed"
    THEME_CHANGED = "theme_changed"
    PAGE_SWITCHED = "page_switched"
    EXPORT_COMPLETED = "export_completed"
    ERROR_OCCURRED = "error_occurred"


@dataclass
class Event:
    """事件数据类"""
    event_type: EventType
    data: Dict[str, Any]
    source: str = ""


class EventBus:
    """事件总线 - 模块间通信"""
    
    _instance = None
    
    @classmethod
    def reset_instance(cls):
        """重置单例实例（用于测试或内存释放）"""
        cls._instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        
        self._listeners: Dict[EventType, List[Callable]] = {}
        self._initialized = True
    
    def subscribe(self, event_type: EventType, listener: Callable) -> None:
        """订阅事件"""
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(listener)
    
    def unsubscribe(self, event_type: EventType, listener: Callable) -> None:
        """取消订阅"""
        if event_type in self._listeners:
            if listener in self._listeners[event_type]:
                self._listeners[event_type].remove(listener)
    
    def clear_all_listeners(self) -> None:
        """清理所有监听器（用于内存释放）"""
        self._listeners.clear()
    
    def publish(self, event: Event) -> None:
        """发布事件"""
        if event.event_type in self._listeners:
            for listener in self._listeners[event.event_type]:
                try:
                    listener(event)
                except Exception as e:
                    print(f"事件处理失败: {e}")
    
    def publish_config_changed(self, page_id: str, card_id: str, config_key: str, value: Any) -> None:
        """发布配置变更事件"""
        event = Event(
            event_type=EventType.CONFIG_CHANGED,
            data={
                "page_id": page_id,
                "card_id": card_id,
                "config_key": config_key,
                "value": value,
            },
            source="ConfigService",
        )
        self.publish(event)
    
    def publish_theme_changed(self, theme_name: str) -> None:
        """发布主题变更事件"""
        event = Event(
            event_type=EventType.THEME_CHANGED,
            data={"theme_name": theme_name},
            source="ThemeService",
        )
        self.publish(event)
    
    def publish_page_switch(self, page_name: str) -> None:
        """发布界面切换事件"""
        event = Event(
            event_type=EventType.PAGE_SWITCHED,
            data={"page_name": page_name},
            source="MainInterface",
        )
        self.publish(event)
