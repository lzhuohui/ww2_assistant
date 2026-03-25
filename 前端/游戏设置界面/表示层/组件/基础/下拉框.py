# -*- coding: utf-8 -*-
"""
模块名称：Dropdown
模块功能：下拉框组件，使用PopupMenuButton实现
实现步骤：
- 使用PopupMenuButton实现下拉框
- 支持选项列表
- 支持值变更回调
- Win11风格
"""

import flet as ft
from typing import List, Callable, Optional, Any

from 前端.游戏设置界面.核心层.配置.界面配置 import UIConfig


USER_WIDTH = 120
USER_HEIGHT = 32


class Dropdown:
    """下拉框组件 - 使用PopupMenuButton实现"""
    
    @staticmethod
    def create(
        options: List[str] = None,
        current_value: str = "",
        width: int = USER_WIDTH,
        height: int = USER_HEIGHT,
        enabled: bool = True,
        on_change: Callable[[str], None] = None,
        config: UIConfig = None,
    ) -> ft.Container:
        if config is None:
            config = UIConfig()
        
        theme_colors = config.当前主题颜色
        
        actual_options = options if options else ["选项A", "选项B"]
        actual_current_value = current_value if current_value else (actual_options[0] if actual_options else "")
        
        current_selected_value = [actual_current_value]
        enabled_state = [enabled]
        
        text_color = theme_colors.get("text_primary") if enabled else theme_colors.get("text_disabled")
        icon_color = theme_colors.get("text_secondary") if enabled else theme_colors.get("text_disabled")
        bg_color = theme_colors.get("bg_secondary") if enabled else theme_colors.get("bg_primary")
        border_color = theme_colors.get("border") if enabled else "transparent"
        
        selected_text = ft.Text(
            actual_current_value,
            size=14,
            color=text_color,
            overflow=ft.TextOverflow.ELLIPSIS,
        )
        
        dropdown_icon = ft.Icon(
            ft.Icons.KEYBOARD_ARROW_DOWN,
            size=18,
            color=icon_color,
        )
        
        button_content = ft.Container(
            content=ft.Row(
                [selected_text, dropdown_icon],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=width,
            height=height,
            border_radius=6,
            bgcolor=bg_color,
            border=ft.border.all(1, border_color),
            padding=ft.padding.symmetric(horizontal=12, vertical=0),
            animate=ft.Animation(167, ft.AnimationCurve.EASE_OUT),
        )
        
        def create_menu_items():
            menu_items = []
            for option in actual_options:
                def create_callback(value=option):
                    def callback(e):
                        current_selected_value[0] = value
                        selected_text.value = value
                        if container.page:
                            container.update()
                        if on_change:
                            on_change(value)
                    return callback
                
                menu_item = ft.PopupMenuItem(
                    content=ft.Text(
                        option,
                        size=14,
                        color=theme_colors.get("text_primary"),
                    ),
                    on_click=create_callback(),
                )
                menu_items.append(menu_item)
            return menu_items
        
        popup_button = ft.PopupMenuButton(
            content=button_content,
            items=create_menu_items(),
            disabled=not enabled,
            bgcolor=theme_colors.get("bg_secondary"),
            menu_padding=ft.padding.all(4),
        )
        
        container = ft.Container(
            content=popup_button,
            width=width,
        )
        
        def handle_hover(e):
            if not enabled_state[0]:
                return
            if e.data == "true":
                button_content.border = ft.border.all(1, theme_colors.get("accent"))
            else:
                button_content.border = ft.border.all(1, theme_colors.get("border"))
            try:
                if container.page:
                    container.update()
            except:
                pass
        
        container.on_hover = handle_hover
        
        def get_value() -> str:
            return current_selected_value[0]
        
        def set_value(new_value: str):
            if new_value in actual_options:
                current_selected_value[0] = new_value
                selected_text.value = new_value
                if container.page:
                    container.update()
        
        def set_enabled(state: bool):
            enabled_state[0] = state
            text_col = theme_colors.get("text_primary") if state else theme_colors.get("text_disabled")
            icon_col = theme_colors.get("text_secondary") if state else theme_colors.get("text_disabled")
            bg_col = theme_colors.get("bg_secondary") if state else theme_colors.get("bg_primary")
            border_col = theme_colors.get("border") if state else "transparent"
            
            selected_text.color = text_col
            dropdown_icon.color = icon_col
            button_content.bgcolor = bg_col
            button_content.border = ft.border.all(1, border_col)
            popup_button.disabled = not state
            
            try:
                if container.page:
                    container.update()
            except:
                pass
        
        def unload_options():
            popup_button.items = []
            try:
                if container.page:
                    container.update()
            except:
                pass
        
        container.get_value = get_value
        container.set_value = set_value
        container.set_enabled = set_enabled
        container.unload_options = unload_options
        
        return container


# *** 标准测试格式: 仅调用被测模块,AI不得添加数据 ***
if __name__ == "__main__":
    def main(page: ft.Page):
        config = UIConfig()
        
        def on_change(value):
            print(f"选择: {value}")
        
        dropdown = Dropdown.create(
            options=["选项A", "选项B", "选项C"],
            current_value="选项A",
            on_change=on_change,
            config=config,
        )
        page.add(dropdown)
    
    ft.app(target=main)
