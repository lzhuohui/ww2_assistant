# -*- coding: utf-8 -*-
"""
主界面 - 页面层（新思路）

设计思路:
    组装组件，构建完整的主界面。
    采用装配模式，协调各组件交互。

功能:
    1. 组装用户信息卡片
    2. 组装导航栏
    3. 组装设置信息内容
    4. 协调导航切换

数据来源:
    所有配置数据从配置目录获取。

使用场景:
    应用主入口。

可独立运行调试: python 主界面.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft
from 配置.界面配置 import 界面配置
from 新思路.组件层.用户信息卡片 import UserInfoCard
from 新思路.组件层.导航栏 import NavBar


class MainPage:
    """主界面 - 页面层"""
    
    @staticmethod
    def create(config: 界面配置) -> ft.Container:
        """
        创建主界面
        
        参数:
            config: 界面配置对象
        
        返回:
            ft.Container: 主界面容器
        """
        theme_colors = config.当前主题颜色
        
        # 内部状态
        current_nav = "系统设置"
        
        # 创建用户信息卡片
        user_info_card = UserInfoCard.create(
            config=config,
            username="测试用户",
        )
        
        # 创建导航栏
        def handle_nav_change(nav_name: str):
            nonlocal current_nav
            current_nav = nav_name
            # TODO: 切换内容区域
            print(f"导航切换: {nav_name}")
        
        nav_bar = NavBar.create(
            config=config,
            on_nav_change=handle_nav_change,
        )
        
        # 左侧面板（用户信息 + 导航栏）
        left_panel = ft.Column(
            [
                user_info_card,
                ft.Container(height=10),
                nav_bar,
            ],
            width=240,
            spacing=0,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.START,
        )
        
        # 右侧内容区域（设置信息）
        # TODO: 根据导航切换内容
        content_area = ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "系统设置",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=theme_colors.get("text_primary"),
                    ),
                    ft.Container(height=20),
                    ft.Text(
                        "这里是设置内容区域",
                        size=14,
                        color=theme_colors.get("text_secondary"),
                    ),
                ],
                spacing=0,
            ),
            padding=ft.Padding.all(20),
            expand=True,
        )
        
        # 主布局（左右分栏）
        main_layout = ft.Row(
            [
                ft.Container(
                    content=left_panel,
                    width=240,
                    bgcolor=theme_colors.get("bg_secondary"),
                    alignment=ft.Alignment(-1, -1),
                ),
                ft.VerticalDivider(width=1, color=theme_colors.get("border")),
                content_area,
            ],
            expand=True,
            spacing=0,
            vertical_alignment=ft.CrossAxisAlignment.START,
        )
        
        # 页面容器
        page_container = ft.Container(
            content=main_layout,
            bgcolor=theme_colors.get("bg_primary"),
            expand=True,
        )
        
        return page_container


# 兼容别名
主界面 = MainPage


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    # 1. 界面配置初始化
    配置 = 界面配置()
    
    # 2. 自动加载用户数据覆盖默认值（在界面配置.__init__中自动完成）
    
    # 3. 正常启动被测模块
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        page.add(MainPage.create(配置))  # 只能更改此处**被测调用模块名称**
    
    ft.run(main)
