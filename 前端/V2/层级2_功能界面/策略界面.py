# -*- coding: utf-8 -*-

"""
模块名称：策略界面.py
模块功能：策略设置界面 - 3个卡片

卡片配置：
1. 建筑速建 - 速建限级、速建类型
2. 资源速产 - 速产限级、速产类型
3. 策点保留 - 保留点数
"""

import flet as ft
from typing import Callable, Dict, Any

from 前端.V2.层级3_卡片组.卡片组 import CardGroup

USER_CARD_SPACING = 10

CARDS_CONFIG = [
    {
        "section": "策略设置.建筑速建",
        "title": "建筑速建",
        "icon": "APARTMENT",
        "subtitle": "达到设置主城等级后,允许加速建筑建设",
        "controls": [
            {"id": "速建限级", "type": "dropdown", "label": "速建限级:"},
            {"id": "速建类型", "type": "dropdown", "label": "速建建筑:"},
        ],
    },
    {
        "section": "策略设置.资源速产",
        "title": "资源速产",
        "icon": "INVENTORY_2",
        "subtitle": "达到设置主城等级后,允许加速资源生产",
        "controls": [
            {"id": "速产限级", "type": "dropdown", "label": "速产限级:"},
            {"id": "速产类型", "type": "dropdown", "label": "速产策略:"},
        ],
    },
    {
        "section": "策略设置.策点保留",
        "title": "策点保留",
        "icon": "SAVINGS",
        "subtitle": "达到设置保留的策略点数后,允许使用策略",
        "controls": [
            {"id": "保留点数", "type": "dropdown", "label": "保留点数:"},
        ],
    },
]

class StrategyPage:
    _card_group: CardGroup = None
    
    @staticmethod
    def create(page: ft.Page, config_service, on_change: Callable = None, theme_colors: Dict = None) -> ft.Control:
        if theme_colors is None:
            theme_colors = {"text_primary": "#000000", "text_secondary": "#666666", "text_disabled": "#999999", "bg_card": "#FFFFFF", "accent": "#0078D4", "border": "#CCCCCC"}
        
        StrategyPage._card_group = CardGroup(page, config_service)
        cards = []
        for card_config in CARDS_CONFIG:
            card = StrategyPage._card_group.create(
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
        if StrategyPage._card_group:
            StrategyPage._card_group.destroy_all()
            StrategyPage._card_group = None

if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    
    from 前端.V2.数据层.仓库.配置仓库 import ConfigRepository
    from 前端.V2.业务层.服务.配置服务 import ConfigService
    
    def main(page: ft.Page):
        page.title = "策略设置测试"
        
        repository = ConfigRepository()
        config_service = ConfigService(repository)
        
        strategy_page = StrategyPage.create(page, config_service)
        page.add(strategy_page)
    
    ft.run(main)
