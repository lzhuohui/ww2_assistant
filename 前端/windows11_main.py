#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows 11风格界面 - 主文件

创建日期: 2026-03-08
作者: AI
版本: v1.0.0

说明：基于Windows 11设计风格的Flet界面实现
"""

import flet as ft
from windows11.components import create_main_layout
from windows11.styles import get_color


def main(page: ft.Page):
    """主函数"""
    # 设置页面
    page.title = "二战风云 - Windows 11风格"
    page.window_width = 1200
    page.window_height = 540
    page.bgcolor = get_color("bg_primary")  
    page.padding = 20
    
    # 清空页面，确保没有其他元素
    page.clean()
    
    # 创建主布局
    main_layout = create_main_layout(page) # 创建主布局
    
    # 添加到页面
    page.add(main_layout) # 添加主布局到页面


if __name__ == "__main__":
    print("正在启动Windows 11风格界面...")
    print("请稍候，界面即将出现...")
    ft.run(main)