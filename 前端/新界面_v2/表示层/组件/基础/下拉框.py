# -*- coding: utf-8 -*-
"""
模块名称：Dropdown
设计思路: 使用PopupMenuButton实现下拉框，Win11风格控件状态
模块隔离: 纯UI组件，不包含业务逻辑
"""

from typing import Callable, List
import flet as ft

from 前端.新界面_v2.核心.配置.界面配置 import UIConfig


# *** 用户指定变量 - AI不得修改, 变量值必须生效 ***
USER_WIDTH = 120  # 默认下拉框宽度
USER_HEIGHT = 32  # 默认下拉框高度
# *********************************


class Dropdown:
    """下拉框 - 使用PopupMenuButton实现，Win11风格"""
    
    @staticmethod
    def create(
        options: List[str]=None,
        current_value: str="",
        width: int=USER_WIDTH,
        height: int=USER_HEIGHT,
        on_change: Callable[[str], None]=None,
        enabled: bool=True,
        config: UIConfig=None,
    ) -> ft.Container:
        if config is None:
            config = UIConfig()
        
        theme_colors = config.当前主题颜色
        
        actual_options = options if options else ["选项A", "选项B", "选项C"]
        actual_current_value = current_value if current_value else (actual_options[0] if actual_options else "")
        
        current_selected_value = [actual_current_value]
        enabled_state = [enabled]
        
        text_color = theme_colors.get("text_primary") if enabled else theme_colors.get("text_hint")
        icon_color = theme_colors.get("text_secondary") if enabled else theme_colors.get("text_hint")
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
            border=ft.Border.all(1, border_color),
            padding=ft.Padding(left=12, right=8, top=0, bottom=0),
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
            bgcolor=theme_colors.get("bg_card"),
            menu_padding=ft.Padding.all(4),
            align=ft.Alignment.TOP_LEFT,
            tooltip="",
        )
        
        container = ft.Container(
            content=popup_button,
            width=width,
        )
        
        def handle_hover(e):
            if not enabled_state[0]:
                return
            if e.data == "true":
                button_content.border = ft.Border.all(1, theme_colors.get("accent"))
            else:
                button_content.border = ft.Border.all(1, theme_colors.get("border"))
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
            text_col = theme_colors.get("text_primary") if state else theme_colors.get("text_hint")
            icon_col = theme_colors.get("text_secondary") if state else theme_colors.get("text_hint")
            bg_col = theme_colors.get("bg_secondary") if state else theme_colors.get("bg_primary")
            border_col = theme_colors.get("border") if state else "transparent"
            
            selected_text.color = text_col
            dropdown_icon.color = icon_col
            button_content.bgcolor = bg_col
            button_content.border = ft.Border.all(1, border_col)
            popup_button.disabled = not state
            
            try:
                if container.page:
                    container.update()
            except:
                pass
        
        def unload_options():
            actual_options.clear()
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


# *** 调试逻辑 ***
if __name__ == "__main__":
    ft.run(lambda page: page.add(Dropdown.create()))
