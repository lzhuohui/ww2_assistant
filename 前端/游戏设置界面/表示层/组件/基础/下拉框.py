# -*- coding: utf-8 -*-
"""
模块名称：Dropdown
模块功能：下拉框组件，使用PopupMenuButton实现
实现步骤：
- 创建时加载选项列表
- 选择后更新值并关闭菜单
- 支持销毁管理减少内存占用
- Win11风格
"""

import flet as ft
from typing import List, Callable

# from 核心层.配置.界面配置 import UIConfig


# *** 用户指定变量: 变量值必须生效,AI不得更改数据 ***
USER_WIDTH = 120  # 下拉框宽度
USER_HEIGHT = 30  # 下拉框高度
# *********************************


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
        config: any = None,
    ) -> ft.Container:
        if config is None:
            # 使用默认颜色配置
            theme_colors = {
                "text_primary": "#000000",
                "text_secondary": "#666666",
                "text_disabled": "#999999",
                "bg_primary": "#FFFFFF",
                "bg_secondary": "#F5F5F5",
                "border": "#CCCCCC",
                "accent": "#0078D4"
            }
        else:
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
        
        # 创建菜单项函数
        def create_menu_items():
            """创建菜单项列表"""
            menu_items = []
            for option in actual_options:
                def create_callback(value=option):
                    def callback(e):
                        # 选择值
                        current_selected_value[0] = value
                        selected_text.value = value
                        
                        # 触发回调
                        if on_change:
                            on_change(value)
                        
                        # 更新显示
                        if container.page:
                            container.update()
                    return callback
                
                menu_item = ft.PopupMenuItem(
                    content=option,
                    on_click=create_callback(),
                )
                menu_items.append(menu_item)
            return menu_items
        
        # 创建PopupMenuButton，创建时加载选项
        popup_menu_button = ft.PopupMenuButton(
            content=ft.Container(
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
            ),
            items=create_menu_items(),  # 创建时加载选项
            menu_padding=0,
            enable_feedback=True,
            tooltip="",  # 隐藏"show menu"提示
        )
        
        container = ft.Container(
            content=popup_menu_button,
            width=width,
        )
        
        def handle_hover(e):
            if not enabled_state[0]:
                return
            button_content = popup_menu_button.content
            if e.data == "true":
                button_content.border = ft.border.all(1, theme_colors.get("accent"))
            else:
                button_content.border = ft.border.all(1, theme_colors.get("border"))
            try:
                if container.page:
                    container.update()
            except:
                pass
        
        popup_menu_button.content.on_hover = handle_hover
        
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
            popup_menu_button.content.bgcolor = bg_col
            popup_menu_button.content.border = ft.border.all(1, border_col)
            
            try:
                if container.page:
                    container.update()
            except:
                pass
        
        def set_options(new_options: List[str]):
            """设置选项列表"""
            nonlocal actual_options
            actual_options = new_options
            
            # 如果当前值是无效的，重置为第一个选项
            if current_selected_value[0] not in new_options and new_options:
                current_selected_value[0] = new_options[0]
                selected_text.value = new_options[0]
            
            # 重新创建菜单项
            popup_menu_button.items = create_menu_items()
            if container.page:
                container.page.update()
        
        container.get_value = get_value
        container.set_value = set_value
        container.set_enabled = set_enabled
        container.set_options = set_options
        
        return container


# *** 标准测试格式: 仅调用被测模块,AI不得添加数据 ***
if __name__ == "__main__":
    def main(page: ft.Page):
        # 创建简单的配置对象
        class SimpleConfig:
            def __init__(self):
                self.当前主题颜色 = {
                    "text_primary": "#000000",
                    "text_secondary": "#666666",
                    "text_disabled": "#999999",
                    "bg_primary": "#FFFFFF",
                    "bg_secondary": "#F5F5F5",
                    "border": "#CCCCCC",
                    "accent": "#0078D4"
                }
        
        config = SimpleConfig()
        
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
