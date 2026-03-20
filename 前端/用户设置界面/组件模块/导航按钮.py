# -*- coding: utf-8 -*-
"""
模块名称：导航按钮 | 层级：组件模块层
设计思路：
    导航按钮组件，组合零件层的卡片容器，提供导航按钮特有功能。
    符合Windows 11设置界面风格，默认深色主题。
    轻量级设计，职责清晰。
    使用统一的文本样式管理，确保文字视觉效果一致。
功能列表：
    1. 图标+文字水平排列
    2. 悬停效果
    3. 选中状态
    4. 外部控制接口
对外接口：
    - create(): 创建导航按钮
    - set_selected(): 设置选中状态
    - get_selected(): 获取选中状态
"""

import flet as ft
from typing import Callable, Optional
from 前端.用户设置界面.单元模块.卡片容器 import CardContainer
from 前端.用户设置界面.单元模块.文本标签 import LabelText
from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider
from 前端.用户设置界面.配置.界面配置 import 界面配置

DEFAULT_WIDTH = 240
DEFAULT_HEIGHT = 34


class NavButton:
    """导航按钮 - 组件模块层"""
    
    @staticmethod
    def create(
        text: str = "导航项",
        icon: str = None,
        selected: bool = False,
        on_click: Callable = None,
        width: int = None,
        height: int = None,
        **kwargs
    ) -> ft.Container:
        """
        创建导航按钮
        
        参数:
            text: 按钮文本
            icon: 图标名称（字符串）
            selected: 是否选中
            on_click: 点击回调
            width: 按钮宽度
            height: 按钮高度
        
        返回:
            ft.Container: 导航按钮容器
        """
        配置 = 界面配置()
        theme_colors = 配置.当前主题颜色
        
        # 创建图标控件
        icon_control = None
        if icon:
            if isinstance(icon, str):
                icon_upper = icon.upper()
                actual_icon = getattr(ft.Icons, icon_upper, ft.Icons.SETTINGS)
            else:
                actual_icon = icon
            icon_control = ft.Icon(actual_icon, size=20, color=theme_colors["accent"])
        else:
            icon_control = None
        
        # 使用LabelText创建文本控件（统一文本样式）
        text_control = LabelText.create(
            text=text,
            role="body",
            win11_style=True,
            expand=True
        )
        
        # 根据选中状态调整颜色
        if selected:
            text_control.color = "#FFFFFF"
        else:
            text_control.color = theme_colors["text_secondary"]
        
        # 创建内容行
        content = ft.Row(
            [
                icon_control,
                ft.Container(width=12),
                text_control
            ] if icon_control else [text_control],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )
        
        # 按钮尺寸
        button_width = width or DEFAULT_WIDTH
        button_height = height or DEFAULT_HEIGHT
        
        # 创建背景容器（用于动画效果）
        bg_container = ft.Container(
            bgcolor="transparent",
            border_radius=8,
            animate=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
            width=0,
            height=button_height,
        )
        
        # 创建内容容器
        content_container = ft.Container(
            content=content,
            padding=4,
            width=button_width,
        )
        
        # 创建堆栈布局
        stack = ft.Stack(
            [
                bg_container,
                content_container,
            ],
            width=button_width,
            height=button_height,
        )
        
        # 创建外层容器
        container = ft.Container(
            content=stack,
            width=button_width,
            height=button_height,
            on_click=on_click,
        )
        
        # 存储状态
        container._selected = selected
        container._bg_container = bg_container
        container._text_control = text_control
        
        def set_selected(is_selected: bool):
            """设置选中状态"""
            container._selected = is_selected
            if is_selected:
                bg_container.bgcolor = theme_colors["accent"]
                bg_container.width = button_width
                text_control.color = "#FFFFFF"
            else:
                bg_container.bgcolor = "transparent"
                bg_container.width = 0
                text_control.color = theme_colors["text_secondary"]
            
            try:
                bg_container.update()
                text_control.update()
            except:
                pass
        
        def get_selected() -> bool:
            """获取选中状态"""
            return container._selected
        
        def toggle(e=None):
            """切换选中状态"""
            set_selected(not container._selected)
            if on_click:
                on_click(e)
        
        # 绑定方法
        container.set_selected = set_selected
        container.get_selected = get_selected
        container.toggle = toggle
        
        # 悬停效果
        def on_hover(e):
            if not container._selected:
                if e.data == "true":
                    bg_container.bgcolor = theme_colors["bg_card"]
                    bg_container.width = button_width
                else:
                    bg_container.bgcolor = "transparent"
                    bg_container.width = 0
                
                try:
                    bg_container.update()
                except:
                    pass
        
        container.on_hover = on_hover
        
        # 初始化选中状态
        if selected:
            set_selected(True)
        
        return container


if __name__ == "__main__":
    配置 = 界面配置()
    ThemeProvider.initialize(配置)
    
    def main(page: ft.Page):
        page.add(NavButton.create(text="测试按钮", icon="SETTINGS", selected=True))
    
    ft.run(main)