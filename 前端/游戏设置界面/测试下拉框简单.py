# -*- coding: utf-8 -*-
"""
简单测试下拉框功能
"""

import flet as ft
import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 直接复制下拉框代码，避免导入问题
class Dropdown:
    """下拉框组件 - 使用PopupMenuButton实现"""
    
    @staticmethod
    def create(
        options=None,
        current_value="",
        width=120,
        height=30,
        enabled=True,
        on_change=None,
        config=None,
    ):
        if options is None:
            options = ["选项A", "选项B", "选项C"]
        
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
        
        actual_options = options
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
        
        def get_value():
            return current_selected_value[0]
        
        def set_value(new_value):
            if new_value in actual_options:
                current_selected_value[0] = new_value
                selected_text.value = new_value
                if container.page:
                    container.update()
        
        def set_enabled(state):
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
        
        def set_options(new_options):
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

def main(page: ft.Page):
    page.title = "下拉框测试"
    page.window_width = 400
    page.window_height = 300
    
    def on_change(value):
        print(f"选择了: {value}")
    
    # 创建3个下拉框
    dropdown1 = Dropdown.create(
        options=["选项1", "选项2", "选项3"],
        current_value="选项1",
        on_change=on_change,
        width=200
    )
    
    dropdown2 = Dropdown.create(
        options=["苹果", "香蕉", "橙子"],
        current_value="苹果",
        on_change=on_change,
        width=200
    )
    
    dropdown3 = Dropdown.create(
        options=["红色", "绿色", "蓝色"],
        current_value="红色",
        on_change=on_change,
        width=200
    )
    
    page.add(
        ft.Column([
            ft.Text("测试下拉框是否能正常打开选项列表", size=16, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            dropdown1,
            dropdown2,
            dropdown3,
            ft.Text("点击下拉框，应该能正常显示选项列表", size=12, color="#666666")
        ], spacing=20)
    )

if __name__ == "__main__":
    ft.app(target=main)