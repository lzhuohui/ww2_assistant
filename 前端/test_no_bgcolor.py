#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最简单版本 - 不设置bgcolor

创建日期: 2026-03-08
作者: AI
版本: v1.0.0

说明：测试不设置bgcolor是否能解决白板问题
"""

import flet as ft


def main(page: ft.Page):
    """主函数"""
    # 设置页面
    page.title = "二战风云 - 无bgcolor测试"
    page.window_width = 1200
    page.window_height = 540
    page.bgcolor = "#1C1C1C"
    page.padding = 0
    
    # 清空页面
    page.clean()
    
    # 导航栏 - 不设置bgcolor
    nav = ft.Container(
        content=ft.Column([
            ft.Text("设置", size=20, weight=ft.FontWeight.BOLD, color="#F2F2F2"),
            ft.Divider(height=16),
            ft.Text("系统", color="#0078D4", size=14, weight=ft.FontWeight.BOLD),
            ft.Text("  设备管理", color="#F2F2F2", size=14),
            ft.Text("  系统信息", color="#F2F2F2", size=14),
            ft.Text("  授权管理", color="#F2F2F2", size=14),
            ft.Divider(height=8),
            ft.Text("通用设置", color="#0078D4", size=14, weight=ft.FontWeight.BOLD),
            ft.Text("  基本参数", color="#F2F2F2", size=14),
            ft.Divider(height=8),
            ft.Text("策略设置", color="#0078D4", size=14, weight=ft.FontWeight.BOLD),
            ft.Text("  策略配置", color="#F2F2F2", size=14)
        ]),
        width=240,
        padding=20
        # 不设置bgcolor
    )
    
    # 内容区域 - 不设置bgcolor
    content = ft.Container(
        content=ft.Column([
            ft.Text("ADB设备", size=18, weight=ft.FontWeight.BOLD, color="#F2F2F2"),
            ft.Text("管理连接的设备", size=12, color="#CCCCCC"),
            ft.Divider(height=16, color="transparent"),
            ft.Text("已连接设备:", color="#F2F2F2"),
            ft.Text("127.0.0.1:5555 (蓝叠模拟器)", size=14, color="#F2F2F2"),
            ft.Divider(height=16, color="transparent"),
            ft.Row([
                ft.Button("刷新设备列表", style=ft.ButtonStyle(bgcolor="#0078D4", color="white", elevation=0)),
                ft.Button("连接新设备", style=ft.ButtonStyle(bgcolor="#2D2D2D", color="#F2F2F2", elevation=0))
            ])
        ]),
        padding=20,
        expand=True
        # 不设置bgcolor
    )
    
    # 创建主布局 - 使用最简单的Row，不设置bgcolor
    main_layout = ft.Row([
        nav,
        ft.VerticalDivider(width=1, color="#404040"),
        content
    ], spacing=0, expand=True)
    
    # 添加到页面
    page.add(main_layout)


if __name__ == "__main__":
    print("正在启动无bgcolor测试...")
    print("测试不设置bgcolor是否能解决白板问题")
    ft.run(main)