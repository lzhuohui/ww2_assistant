# -*- coding: utf-8 -*-
"""
模块名称：通用按钮
设计思路及联动逻辑:
    提供通用按钮功能，支持多种按钮样式。
    1. 支持文字按钮、轮廓按钮、图标按钮
    2. 通过ThemeProvider获取主题，无需传入config
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
# （用户未指定变量）
# *********************************


class Button:
    """通用按钮 - 纯UI控件"""
    
    @staticmethod
    def create(
        text: str="按钮",
        icon: str="",
        style: str="text",
        selected: bool=False,
        on_click: Callable=None,
        width: int=120,
        height: int=36,
        enabled: bool=True,
        toggle_mode: bool=False,
        **kwargs
    ) -> ft.Control:
        text_color = ThemeProvider.get_color("text_primary")
        accent_color = ThemeProvider.get_color("accent")
        bg_secondary = ThemeProvider.get_color("bg_secondary")
        bg_hover = ThemeProvider.get_color("bg_hover")
        bg_pressed = ThemeProvider.get_color("bg_pressed")
        
        配置 = 界面配置()
        animate_duration = 配置.获取尺寸("动画", "duration_fast")
        button_height = 配置.获取尺寸("按钮", "default_height") or 36
        button_radius = 配置.获取尺寸("按钮", "default_border_radius") or 8
        icon_size = 配置.获取尺寸("按钮", "icon_size") or 18
        padding_h = 配置.获取尺寸("按钮", "padding_horizontal") or 12
        padding_v = 配置.获取尺寸("按钮", "padding_vertical") or 8
        selected_color = 配置.获取尺寸("按钮", "selected_color") or "#FFFFFF"
        
        selected_bgcolor = accent_color
        
        current_selected = [selected]
        
        if style == "icon":
            if isinstance(icon, str) and icon:
                icon_upper = icon.upper()
                actual_icon = getattr(ft.Icons, icon_upper, ft.Icons.SETTINGS)
            else:
                actual_icon = ft.Icons.SETTINGS
            
            icon_size_large = 配置.获取尺寸("图标", "size_large") or 24
            icon_btn = ft.IconButton(
                icon=actual_icon,
                on_click=on_click,
                width=width or button_height,
                height=height or button_height,
                icon_color=selected_color if current_selected[0] else text_color,
                style=ft.ButtonStyle(
                    shape=ft.CircleBorder(),
                    padding=8,
                    bgcolor=selected_bgcolor if current_selected[0] else "transparent",
                ),
                disabled=not enabled,
            )
            
            def icon_toggle(e):
                if toggle_mode:
                    current_selected[0] = not current_selected[0]
                    icon_btn.icon_color = selected_color if current_selected[0] else text_color
                    icon_btn.style.bgcolor = selected_bgcolor if current_selected[0] else "transparent"
                    try:
                        icon_btn.update()
                    except:
                        pass
                if on_click:
                    on_click(e)
            
            icon_btn.on_click = icon_toggle
            
            def icon_set_selected(value: bool):
                current_selected[0] = value
                icon_btn.icon_color = selected_color if current_selected[0] else text_color
                icon_btn.style.bgcolor = selected_bgcolor if current_selected[0] else "transparent"
                try:
                    icon_btn.update()
                except:
                    pass
            
            def icon_get_selected() -> bool:
                return current_selected[0]
            
            def icon_toggle_state():
                icon_set_selected(not current_selected[0])
            
            icon_btn.set_selected = icon_set_selected
            icon_btn.get_selected = icon_get_selected
            icon_btn.toggle = icon_toggle_state
            
            return icon_btn
        
        def create_content(is_selected):
            icon_control = None
            if icon:
                if isinstance(icon, str):
                    icon_upper = icon.upper()
                    actual_icon = getattr(ft.Icons, icon_upper, ft.Icons.SETTINGS)
                else:
                    actual_icon = icon
                icon_control = ft.Icon(actual_icon, color=selected_color if is_selected else text_color, size=icon_size)
            
            if icon_control:
                return ft.Row(
                    [
                        icon_control,
                        ft.Text(text, color=selected_color if is_selected else text_color, size=14, weight=ft.FontWeight.NORMAL, expand=True),
                    ],
                    spacing=8,
                    alignment=ft.MainAxisAlignment.START if style == "nav" else ft.MainAxisAlignment.CENTER,
                    expand=True,
                )
            else:
                return ft.Text(text, color=selected_color if is_selected else text_color, size=14, weight=ft.FontWeight.NORMAL)
        
        if style == "text" or style == "nav":
            shadow = ft.BoxShadow(
                spread_radius=0,
                blur_radius=4,
                color=ThemeProvider.get_color("shadow"),
                offset=ft.Offset(0, 2),
            )
            
            container = ft.Container(
                content=create_content(current_selected[0]),
                width=width,
                height=height or button_height,
                bgcolor=selected_bgcolor if current_selected[0] else bg_secondary,
                border=ft.Border.all(1, accent_color) if not current_selected[0] else None,
                border_radius=ft.BorderRadius.all(button_radius),
                padding=ft.Padding.symmetric(horizontal=padding_h, vertical=padding_v),
                alignment=ft.Alignment(-1, 0) if style == "nav" else ft.Alignment(0, 0),
                ink=True,
                animate=animate_duration,
                shadow=shadow,
                disabled=not enabled,
            )
            
            def update_button_state():
                is_selected = current_selected[0]
                container.bgcolor = selected_bgcolor if is_selected else bg_secondary
                container.border = None if is_selected else ft.Border.all(1, accent_color)
                container.content = create_content(is_selected)
                try:
                    container.update()
                except:
                    pass
            
            def handle_click(e):
                if toggle_mode:
                    current_selected[0] = not current_selected[0]
                    update_button_state()
                if on_click:
                    on_click(e)
            
            container.on_click = handle_click
            
            def handle_hover(e):
                if e.data == "true":
                    if not current_selected[0]:
                        container.bgcolor = bg_hover
                        container.border = ft.Border.all(1, accent_color)
                else:
                    if not current_selected[0]:
                        container.bgcolor = bg_secondary
                        container.border = ft.Border.all(1, accent_color)
                try:
                    container.update()
                except:
                    pass
            
            container.on_hover = handle_hover
            
            def handle_tap_down(e):
                if not current_selected[0]:
                    container.bgcolor = bg_pressed
                    try:
                        container.update()
                    except:
                        pass
            
            container.on_tap_down = handle_tap_down
            
            def handle_tap_up(e):
                if not current_selected[0]:
                    container.bgcolor = bg_hover
                    try:
                        container.update()
                    except:
                        pass
            
            container.on_tap_up = handle_tap_up
            
            def set_selected(value: bool):
                current_selected[0] = value
                update_button_state()
            
            def get_selected() -> bool:
                return current_selected[0]
            
            def toggle_state():
                set_selected(not current_selected[0])
            
            container.set_selected = set_selected
            container.get_selected = get_selected
            container.toggle = toggle_state
            
            return container
        else:
            outlined_btn = ft.OutlinedButton(
                content=create_content(current_selected[0]),
                on_click=on_click,
                width=width,
                height=height,
                style=ft.ButtonStyle(
                    color=selected_color if current_selected[0] else text_color,
                    shape=ft.RoundedRectangleBorder(radius=button_radius),
                    side=ft.BorderSide(width=1, color=selected_bgcolor if current_selected[0] else accent_color),
                    bgcolor=selected_bgcolor if current_selected[0] else "transparent",
                    padding=ft.Padding.symmetric(horizontal=padding_h + 4, vertical=padding_v),
                ),
                disabled=not enabled,
            )
            
            def outlined_toggle(e):
                if toggle_mode:
                    current_selected[0] = not current_selected[0]
                    is_selected = current_selected[0]
                    outlined_btn.style.color = selected_color if is_selected else text_color
                    outlined_btn.style.side = ft.BorderSide(width=1, color=selected_bgcolor if is_selected else accent_color)
                    outlined_btn.style.bgcolor = selected_bgcolor if is_selected else "transparent"
                    outlined_btn.content = create_content(is_selected)
                    try:
                        outlined_btn.update()
                    except:
                        pass
                if on_click:
                    on_click(e)
            
            outlined_btn.on_click = outlined_toggle
            
            def outlined_set_selected(value: bool):
                current_selected[0] = value
                is_selected = current_selected[0]
                outlined_btn.style.color = selected_color if is_selected else text_color
                outlined_btn.style.side = ft.BorderSide(width=1, color=selected_bgcolor if is_selected else accent_color)
                outlined_btn.style.bgcolor = selected_bgcolor if is_selected else "transparent"
                outlined_btn.content = create_content(is_selected)
                try:
                    outlined_btn.update()
                except:
                    pass
            
            def outlined_get_selected() -> bool:
                return current_selected[0]
            
            def outlined_toggle_state():
                outlined_set_selected(not current_selected[0])
            
            outlined_btn.set_selected = outlined_set_selected
            outlined_btn.get_selected = outlined_get_selected
            outlined_btn.toggle = outlined_toggle_state
            
            return outlined_btn


# *** 调试逻辑 ***
if __name__ == "__main__":
    ft.run(lambda page: page.add(Button.create()))
