# -*- coding: utf-8 -*-
"""
打扫设置页面 - 页面层

设计思路:
    使用开关下拉卡片创建打扫设置页面。

功能:
    1. 打扫城区卡片（开关）
    2. 打扫政区卡片（开关）

使用场景:
    被主界面调用。
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft
from typing import Callable
from 配置.界面配置 import 界面配置
from 新思路.组件层.开关下拉卡片 import SwitchDropdownCard


class CleaningSettingsPage:
    """打扫设置页面"""
    
    @staticmethod
    def create(config: 界面配置, page: ft.Page = None, on_refresh: Callable[[], None] = None) -> ft.Container:
        """
        创建打扫设置页面
        
        参数:
            config: 界面配置对象
            page: 页面对象
            on_refresh: 刷新回调
        
        返回:
            ft.Container: 打扫设置页面容器
        """
        theme_colors = config.当前主题颜色
        
        def on_state_change_district(enabled: bool):
            """打扫城区开关状态变化"""
            print(f"打扫城区: {'开启' if enabled else '关闭'}")
        
        def on_state_change_region(enabled: bool):
            """打扫政区开关状态变化"""
            print(f"打扫政区: {'开启' if enabled else '关闭'}")
        
        district_card = SwitchDropdownCard.create(
            config=config,
            title="打扫城区",
            icon="CLEANING_SERVICES",
            enabled=True,
            on_state_change=on_state_change_district,
            subtitle="开启后执行打扫城区任务",
        )
        
        region_card = SwitchDropdownCard.create(
            config=config,
            title="打扫政区",
            icon="DOMAIN",
            enabled=True,
            on_state_change=on_state_change_region,
            subtitle="开启后执行打扫政区任务",
        )
        
        page_content = ft.Column(
            [
                ft.Text(
                    "打扫设置",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=theme_colors.get("text_primary"),
                ),
                ft.Container(height=20),
                district_card,
                ft.Container(height=15),
                region_card,
            ],
            spacing=0,
            scroll=ft.ScrollMode.HIDDEN,
            expand=True,
        )
        
        page_container = ft.Container(
            content=page_content,
            padding=ft.Padding.all(20),
            expand=True,
        )
        
        return page_container


打扫设置页面 = CleaningSettingsPage


if __name__ == "__main__":
    配置 = 界面配置()
    
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        page.add(CleaningSettingsPage.create(配置))
    
    ft.run(main)
