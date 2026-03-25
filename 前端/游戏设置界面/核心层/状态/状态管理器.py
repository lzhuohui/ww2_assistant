# -*- coding: utf-8 -*-
"""
模块名称：StateManager
模块功能：统一状态管理器，支持状态订阅和变更通知
实现步骤：
- 使用字典存储状态
- 支持订阅/取消订阅
- 状态变更通知订阅者
"""

from typing import Any, Callable, Dict, List


class StateManager:
    """状态管理器 - 统一管理所有状态"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._state: Dict[str, Any] = {}
            cls._instance._subscribers: Dict[str, List[Callable]] = {}
        return cls._instance
    
    def get_state(self, key: str, default: Any = None) -> Any:
        """获取状态值"""
        return self._state.get(key, default)
    
    def set_state(self, key: str, value: Any) -> None:
        """设置状态值，并通知订阅者"""
        old_value = self._state.get(key)
        self._state[key] = value
        if old_value != value and key in self._subscribers:
            for callback in self._subscribers[key]:
                try:
                    callback(key, value, old_value)
                except Exception:
                    pass
    
    def subscribe(self, key: str, callback: Callable[[str, Any, Any], None]) -> None:
        """订阅状态变更"""
        if key not in self._subscribers:
            self._subscribers[key] = []
        if callback not in self._subscribers[key]:
            self._subscribers[key].append(callback)
    
    def unsubscribe(self, key: str, callback: Callable) -> None:
        """取消订阅"""
        if key in self._subscribers and callback in self._subscribers[key]:
            self._subscribers[key].remove(callback)
    
    def clear_state(self, key: str = None) -> None:
        """清除状态"""
        if key:
            self._state.pop(key, None)
        else:
            self._state.clear()
    
    def get_all_state(self) -> Dict[str, Any]:
        """获取所有状态"""
        return self._state.copy()


# *** 标准测试格式: 仅调用被测模块,AI不得添加数据 ***
if __name__ == "__main__":
    USER_TEST_KEY = "test_key"
    USER_TEST_VALUE = "test_value"
    
    manager = StateManager()
    
    def on_change(key: str, new_value: Any, old_value: Any):
        print(f"状态变更: {key} = {old_value} -> {new_value}")
    
    manager.subscribe(USER_TEST_KEY, on_change)
    manager.set_state(USER_TEST_KEY, USER_TEST_VALUE)
    print(f"获取状态: {manager.get_state(USER_TEST_KEY)}")
