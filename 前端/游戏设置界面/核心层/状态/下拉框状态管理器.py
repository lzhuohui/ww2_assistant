# -*- coding: utf-8 -*-
"""
模块名称：DropdownStateManager
模块功能：管理下拉框的懒加载状态，确保任何时候只有一个下拉框有完整选项列表
实现共识 #020 的核心要求

实现步骤：
1. 跟踪当前活动下拉框
2. 管理下拉框的加载状态
3. 销毁上一个下拉框的选项列表
4. 确保内存优化效果
"""

from typing import Dict, Any, Optional, Set
import threading


class DropdownStateManager:
    """下拉框状态管理器 - 实现共识 #020 的懒加载方案"""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialized = False
            return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._current_active_dropdown: Optional[str] = None
            self._loaded_dropdowns: Set[str] = set()
            self._dropdown_states: Dict[str, Dict[str, Any]] = {}
            self._initialized = True
    
    def register_dropdown(self, dropdown_id: str, option_loader=None) -> None:
        """注册下拉框"""
        self._dropdown_states[dropdown_id] = {
            "option_loader": option_loader,
            "has_loaded": False,
            "options": [],
            "container": None,  # 存储下拉框容器引用
        }
    
    def on_dropdown_click(self, dropdown_id: str) -> None:
        """处理下拉框点击事件"""
        print(f"[懒加载管理器] 下拉框 {dropdown_id} 被点击")
        
        # 1. 销毁上一个下拉框的选项列表
        if self._current_active_dropdown and self._current_active_dropdown != dropdown_id:
            self._unload_dropdown(self._current_active_dropdown)
        
        # 2. 加载当前下拉框的选项列表
        if not self._is_loaded(dropdown_id):
            self._load_dropdown(dropdown_id)
        
        # 3. 更新当前活动下拉框
        self._current_active_dropdown = dropdown_id
    
    def _load_dropdown(self, dropdown_id: str) -> None:
        """加载下拉框的选项列表"""
        state = self._dropdown_states.get(dropdown_id)
        if not state:
            return
        
        if state["option_loader"] and not state["has_loaded"]:
            print(f"[懒加载管理器] 加载下拉框 {dropdown_id} 的选项列表")
            state["options"] = state["option_loader"]()
            state["has_loaded"] = True
            self._loaded_dropdowns.add(dropdown_id)
    
    def _unload_dropdown(self, dropdown_id: str) -> None:
        """卸载下拉框的选项列表（释放内存）"""
        state = self._dropdown_states.get(dropdown_id)
        if not state:
            return
        
        if state["has_loaded"]:
            print(f"[懒加载管理器] 卸载下拉框 {dropdown_id} 的选项列表")
            # 清空选项列表，释放内存
            state["options"] = []
            state["has_loaded"] = False
            if dropdown_id in self._loaded_dropdowns:
                self._loaded_dropdowns.remove(dropdown_id)
    
    def _is_loaded(self, dropdown_id: str) -> bool:
        """检查下拉框是否已加载"""
        state = self._dropdown_states.get(dropdown_id)
        return state["has_loaded"] if state else False
    
    def get_options(self, dropdown_id: str) -> list:
        """获取下拉框的选项列表"""
        state = self._dropdown_states.get(dropdown_id)
        if state and state["has_loaded"]:
            return state["options"]
        return []
    
    def set_container(self, dropdown_id: str, container) -> None:
        """设置下拉框容器引用"""
        if dropdown_id in self._dropdown_states:
            self._dropdown_states[dropdown_id]["container"] = container
    
    def get_current_active(self) -> Optional[str]:
        """获取当前活动下拉框"""
        return self._current_active_dropdown
    
    def get_loaded_count(self) -> int:
        """获取已加载的下拉框数量"""
        return len(self._loaded_dropdowns)
    
    def clear_all(self) -> None:
        """清空所有状态（界面切换时调用）"""
        print(f"[懒加载管理器] 清空所有状态，当前已加载 {self.get_loaded_count()} 个下拉框")
        for dropdown_id in list(self._loaded_dropdowns):
            self._unload_dropdown(dropdown_id)
        self._current_active_dropdown = None
        self._loaded_dropdowns.clear()


# 全局单例实例
dropdown_state_manager = DropdownStateManager()