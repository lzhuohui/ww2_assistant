# -*- coding: utf-8 -*-
"""
模块名称：下拉框
设计思路及联动逻辑:
    使用PopupMenuButton实现下拉菜单，自动处理菜单位置。
    1. 支持自定义宽高和自动定位
    2. 菜单宽度优化，支持值变化回调
模块隔离原则:
    1. 不直接创建被调用模块的内容
    2. 不覆盖被调用模块的计算结果
    3. 用户指定变量除外
"""

from typing import Callable, List

import flet as ft

from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider
from 前端.用户设置界面.配置.界面配置 import 界面配置


# *** 用户指定变量 - AI不得修改, 变量值必须生效 ***
USER_WIDTH = 150  # 默认宽度
USER_HEIGHT = 32  # 默认高度
# *********************************


class Dropdown:
    """自定义下拉框 - 使用PopupMenuButton实现"""
    
    @staticmethod
    def create(
        options: List[str]=None,
        value: str="",
        width: int=USER_WIDTH,
        height: int=USER_HEIGHT,
        on_change: Callable[[str], None]=None,
        enabled: bool=True,
        **kwargs
    ) -> ft.Container:
        current_width = width
        current_height = height
        
        actual_options = options if options else ["选项A", "选项B", "选项C"]
        current_value = value if value else (actual_options[0] if actual_options else "")
        
        theme_colors = {
            "text_primary": ThemeProvider.get_color("text_primary"),
            "text_secondary": ThemeProvider.get_color("text_secondary"),
            "bg_secondary": ThemeProvider.get_color("bg_secondary"),
            "bg_card": ThemeProvider.get_color("bg_card"),
            "border": ThemeProvider.get_color("border"),
        }
        
        selected_text = ft.Text(
            current_value,
            size=14,
            color=theme_colors["text_primary"],
            overflow=ft.TextOverflow.ELLIPSIS,
        )
        
        button_content = ft.Row(
            [selected_text, ft.Icon(ft.Icons.KEYBOARD_ARROW_DOWN, size=18)],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        
        button_container = ft.Container(
            content=button_content,
            width=current_width,
            height=current_height,
            border_radius=6,
            bgcolor=theme_colors["bg_secondary"],
            border=ft.Border.all(1, theme_colors["border"]),
            padding=ft.Padding(left=12, right=8, top=0, bottom=0),
        )
        
        menu_items = []
        
        def select_option(option: str):
            nonlocal current_value
            current_value = option
            selected_text.value = option
            if selected_text.page:
                selected_text.update()
            if on_change:
                on_change(option)
        
        for option in actual_options:
            item = ft.PopupMenuItem(
                content=ft.Container(
                    content=ft.Text(
                        option,
                        color=theme_colors["text_primary"],
                        size=14,
                    ),
                    bgcolor=theme_colors["bg_card"],
                    padding=ft.Padding(left=12, right=12, top=8, bottom=8),
                ),
                on_click=lambda e, o=option: select_option(o),
            )
            menu_items.append(item)
        
        popup_button = ft.PopupMenuButton(
            content=button_container,
            items=menu_items,
            disabled=not enabled,
            tooltip="",
            menu_padding=ft.Padding.all(0),
            bgcolor=theme_colors["bg_card"],
        )
        
        container = ft.Container(
            content=popup_button,
            width=current_width,
            height=current_height,
        )
        
        def get_value() -> str:
            return current_value
        
        def set_value(new_value: str):
            nonlocal current_value
            if new_value in actual_options:
                current_value = new_value
                selected_text.value = new_value
                if selected_text.page:
                    selected_text.update()
        
        def set_enabled(is_enabled: bool):
            popup_button.disabled = not is_enabled
            if popup_button.page:
                popup_button.update()
        
        def set_state(is_enabled: bool):
            selected_text.opacity = 1.0 if is_enabled else 0.4
            try:
                if selected_text.page:
                    selected_text.update()
            except RuntimeError:
                pass
        
        container.get_value = get_value
        container.set_value = set_value
        container.set_enabled = set_enabled
        container.set_state = set_state
        
        return container


# *** 调试逻辑 ***
if __name__ == "__main__":
    ft.run(lambda page: page.add(Dropdown.create()))
