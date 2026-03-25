# -*- coding: utf-8 -*-
"""
模块名称：EventBus
模块功能：事件发布订阅机制
实现步骤：
- 支持事件订阅
- 支持事件发布
- 支持取消订阅
"""

from typing import Dict, List, Callable, Any


class EventBus:
    """事件总线 - 事件发布订阅"""
    
    def __init__(self):
        self._subscribers: Dict[str, List[Callable[[Any], None]]] = {}
    
    def subscribe(self, event_type: str, callback: Callable[[Any], None]) -> None:
        """订阅事件"""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        if callback not in self._subscribers[event_type]:
            self._subscribers[event_type].append(callback)
    
    def unsubscribe(self, event_type: str, callback: Callable[[Any], None]) -> None:
        """取消订阅"""
        if event_type in self._subscribers and callback in self._subscribers[event_type]:
            self._subscribers[event_type].remove(callback)
    
    def publish(self, event_type: str, data: Any = None) -> None:
        """发布事件"""
        if event_type in self._subscribers:
            for callback in self._subscribers[event_type]:
                try:
                    callback(data)
                except Exception:
                    pass
    
    def clear(self) -> None:
        """清除所有订阅"""
        self._subscribers.clear()


# *** 标准测试格式: 仅调用被测模块,AI不得添加数据 ***
if __name__ == "__main__":
    USER_TEST_EVENT = "test_event"
    
    bus = EventBus()
    received = []
    
    def on_event(data):
        received.append(data)
    
    bus.subscribe(USER_TEST_EVENT, on_event)
    bus.publish(USER_TEST_EVENT, "test_data")
    
    print(f"事件测试: received = {received}")
