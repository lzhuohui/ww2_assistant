# -*- coding: utf-8 -*-
"""模块名称：个性化界面 | 设计思路：个性化配置界面，主题/调色板/风格设置 | 模块隔离原则"""

import flet as ft
from typing import Dict, Any, List, Callable

from 前端.新界面.核心接口.界面配置 import 界面配置
from 前端.新界面.核心接口.主题提供者 import ThemeProvider
from 前端.新界面.组件模块.卡片容器 import CardContainer


# *** 用户指定变量 - AI不得修改, 变量值必须生效 ***
USER_CARD_WIDTH = 500
USER_CARD_HEIGHT = 70
USER_CARD_SPACING = 8
# *********************************


class 个性化界面:
    """个性化配置界面"""
    
    @staticmethod
    def create(
        config: 界面配置=None,
        on_theme_change: Callable[[str], None]=None,
        on_palette_change: Callable[[str], None]=None,
        on_style_change: Callable[[str], None]=None,
        width: int=USER_CARD_WIDTH,
    ) -> ft.Column:
        if config is None:
            config = 界面配置()
        
        ThemeProvider.initialize(config)
        theme_colors = config.当前主题颜色
        
        current_theme = config.主题名称
        current_palette = config.调色板名称
        current_style = config.当前风格名称
        
        themes = [
            {"name": "浅色", "color": "#FFFFFF"},
            {"name": "深色", "color": "#1A1A2E"},
            {"name": "日出", "color": "#FFE4B5"},
            {"name": "捕捉", "color": "#98FB98"},
            {"name": "聚焦", "color": "#87CEEB"},
        ]
        
        palettes = [
            {"name": "水生", "color": "#006994"},
            {"name": "沙漠", "color": "#C19A6B"},
            {"name": "黄昏", "color": "#FF6B6B"},
            {"name": "夜空", "color": "#2C3E50"},
        ]
        
        styles = [
            {"name": "普通平铺", "label": "平铺"},
            {"name": "3D立体", "label": "立体"},
        ]
        
        def create_color_block(name: str, color: str, selected: bool, on_click: Callable) -> ft.Container:
            return ft.Container(
                content=ft.Container(
                    content=ft.Text(name, size=10, color=theme_colors.get("text_primary") if not selected else "#FFFFFF"),
                    alignment=ft.Alignment(0, 0.5),
                    padding=ft.Padding(left=0, right=0, top=28, bottom=4),
                ),
                width=60,
                height=50,
                bgcolor=color,
                border_radius=8,
                border=ft.Border.all(3, theme_colors.get("accent")) if selected else None,
                on_click=lambda e: on_click(name),
            )
        
        theme_blocks = []
        for t in themes:
            selected = t["name"] == current_theme
            theme_blocks.append(create_color_block(
                t["name"], t["color"], selected,
                lambda n: handle_theme_change(n)
            ))
        
        palette_blocks = []
        for p in palettes:
            selected = p["name"] == current_palette
            palette_blocks.append(create_color_block(
                p["name"], p["color"], selected,
                lambda n: handle_palette_change(n)
            ))
        
        def handle_theme_change(theme_name: str):
            config.切换主题(theme_name)
            if on_theme_change:
                on_theme_change(theme_name)
        
        def handle_palette_change(palette_name: str):
            config.切换调色板(palette_name)
            if on_palette_change:
                on_palette_change(palette_name)
        
        def handle_style_change(style_name: str):
            config.切换风格(style_name)
            if on_style_change:
                on_style_change(style_name)
        
        theme_card = CardContainer.create(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.PALETTE, size=20, color=theme_colors.get("accent")),
                    ft.Container(width=8),
                    ft.Text("主题设置", size=14, weight=ft.FontWeight.BOLD, color=theme_colors.get("text_primary")),
                ], spacing=0),
                ft.Container(height=12),
                ft.Row(theme_blocks, spacing=10),
            ], spacing=0),
            config=config,
            height=USER_CARD_HEIGHT + 30,
            width=width,
            padding=16,
        )
        
        palette_card = CardContainer.create(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.CONTRAST, size=20, color=theme_colors.get("accent")),
                    ft.Container(width=8),
                    ft.Text("调色板设置", size=14, weight=ft.FontWeight.BOLD, color=theme_colors.get("text_primary")),
                ], spacing=0),
                ft.Container(height=12),
                ft.Row(palette_blocks, spacing=10),
            ], spacing=0),
            config=config,
            height=USER_CARD_HEIGHT + 30,
            width=width,
            padding=16,
        )
        
        style_row = ft.Row([], spacing=10)
        for s in styles:
            selected = s["name"] == current_style
            btn = ft.Container(
                content=ft.Text(s["label"], size=12, color=theme_colors.get("text_primary")),
                width=80,
                height=36,
                bgcolor=theme_colors.get("bg_secondary"),
                border_radius=8,
                border=ft.Border.all(2, theme_colors.get("accent")) if selected else None,
                alignment=ft.Alignment(0, 0),
                on_click=lambda e, n=s["name"]: handle_style_change(n),
            )
            style_row.controls.append(btn)
        
        style_card = CardContainer.create(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.STYLE, size=20, color=theme_colors.get("accent")),
                    ft.Container(width=8),
                    ft.Text("风格设置", size=14, weight=ft.FontWeight.BOLD, color=theme_colors.get("text_primary")),
                ], spacing=0),
                ft.Container(height=12),
                style_row,
            ], spacing=0),
            config=config,
            height=USER_CARD_HEIGHT,
            width=width,
            padding=16,
        )
        
        content = ft.Column(
            controls=[theme_card, palette_card, style_card],
            spacing=USER_CARD_SPACING,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )
        
        def dispose():
            pass
        
        content.dispose = dispose
        
        return content


if __name__ == "__main__":
    config = 界面配置()
    ThemeProvider.initialize(config)
    
    ft.run(lambda page: page.add(个性化界面.create(config=config)))
