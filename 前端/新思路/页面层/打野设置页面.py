# -*- coding: utf-8 -*-
"""
打野设置页面 - 页面层

设计思路:
    使用通用卡片创建打野设置页面。

功能:
    1. 自动打野卡片（开关）

使用场景:
    被主界面调用。
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft
from typing import Callable
from 配置.界面配置 import 界面配置
from 配置.配置管理器 import ConfigManager
from 新思路.组件层.通用卡片 import UniversalCard


class WildSettingsPage:
    """打野设置页面"""
    
    @staticmethod
    def create(config: 界面配置, page: ft.Page = None, on_refresh: Callable[[], None] = None) -> ft.Container:
        """
        创建打野设置页面
        
        参数:
            config: 界面配置对象
            page: 页面对象
            on_refresh: 刷新回调
        
        返回:
            ft.Container: 打野设置页面容器
        """
        theme_colors = config.当前主题颜色
        config_manager = ConfigManager()
        
        wild_enabled = config_manager.get_value("自动打野", "开关", True)
        
        config_manager.set_value("自动打野", "开关", wild_enabled)
        
        def on_wild_state_change(enabled: bool):
            config_manager.set_value("自动打野", "开关", enabled)
        
        wild_card = UniversalCard.create(
            config=config,
            title="自动打野",
            icon="EXPLORE",
            enabled=wild_enabled,
            on_state_change=on_wild_state_change,
            subtitle="开启后执行自动打野任务",
        )
        
        page_content = ft.Column(
            [
                ft.Text(
                    "打野设置",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=theme_colors.get("text_primary"),
                ),
                ft.Container(height=20),
                wild_card,
            ],
            spacing=0,
            scroll=ft.ScrollMode.HIDDEN,
            expand=True,
        )
        
        page_container = ft.Container(
            content=page_content,
            padding=ft.Padding.all(0),
            expand=True,
        )
        
        return page_container


打野设置页面 = WildSettingsPage


if __name__ == "__main__":
    配置 = 界面配置()
    
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        page.add(WildSettingsPage.create(配置))
    
    ft.run(main)
