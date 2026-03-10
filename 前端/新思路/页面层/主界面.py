# -*- coding: utf-8 -*-
"""
主界面 - 页面层（新思路）

设计思路:
    组装组件，构建完整的主界面。
    采用装配模式，协调各组件交互。
    匹配Win11设置界面风格。

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
from 新思路.页面层.系统设置页面 import SystemSettingsPage


class MainPage:
    """主界面 - 页面层"""
    
    def __init__(self, config: 界面配置):
        self.config = config
        self.theme_colors = config.当前主题颜色
        self.current_nav = "系统"
        self.content_area = None
        self.page = None
    
    def create(self) -> ft.Container:
        """
        创建主界面
        
        返回:
            ft.Container: 主界面容器
        """
        # 创建用户信息卡片
        user_info_card = UserInfoCard.create(
            config=self.config,
            username="试用用户",
            is_registered=False,
            expire_days=7,
        )
        
        # 创建导航栏
        nav_bar = NavBar.create(
            config=self.config,
            on_nav_change=self.handle_nav_change,
        )
        
        # 左侧导航面板（Win11风格）
        left_panel = ft.Container(
            content=ft.Column(
                [
                    # 用户信息区域
                    ft.Container(
                        content=user_info_card,
                        padding=ft.Padding(left=12, right=12, top=16, bottom=12),
                    ),
                    # 分割线
                    ft.Container(
                        content=ft.Divider(height=1, color=self.theme_colors.get("border")),
                        padding=ft.Padding(left=12, right=12),
                    ),
                    # 导航栏
                    ft.Container(
                        content=nav_bar,
                        padding=ft.Padding(left=8, right=8, top=8, bottom=8),
                        expand=True,
                    ),
                ],
                spacing=0,
                scroll=ft.ScrollMode.AUTO,
            ),
            width=280,
            bgcolor=self.theme_colors.get("bg_secondary"),
            border_radius=ft.BorderRadius(top_left=0, top_right=8, bottom_left=0, bottom_right=8),
        )
        
        # 右侧内容区域（Win11风格）
        self.content_area = ft.Container(
            content=self.get_page_content(self.current_nav),
            padding=ft.Padding(left=40, right=40, top=32, bottom=32),
            expand=True,
        )
        
        # 主布局（左右分栏，Win11风格）
        main_layout = ft.Row(
            [
                left_panel,
                # 内容区域
                ft.Container(
                    content=self.content_area,
                    expand=True,
                ),
            ],
            expand=True,
            spacing=16,
            vertical_alignment=ft.CrossAxisAlignment.START,
        )
        
        # 页面容器
        page_container = ft.Container(
            content=main_layout,
            bgcolor=self.theme_colors.get("bg_primary"),
            padding=ft.Padding.all(0),
            expand=True,
        )
        
        return page_container
    
    def get_page_content(self, nav_name: str) -> ft.Control:
        """获取页面内容"""
        if nav_name == "系统":
            return SystemSettingsPage.create(self.config)
        else:
            # 其他页面暂未实现
            return ft.Column(
                [
                    ft.Text(
                        nav_name,
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color=self.theme_colors.get("text_primary"),
                    ),
                    ft.Container(height=24),
                    ft.Text(
                        f"{nav_name}页面开发中...",
                        size=14,
                        color=self.theme_colors.get("text_secondary"),
                    ),
                ],
                spacing=0,
                expand=True,
            )
    
    def handle_nav_change(self, nav_name: str):
        """处理导航切换"""
        self.current_nav = nav_name
        self.content_area.content = self.get_page_content(nav_name)
        self.content_area.update()


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
        main_page = MainPage(配置)
        page.add(main_page.create())  # 只能更改此处**被测调用模块名称**
    
    ft.run(main)
