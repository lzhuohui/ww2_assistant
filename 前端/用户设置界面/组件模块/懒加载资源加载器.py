# -*- coding: utf-8 -*-
"""
模块名称：懒加载资源加载器 | 层级：组件模块层
设计思路：
    单一职责：根据配置创建控件。
    支持多种控件类型的创建。

功能：
    1. 解析控件配置
    2. 创建下拉框控件
    3. 创建输入框控件（预留）
    4. 创建开关控件（预留）

对外接口：
    - create_control(): 根据配置创建控件
"""

import flet as ft
from typing import Dict, Any, Callable, Optional, List
from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider
from 前端.用户设置界面.单元模块.下拉框 import Dropdown


class LazyLoader:
    """懒加载资源加载器 - 负责根据配置创建控件"""
    
    @staticmethod
    def create_control(
        control_config: Dict[str, Any],
        card_name: str,
        config_manager: Any = None,
        on_value_change: Callable[[str, Any], None] = None,
    ) -> Optional[ft.Control]:
        """
        根据配置创建控件
        
        参数:
            control_config: 控件配置
            card_name: 卡片名称
            config_manager: 配置管理器
            on_value_change: 值变化回调
        
        返回:
            创建的控件，如果类型不支持则返回None
        """
        control_type = control_config.get("type")
        
        if control_type == "dropdown":
            return LazyLoader._create_dropdown(
                control_config, card_name, config_manager, on_value_change
            )
        
        return None
    
    @staticmethod
    def create_controls(
        controls_config: List[Dict[str, Any]],
        card_name: str,
        config_manager: Any = None,
        on_value_change: Callable[[str, Any], None] = None,
    ) -> List[ft.Control]:
        """
        批量创建控件
        
        参数:
            controls_config: 控件配置列表
            card_name: 卡片名称
            config_manager: 配置管理器
            on_value_change: 值变化回调
        
        返回:
            创建的控件列表
        """
        controls = []
        for config in controls_config:
            control = LazyLoader.create_control(
                config, card_name, config_manager, on_value_change
            )
            if control:
                controls.append(control)
        return controls
    
    @staticmethod
    def _create_dropdown(
        control_config: Dict[str, Any],
        card_name: str,
        config_manager: Any,
        on_value_change: Callable[[str, Any], None],
    ) -> ft.Control:
        """创建下拉框控件"""
        config_key = control_config.get("config_key", "")
        label = control_config.get("label", "")
        options = control_config.get("options", [])
        value = control_config.get("value", "")
        width = control_config.get("width")
        
        if config_manager:
            saved_value = config_manager.get_value(card_name, config_key, value)
            value = saved_value
        
        def on_change(v):
            if on_value_change:
                on_value_change(config_key, v)
            if config_manager:
                config_manager.set_value(card_name, config_key, v)
        
        dropdown = Dropdown.create(
            options=options,
            value=value,
            width=width,
            on_change=on_change,
        )
        
        label_text = ft.Text(
            f"{label}:",
            color=ThemeProvider.get_color("text_secondary"),
            size=14,
        )
        
        return ft.Row(
            [label_text, dropdown],
            alignment=ft.MainAxisAlignment.END,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8,
            expand=True,
        )


懒加载加载器 = LazyLoader
