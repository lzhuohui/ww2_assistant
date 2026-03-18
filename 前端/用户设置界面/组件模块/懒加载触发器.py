# -*- coding: utf-8 -*-
"""
模块名称：懒加载触发器 | 层级：组件模块层
设计思路：
    单一职责：检测点击事件并触发加载。
    使用回调机制解耦。

功能：
    1. 检测点击事件
    2. 判断是否可触发加载
    3. 触发加载回调

对外接口：
    - create_trigger(): 创建触发器
    - can_trigger(): 判断是否可触发
"""

import flet as ft
from typing import Callable, Optional


class LazyTrigger:
    """懒加载触发器 - 负责检测点击事件并触发加载"""
    
    @staticmethod
    def create(
        on_trigger: Callable[[], None],
        is_loaded: Callable[[], bool],
        is_enabled: Callable[[], bool],
    ) -> Callable[[ft.ControlEvent], None]:
        """
        创建触发器
        
        参数:
            on_trigger: 触发加载回调
            is_loaded: 判断是否已加载
            is_enabled: 判断是否启用
        
        返回:
            点击事件处理函数
        """
        def handle_click(e: ft.ControlEvent):
            if is_loaded() or not is_enabled():
                return
            on_trigger()
        
        return handle_click
    
    @staticmethod
    def can_trigger(is_loaded: bool, is_enabled: bool) -> bool:
        """判断是否可触发加载"""
        return not is_loaded and is_enabled


懒加载触发器 = LazyTrigger
