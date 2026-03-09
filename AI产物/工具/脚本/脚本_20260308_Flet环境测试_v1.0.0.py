#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flet环境测试脚本

创建日期: 2026-03-08
作者: AI
版本: v1.0.0

用途: 验证Flet开发环境配置是否正确
"""

import flet as ft


def main(page: ft.Page):
    """测试Flet应用"""
    # 页面配置
    page.title = "Flet测试应用"
    page.window_width = 600
    page.window_height = 400
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # 状态变量
    name = ft.Ref[ft.TextField]()
    greeting = ft.Ref[ft.Text]()
    
    # 按钮点击事件
    def say_hello(e):
        greeting.current.value = f"你好，{name.current.value}！"
        page.update()
    
    # 构建界面
    page.add(
        ft.Text("Flet测试应用", size=24, weight=ft.FontWeight.BOLD),
        ft.Text("这是一个测试界面，用于验证Flet环境配置", size=16),
        ft.Divider(),
        ft.TextField(
            ref=name,
            label="请输入你的名字",
            value="张三",
            width=300
        ),
        ft.ElevatedButton(
            "点击问好",
            on_click=say_hello
        ),
        ft.Text(
            ref=greeting,
            size=18,
            color=ft.colors.BLUE
        ),
        ft.Divider(),
        ft.Text("测试内容：", size=16, weight=ft.FontWeight.BOLD),
        ft.Text("1. 文本显示", size=14),
        ft.Text("2. 输入框输入", size=14),
        ft.Text("3. 按钮点击", size=14),
        ft.Text("4. 界面更新", size=14)
    )


if __name__ == "__main__":
    ft.app(target=main)
