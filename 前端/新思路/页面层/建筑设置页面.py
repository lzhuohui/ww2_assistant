# -*- coding: utf-8 -*-
"""
建筑设置页面 - 页面层

设计思路:
    使用懒加载通用卡片，点击后才加载实际控件。
    切换时销毁上一个卡片，保持内存低占用。

功能:
    1. 默认加载"主帅主城"
    2. 其他卡片显示"点击加载"
    3. 切换时保存上一个卡片数据并销毁

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
from 新思路.组件层.懒加载通用卡片 import LazyUniversalCard, LazyCardManager

DEFAULT_DROPDOWN_WIDTH = 60


class BuildingSettingsPage:
    """建筑设置页面"""
    
    @staticmethod
    def create(config: 界面配置, page: ft.Page = None, on_refresh: Callable[[], None] = None) -> ft.Container:
        theme_colors = config.当前主题颜色
        
        config_manager = ConfigManager()
        manager = LazyCardManager()
        manager.config_manager = config_manager
        
        for card_name, card_config in config_manager.building_configs.items():
            if "controls" in card_config:
                for control in card_config["controls"]:
                    if control.get("type") == "dropdown" and "width" not in control:
                        control["width"] = DEFAULT_DROPDOWN_WIDTH
        
        def on_value_change(config_key: str, value: any):
            print(f"配置变化: {config_key} = {value}")
        
        card_names = ["主帅主城", "主帅分城", "付帅主城", "付帅分城", "军团城市"]
        
        lazy_cards = []
        for i, card_name in enumerate(card_names):
            card_config = config_manager.get_card_config(card_name)
            if card_config:
                is_default = (i == 0)
                card = LazyUniversalCard(
                    config=config,
                    card_name=card_name,
                    card_config=card_config,
                    config_manager=config_manager,
                    on_value_change=on_value_change,
                    is_default=is_default,
                )
                lazy_cards.append(card.create())
        
        page_content = ft.Column(
            [
                ft.Text(
                    "建筑设置",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=theme_colors.get("text_primary"),
                ),
                ft.Container(height=10),
                *[ft.Container(content=card, margin=ft.Margin(bottom=10)) for card in lazy_cards],
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


建筑设置页面 = BuildingSettingsPage


if __name__ == "__main__":
    配置 = 界面配置()
    
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        page.add(BuildingSettingsPage.create(配置))
    
    ft.run(main)
