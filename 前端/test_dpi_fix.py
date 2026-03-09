#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DPI缩放问题测试

创建日期: 2026-03-08
作者: AI
版本: v1.0.0

说明：测试Windows 11 DPI缩放问题的解决方案
"""

import flet as ft
import ctypes


def main(page: ft.Page):
    """主函数"""
    # 尝试禁用DPI缩放
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)  # PROCESS_PER_MONITOR_DPI_AWARE
    except:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except:
            pass
    
    # 设置页面
    page.title = "二战风云 - DPI修复测试"
    page.window_width = 1200
    page.window_height = 540
    page.bgcolor = "#1C1C1C"
    page.padding = 0
    
    # 清空页面
    page.clean()
    
    # 导航栏
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
        padding=20,
        bgcolor="#1C1C1C"
    )
    
    # 内容区域
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
        bgcolor="#1C1C1C",
        expand=True
    )
    
    # 创建主布局 - 使用最简单的Row
    main_layout = ft.Row([
        nav,
        ft.VerticalDivider(width=1, color="#404040"),
        content
    ], spacing=0, expand=True)
    
    # 添加到页面
    page.add(main_layout)


if __name__ == "__main__":
    print("正在启动DPI修复测试...")
    print("已尝试禁用DPI缩放，测试是否能解决三层问题")
    ft.run(main)