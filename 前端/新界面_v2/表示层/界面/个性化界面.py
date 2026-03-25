# -*- coding: utf-8 -*-
"""
模块名称：PersonalizationPage
设计思路: 个性化配置界面，使用主题色块组件
模块隔离: 界面层依赖组件层
"""

import flet as ft
from typing import Dict, Any, List, Callable, Optional

from 前端.新界面_v2.核心.配置.界面配置 import UIConfig
from 前端.新界面_v2.表示层.组件.复合.折叠卡片 import CollapsibleCard
from 前端.新界面_v2.表示层.组件.基础.主题色块 import ThemeColorBlock
from 前端.新界面_v2.核心.常量.全局常量 import USER_SPACING, USER_CARD_SPACING


class PersonalizationPage:
    """个性化配置界面"""
    
    current_loaded_card: Optional[ft.Container] = None
    
    @staticmethod
    def create(
        config: UIConfig=None,
        save_callback: Callable[[str, str, str], None]=None,
    ) -> ft.Container:
        if config is None:
            config = UIConfig()
        
        theme_colors = config.当前主题颜色
        card_list: List[ft.Control] = []
        current_loaded_card = [None]
        
        current_theme = [config.theme_name]
        current_palette = [config.palette_name]
        current_style = [config.current_style_name]
        
        def destroy_loaded_card():
            if current_loaded_card[0] and hasattr(current_loaded_card[0], 'is_loaded'):
                if current_loaded_card[0].is_loaded():
                    current_loaded_card[0].destroy_controls()
            current_loaded_card[0] = None
        
        # 主题设置
        theme_color_list = [
            {"name": "浅色", "value": "#FFFFFF"},
            {"name": "深色", "value": "#1A1A2E"},
            {"name": "日出", "value": "#FFE4B5"},
            {"name": "捕捉", "value": "#98FB98"},
            {"name": "聚焦", "value": "#87CEEB"},
        ]
        
        theme_block_container = ft.Container()
        
        def update_theme_blocks():
            display_theme_name = "浅色" if current_theme[0] == "light" else "深色"
            selected_color = next((item["value"] for item in theme_color_list if item["name"] == display_theme_name), "#1A1A2E")
            theme_block_container.content = ThemeColorBlock.create_group(
                color_list=theme_color_list,
                selected_color=selected_color,
                on_select=handle_theme_switch,
                config=config,
            )
            try:
                if theme_block_container.page:
                    theme_block_container.page.update()
            except:
                pass
        
        def handle_theme_switch(color_value: str):
            for item in theme_color_list:
                if item["value"] == color_value:
                    current_theme[0] = item["name"]
                    theme_name = "light" if item["name"] == "浅色" else "dark"
                    config.switch_theme(theme_name)
                    if save_callback:
                        save_callback("个性化", "theme", theme_name)
                    update_theme_blocks()
                    break
        
        update_theme_blocks()
        
        theme_card = CollapsibleCard.create(
            title="主题设置",
            icon="PALETTE",
            subtitle="选择界面主题颜色",
            enabled=True,
            controls=[theme_block_container],
            config=config,
        )
        card_list.append(theme_card)
        
        # 调色板设置
        palette_colors = [
            {"name": "水生", "value": "#006994"},
            {"name": "沙漠", "value": "#C19A6B"},
            {"name": "黄昏", "value": "#FF6B6B"},
            {"name": "夜空", "value": "#2C3E50"},
        ]
        
        palette_block_container = ft.Container()
        
        def update_palette_blocks():
            selected_palette = next((item["value"] for item in palette_colors if item["name"] == current_palette[0]), "#006994")
            palette_block_container.content = ThemeColorBlock.create_group(
                color_list=palette_colors,
                selected_color=selected_palette,
                on_select=handle_palette_switch,
                config=config,
            )
            try:
                if palette_block_container.page:
                    palette_block_container.page.update()
            except:
                pass
        
        def handle_palette_switch(color_value: str):
            for item in palette_colors:
                if item["value"] == color_value:
                    current_palette[0] = item["name"]
                    config.switch_palette(item["name"])
                    if save_callback:
                        save_callback("个性化", "palette", item["name"])
                    update_palette_blocks()
                    break
        
        update_palette_blocks()
        
        palette_card = CollapsibleCard.create(
            title="调色板",
            icon="CONTRAST",
            subtitle="选择界面配色方案",
            enabled=True,
            controls=[palette_block_container],
            config=config,
        )
        card_list.append(palette_card)
        
        # 风格设置
        style_colors = [
            {"name": "平铺", "value": "#E0E0E0"},
            {"name": "立体", "value": "#FFFFFF"},
        ]
        
        style_block_container = ft.Container()
        
        def update_style_blocks():
            selected_style = next((item["value"] for item in style_colors if item["name"] == ("立体" if current_style[0] == "3D立体" else "平铺")), "#E0E0E0")
            style_block_container.content = ThemeColorBlock.create_group(
                color_list=style_colors,
                selected_color=selected_style,
                on_select=handle_style_switch,
                config=config,
            )
            try:
                if style_block_container.page:
                    style_block_container.page.update()
            except:
                pass
        
        def handle_style_switch(color_value: str):
            for item in style_colors:
                if item["value"] == color_value:
                    style_name = "3D立体" if item["name"] == "立体" else "普通平铺"
                    current_style[0] = style_name
                    config.switch_style(style_name)
                    if save_callback:
                        save_callback("个性化", "style", style_name)
                    update_style_blocks()
                    break
        
        update_style_blocks()
        
        style_card = CollapsibleCard.create(
            title="风格设置",
            icon="STYLE",
            subtitle="选择界面显示风格",
            enabled=True,
            controls=[style_block_container],
            config=config,
        )
        card_list.append(style_card)
        
        title_bar = ft.Row([
            ft.Icon(ft.Icons.PALETTE, size=20, color=theme_colors.get("accent")),
            ft.Container(width=6),
            ft.Text("个性化设置", size=16, weight=ft.FontWeight.BOLD, color=theme_colors.get("text_primary")),
        ], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER)
        
        card_column = ft.Column(
            controls=card_list,
            spacing=USER_CARD_SPACING,
            scroll=ft.ScrollMode.HIDDEN,
            expand=True,
        )
        
        content_column = ft.Column(
            controls=[
                title_bar,
                ft.Container(height=USER_SPACING),
                card_column,
            ],
            spacing=0,
            expand=True,
        )
        
        content_column.destroy_loaded_card = destroy_loaded_card
        
        return ft.Container(
            content=content_column,
            expand=True,
        )


if __name__ == "__main__":
    ft.app(target=lambda page: page.add(PersonalizationPage.create()))