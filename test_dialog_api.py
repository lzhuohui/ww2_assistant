# -*- coding: utf-8 -*-
import flet as ft

def main(page: ft.Page):
    page.title = "对话框API测试"
    
    def on_click(e):
        print("点击按钮")
        
        # 创建对话框
        dialog = ft.AlertDialog(
            modal=True,
            content=ft.Column([
                ft.TextButton("选项A", on_click=lambda e: print("选择A")),
                ft.TextButton("选项B", on_click=lambda e: print("选择B")),
                ft.TextButton("选项C", on_click=lambda e: print("选择C")),
            ]),
        )
        
        # 使用show_dialog方法
        page.show_dialog(dialog)
        print("对话框已通过show_dialog打开")
    
    button = ft.ElevatedButton("点击打开对话框", on_click=on_click)
    page.add(button)

ft.app(target=main)
