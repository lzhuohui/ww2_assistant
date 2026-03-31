# -*- coding: utf-8 -*-

"""
模块名称：个性化界面.py
模块功能：个性化设置界面 - 主题色和强调色选择

卡片配置：
1. 主题色选择 - 浅色/深色
2. 强调色选择 - 多种颜色

数据来源：
- 主题配置从config_service获取
- 强调色配置从config_service获取
"""

import flet as ft
from typing import Callable, Dict, Any

from 前端.V2.层级5_基础模块.主题色块 import ThemeBlock
from 前端.V2.层级5_基础模块.强调色色块 import AccentBlock, DEFAULT_ACCENT_COLORS

USER_CARD_SPACING = 10

class PersonalizationPage:
    
    @staticmethod
    def create(
        page: ft.Page,
        config_service,
        on_change: Callable = None,
        theme_colors: Dict = None,
        on_theme_change: Callable = None,
    ) -> ft.Control:
        if theme_colors is None:
            theme_colors = {"text_primary": "#000000", "text_secondary": "#666666", "bg_card": "#FFFFFF", "accent": "#0078D4", "border": "#CCCCCC"}
        
        current_theme = config_service.get_current_theme() if config_service else "light"
        current_accent = config_service.get_current_accent() if config_service else "blue"
        
        all_themes = config_service.get_all_themes() if config_service else ["light", "dark"]
        all_accents = config_service.get_all_accents() if config_service else []
        
        accent_colors = {}
        for accent in all_accents:
            accent_colors[accent.get("key")] = {
                "name": accent.get("name"),
                "value": accent.get("value")
            }
        if not accent_colors:
            accent_colors = DEFAULT_ACCENT_COLORS
        
        current_theme_state = [current_theme]
        current_accent_state = [current_accent]
        
        def on_theme_click(theme_name: str):
            current_theme_state[0] = theme_name
            if config_service:
                config_service.set_current_theme(theme_name)
            theme_row.controls = [
                ThemeBlock.create(name, name == current_theme_state[0], on_theme_click)
                for name in all_themes
            ]
            if on_change:
                on_change("个性化设置.主题", "主题色", theme_name)
            if on_theme_change:
                on_theme_change()
            page.update()
        
        def on_accent_click(accent_name: str):
            current_accent_state[0] = accent_name
            if config_service:
                config_service.set_current_accent(accent_name)
            accent_row.controls = [
                AccentBlock.create(
                    accent.get("key", accent.get("name")),
                    accent.get("key", accent.get("name")) == current_accent_state[0],
                    on_accent_click,
                    accent_colors=accent_colors
                )
                for accent in all_accents
            ] if all_accents else [
                AccentBlock.create(name, name == current_accent_state[0], on_accent_click, accent_colors=accent_colors)
                for name in accent_colors.keys()
            ]
            if on_change:
                on_change("个性化设置.强调色", "强调色", accent_name)
            if on_theme_change:
                on_theme_change()
            page.update()
        
        theme_title = ft.Text("主题色", size=14, weight=ft.FontWeight.BOLD, color=theme_colors.get("text_primary"))
        theme_row = ft.Row([
            ThemeBlock.create(name, name == current_theme_state[0], on_theme_click)
            for name in all_themes
        ], spacing=8)
        
        accent_title = ft.Text("强调色", size=14, weight=ft.FontWeight.BOLD, color=theme_colors.get("text_primary"))
        accent_row = ft.Row([
            AccentBlock.create(
                accent.get("key", accent.get("name")),
                accent.get("key", accent.get("name")) == current_accent_state[0],
                on_accent_click,
                accent_colors=accent_colors
            )
            for accent in all_accents
        ] if all_accents else [
            AccentBlock.create(name, name == current_accent_state[0], on_accent_click, accent_colors=accent_colors)
            for name in accent_colors.keys()
        ], spacing=8, wrap=True)
        
        content = ft.Column([
            ft.Container(theme_title, padding=ft.padding.only(bottom=8)),
            theme_row,
            ft.Container(height=16),
            ft.Container(accent_title, padding=ft.padding.only(bottom=8)),
            accent_row,
        ], spacing=0)
        
        return ft.Container(content=content, padding=16)
    
    @staticmethod
    def destroy():
        pass

if __name__ == "__main__":
    def main(page: ft.Page):
        page.title = "个性化设置测试"
        
        class MockConfigService:
            def get_current_theme(self):
                return "light"
            def get_current_accent(self):
                return "blue"
            def get_all_themes(self):
                return ["light", "dark"]
            def get_all_accents(self):
                return [
                    {"key": "blue", "name": "蓝色", "value": "#0078D4"},
                    {"key": "red", "name": "红色", "value": "#D13438"},
                ]
            def set_current_theme(self, name):
                print(f"设置主题: {name}")
            def set_current_accent(self, name):
                print(f"设置强调色: {name}")
        
        config_service = MockConfigService()
        personalization_page = PersonalizationPage.create(page, config_service)
        page.add(personalization_page)
    
    ft.run(main)
