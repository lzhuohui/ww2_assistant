# -*- coding: utf-8 -*-
"""
测试窗口尺寸是否生效
"""

import flet as ft
from 前端.新界面_v2.入口.主界面 import USER_WINDOW_WIDTH, USER_WINDOW_HEIGHT, USER_SPACING

def test_window_size(page: ft.Page):
    """测试窗口尺寸设置"""
    # 直接设置窗口尺寸
    page.window.width = USER_WINDOW_WIDTH
    page.window.height = USER_WINDOW_HEIGHT
    page.window.resizable = False
    
    # 添加一个简单的界面来验证
    page.add(
        ft.Container(
            content=ft.Column([
                ft.Text(f"窗口宽度: {USER_WINDOW_WIDTH}", size=16, weight=ft.FontWeight.BOLD),
                ft.Text(f"窗口高度: {USER_WINDOW_HEIGHT}", size=16, weight=ft.FontWeight.BOLD),
                ft.Text(f"USER_SPACING: {USER_SPACING}", size=16, weight=ft.FontWeight.BOLD),
                ft.Container(height=USER_SPACING),
                ft.Text("如果窗口尺寸不是1200x540，说明变量没生效", size=14, color="red"),
            ]),
            padding=USER_SPACING * 2,
            expand=True,
        )
    )
    
    # 打印调试信息
    print(f"设置的窗口宽度: {USER_WINDOW_WIDTH}")
    print(f"设置的窗口高度: {USER_WINDOW_HEIGHT}")
    print(f"实际的窗口宽度: {page.window.width}")
    print(f"实际的窗口高度: {page.window.height}")
    print(f"实际的USER_SPACING: {USER_SPACING}")

if __name__ == "__main__":
    ft.run(test_window_size)