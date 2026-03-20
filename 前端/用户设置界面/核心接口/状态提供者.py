# -*- coding: utf-8 -*-
"""
状态提供者 - 核心接口

设计思路:
    提供全局状态管理的统一访问接口，负责状态的存储、获取和更新。

功能:
    1. 状态初始化：初始化全局状态
    2. 状态获取：获取状态值
    3. 状态设置：设置状态值
    4. 状态监听：监听状态变化

数据来源:
    状态数据存储在内存中，提供全局访问。

使用场景:
    被界面层、组件层、单元层调用，用于管理全局状态。

可独立运行调试: python 状态提供者.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from typing import Any, Dict, List, Callable


class StateProvider:
    """状态提供者 - 核心接口"""
    
    _instance = None
    _state: Dict[str, Any] = {}
    _listeners: Dict[str, List[Callable]] = {}
    
    def __new__(cls):
        """单例模式"""
        if cls._instance is None:
            cls._instance = super(StateProvider, cls).__new__(cls)
        return cls._instance
    
    @classmethod
    def initialize(cls, initial_state: Dict[str, Any] = None):
        """
        初始化状态提供者
        
        参数:
            initial_state: 初始状态字典
        """
        if initial_state:
            cls._state.update(initial_state)
    
    @classmethod
    def get_state(cls, key: str, default: Any = None) -> Any:
        """
        获取状态值
        
        参数:
            key: 状态键
            default: 默认值
        
        返回:
            Any: 状态值
        """
        return cls._state.get(key, default)
    
    @classmethod
    def set_state(cls, key: str, value: Any):
        """
        设置状态值
        
        参数:
            key: 状态键
            value: 状态值
        """
        old_value = cls._state.get(key)
        cls._state[key] = value
        
        # 通知监听器
        if key in cls._listeners:
            for listener in cls._listeners[key]:
                listener(value, old_value)
    
    @classmethod
    def remove_state(cls, key: str):
        """
        移除状态值
        
        参数:
            key: 状态键
        """
        if key in cls._state:
            old_value = cls._state[key]
            del cls._state[key]
            
            # 通知监听器
            if key in cls._listeners:
                for listener in cls._listeners[key]:
                    listener(None, old_value)
    
    @classmethod
    def clear_state(cls):
        """
        清空所有状态
        """
        cls._state.clear()
    
    @classmethod
    def get_all_state(cls) -> Dict[str, Any]:
        """
        获取所有状态
        
        返回:
            Dict[str, Any]: 所有状态字典
        """
        return cls._state.copy()
    
    @classmethod
    def add_listener(cls, key: str, listener: Callable[[Any, Any], None]):
        """
        添加状态监听器
        
        参数:
            key: 状态键
            listener: 监听器函数，接收新值和旧值
        """
        if key not in cls._listeners:
            cls._listeners[key] = []
        cls._listeners[key].append(listener)
    
    @classmethod
    def remove_listener(cls, key: str, listener: Callable[[Any, Any], None]):
        """
        移除状态监听器
        
        参数:
            key: 状态键
            listener: 监听器函数
        """
        if key in cls._listeners:
            if listener in cls._listeners[key]:
                cls._listeners[key].remove(listener)
    
    @classmethod
    def remove_all_listeners(cls, key: str):
        """
        移除指定状态的所有监听器
        
        参数:
            key: 状态键
        """
        if key in cls._listeners:
            del cls._listeners[key]


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    # 1. 初始化状态提供者
    StateProvider.initialize({"current_page": "首页", "user_logged_in": False})
    
    # 2. 测试获取状态
    print("=== 测试获取状态 ===")
    print(f"获取状态 'current_page': {StateProvider.get_state('current_page')}")
    print(f"获取状态 'user_logged_in': {StateProvider.get_state('user_logged_in')}")
    print(f"获取不存在的状态: {StateProvider.get_state('non_existent', '默认值')}")
    
    # 3. 测试监听器
    print("\n=== 测试监听器 ===")
    def page_change_listener(new_value, old_value):
        print(f"页面变化: {old_value} -> {new_value}")
    
    StateProvider.add_listener("current_page", page_change_listener)
    
    # 4. 测试设置状态
    print("\n=== 测试设置状态 ===")
    StateProvider.set_state("current_page", "设置页")
    StateProvider.set_state("user_logged_in", True)
    
    # 5. 测试获取设置后的状态
    print("\n=== 测试获取设置后的状态 ===")
    print(f"设置后 'current_page': {StateProvider.get_state('current_page')}")
    print(f"设置后 'user_logged_in': {StateProvider.get_state('user_logged_in')}")
    
    # 6. 测试移除状态
    print("\n=== 测试移除状态 ===")
    StateProvider.remove_state("user_logged_in")
    print(f"移除后 'user_logged_in': {StateProvider.get_state('user_logged_in', '未登录')}")
    
    # 7. 测试获取所有状态
    print("\n=== 测试获取所有状态 ===")
    all_state = StateProvider.get_all_state()
    print(f"所有状态: {all_state}")