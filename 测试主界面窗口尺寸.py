# -*- coding: utf-8 -*-
"""
测试主界面窗口尺寸设置
"""

import flet as ft
import time

# 直接导入主界面模块
from 前端.新界面_v2.入口.主界面 import MainInterface, USER_WINDOW_WIDTH, USER_WINDOW_HEIGHT

def main(page: ft.Page):
    # 打印用户指定的窗口尺寸
    print(f"用户指定窗口宽度: {USER_WINDOW_WIDTH}")
    print(f"用户指定窗口高度: {USER_WINDOW_HEIGHT}")
    
    # 直接设置窗口尺寸（模拟旧版的做法）
    page.window.width = USER_WINDOW_WIDTH
    page.window.height = USER_WINDOW_HEIGHT
    page.window.resizable = False
    page.update()
    time.sleep(1)
    print(f"直接设置后窗口宽度: {page.window.width}")
    print(f"直接设置后窗口高度: {page.window.height}")
    
    # 使用MainInterface的setup_window方法
    from 前端.新界面_v2.核心.配置.界面配置 import UIConfig
    config = UIConfig()
    MainInterface.setup_window(page, config)
    time.sleep(1)
    print(f"使用setup_window后窗口宽度: {page.window.width}")
    print(f"使用setup_window后窗口高度: {page.window.height}")
    
    # 添加主界面内容
    main_interface = MainInterface.create(page=page, config=config)
    page.add(main_interface)
    time.sleep(2)
    print(f"添加主界面后窗口宽度: {page.window.width}")
    print(f"添加主界面后窗口高度: {page.window.height}")

if __name__ == "__main__":
    ft.run(main)