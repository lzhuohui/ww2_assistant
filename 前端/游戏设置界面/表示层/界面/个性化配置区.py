# -*- coding: utf-8 -*-
"""
模块名称：PersonalizationConfigSection
模块功能：个性化配置区，包含主题模式和强调色设置
实现步骤：
- 创建主题模式卡片（浅色/深色）
- 创建强调色选择卡片
- 支持主题和强调色切换
"""

import flet as ft
from typing import Dict, Any, List, Callable, Optional

from 前端.游戏设置界面.核心层.配置.界面配置 import UIConfig, ACCENT_COLORS
from 前端.游戏设置界面.表示层.组件.复合.卡片组管理器 import CardGroupManager, create_managed_card
from 前端.游戏设置界面.表示层.组件.基础.主题色块 import ThemeColorBlock
from 前端.游戏设置界面.业务层.服务.配置服务 import ConfigService


# *** 用户指定变量: 变量值必须生效,AI不得更改数据 ***
USER_CARD_SPACING = 10
USER_SPACING = 10
# *********************************


class PersonalizationConfigSection:
    """个性化配置区 - 主题模式和强调色设置"""
    
    @staticmethod
    def create(
        config: UIConfig = None,
        config_service: ConfigService = None,
        save_callback: Callable[[str, str, str], None] = None,
        page: ft.Page = None,
        on_theme_change: Callable[[], None] = None,
        expanded_card_titles: list = None,
    ) -> tuple:
        if config is None:
            config = UIConfig()
        if config_service is None:
            config_service = ConfigService()
        if page is None:
            page = config._page if hasattr(config, '_page') else None
        if expanded_card_titles is None:
            expanded_card_titles = []
        
        manager = CardGroupManager()
        card_list: List[ft.Control] = []
        
        current_theme = [config.theme_name]
        current_accent = [config.accent_name]
        
        theme_mode_list = [
            {"name": "浅色", "value": "#FFFFFF", "key": "light"},
            {"name": "深色", "value": "#202020", "key": "dark"},
        ]
        
        accent_color_list = []
        for accent_key, accent_data in ACCENT_COLORS.items():
            accent_color_list.append({
                "name": accent_data["name"],
                "value": accent_data["value"],
                "key": accent_key,
            })
        
        theme_block_container = ft.Container()
        accent_block_container = ft.Container()
        
        def update_theme_blocks():
            selected_color = next(
                (item["value"] for item in theme_mode_list if item["key"] == current_theme[0]),
                "#202020"
            )
            theme_block_container.content = ThemeColorBlock.create_group(
                color_list=theme_mode_list,
                selected_color=selected_color,
                on_select=handle_theme_switch,
                config=config,
            )
            try:
                if theme_block_container.page:
                    theme_block_container.page.update()
            except:
                pass
        
        def update_accent_blocks():
            selected_color = next(
                (item["value"] for item in accent_color_list if item["key"] == current_accent[0]),
                "#0078D4"
            )
            accent_block_container.content = ThemeColorBlock.create_group(
                color_list=accent_color_list,
                selected_color=selected_color,
                on_select=handle_accent_switch,
                config=config,
            )
            try:
                if accent_block_container.page:
                    accent_block_container.page.update()
            except:
                pass
        
        def save_expanded_state():
            expanded = []
            if theme_card.get_is_expanded():
                expanded.append("主题模式")
            if accent_card.get_is_expanded():
                expanded.append("强调色")
            config._expanded_card_titles = expanded
        
        def handle_theme_switch(color_value: str):
            for item in theme_mode_list:
                if item["value"] == color_value:
                    current_theme[0] = item["key"]
                    config.switch_theme(item["key"])
                    save_expanded_state()
                    if save_callback:
                        save_callback("个性化", "theme", item["key"])
                    if on_theme_change:
                        on_theme_change()
                    break
        
        def handle_accent_switch(color_value: str):
            for item in accent_color_list:
                if item["value"] == color_value:
                    current_accent[0] = item["key"]
                    config.switch_accent(item["key"])
                    save_expanded_state()
                    if save_callback:
                        save_callback("个性化", "accent", item["key"])
                    if on_theme_change:
                        on_theme_change()
                    break
        
        update_theme_blocks()
        update_accent_blocks()
        
        theme_card = create_managed_card(
            manager=manager,
            title="主题模式",
            icon="BRIGHTNESS_MEDIUM",
            subtitle="选择界面主题模式",
            enabled=True,
            controls=[theme_block_container],
            config=config,
        )
        card_list.append(theme_card)
        
        accent_card = create_managed_card(
            manager=manager,
            title="强调色",
            icon="PALETTE",
            subtitle="选择界面强调色",
            enabled=True,
            controls=[accent_block_container],
            config=config,
        )
        card_list.append(accent_card)
        
        if "主题模式" in expanded_card_titles:
            theme_card.load_controls()
            theme_card.is_expanded = True
            manager.current_expanded_card = theme_card
        if "强调色" in expanded_card_titles:
            accent_card.load_controls()
            accent_card.is_expanded = True
            manager.current_expanded_card = accent_card
        
        card_column = ft.Column(
            controls=card_list,
            spacing=USER_CARD_SPACING,
            scroll=ft.ScrollMode.HIDDEN,
            expand=True,
        )
        
        content_column = ft.Column(
            controls=[
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
