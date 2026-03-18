# -*- coding: utf-8 -*-
"""
模块名称：主题色块 | 层级：零件层
设计思路：
    纯UI控件，用于主题颜色选择。
    不包含业务逻辑，所有样式从ThemeProvider获取。
    通过回调函数通知父组件颜色变化。
功能列表：
    1. 显示单个颜色块
    2. 支持选中状态高亮
    3. 支持点击交互
对外接口：
    - create(): 创建主题色块
    - create_group(): 创建主题色块组
"""

import flet as ft
from typing import Callable
from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider
from 前端.配置.界面配置 import 界面配置

# *** 用户指定变量 - AI不得修改 ***
# *********************************


class ThemeColorBlock:
    """主题色块 - 单个颜色选择块"""
    
    @staticmethod
    def create(
        color_value: str,
        color_name: str = "",
        selected: bool = False,
        on_click: Callable[[str], None] = None,
        size: int = 40,
        **kwargs
    ) -> ft.Container:
        """
        创建主题色块
        
        参数:
            color_value: 颜色值（如 "#FF5722"）
            color_name: 颜色名称（可选，用于提示）
            selected: 是否选中
            on_click: 点击回调，参数为颜色值
            size: 色块尺寸
            **kwargs: 其他Container参数
        
        返回:
            ft.Container: 色块容器
        """
        border_color = ThemeProvider.get_color("primary") if selected else "transparent"
        border_width = 3 if selected else 0
        
        def handle_click(e):
            if on_click:
                on_click(color_value)
        
        # Win11风格主题色块
        return ft.Container(
            width=size,
            height=size,
            bgcolor=color_value,
            border=ft.border.all(border_width, border_color),
            border_radius=ft.BorderRadius.all(size // 3),  # Win11风格更圆润的圆角
            on_click=handle_click,
            tooltip=color_name if color_name else color_value,
            ink=True,
            # Win11风格交互效果
            hover=ft.MouseCursor.POINTER,
            **kwargs
        )
    
    @staticmethod
    def create_group(
        colors: list = None,
        selected_color: str = "",
        on_select: Callable[[str], None] = None,
        size: int = 40,
        spacing: int = 10,
        **kwargs
    ) -> ft.Row:
        """
        创建主题色块组
        
        参数:
            colors: 颜色列表，每项为字典 {"name": "名称", "value": "#颜色值"}
            selected_color: 当前选中的颜色值
            on_select: 选择回调，参数为颜色值
            size: 色块尺寸
            spacing: 色块间距
            **kwargs: 其他Row参数
        
        返回:
            ft.Row: 色块组容器
        """
        # 如果没有传入colors，使用默认颜色列表
        if colors is None:
            colors = [
                {"name": "红色", "value": "#FF5722"},
                {"name": "蓝色", "value": "#2196F3"},
                {"name": "绿色", "value": "#4CAF50"},
            ]
        
        blocks = []
        
        for color_item in colors:
            color_value = color_item.get("value", "#000000")
            color_name = color_item.get("name", "")
            
            block = ThemeColorBlock.create(
                color_value=color_value,
                color_name=color_name,
                selected=(color_value == selected_color),
                on_click=on_select,
                size=size
            )
            blocks.append(block)
        
        return ft.Row(
            controls=blocks,
            spacing=spacing,
            wrap=True,
            **kwargs
        )


# *** 调试逻辑 ***
if __name__ == "__main__":
    配置 = 界面配置()
    ThemeProvider.initialize(配置)
    
    def on_color_select(color):
        print(f"选中颜色: {color}")
    
    def main(page: ft.Page):
        page.add(ThemeColorBlock.create_group())
    ft.run(main)
