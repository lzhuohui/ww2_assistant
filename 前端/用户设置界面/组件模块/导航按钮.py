# -*- coding: utf-8 -*-
"""
模块名称：导航按钮 | 层级：组件模块层
设计思路：
    导航按钮组件，组合零件层的卡片容器，提供导航按钮特有功能。
    符合Windows 11设置界面风格，默认深色主题。
    轻量级设计，职责清晰。
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
from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider
from 前端.配置.界面配置 import 界面配置


# *** 用户指定变量 - AI不得修改 ***
DEFAULT_WIDTH = 240
DEFAULT_HEIGHT = 34
# *********************************


class NavButton:
    """
    导航按钮 - 组件模块层
    
    职责：图标+文字、悬停效果、选中状态
    宽度由导航界面模块控制
    """
    
    @staticmethod
    def create(
        text: str = "导航项",
        icon: str = None,
        selected: bool = False,
        on_click: Callable = None,
        width: int = None,
        height: int = None,
        enabled: bool = True,
        config: 界面配置 = None,
        **kwargs
    ) -> ft.Container:
        """
        创建导航按钮
        
        参数:
            text: 按钮名称
            icon: 图标名称（字符串或ft.Icons枚举）
            selected: 选中状态
            on_click: 点击回调
            width: 按钮宽度（由导航界面传入）
            height: 按钮高度（可选）
            enabled: 启用状态
            config: 界面配置对象（可选）
        
        返回:
            ft.Container: 导航按钮容器
        """
        # 获取配置对象
        配置 = config or 界面配置()
        
        # 获取主题颜色
        theme_colors = 配置.当前主题颜色
        
        # 状态变量
        is_selected = [selected]
        is_hovering = [False]
        
        # 处理图标
        if icon:
            if isinstance(icon, str):
                icon_upper = icon.upper()
                actual_icon = getattr(ft.Icons, icon_upper, ft.Icons.SETTINGS)
            else:
                actual_icon = icon
            icon_control = ft.Icon(actual_icon, size=20, color=theme_colors["accent"])
        else:
            icon_control = None
        
        # 创建文本控件
        text_control = ft.Text(
            text,
            size=14,
            weight=ft.FontWeight.NORMAL,
            color=theme_colors["text_secondary"],
            expand=True
        )
        
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
        stack_content = ft.Stack(
            [bg_container, content_container],
        )
        
        def update_appearance():
            """更新按钮外观"""
            if is_selected[0]:
                bg_container.width = button_width
                bg_container.bgcolor = theme_colors["bg_selected"]
                if icon_control:
                    icon_control.color = "#FFFFFF"
                text_control.color = "#FFFFFF"
            elif is_hovering[0]:
                bg_container.width = button_width
                bg_container.bgcolor = theme_colors["bg_hover"]
                if icon_control:
                    icon_control.color = theme_colors["accent"]
                text_control.color = theme_colors["text_primary"]
            else:
                bg_container.width = 0
                bg_container.bgcolor = "transparent"
                if icon_control:
                    icon_control.color = theme_colors["accent"]
                text_control.color = theme_colors["text_secondary"]
            
            try:
                if container.page:
                    container.update()
            except RuntimeError:
                pass
        
        def set_selected(selected: bool):
            """设置选中状态"""
            is_selected[0] = selected
            update_appearance()
        
        def get_selected() -> bool:
            """获取选中状态"""
            return is_selected[0]
        
        def handle_click(e):
            """处理点击"""
            if on_click:
                on_click(e)
        
        def handle_hover(e):
            """处理悬停"""
            is_hovering[0] = (e.data == "true")
            update_appearance()
        
        # 使用卡片容器统一风格（禁用悬停效果，使用自定义悬停）
        container = CardContainer.create(
            config=配置,
            content=stack_content,
            width=button_width,
            height=button_height,
            on_hover_enabled=False,
            **kwargs
        )
        
        # 添加自定义悬停和点击事件
        container.on_click = handle_click
        container.on_hover = handle_hover
        container.ink = True
        
        # 暴露控制接口
        container.set_selected = set_selected
        container.get_selected = get_selected
        
        return container


# 兼容别名
导航按钮 = NavButton


# *** 调试逻辑 ***
if __name__ == "__main__":
    from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider
    配置 = 界面配置()
    ThemeProvider.initialize(配置)
    
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        page.add(
            ft.Column([
                NavButton.create(text="系统", icon="SETTINGS", selected=True, config=配置),
                NavButton.create(text="策略", icon="ROCKET_LAUNCH", selected=False, config=配置),
                NavButton.create(text="任务", icon="ASSIGNMENT", selected=False, config=配置),
            ])
        )
    
    ft.run(main)
