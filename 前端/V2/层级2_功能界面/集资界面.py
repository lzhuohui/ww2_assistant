# -*- coding: utf-8 -*-

"""
模块名称：集资界面.py
模块功能：集资设置界面 - 小号上贡、分城纳租

卡片配置：
1. 小号上贡 - 上贡限级、上贡限量、主要统帅、次要统帅
2. 分城纳租 - 分城等级、纳租限量

数据来源：从V1版本集资配置区.py重构
"""

import flet as ft
from typing import Callable, Dict, Any

from 前端.V2.层级3_卡片组.卡片组 import CardGroup

USER_CARD_SPACING = 10

CARDS_CONFIG = [
    {
        "section": "集资设置.小号上贡",
        "title": "小号上贡",
        "icon": "PAYMENTS",
        "subtitle": "小号达到等级后上贡资源",
        "controls": [
            {"id": "上贡限级", "type": "dropdown", "label": "限级选择"},
            {"id": "上贡限量", "type": "dropdown", "label": "限量选择"},
            {"id": "主要统帅", "type": "dropdown", "label": "主要统帅"},
            {"id": "次要统帅", "type": "dropdown", "label": "次要统帅"},
        ],
    },
    {
        "section": "集资设置.分城纳租",
        "title": "分城纳租",
        "icon": "ACCOUNT_BALANCE_WALLET",
        "subtitle": "分城达到等级后纳租",
        "controls": [
            {"id": "分城等级", "type": "dropdown", "label": "等级选择"},
            {"id": "纳租限量", "type": "dropdown", "label": "限量选择"},
        ],
    },
]

class FundingPage:
    _card_group: CardGroup = None
    
    @staticmethod
    def create(page: ft.Page, config_service, on_change: Callable = None, theme_colors: Dict = None) -> ft.Control:
        if theme_colors is None:
            theme_colors = {"text_primary": "#000000", "text_secondary": "#666666", "text_disabled": "#999999", "bg_card": "#FFFFFF", "accent": "#0078D4", "border": "#CCCCCC"}
        
        FundingPage._card_group = CardGroup(page, config_service)
        cards = []
        for card_config in CARDS_CONFIG:
            card = FundingPage._card_group.create(
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
        if FundingPage._card_group:
            FundingPage._card_group.destroy_all()
            FundingPage._card_group = None

if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    
    from 前端.V2.数据层.仓库.配置仓库 import ConfigRepository
    from 前端.V2.业务层.服务.配置服务 import ConfigService
    
    def main(page: ft.Page):
        page.title = "集资设置测试"
        
        repository = ConfigRepository()
        config_service = ConfigService(repository)
        
        funding_page = FundingPage.create(page, config_service)
        page.add(funding_page)
    
    ft.app(target=main)
