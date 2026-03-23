# -*- coding: utf-8 -*-
"""
模块名称：主题色块
设计思路及联动逻辑:
    纯UI控件，用于主题颜色选择。
    1. 通过ThemeProvider获取样式，不包含业务逻辑
    2. 支持选中状态高亮和点击交互回调
模块隔离原则:
    1. 不直接创建被调用模块的内容
    2. 不覆盖被调用模块的计算结果
    3. 用户指定变量除外
"""

from typing import Callable

import flet as ft

from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider
from 前端.用户设置界面.配置.界面配置 import 界面配置


# *** 用户指定变量 - AI不得修改, 变量值必须生效 ***
USER_SIZE = 40  # 默认色块大小
# *********************************


class ThemeColorBlock:
    """主题色块 - 单个颜色选择块"""
    
    @staticmethod
    def create(
        color_value: str="#FF5722",
        color_name: str="",
        selected: bool=False,
        on_click: Callable[[str], None]=None,
        size: int=40,
        config: 界面配置=None,
        theme_name: str="",
        bg_color: str="",
        is_selected: bool=False,
        **kwargs
    ) -> ft.Container:
        actual_color = bg_color if bg_color else color_value
        actual_name = theme_name if theme_name else color_name
        actual_selected = is_selected if is_selected else selected
        
        border_color = ThemeProvider.get_color("primary") if actual_selected else "transparent"
        border_width = 3 if actual_selected else 0
        
        def handle_click(e):
            if on_click:
                on_click(e)
        
        return ft.Container(
            width=size,
            height=size,
            bgcolor=actual_color,
            border=ft.Border.all(border_width, border_color),
            border_radius=ft.BorderRadius.all(size // 3),
            on_click=handle_click,
            tooltip=actual_name if actual_name else actual_color,
            ink=True,
            **kwargs
        )
    
    @staticmethod
    def create_group(
        colors: list=None,
        selected_color: str="",
        on_select: Callable[[str], None]=None,
        size: int=40,
        spacing: int=10,
        **kwargs
    ) -> ft.Row:
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
    ft.run(lambda page: page.add(ThemeColorBlock.create_group()))
