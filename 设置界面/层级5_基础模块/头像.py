# -*- coding: utf-8 -*-

"""
模块名称：头像.py
模块功能：头像组件，支持双击编辑金色文字

职责：
- 圆形容器
- 金色文字
- 双击编辑功能

不负责：
- 用户信息获取
- 数据持久化
"""

import flet as ft
import time
from typing import Dict, Optional, Callable

from 设置界面.层级0_数据管理.配置管理 import ConfigManager

DEFAULT_TEXT = "帅"

class Avatar:
    """
    头像组件 - V3版本
    
    职责：
    - 圆形容器
    - 金色文字
    - 双击编辑功能
    
    不负责：
    - 用户信息获取
    - 数据持久化
    """
    
    _config_manager: ConfigManager = None
    
    @classmethod
    def set_config_manager(cls, config_manager: ConfigManager):
        """设置配置管理实例"""
        cls._config_manager = config_manager
    
    @staticmethod
    def _check_config_manager():
        """检查配置管理是否已设置"""
        if Avatar._config_manager is None:
            raise RuntimeError(
                "Avatar模块未设置config_manager，"
                "请先调用 Avatar.set_config_manager(config_manager)"
            )
    
    @staticmethod
    def get_size() -> int:
        """获取头像尺寸"""
        Avatar._check_config_manager()
        value = Avatar._config_manager.get_ui_config("头像", "尺寸")
        return value if value else 50
    
    @staticmethod
    def _get_theme_colors() -> Dict[str, str]:
        """获取主题颜色"""
        Avatar._check_config_manager()
        return Avatar._config_manager.get_theme_colors()
    
    @staticmethod
    def create(
        text: str = None,
        size: int = None,
        bg_color: str = None,
        text_color: str = "#FFD700",
        on_text_change: Optional[Callable[[str], None]] = None,
        enabled: bool = True,
        theme_colors: Dict[str, str] = None,
    ) -> ft.Container:
        """
        创建可编辑的圆形头像
        
        参数:
        - text: 显示的文字
        - size: 头像尺寸
        - bg_color: 背景颜色
        - text_color: 文字颜色（金色）
        - on_text_change: 文字变化回调
        - enabled: 是否启用
        - theme_colors: 主题颜色
        """
        if text is None:
            text = DEFAULT_TEXT
        
        if size is None:
            size = Avatar.get_size()
        
        if theme_colors is None:
            theme_colors = Avatar._get_theme_colors()
        
        if bg_color is None:
            bg_color = theme_colors.get("bg_card", "#2D2D2D")
        
        current_text = text[0] if text and len(text) > 0 else DEFAULT_TEXT
        editing = False
        last_click_time = 0
        text_ratio = 0.5
        
        radius = size / 2
        
        def create_text_content():
            return ft.Text(
                current_text,
                size=int(size * text_ratio),
                color=text_color,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
            )
        
        def create_edit_content():
            return ft.TextField(
                value=current_text,
                text_align=ft.TextAlign.CENTER,
                border=ft.InputBorder.NONE,
                text_size=int(size * text_ratio),
                color=text_color,
                bgcolor="transparent",
                dense=True,
                content_padding=ft.Padding.all(0),
                autofocus=True,
                on_submit=lambda e: finish_edit(e.control.value),
                on_blur=lambda e: finish_edit(e.control.value),
            )
        
        def finish_edit(new_text: str):
            nonlocal current_text, editing
            
            if new_text and len(new_text) == 1 and '\u4e00' <= new_text <= '\u9fff':
                old_text = current_text
                current_text = new_text
                
                if on_text_change and old_text != new_text:
                    on_text_change(new_text)
            
            editing = False
            avatar_container.content = create_text_content()
            try:
                avatar_container.update()
            except:
                pass
        
        def handle_click(e):
            nonlocal editing, last_click_time
            
            if not enabled:
                return
            
            current_time = time.time()
            
            if editing:
                return
            
            if current_time - last_click_time < 0.3:
                editing = True
                avatar_container.content = create_edit_content()
                try:
                    avatar_container.update()
                except:
                    pass
            
            last_click_time = current_time
        
        avatar_container = ft.Container(
            content=create_text_content(),
            width=size,
            height=size,
            bgcolor=bg_color,
            border_radius=radius,
            alignment=ft.alignment.Alignment(0, 0),
            shadow=ft.BoxShadow(
                spread_radius=2,
                blur_radius=8,
                color=text_color + "66",
                offset=ft.Offset(0, 0),
            ),
        )
        
        container = ft.Container(
            content=avatar_container,
            on_click=handle_click,
        )
        
        def set_text(new_text: str):
            nonlocal current_text
            if new_text and len(new_text) == 1 and '\u4e00' <= new_text <= '\u9fff':
                current_text = new_text
                if not editing:
                    avatar_container.content = create_text_content()
                    try:
                        avatar_container.update()
                    except:
                        pass
        
        def get_text() -> str:
            return current_text
        
        container.set_text = set_text
        container.get_text = get_text
        
        return container
