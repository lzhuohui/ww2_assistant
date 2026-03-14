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
from 新思路.零件层.卡片容器 import CardContainer
from 新思路.组件层.用户信息卡片 import UserInfoCard
from 新思路.组件层.导航栏 import NavBar
from 新思路.页面层.系统设置页面 import SystemSettingsPage
from 新思路.页面层.策略设置页面 import StrategySettingsPage
from 新思路.页面层.任务设置页面 import TaskSettingsPage
from 新思路.页面层.建筑设置页面 import BuildingSettingsPage
from 新思路.页面层.集资设置页面 import FundraisingSettingsPage
from 新思路.页面层.打扫设置页面 import CleaningSettingsPage
from 新思路.页面层.打野设置页面 import WildSettingsPage
from 新思路.页面层.账号设置页面 import AccountSettingsPage
from 新思路.页面层.个性化设置页面 import PersonalizationSettingsPage
from 新思路.页面层.关于设置页面 import AboutSettingsPage


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
        # 设置窗口尺寸（从配置文件读取）
        if self.page:
            ui_config = self.config.定义尺寸.get("界面", {})
            self.page.window.width = ui_config.get("window_width", 1200)
            self.page.window.height = ui_config.get("window_height", 540)
        
        # 创建用户信息卡片
        user_info_card = UserInfoCard.create(
            config=self.config,
            username="试用用户",
            is_registered=False,
            expire_days=7,
            on_click=self.show_license_dialog,
        )
        
        # 创建导航栏
        nav_bar = NavBar.create(
            config=self.config,
            on_nav_change=self.handle_nav_change,
        )
        
        # 左侧导航面板（Win11风格）
        ui_config = self.config.定义尺寸.get("界面", {})
        
        left_panel = CardContainer.create(
            config=self.config,
            content=ft.Column(
                [
                    ft.Container(
                        content=user_info_card,
                    ),
                    ft.Container(
                        content=ft.Divider(height=1, color=self.theme_colors.get("border")),
                        padding=ft.Padding(
                            left=ui_config.get("divider_padding_left", 12),
                            right=ui_config.get("divider_padding_right", 12),
                        ),
                    ),
                    ft.Container(
                        content=nav_bar,
                        width=ui_config.get("left_panel_width", 280),
                        expand=True,
                    ),
                ],
                spacing=0,
                expand=True,
            ),
            width=ui_config.get("left_panel_width", 280),
            on_hover_enabled=False,
        )
        
        # 右侧内容区域（Win11风格）
        self.content_area = ft.Container(
            content=self.get_page_content(self.current_nav),
            padding=ft.Padding(
                left=ui_config.get("content_padding_left", 40),
                right=ui_config.get("content_padding_right", 40),
                top=ui_config.get("content_padding_top", 32),
                bottom=ui_config.get("content_padding_bottom", 32),
            ),
            expand=True,
            bgcolor=self.theme_colors.get("bg_primary"),
        )
        
        # 主布局（左右分栏，Win11风格）
        main_layout = ft.Row(
            [
                left_panel,
                # 内容区域
                self.content_area,
            ],
            expand=True,
            spacing=0,
            vertical_alignment=ft.CrossAxisAlignment.START,
        )
        
        page_padding = ui_config.get("page_padding", 10)
        
        # 页面容器
        page_container = ft.Container(
            content=main_layout,
            bgcolor=self.theme_colors.get("bg_primary"),
            padding=ft.Padding(
                left=page_padding,
                top=page_padding,
                right=0,
                bottom=page_padding,
            ),
            expand=True,
        )
        
        return page_container
    
    def get_page_content(self, nav_name: str) -> ft.Control:
        """获取页面内容"""
        if nav_name == "系统":
            return SystemSettingsPage.create(self.config, self.page, self.refresh)
        elif nav_name == "策略":
            return StrategySettingsPage.create(self.config, self.page, self.refresh)
        elif nav_name == "任务":
            return TaskSettingsPage.create(self.config, self.page, self.refresh)
        elif nav_name == "建筑":
            return BuildingSettingsPage.create(self.config, self.page, self.refresh)
        elif nav_name == "集资":
            return FundraisingSettingsPage.create(self.config, self.page, self.refresh)
        elif nav_name == "账号":
            return AccountSettingsPage.create(self.config, self.page, self.refresh)
        elif nav_name == "打扫":
            return CleaningSettingsPage.create(self.config, self.page, self.refresh)
        elif nav_name == "打野":
            return WildSettingsPage.create(self.config, self.page, self.refresh)
        elif nav_name == "个性化":
            return PersonalizationSettingsPage.create(self.config, self.page, self.refresh)
        elif nav_name == "关于":
            return AboutSettingsPage.create(self.config, self.page, self.refresh)
        else:
            return self.get_placeholder_page(nav_name)
    
    def get_placeholder_page(self, nav_name: str) -> ft.Column:
        """获取占位页面"""
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
    
    def show_license_dialog(self):
        """显示授权管理对话框"""
        def close_dialog(e):
            license_dialog.open = False
            self.page.update()
        
        def activate(e):
            code = license_input.value
            if code:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"授权码已提交: {code}"),
                    duration=2000,
                )
                self.page.snack_bar.open = True
                license_dialog.open = False
                self.page.update()
        
        def go_to_about(e):
            license_dialog.open = False
            self.page.update()
            self.handle_nav_change("关于")
        
        license_input = ft.TextField(
            label="请输入授权码",
            width=300,
            border_color=self.theme_colors.get("accent"),
        )
        
        license_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("授权管理", size=20, weight=ft.FontWeight.BOLD),
            content=ft.Column(
                [
                    ft.Text("当前状态：试用用户", size=14, color=self.theme_colors.get("text_secondary")),
                    ft.Text("剩余天数：7天", size=14, color=self.theme_colors.get("text_secondary")),
                    ft.Container(height=10),
                    license_input,
                    ft.Container(height=10),
                    ft.TextButton(
                        "获取授权码 → 查看联系方式",
                        on_click=go_to_about,
                        style=ft.ButtonStyle(
                            color=self.theme_colors.get("accent"),
                        ),
                    ),
                ],
                tight=True,
                spacing=5,
            ),
            actions=[
                ft.TextButton("取消", on_click=close_dialog),
                ft.Button("激活", on_click=activate),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        self.page.dialog = license_dialog
        license_dialog.open = True
        self.page.update()
    
    def refresh(self):
        """刷新整个界面（主题切换后调用）"""
        # 更新主题颜色
        self.theme_colors = self.config.当前主题颜色
        
        # 重新创建整个界面以应用新主题
        if self.page:
            # 清空页面
            self.page.controls.clear()
            # 重新创建主界面
            main_page = MainPage(self.config)
            main_page.page = self.page
            self.page.add(main_page.create())
            # 更新页面
            self.page.update()


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
        main_page.page = page  # 设置page引用，用于刷新
        page.add(main_page.create())  # 只能更改此处**被测调用模块名称**
    
    ft.run(main)
