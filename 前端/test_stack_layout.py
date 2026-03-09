#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试使用ft.Stack布局

创建日期: 2026-03-08
作者: AI
版本: v1.0.0

说明：测试使用ft.Stack布局是否可以解决ft.Icon导致的白板问题
"""

import flet as ft


class NavBarWithStack(ft.Container):
    """使用ft.Stack布局的导航栏类"""
    def __init__(self, on_nav_change=None):
        super().__init__()
        self.on_nav_change = on_nav_change
        self.expanded_groups = set()
        self.active_group = None
        self.active_item = None
        self._build()
    
    def _build(self):
        """构建导航栏"""
        controls = [
            ft.Text("设置", size=20, weight=ft.FontWeight.BOLD, color="#F2F2F2"),
            ft.Divider(height=16)
        ]
        
        # 添加分组
        groups = ["系统", "通用设置", "策略设置"]
        for group in groups:
            is_expanded = group in self.expanded_groups
            group_title = ft.Container(
                content=ft.Row([
                    ft.Text(group, color="#0078D4", size=14, weight=ft.FontWeight.BOLD),
                    ft.Icon(
                        "expand_more" if is_expanded else "chevron_right",
                        size=16,
                        color="#CCCCCC"
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=ft.Padding(left=16, right=16, top=8, bottom=8),
                on_click=lambda e, g=group: self._on_group_click(g)
            )
            controls.append(group_title)
        
        self.content = ft.Column(controls, spacing=0)
        self.width = 240
        self.padding = 20
        self.bgcolor = "#1C1C1C"
    
    def _on_group_click(self, group_name):
        """分组点击事件"""
        if group_name in self.expanded_groups:
            self.expanded_groups.remove(group_name)
        else:
            self.expanded_groups.add(group_name)
        
        self.active_group = group_name
        self._build()
        
        if self.on_nav_change:
            self.on_nav_change(group_name)


def main(page: ft.Page):
    """主函数"""
    # 设置页面
    page.title = "二战风云 - Stack布局测试"
    page.window_width = 1200
    page.window_height = 540
    page.bgcolor = "#1C1C1C"
    page.padding = 0
    
    # 清空页面
    page.clean()
    
    # 导航变化回调
    def on_nav_change(item_id):
        print(f"导航变化: {item_id}")
    
    # 导航栏 - 使用NavBarWithStack类
    nav = NavBarWithStack(on_nav_change)
    
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
    
    # 创建主布局 - 使用ft.Stack，与旧版本相同
    内容区容器 = ft.Container(
        content=content,
        top=0,
        left=240,
        right=0,
        bottom=0,
        bgcolor="#1C1C1C"
    )
    
    导航栏容器 = ft.Container(
        content=nav,
        width=240,
        top=0,
        left=0,
        bottom=0,
        bgcolor="#1C1C1C"
    )
    
    主容器 = ft.Stack([
        内容区容器,
        导航栏容器,
    ], expand=True)
    
    # 添加到页面
    page.add(主容器)


if __name__ == "__main__":
    print("正在启动Stack布局测试...")
    print("测试使用ft.Stack布局是否可以解决ft.Icon导致的白板问题")
    ft.run(main)