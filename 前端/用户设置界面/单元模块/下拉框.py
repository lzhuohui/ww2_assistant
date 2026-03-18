# -*- coding: utf-8 -*-
"""
模块名称：下拉框 | 层级：零件层
设计思路：
    使用PopupMenuButton实现下拉菜单，自动处理菜单位置。
    支持自定义宽高。

功能：
    1. 显示默认值：创建按钮时显示默认值，界面美观
    2. 自动定位：菜单自动跟随按钮位置
    3. 菜单宽度优化
    4. 支持自定义宽高

对外接口：
    - create(): 创建下拉框
    - get_value(): 获取当前值
    - set_value(): 设置当前值
    - set_enabled(): 设置启用状态
    - set_state(): 设置状态（透明度）
"""

import flet as ft
from typing import Callable, List, Optional
from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider
from 前端.配置.界面配置 import 界面配置

# *** 用户指定变量 - AI不得修改 ***
DEFAULT_WIDTH = 150
DEFAULT_HEIGHT = 32
# *********************************


class Dropdown:
    """自定义下拉框 - 使用PopupMenuButton实现"""
    
    @staticmethod
    def create(
        options: List[str] = None,
        value: str = None,
        width: int = None,
        height: int = None,
        on_change: Callable[[str], None] = None,
        enabled: bool = True,
        **kwargs
    ) -> ft.Container:
        """
        创建下拉框
        
        参数:
            options: 选项列表（默认示例选项）
            value: 默认值（默认选择第一个选项）
            width: 宽度（默认为DEFAULT_WIDTH）
            height: 高度（默认为DEFAULT_HEIGHT）
            on_change: 值变化回调
            enabled: 启用状态
            **kwargs: 其他参数
        
        返回:
            ft.Container: 下拉框控件
        """
        current_width = width if width is not None else DEFAULT_WIDTH
        current_height = height if height is not None else DEFAULT_HEIGHT
        
        if options is None:
            options = ["选项A", "选项B", "选项C"]
        
        current_value = value if value else (options[0] if options else "")
        
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
        
        for option in options:
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
            if new_value in options:
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
    配置 = 界面配置()
    from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider
    ThemeProvider.initialize(配置)
    def main(page: ft.Page):
        dropdown = Dropdown.create(
            options=["选项A", "选项B", "选项C"],
            value="选项A",
            on_change=lambda v: print(f"选择: {v}"),
        )
        page.add(dropdown)
    ft.run(main)
