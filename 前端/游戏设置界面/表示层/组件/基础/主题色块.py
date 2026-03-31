# -*- coding: utf-8 -*-
"""
模块名称：ThemeColorBlock
模块功能：主题色块组件
实现步骤：
- 创建色块组
- 支持选中状态
- 支持点击回调
"""

import flet as ft
from typing import List, Dict, Callable, Optional

from 前端.游戏设置界面.核心层.配置.界面配置 import UIConfig


# *** 用户指定变量: 变量值必须生效,AI不得更改数据 ***
USER_BLOCK_SIZE = 40  # 色块大小
USER_BLOCK_SPACING = 10  # 色块间距
# *********************************


class ThemeColorBlock:
    """主题色块组件"""
    
    @staticmethod
    def create(
        color_name: str = "",
        color_value: str = "#0078D4",
        selected: bool = False,
        on_select: Callable[[str], None] = None,
        config: UIConfig = None,
    ) -> ft.Container:
        if config is None:
            config = UIConfig()
        
        theme_colors = config.当前主题颜色
        
        def on_click_handler(e):
            if on_select:
                on_select(color_value)
        
        container = ft.Container(
            width=USER_BLOCK_SIZE,
            height=USER_BLOCK_SIZE,
            bgcolor=color_value,
            border_radius=8,
            border=ft.border.all(3, theme_colors.get("accent")) if selected else None,
            on_click=on_click_handler if on_select else None,
        )
        
        return container
    
    @staticmethod
    def create_group(
        color_list: List[Dict[str, str]] = None,
        selected_color: str = None,
        on_select: Callable[[str], None] = None,
        config: UIConfig = None,
    ) -> ft.Row:
        if config is None:
            config = UIConfig()
        
        if color_list is None:
            color_list = [
                {"name": "默认", "value": "#0078D4"},
            ]
        
        blocks = []
        for item in color_list:
            block = ThemeColorBlock.create(
                color_name=item.get("name", ""),
                color_value=item.get("value", "#0078D4"),
                selected=item.get("value") == selected_color,
                on_select=on_select,
                config=config,
            )
            blocks.append(block)
        
        return ft.Row(
            controls=blocks,
            spacing=USER_BLOCK_SPACING,
            alignment=ft.MainAxisAlignment.START,
        )


# *** 标准测试格式: 仅调用被测模块,AI不得添加数据 ***
if __name__ == "__main__":
    def main(page: ft.Page):
        config = UIConfig()
        
        colors = [
            {"name": "蓝色", "value": "#0078D4"},
            {"name": "绿色", "value": "#107C10"},
            {"name": "红色", "value": "#D13438"},
        ]
        
        def on_select(color):
            print(f"选择颜色: {color}")
        
        group = ThemeColorBlock.create_group(
            color_list=colors,
            selected_color="#0078D4",
            on_select=on_select,
            config=config,
        )
        page.add(group)
    
    ft.run(main)
