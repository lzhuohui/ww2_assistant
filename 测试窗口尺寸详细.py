# -*- coding: utf-8 -*-
"""
详细测试窗口尺寸设置
"""

import flet as ft
import time

# 测试用户指定变量
USER_WINDOW_WIDTH = 1200  # 窗口宽度
USER_WINDOW_HEIGHT = 540  # 窗口高度

def test_method_1(page: ft.Page):
    """方法1: 直接设置window属性"""
    print("测试方法1: 直接设置window属性")
    page.window.width = USER_WINDOW_WIDTH
    page.window.height = USER_WINDOW_HEIGHT
    page.window.resizable = False
    page.update()
    time.sleep(1)
    print(f"  结果: 宽度={page.window.width}, 高度={page.window.height}")

def test_method_2(page: ft.Page):
    """方法2: 使用page属性"""
    print("测试方法2: 使用page属性")
    try:
        page.window_width = USER_WINDOW_WIDTH
        page.window_height = USER_WINDOW_HEIGHT
        page.window_resizable = False
        page.update()
        time.sleep(1)
        print(f"  结果: 宽度={page.window_width}, 高度={page.window_height}")
    except Exception as e:
        print(f"  失败: {e}")

def test_method_3(page: ft.Page):
    """方法3: 先设置再update"""
    print("测试方法3: 先设置再update")
    page.window.width = USER_WINDOW_WIDTH
    page.window.height = USER_WINDOW_HEIGHT
    page.window.resizable = False
    page.update()
    time.sleep(1)
    print(f"  结果: 宽度={page.window.width}, 高度={page.window.height}")

def main(page: ft.Page):
    # 测试不同的窗口尺寸设置方法
    test_method_1(page)
    test_method_2(page)
    test_method_3(page)
    
    # 显示当前窗口尺寸
    page.add(
        ft.Text(f"最终窗口宽度: {page.window.width}"),
        ft.Text(f"最终窗口高度: {page.window.height}"),
        ft.Text(f"用户指定宽度: {USER_WINDOW_WIDTH}"),
        ft.Text(f"用户指定高度: {USER_WINDOW_HEIGHT}")
    )

if __name__ == "__main__":
    ft.run(main)