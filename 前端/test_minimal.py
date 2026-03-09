#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最简单的测试 - 只显示文本

创建日期: 2026-03-08
作者: AI
版本: v1.0.0

说明：测试最简单的界面，确认是否是Flet本身的问题
"""

import flet as ft


def main(page: ft.Page):
    """主函数"""
    # 设置页面
    page.title = "二战风云 - 最简单测试"
    page.window_width = 1200
    page.window_height = 540
    page.bgcolor = "#1C1C1C"
    page.padding = 0
    
    # 清空页面
    page.clean()
    
    # 只显示一个简单的文本
    page.add(
        ft.Container(
            content=ft.Text("这是一个最简单的测试", size=24, color="#F2F2F2"),
            alignment=ft.alignment.Alignment(0.5, 0.5),  # 使用正确的API
            expand=True
        )
    )


if __name__ == "__main__":
    print("正在启动最简单的测试...")
    print("如果这个也有三层问题，那么问题可能是Flet本身的问题")
    ft.run(main)