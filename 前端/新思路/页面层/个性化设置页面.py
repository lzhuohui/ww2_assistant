# -*- coding: utf-8 -*-
"""
个性化设置页面 - 页面层

设计思路:
    使用通用卡片创建个性化设置页面，统一风格。

功能:
    1. 主题设置卡片
    2. 调色板设置卡片

数据来源:
    所有配置数据从配置目录获取。

使用场景:
    被主界面调用。

可独立运行调试: python 个性化设置页面.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft
from typing import Callable
from 配置.界面配置 import 界面配置
from 新思路.组件层.通用卡片 import UniversalCard
from 新思路.零件层.主题色块 import ThemeColorBlock


class PersonalizationSettingsPage:
    """个性化设置页面 - 页面层"""
    
    @staticmethod
    def create(config: 界面配置, page: ft.Page = None, on_refresh: Callable[[], None] = None) -> ft.Container:
        """
        创建个性化设置页面
        
        参数:
            config: 界面配置对象
            page: 页面对象（可选，用于更新页面显示）
            on_refresh: 刷新回调（主题/调色板切换后调用）
        
        返回:
            ft.Container: 个性化设置页面容器
        """
        theme_colors = config.当前主题颜色
        config_manager = config.配置管理器
        
        current_theme = config.主题名称
        current_palette = config.调色板名称
        
        saved_palette_enabled = config_manager.get_value("个性化", "调色板开关", True)
        
        def on_theme_click(theme_name: str):
            if theme_name != current_theme:
                config.切换主题(theme_name)
                config_manager.set_value("个性化", "主题", theme_name)
                if on_refresh:
                    on_refresh()
        
        def on_palette_enabled_change(enabled: bool):
            config_manager.set_value("个性化", "调色板开关", enabled)
            if not enabled:
                config.切换调色板
                config_manager.set_value("个性化", "调色板", "")
            else:
                saved_palette = config_manager.get_value("个性化", "调色板")
                if saved_palette:
                    config.切换调色板(saved_palette)
            if on_refresh:
                on_refresh()
        
        def on_palette_click(palette_name: str):
            actual_current_palette = config.调色板名称
            if palette_name == actual_current_palette:
                config.切换调色板
                config_manager.set_value("个性化", "调色板", "")
            else:
                config.切换调色板(palette_name)
                config_manager.set_value("个性化", "调色板", palette_name)
            if on_refresh:
                on_refresh()
        
        theme_block_controls = [
            ThemeColorBlock.create(
                config=config,
                theme_name="浅色",
                bg_color="#FFFFFF",
                is_selected=(current_theme == "浅色"),
                on_click=lambda e: on_theme_click("浅色"),
            ),
            ThemeColorBlock.create(
                config=config,
                theme_name="深色",
                bg_color="#1A1A2E",
                is_selected=(current_theme == "深色"),
                on_click=lambda e: on_theme_click("深色"),
            ),
            ThemeColorBlock.create(
                config=config,
                theme_name="日出",
                bg_color="#FFE4B5",
                is_selected=(current_theme == "日出"),
                on_click=lambda e: on_theme_click("日出"),
            ),
            ThemeColorBlock.create(
                config=config,
                theme_name="捕捉",
                bg_color="#98FB98",
                is_selected=(current_theme == "捕捉"),
                on_click=lambda e: on_theme_click("捕捉"),
            ),
            ThemeColorBlock.create(
                config=config,
                theme_name="聚焦",
                bg_color="#87CEEB",
                is_selected=(current_theme == "聚焦"),
                on_click=lambda e: on_theme_click("聚焦"),
            ),
        ]
        
        theme_card = UniversalCard.create(
            config=config,
            title="主题设置",
            icon="PALETTE",
            enabled=True,
            controls=theme_block_controls,
            controls_per_row=5,
            subtitle="选择界面主题风格",
        )
        
        palette_block_controls = [
            ThemeColorBlock.create(
                config=config,
                theme_name="水生",
                bg_color="#006994",
                is_selected=(saved_palette_enabled and current_palette == "水生"),
                on_click=lambda e: on_palette_click("水生"),
            ),
            ThemeColorBlock.create(
                config=config,
                theme_name="沙漠",
                bg_color="#C19A6B",
                is_selected=(saved_palette_enabled and current_palette == "沙漠"),
                on_click=lambda e: on_palette_click("沙漠"),
            ),
            ThemeColorBlock.create(
                config=config,
                theme_name="黄昏",
                bg_color="#FF6B6B",
                is_selected=(saved_palette_enabled and current_palette == "黄昏"),
                on_click=lambda e: on_palette_click("黄昏"),
            ),
            ThemeColorBlock.create(
                config=config,
                theme_name="夜空",
                bg_color="#2C3E50",
                is_selected=(saved_palette_enabled and current_palette == "夜空"),
                on_click=lambda e: on_palette_click("夜空"),
            ),
        ]
        
        palette_card = UniversalCard.create(
            config=config,
            title="调色板设置",
            icon="CONTRAST",
            enabled=saved_palette_enabled,
            on_state_change=on_palette_enabled_change,
            controls=palette_block_controls,
            controls_per_row=4,
            subtitle="选择高对比度调色板",
        )
        
        def on_style_click(style_name: str):
            if style_name != config.当前风格名称:
                config.切换风格(style_name)
                config_manager.set_value("个性化", "风格", style_name)
                if on_refresh:
                    on_refresh()
        
        style_block_controls = [
            ThemeColorBlock.create(
                config=config,
                theme_name="平铺",
                bg_color="#E0E0E0",
                is_selected=(config.当前风格名称 == "普通平铺"),
                on_click=lambda e: on_style_click("普通平铺"),
            ),
            ThemeColorBlock.create(
                config=config,
                theme_name="立体",
                bg_color="#FFFFFF",
                is_selected=(config.当前风格名称 == "3D立体"),
                on_click=lambda e: on_style_click("3D立体"),
            ),
        ]
        
        style_card = UniversalCard.create(
            config=config,
            title="风格设置",
            icon="STYLE",
            enabled=True,
            controls=style_block_controls,
            controls_per_row=2,
            subtitle="选择界面风格",
        )
        
        page_title = ft.Container(
            content=ft.Text(
                "个性化设置",
                size=24,
                weight=ft.FontWeight.BOLD,
                color=theme_colors.get("text_primary"),
            ),
            padding=ft.Padding(bottom=4),
        )
        
        scrollable_content = ft.Column(
            [
                theme_card,
                ft.Container(height=5),
                palette_card,
                ft.Container(height=5),
                style_card,
            ],
            spacing=0,
            scroll=ft.ScrollMode.HIDDEN,
            expand=True,
        )
        
        page_content = ft.Column(
            [
                page_title,
                scrollable_content,
            ],
            spacing=0,
            expand=True,
        )
        
        page_container = ft.Container(
            content=page_content,
            padding=ft.Padding.all(0),
            expand=True,
        )
        
        return page_container


个性化设置页面 = PersonalizationSettingsPage


if __name__ == "__main__":
    配置 = 界面配置()
    
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        page.add(PersonalizationSettingsPage.create(配置))
    
    ft.run(main)
