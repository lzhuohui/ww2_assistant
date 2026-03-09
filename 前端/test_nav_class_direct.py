#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试NavigationBar类 - 直接使用颜色值

创建日期: 2026-03-08
作者: AI
版本: v1.0.0

说明：测试使用NavigationBar类，但直接使用颜色值，不通过get_color函数
"""

import flet as ft
import sys
sys.path.append('.')
from windows11.navigation import NavigationBar


def main(page: ft.Page):
    """主函数"""
    # 设置页面
    page.title = "二战风云 - NavigationBar类测试（直接颜色）"
    page.window_width = 1200
    page.window_height = 540
    page.bgcolor = "#1C1C1C"
    page.padding = 0
    
    # 清空页面
    page.clean()
    
    # 导航数据
    navigation_data = {
        "系统": {
            "items": [
                {"id": "system_device", "text": "设备管理"},
                {"id": "system_info", "text": "系统信息"},
                {"id": "system_activation", "text": "授权管理"}
            ]
        },
        "通用设置": {
            "items": [
                {"id": "general_settings", "text": "基本参数"}
            ]
        },
        "策略设置": {
            "items": [
                {"id": "strategy_settings", "text": "策略配置"}
            ]
        }
    }
    
    # 导航变化回调
    def on_nav_change(item_id):
        print(f"导航变化: {item_id}")
    
    # 导航栏 - 使用NavigationBar类
    nav = NavigationBar(navigation_data, on_nav_change)
    
    # 内容区域
    content = ft.Column([
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
    ])
    
    # 创建主布局 - 使用与主项目完全相同的结构
    main_layout = ft.Container(
        content=ft.Row([
            nav,
            ft.VerticalDivider(width=1, color="#404040"),
            ft.Container(
                content=content,
                expand=True
            )
        ], spacing=0),
        expand=True,
        bgcolor="#1C1C1C"
    )
    
    # 添加到页面
    page.add(main_layout)


if __name__ == "__main__":
    print("正在启动NavigationBar类测试（直接颜色）...")
    print("测试使用NavigationBar类，但直接使用颜色值")
    ft.run(main)