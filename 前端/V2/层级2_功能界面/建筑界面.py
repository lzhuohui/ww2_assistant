# -*- coding: utf-8 -*-

"""
模块名称：建筑界面.py
模块功能：建筑设置界面 - 5个卡片

卡片配置：
1. 主帅主城 - 城市、兵工、陆军、空军、商业、补给、内塔、村庄、资源、军工、港口、外塔
2. 副帅主城 - 城市、兵工、陆军、空军、商业、补给、内塔、村庄、资源、军工、港口、外塔
3. 所有分城 - 城市、兵工、陆军、空军、商业、补给、内塔、村庄、资源、军工、港口、外塔
4. 军团城市 - 城市、兵工、军需、陆军、空军、炮塔、编号
5. 建筑优先 - 资源建筑、塔防建筑
"""

import flet as ft
from typing import Callable, Dict, Any

from 前端.V2.层级3_卡片组.卡片组 import CardGroup

USER_CARD_SPACING = 10

CARDS_CONFIG = [
    {
        "section": "建筑设置.主帅主城",
        "title": "主帅主城",
        "icon": "DOMAIN",
        "subtitle": "设置主帅主城建筑等级",
        "controls": [
            {"id": "城市等级", "type": "dropdown", "label": "城市"},
            {"id": "兵工厂等级", "type": "dropdown", "label": "兵工"},
            {"id": "陆军基地", "type": "dropdown", "label": "陆军"},
            {"id": "空军基地", "type": "dropdown", "label": "空军"},
            {"id": "商业区", "type": "dropdown", "label": "商业"},
            {"id": "补给品厂", "type": "dropdown", "label": "补给"},
            {"id": "内塔等级", "type": "dropdown", "label": "内塔"},
            {"id": "村庄等级", "type": "dropdown", "label": "村庄"},
            {"id": "资源等级", "type": "dropdown", "label": "资源"},
            {"id": "军工等级", "type": "dropdown", "label": "军工"},
            {"id": "港口等级", "type": "dropdown", "label": "港口"},
            {"id": "外塔等级", "type": "dropdown", "label": "外塔"},
        ],
        "controls_per_row": 6,
    },
    {
        "section": "建筑设置.副帅主城",
        "title": "副帅主城",
        "icon": "APARTMENT",
        "subtitle": "设置副帅主城建筑等级",
        "controls": [
            {"id": "城市等级", "type": "dropdown", "label": "城市"},
            {"id": "兵工厂等级", "type": "dropdown", "label": "兵工"},
            {"id": "陆军基地", "type": "dropdown", "label": "陆军"},
            {"id": "空军基地", "type": "dropdown", "label": "空军"},
            {"id": "商业区", "type": "dropdown", "label": "商业"},
            {"id": "补给品厂", "type": "dropdown", "label": "补给"},
            {"id": "内塔等级", "type": "dropdown", "label": "内塔"},
            {"id": "村庄等级", "type": "dropdown", "label": "村庄"},
            {"id": "资源等级", "type": "dropdown", "label": "资源"},
            {"id": "军工等级", "type": "dropdown", "label": "军工"},
            {"id": "港口等级", "type": "dropdown", "label": "港口"},
            {"id": "外塔等级", "type": "dropdown", "label": "外塔"},
        ],
        "controls_per_row": 6,
    },
    {
        "section": "建筑设置.所有分城",
        "title": "所有分城",
        "icon": "LOCATION_CITY",
        "subtitle": "设置所有分城建筑等级",
        "controls": [
            {"id": "城市等级", "type": "dropdown", "label": "城市"},
            {"id": "兵工厂等级", "type": "dropdown", "label": "兵工"},
            {"id": "陆军基地", "type": "dropdown", "label": "陆军"},
            {"id": "空军基地", "type": "dropdown", "label": "空军"},
            {"id": "商业区", "type": "dropdown", "label": "商业"},
            {"id": "补给品厂", "type": "dropdown", "label": "补给"},
            {"id": "内塔等级", "type": "dropdown", "label": "内塔"},
            {"id": "村庄等级", "type": "dropdown", "label": "村庄"},
            {"id": "资源等级", "type": "dropdown", "label": "资源"},
            {"id": "军工等级", "type": "dropdown", "label": "军工"},
            {"id": "港口等级", "type": "dropdown", "label": "港口"},
            {"id": "外塔等级", "type": "dropdown", "label": "外塔"},
        ],
        "controls_per_row": 6,
    },
    {
        "section": "建筑设置.军团城市",
        "title": "军团城市",
        "icon": "ACCOUNT_BALANCE",
        "subtitle": "设置军团城市建筑等级",
        "controls": [
            {"id": "城市等级", "type": "dropdown", "label": "城市"},
            {"id": "兵工厂等级", "type": "dropdown", "label": "兵工"},
            {"id": "军需等级", "type": "dropdown", "label": "军需"},
            {"id": "陆军基地", "type": "dropdown", "label": "陆军"},
            {"id": "空军基地", "type": "dropdown", "label": "空军"},
            {"id": "炮塔等级", "type": "dropdown", "label": "炮塔"},
            {"id": "城市编号", "type": "dropdown", "label": "编号"},
        ],
        "controls_per_row": 7,
    },
    {
        "section": "建筑设置.建筑优先",
        "title": "建筑优先",
        "icon": "HOME_WORK",
        "subtitle": "按选择顺序建设建筑",
        "controls": [
            {"id": "资源建筑", "type": "dropdown", "label": "资源"},
            {"id": "塔防建筑", "type": "dropdown", "label": "塔防"},
        ],
        "controls_per_row": 2,
    },
]

class BuildingPage:
    _card_group: CardGroup = None
    
    @staticmethod
    def create(page: ft.Page, config_service, on_change: Callable = None, theme_colors: Dict = None) -> ft.Control:
        if theme_colors is None:
            theme_colors = {"text_primary": "#000000", "text_secondary": "#666666", "text_disabled": "#999999", "bg_card": "#FFFFFF", "accent": "#0078D4", "border": "#CCCCCC"}
        
        BuildingPage._card_group = CardGroup(page, config_service)
        cards = []
        for card_config in CARDS_CONFIG:
            card = BuildingPage._card_group.create(
                section=card_config.get("section", ""),
                title=card_config.get("title", ""),
                icon=card_config.get("icon", "HOME"),
                subtitle=card_config.get("subtitle", ""),
                controls_config=card_config.get("controls", []),
                has_switch=True,
                on_change=on_change,
                theme_colors=theme_colors,
                controls_per_row=card_config.get("controls_per_row", None),
            )
            cards.append(card)
        
        return ft.Column(cards, spacing=USER_CARD_SPACING, scroll=ft.ScrollMode.AUTO, expand=True)
    
    @staticmethod
    def destroy():
        if BuildingPage._card_group:
            BuildingPage._card_group.destroy_all()
            BuildingPage._card_group = None

if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    
    from 前端.V2.数据层.仓库.配置仓库 import ConfigRepository
    from 前端.V2.业务层.服务.配置服务 import ConfigService
    
    def main(page: ft.Page):
        page.title = "建筑设置测试"
        
        repository = ConfigRepository()
        config_service = ConfigService(repository)
        
        building_page = BuildingPage.create(page, config_service)
        page.add(building_page)
    
    ft.app(target=main)
