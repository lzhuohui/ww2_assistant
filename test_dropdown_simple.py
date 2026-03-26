# -*- coding: utf-8 -*-
import flet as ft

def main(page: ft.Page):
    page.title = "下拉框测试"
    
    # 创建一个简单的Container测试点击事件
    def on_click(e):
        print("Container被点击")
        # 创建对话框
        dialog = ft.AlertDialog(
            modal=True,
            content=ft.Column([
                ft.TextButton("选项A", on_click=lambda e: print("选择A")),
                ft.TextButton("选项B", on_click=lambda e: print("选择B")),
            ]),
        )
        page.dialog = dialog
        dialog.open = True
        page.update()
        print("对话框已设置")
    
    container = ft.Container(
        content=ft.Row([
            ft.Text("点击我"),
            ft.Icon(ft.Icons.KEYBOARD_ARROW_DOWN),
        ]),
        width=120,
        height=30,
        bgcolor="#ECEFF1",
        border=ft.border.all(1, "#90A4AE"),
        border_radius=6,
        on_click=on_click,
    )
    
    page.add(container)
    print("页面已加载")

ft.app(target=main)
