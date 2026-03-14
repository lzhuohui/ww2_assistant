# -*- coding: utf-8 -*-
"""
导航按钮 - 零件层（新思路）

设计思路:
    独立功能模块，轻量级设计。
    导航按钮，支持选中状态和悬停效果。
    使用卡片容器统一风格。

功能:
    1. 图标+文字水平排列
    2. 悬停效果
    3. 选中状态
    4. 外部控制接口

数据来源:
    所有配置数据从配置目录获取。

使用场景:
    被组件层模块调用，也可独立使用。

可独立运行调试: python 导航按钮.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft
from typing import Callable, Optional
from 配置.界面配置 import 界面配置
from 新思路.零件层.卡片容器 import CardContainer


DEFAULT_WIDTH = 240


class NavButton:
    """导航按钮 - 独立功能模块
    
    职责：图标+文字、悬停效果、选中状态
    宽度由导航栏模块控制
    """
    
    @staticmethod
    def create(
        config: 界面配置,
        name: str = "通用设置",
        icon: str = "SETTINGS",
        width: float = None,
        on_click: Callable = None,
        **kwargs
    ) -> ft.Container:
        """
        创建导航按钮组件
        
        参数:
            config: 界面配置对象
            name: 按钮名称
            icon: 图标名称
            width: 按钮宽度（由导航栏传入）
            on_click: 点击回调
        
        返回:
            ft.Container: 导航按钮容器
        """
        theme_colors = config.当前主题颜色
        
        is_selected = False
        is_hovering = False
        
        icon_upper = icon.upper() if isinstance(icon, str) else "SETTINGS"
        actual_icon = getattr(ft.Icons, icon_upper, ft.Icons.SETTINGS)
        
        icon_control = ft.Icon(actual_icon, size=20, color=theme_colors["accent"])
        
        text_control = ft.Text(
            name,
            size=14,
            weight=ft.FontWeight.NORMAL,
            color=theme_colors["text_secondary"]
        )
        
        content = ft.Row(
            [
                icon_control,
                ft.Container(width=12),
                text_control
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )
        
        bg_container = ft.Container(
            bgcolor="transparent",
            border_radius=8,
            animate=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
            width=0,
            height=32,
        )
        
        content_container = ft.Container(
            content=content,
            padding=4,
            width=width,
        )
        
        stack_content = ft.Stack(
            [bg_container, content_container],
            alignment=ft.Alignment(0, 0)
        )
        
        def update_appearance():
            """更新按钮外观"""
            nonlocal is_selected, is_hovering
            
            if is_selected:
                bg_container.width = width
                bg_container.bgcolor = theme_colors["bg_selected"]
                icon_control.color = "#FFFFFF"
                text_control.color = "#FFFFFF"
            elif is_hovering:
                bg_container.width = width
                bg_container.bgcolor = theme_colors["bg_hover"]
                icon_control.color = theme_colors["accent"]
                text_control.color = theme_colors["text_primary"]
            else:
                bg_container.width = 0
                bg_container.bgcolor = "transparent"
                icon_control.color = theme_colors["accent"]
                text_control.color = theme_colors["text_secondary"]
            
            try:
                if container.page:
                    container.update()
            except RuntimeError:
                pass
        
        def set_selected(selected: bool):
            """设置选中状态"""
            nonlocal is_selected
            is_selected = selected
            update_appearance()
        
        def handle_click(e):
            """处理点击"""
            if on_click:
                on_click(e)
        
        def handle_hover(e):
            """处理悬停"""
            nonlocal is_hovering
            is_hovering = (e.data == "true")
            update_appearance()
        
        # 使用卡片容器统一风格（禁用悬停效果，使用自定义悬停）
        container = CardContainer.create(
            config=config,
            content=stack_content,
            width=width,
            on_hover_enabled=False,
        )
        
        # 添加自定义悬停和点击事件
        container.on_click = handle_click
        container.on_hover = handle_hover
        container.ink = True
        
        # 暴露控制接口
        container.set_selected = set_selected
        container.get_selected = lambda: is_selected
        
        return container


导航按钮 = NavButton


if __name__ == "__main__":
    配置 = 界面配置()
    
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        page.add(NavButton.create(配置, name="通用设置", icon="SETTINGS"))
    
    ft.run(main)
