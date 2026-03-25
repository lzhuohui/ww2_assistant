# -*- coding: utf-8 -*-
"""
测试窗口尺寸设置
"""

import flet as ft

# 测试用户指定变量
USER_WINDOW_WIDTH = 1200  # 窗口宽度
USER_WINDOW_HEIGHT = 540  # 窗口高度

def main(page: ft.Page):
    # 设置窗口尺寸
    page.window.width = USER_WINDOW_WIDTH
    page.window.height = USER_WINDOW_HEIGHT
    page.window.resizable = False
    
    # 显示当前窗口尺寸
    page.add(
        ft.Text(f"窗口宽度: {page.window.width}"),
        ft.Text(f"窗口高度: {page.window.height}"),
        ft.Text(f"用户指定宽度: {USER_WINDOW_WIDTH}"),
        ft.Text(f"用户指定高度: {USER_WINDOW_HEIGHT}")
    )

if __name__ == "__main__":
    ft.run(main)