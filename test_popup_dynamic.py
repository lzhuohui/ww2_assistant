# -*- coding: utf-8 -*-
import flet as ft

def main(page: ft.Page):
    page.title = "PopupMenuButton动态加载测试"
    
    is_loaded = [False]
    
    def create_menu_items():
        print("创建菜单项")
        return [
            ft.PopupMenuItem(content="选项A", on_click=lambda e: print("选择A")),
            ft.PopupMenuItem(content="选项B", on_click=lambda e: print("选择B")),
            ft.PopupMenuItem(content="选项C", on_click=lambda e: print("选择C")),
        ]
    
    def handle_open(e):
        print(f"菜单打开事件触发, is_loaded: {is_loaded[0]}")
        if not is_loaded[0]:
            popup.items = create_menu_items()
            is_loaded[0] = True
            page.update()
            print("选项已动态加载")
    
    popup = ft.PopupMenuButton(
        content=ft.Container(
            content=ft.Text("点击我"),
            width=120,
            height=30,
            bgcolor="#ECEFF1",
            border=ft.border.all(1, "#90A4AE"),
            border_radius=6,
            padding=ft.padding.symmetric(horizontal=12, vertical=0),
        ),
        items=[],  # 初始为空
        on_open=handle_open,
    )
    
    page.add(popup)
    print("页面已加载")

ft.app(target=main)
