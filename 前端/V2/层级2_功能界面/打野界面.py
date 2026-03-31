# -*- coding: utf-8 -*-

"""
模块名称：打野界面.py
模块功能：打野设置界面 - 自动打野配置

卡片配置：
1. 自动打野 - 野怪等级选择、搜索频率选择

数据来源：从V1版本打野配置区.py重构
"""

import flet as ft
from typing import Callable, Dict, Any

from 前端.V2.层级3_卡片组.卡片组 import CardGroup

USER_CARD_SPACING = 10

CARDS_CONFIG = [
    {
        "section": "打野设置.自动打野",
        "title": "自动打野",
        "icon": "EXPLORE",
        "subtitle": "自动搜索并攻击野怪",
        "controls": [
            {"id": "野怪等级", "type": "dropdown", "label": "等级选择"},
            {"id": "搜索频率", "type": "dropdown", "label": "频率选择"},
        ],
    },
]

class HuntingPage:
    _card_group: CardGroup = None
    
    @staticmethod
    def create(page: ft.Page, config_service, on_change: Callable = None, theme_colors: Dict = None) -> ft.Control:
        if theme_colors is None:
            theme_colors = {"text_primary": "#000000", "text_secondary": "#666666", "text_disabled": "#999999", "bg_card": "#FFFFFF", "accent": "#0078D4", "border": "#CCCCCC"}
        
        HuntingPage._card_group = CardGroup(page, config_service)
        cards = []
        for card_config in CARDS_CONFIG:
            card = HuntingPage._card_group.create(
                section=card_config.get("section", ""),
                title=card_config.get("title", ""),
                icon=card_config.get("icon", "HOME"),
                subtitle=card_config.get("subtitle", ""),
                controls_config=card_config.get("controls", []),
                has_switch=True,
                on_change=on_change,
                theme_colors=theme_colors,
            )
            cards.append(card)
        
        return ft.Column(cards, spacing=USER_CARD_SPACING, scroll=ft.ScrollMode.AUTO, expand=True)
    
    @staticmethod
    def destroy():
        if HuntingPage._card_group:
            HuntingPage._card_group.destroy_all()
            HuntingPage._card_group = None

if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    
    from 前端.V2.数据层.仓库.配置仓库 import ConfigRepository
    from 前端.V2.业务层.服务.配置服务 import ConfigService
    
    def main(page: ft.Page):
        page.title = "打野设置测试"
        
        repository = ConfigRepository()
        config_service = ConfigService(repository)
        
        hunting_page = HuntingPage.create(page, config_service)
        page.add(hunting_page)
    
    ft.run(main)
