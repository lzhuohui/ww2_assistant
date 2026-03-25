# -*- coding: utf-8 -*-
"""
模块名称：PersonalizationConfigSection
模块功能：个性化配置区，包含主题、调色板、风格设置
实现步骤：
- 创建个性化配置卡片
- 使用none销毁策略
- 支持色块重新创建
- 支持主题切换
"""

import flet as ft
from typing import Dict, Any, List, Callable, Optional

from 前端.游戏设置界面.核心层.配置.界面配置 import UIConfig
from 前端.游戏设置界面.表示层.组件.复合.卡片组管理器 import CardGroupManager, create_managed_card
from 前端.游戏设置界面.表示层.组件.基础.主题色块 import ThemeColorBlock
from 前端.游戏设置界面.业务层.服务.配置服务 import ConfigService


USER_CARD_SPACING = 10
USER_SPACING = 10


class PersonalizationConfigSection:
    """个性化配置区 - 使用none策略"""
    
    @staticmethod
    def create(
        config: UIConfig = None,
        config_service: ConfigService = None,
        save_callback: Callable[[str, str, str], None] = None,
    ) -> tuple:
        if config is None:
            config = UIConfig()
        if config_service is None:
            config_service = ConfigService()
        
        theme_colors = config.当前主题颜色
        manager = CardGroupManager(destroy_strategy="none")
        card_list: List[ft.Control] = []
        
        current_theme = [config.theme_name]
        current_palette = [config.palette_name]
        current_style = [config.current_style_name]
        
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
        
        theme_card = create_managed_card(
            manager=manager,
            title="主题设置",
            icon="PALETTE",
            subtitle="选择界面主题颜色",
            enabled=True,
            controls=[theme_block_container],
            config=config,
        )
        card_list.append(theme_card)
        
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
        
        palette_card = create_managed_card(
            manager=manager,
            title="调色板",
            icon="CONTRAST",
            subtitle="选择界面配色方案",
            enabled=True,
            controls=[palette_block_container],
            config=config,
        )
        card_list.append(palette_card)
        
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
        
        style_card = create_managed_card(
            manager=manager,
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
        
        content_column.card_manager = manager
        
        return content_column, manager


# *** 标准测试格式: 仅调用被测模块,AI不得添加数据 ***
if __name__ == "__main__":
    def main(page: ft.Page):
        config = UIConfig()
        service = ConfigService()
        section, manager = PersonalizationConfigSection.create(config=config, config_service=service)
        page.add(section)
    
    ft.app(target=main)
