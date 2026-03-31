# -*- coding: utf-8 -*-

"""
模块名称：任务界面.py
模块功能：任务设置界面 - 2个卡片

卡片配置：
1. 主线任务 - 主城等级
2. 支线任务 - 支线主城等级
"""

import flet as ft
from typing import Callable, Dict, Any

from 前端.V2.层级3_卡片组.卡片组 import CardGroup

USER_CARD_SPACING = 10

CARDS_CONFIG = [
    {
        "section": "任务设置.主线任务",
        "title": "主线任务",
        "icon": "FLAG",
        "subtitle": "达到设置主城等级后,允许执行主线任务",
        "controls": [
            {"id": "主城等级", "type": "dropdown", "label": "限级选择"},
        ],
    },
    {
        "section": "任务设置.支线任务",
        "title": "支线任务",
        "icon": "ASSIGNMENT",
        "subtitle": "达到设置主城等级后,允许执行支线任务",
        "controls": [
            {"id": "支线主城等级", "type": "dropdown", "label": "限级选择"},
        ],
    },
]

class TaskPage:
    _card_group: CardGroup = None
    
    @staticmethod
    def create(page: ft.Page, config_service, on_change: Callable = None, theme_colors: Dict = None) -> ft.Control:
        if theme_colors is None:
            theme_colors = {"text_primary": "#000000", "text_secondary": "#666666", "text_disabled": "#999999", "bg_card": "#FFFFFF", "accent": "#0078D4", "border": "#CCCCCC"}
        
        TaskPage._card_group = CardGroup(page, config_service)
        cards = []
        for card_config in CARDS_CONFIG:
            card = TaskPage._card_group.create(
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
        if TaskPage._card_group:
            TaskPage._card_group.destroy_all()
            TaskPage._card_group = None

if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    
    from 前端.V2.数据层.仓库.配置仓库 import ConfigRepository
    from 前端.V2.业务层.服务.配置服务 import ConfigService
    
    def main(page: ft.Page):
        page.title = "任务设置测试"
        
        repository = ConfigRepository()
        config_service = ConfigService(repository)
        
        task_page = TaskPage.create(page, config_service)
        page.add(task_page)
    
    ft.app(target=main)
