# -*- coding: utf-8 -*-
"""
主界面优化版 - 页面层

设计思路:
    页面延迟创建， 配置延迟保存。
    建筑设置页面使用懒加载版本。

功能:
    1. 页面延迟创建
    2. 配置延迟保存
    3. 退出时保存当前卡片数据

使用场景:
    应用主入口。
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft
from 配置.界面配置 import 界面配置
from 配置.配置管理器 import ConfigManager
from 新思路.组件层.用户信息卡片 import UserInfoCard
from 新思路.组件层.导航栏 import NavBar
from 优化界面.组件层.懒加载通用卡片 import LazyCardManager


class MainPageOptimized:
    """主界面优化版 - 页面延迟创建， 配置延迟保存"""
    
    def __init__(self, config: 界面配置):
        self.config = config
        self.theme_colors = config.当前主题颜色
        self.current_nav = "系统"
        self.content_area = None
        self.page = None
        self.config_manager = None
        self.pages_cache = {}
    
    def create(self) -> ft.Container:
        """创建主界面"""
        self.config_manager = ConfigManager()
        
        if self.page:
            ui_config = self.config.定义尺寸.get("界面", {})
            self.page.window.width = ui_config.get("window_width", 1200)
            self.page.window.height = ui_config.get("window_height", 540)
        
        user_info_card = UserInfoCard.create(
            config=self.config,
            username="试用用户",
            is_registered=False,
            expire_days=7,
        )
        
        nav_bar = NavBar.create(
            config=self.config,
            on_nav_change=self.handle_nav_change,
        )
        
        ui_config = self.config.定义尺寸.get("界面", {})
        
        left_panel = ft.Container(
            content=ft.Column(
                [
                    user_info_card,
                    ft.Container(
                        content=ft.Divider(height=1, color=self.theme_colors.get("border")),
                        padding=ft.Padding(
                            left=ui_config.get("divider_padding_left", 12),
                            right=ui_config.get("divider_padding_right", 12),
                        ),
                    ),
                    nav_bar,
                ],
                spacing=0,
                scroll=ft.ScrollMode.AUTO,
                expand=True,
            ),
            width=ui_config.get("left_panel_width", 280),
            bgcolor=self.theme_colors.get("bg_secondary"),
        )
        
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
        
        main_layout = ft.Row(
            [
                left_panel,
                self.content_area,
            ],
            expand=True,
            spacing=0,
            vertical_alignment=ft.CrossAxisAlignment.START,
        )
        
        page_container = ft.Container(
            content=main_layout,
            bgcolor=self.theme_colors.get("bg_primary"),
            padding=ft.Padding.all(0),
            expand=True,
        )
        
        return page_container
    
    def get_page_content(self, nav_name: str) -> ft.Control:
        """获取页面内容（带缓存）"""
        if nav_name in self.pages_cache:
            return self.pages_cache[nav_name]
        
        content = self._create_page(nav_name)
        
        if nav_name != "建筑":
            self.pages_cache[nav_name] = content
        
        return content
    
    def _create_page(self, nav_name: str) -> ft.Control:
        """创建页面"""
        if nav_name == "系统":
            from 新思路.页面层.系统设置页面 import SystemSettingsPage
            return SystemSettingsPage.create(self.config, self.page, self.refresh)
        elif nav_name == "策略":
            from 新思路.页面层.策略设置页面 import StrategySettingsPage
            return StrategySettingsPage.create(self.config, self.page, self.refresh)
        elif nav_name == "任务":
            from 新思路.页面层.任务设置页面 import TaskSettingsPage
            return TaskSettingsPage.create(self.config, self.page, self.refresh)
        elif nav_name == "建筑":
            from 优化界面.页面层.建筑设置页面懒加载 import BuildingSettingsPageLazy
            return BuildingSettingsPageLazy.create(self.config, self.page, self.refresh)
        elif nav_name == "集资":
            from 新思路.页面层.集资设置页面 import FundraisingSettingsPage
            return FundraisingSettingsPage.create(self.config, self.page, self.refresh)
        elif nav_name == "打扫":
            from 新思路.页面层.打扫战场页面 import BattlefieldSettingsPage
            return BattlefieldSettingsPage.create(self.config, self.page, self.refresh)
        elif nav_name == "打野":
            from 新思路.页面层.打野设置页面 import WildSettingsPage
            return WildSettingsPage.create(self.config, self.page, self.refresh)
        elif nav_name == "账号":
            return self.get_placeholder_page(nav_name)
        elif nav_name == "关于":
            return self.get_placeholder_page(nav_name)
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
        # 保存当前卡片数据
        if self.current_nav == "建筑":
            manager = LazyCardManager()
            manager.save_current()
        
        # 保存配置
        if self.config_manager:
            self.config_manager.save_all()
        
        self.current_nav = nav_name
        self.content_area.content = self.get_page_content(nav_name)
        self.content_area.update()
    
    def refresh(self):
        """刷新界面"""
        self.theme_colors = self.config.当前主题_color
        
        if self.page:
            self.page.controls.clear()
            main_page = MainPageOptimized(self.config)
            main_page.page = self.page
            main_page.pages_cache = self.pages_cache
            main_page.config_manager = self.config_manager
            self.page.add(main_page.create())
            self.page.update()


主界面优化版 = MainPageOptimized


if __name__ == "__main__":
    配置 = 界面配置()
    
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        main_page = MainPageOptimized(配置)
        main_page.page = page
        page.add(main_page.create())
    
    ft.run(main)
