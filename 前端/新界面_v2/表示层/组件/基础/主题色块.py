# -*- coding: utf-8 -*-
"""
模块名称：ThemeColorBlock
设计思路: 纯UI控件，用于主题颜色选择
模块隔离: 基础组件，不依赖其他业务组件
"""

import flet as ft
from typing import Callable, List, Dict

from 前端.新界面_v2.核心.配置.界面配置 import UIConfig


# *** 用户指定变量 - AI不得修改, 变量值必须生效 ***
USER_SIZE = 40  # 默认色块大小
# *********************************


class ThemeColorBlock:
    """主题色块组件"""
    
    @staticmethod
    def create(
        color_value: str="#FF5722",
        color_name: str="",
        selected: bool=False,
        on_click: Callable[[str], None]=None,
        size: int=USER_SIZE,
        config: UIConfig=None,
    ) -> ft.Container:
        if config is None:
            config = UIConfig()
        
        theme_colors = config.当前主题颜色
        border_color = theme_colors.get("accent") if selected else "transparent"
        border_width = 3 if selected else 0
        
        def handle_click(e):
            if on_click:
                on_click(color_value)
        
        return ft.Container(
            width=size,
            height=size,
            bgcolor=color_value,
            border=ft.Border.all(border_width, border_color),
            border_radius=ft.BorderRadius.all(size // 3),
            on_click=handle_click,
            tooltip=color_name if color_name else color_value,
            ink=True,
        )
    
    @staticmethod
    def create_group(
        color_list: List[Dict]=None,
        selected_color: str="",
        on_select: Callable[[str], None]=None,
        size: int=USER_SIZE,
        spacing: int=10,
        config: UIConfig=None,
    ) -> ft.Row:
        if color_list is None:
            color_list = [
                {"name": "红色", "value": "#FF5722"},
                {"name": "蓝色", "value": "#2196F3"},
                {"name": "绿色", "value": "#4CAF50"},
            ]
        
        if config is None:
            config = UIConfig()
        
        color_blocks = []
        
        for color_item in color_list:
            color_value = color_item.get("value", "#000000")
            color_name = color_item.get("name", "")
            
            block = ThemeColorBlock.create(
                color_value=color_value,
                color_name=color_name,
                selected=(color_value == selected_color),
                on_click=on_select,
                size=size,
                config=config,
            )
            color_blocks.append(block)
        
        return ft.Row(
            controls=color_blocks,
            spacing=spacing,
            wrap=True,
        )


# *** 调试逻辑 ***
if __name__ == "__main__":
    ft.run(lambda page: page.add(ThemeColorBlock.create_group()))
