# -*- coding: utf-8 -*-
"""
模块名称：懒加载状态管理器 | 层级：组件模块层
设计思路：
    单一职责：管理懒加载卡片的状态。
    使用单例模式确保全局状态一致性。

功能：
    1. 管理当前加载的卡片
    2. 管理卡片的加载状态
    3. 管理卡片的启用状态
    4. 提供状态查询接口

对外接口：
    - LazyState: 懒加载状态管理器
"""

from typing import Dict, Optional, Any
from dataclasses import dataclass


@dataclass
class CardState:
    """卡片状态数据类"""
    is_loaded: bool = False
    is_enabled: bool = True
    card_name: str = ""


class LazyState:
    """懒加载状态管理器 - 单一职责：状态管理"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._current_card_name: Optional[str] = None
        self._card_states: Dict[str, CardState] = {}
        self._config_manager: Optional[Any] = None
        self._initialized = True
    
    def register(self, card_name: str) -> CardState:
        """注册卡片状态"""
        if card_name not in self._card_states:
            self._card_states[card_name] = CardState(card_name=card_name)
        return self._card_states[card_name]
    
    def register_card(self, card_name: str, card_obj: Any):
        """注册卡片对象"""
        self.register(card_name)
        if not hasattr(self, '_card_objects'):
            self._card_objects = {}
        self._card_objects[card_name] = card_obj
    
    def get_card(self, card_name: str) -> Optional[Any]:
        """获取卡片对象"""
        if hasattr(self, '_card_objects'):
            return self._card_objects.get(card_name)
        return None
    
    def get_state(self, card_name: str) -> Optional[CardState]:
        """获取卡片状态"""
        return self._card_states.get(card_name)
    
    def set_loaded(self, card_name: str, loaded: bool):
        """设置加载状态"""
        state = self.get_state(card_name)
        if state:
            state.is_loaded = loaded
    
    def is_loaded(self, card_name: str) -> bool:
        """检查是否已加载"""
        state = self.get_state(card_name)
        return state.is_loaded if state else False
    
    def set_enabled(self, card_name: str, enabled: bool):
        """设置启用状态"""
        state = self.get_state(card_name)
        if state:
            state.is_enabled = enabled
    
    def is_enabled(self, card_name: str) -> bool:
        """检查是否启用"""
        state = self.get_state(card_name)
        return state.is_enabled if state else True
    
    def set_current(self, card_name: str):
        """设置当前卡片"""
        self._current_card_name = card_name
    
    def get_current(self) -> Optional[str]:
        """获取当前卡片"""
        return self._current_card_name
    
    def set_config_manager(self, config_manager: Any):
        """设置配置管理器"""
        self._config_manager = config_manager
    
    def get_config_manager(self) -> Optional[Any]:
        """获取配置管理器"""
        return self._config_manager
    
    def save_current(self):
        """保存当前卡片数据"""
        if self._current_card_name and self._config_manager:
            self._config_manager.save_all()
    
    def reset(self):
        """重置所有状态"""
        self._card_states.clear()
        self._current_card_name = None


懒加载状态 = LazyState
