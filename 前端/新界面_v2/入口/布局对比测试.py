# -*- coding: utf-8 -*-
"""
布局对比测试 - 验证修复前后的布局差异
"""

import flet as ft
from 前端.新界面_v2.核心.配置.界面配置 import UIConfig
from 前端.新界面_v2.核心.常量.全局常量 import USER_SPACING
from 前端.新界面_v2.表示层.界面.系统界面 import SystemPage
from 前端.新界面_v2.表示层.组件.复合.用户信息卡片 import UserInfoCard
from 前端.新界面_v2.表示层.组件.基础.卡片容器 import USER_PADDING


def 创建修复前版本():
    """创建修复前的版本 - 有问题的版本"""
    config = UIConfig()
    theme_colors = config.当前主题颜色
    
    # 左侧导航面板
    user_info = UserInfoCard.create(config=config)
    
    nav_panel = ft.Container(
        content=ft.Column([
            user_info,
            ft.Container(height=USER_SPACING),
        ], spacing=0),
        width=280,
        padding=ft.Padding(
            left=USER_SPACING,
            top=USER_SPACING,
            right=USER_SPACING * 2,
            bottom=USER_SPACING,
        ),
        bgcolor=theme_colors.get("bg_primary"),
        border=ft.Border.all(2, "red"),  # 红色边框显示左侧面板
    )
    
    # 右侧内容区域 - 使用修复前的padding.top值
    system_page = SystemPage.create(config=config)
    
    content_container = ft.Container(
        content=system_page,
        padding=ft.Padding(
            left=USER_SPACING * 2,
            top=USER_SPACING + USER_PADDING,  # 修复前的问题：多了USER_PADDING
            right=USER_SPACING,
            bottom=USER_SPACING * 2,
        ),
        expand=True,
        border=ft.Border.all(2, "blue"),  # 蓝色边框显示右侧内容
    )
    
    return ft.Row([nav_panel, content_container], expand=True, spacing=0)


def 创建修复后版本():
    """创建修复后的版本 - 正确的版本"""
    config = UIConfig()
    theme_colors = config.当前主题颜色
    
    # 左侧导航面板
    user_info = UserInfoCard.create(config=config)
    
    nav_panel = ft.Container(
        content=ft.Column([
            user_info,
            ft.Container(height=USER_SPACING),
        ], spacing=0),
        width=280,
        padding=ft.Padding(
            left=USER_SPACING,
            top=USER_SPACING,
            right=USER_SPACING * 2,
            bottom=USER_SPACING,
        ),
        bgcolor=theme_colors.get("bg_primary"),
        border=ft.Border.all(2, "green"),  # 绿色边框显示左侧面板
    )
    
    # 右侧内容区域 - 使用修复后的padding.top值
    system_page = SystemPage.create(config=config)
    
    content_container = ft.Container(
        content=system_page,
        padding=ft.Padding(
            left=USER_SPACING * 2,
            top=USER_SPACING,  # 修复后：只使用USER_SPACING
            right=USER_SPACING,
            bottom=USER_SPACING * 2,
        ),
        expand=True,
        border=ft.Border.all(2, "orange"),  # 橙色边框显示右侧内容
    )
    
    return ft.Row([nav_panel, content_container], expand=True, spacing=0)


def test_layout_comparison(page: ft.Page):
    """布局对比测试"""
    config = UIConfig()
    
    # 设置窗口 - 加宽以容纳两个并排的界面
    page.window.width = 1600
    page.window.height = 600
    page.window.resizable = False
    page.bgcolor = config.当前主题颜色.get("bg_primary")
    page.padding = USER_SPACING
    
    # 创建对比界面
    layout = ft.Column([
        ft.Text("布局对比测试", size=18, weight=ft.FontWeight.BOLD),
        ft.Text(f"USER_SPACING: {USER_SPACING}, USER_PADDING: {USER_PADDING}", size=14),
        ft.Container(height=USER_SPACING),
        
        # 对比说明
        ft.Row([
            ft.Column([
                ft.Text("修复前（问题版本）", size=14, weight=ft.FontWeight.BOLD, color="red"),
                ft.Text("右侧顶部padding: USER_SPACING + USER_PADDING", size=12),
                ft.Container(height=4),
            ]),
            ft.Container(width=USER_SPACING * 4),
            ft.Column([
                ft.Text("修复后（正确版本）", size=14, weight=ft.FontWeight.BOLD, color="green"),
                ft.Text("右侧顶部padding: USER_SPACING", size=12),
                ft.Container(height=4),
            ]),
        ]),
        
        ft.Container(height=USER_SPACING),
        
        # 主要对比区域
        ft.Row([
            创建修复前版本(),
            ft.Container(width=USER_SPACING),
            创建修复后版本(),
        ], expand=True),
    ])
    
    page.add(layout)
    
    print(f"布局对比测试启动")
    print(f"左侧面板顶部: 距离窗口顶部 {USER_SPACING}px")
    print(f"修复前右侧顶部: 距离窗口顶部 {USER_SPACING + USER_PADDING}px")
    print(f"修复后右侧顶部: 距离窗口顶部 {USER_SPACING}px")
    print(f"垂直对齐差异: {USER_PADDING}px")


if __name__ == "__main__":
    ft.run(test_layout_comparison)