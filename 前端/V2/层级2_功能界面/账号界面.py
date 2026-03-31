# -*- coding: utf-8 -*-

"""
模块名称：账号界面.py
模块功能：账号设置界面 - 15个卡片

卡片配置：
账号01-15 - 类型、名称、账号、密码、方案、平台
"""

import flet as ft
from typing import Callable, Dict, Any

from 前端.V2.层级3_卡片组.卡片组 import CardGroup

USER_CARD_SPACING = 10
MAX_ACCOUNTS = 15

ACCOUNT_CONTROLS = [
    {"id": "类型", "type": "dropdown", "label": "类型:"},
    {"id": "名称", "type": "input", "label": "名称:", "hint": "输入名称"},
    {"id": "账号", "type": "input", "label": "账号:", "hint": "输入账号"},
    {"id": "密码", "type": "input", "label": "密码:", "hint": "输入密码", "password": True},
    {"id": "方案", "type": "dropdown", "label": "方案:"},
    {"id": "平台", "type": "dropdown", "label": "平台:"},
]

class AccountPage:
    _card_group: CardGroup = None
    
    @staticmethod
    def create(page: ft.Page, config_service, on_change: Callable = None, theme_colors: Dict = None) -> ft.Control:
        if theme_colors is None:
            theme_colors = {"text_primary": "#000000", "text_secondary": "#666666", "text_disabled": "#999999", "bg_card": "#FFFFFF", "accent": "#0078D4", "border": "#CCCCCC"}
        
        AccountPage._card_group = CardGroup(page, config_service)
        cards = []
        for i in range(1, MAX_ACCOUNTS + 1):
            card = AccountPage._card_group.create(
                section=f"账号设置.账号{i:02d}",
                title=f"账号{i:02d}",
                icon="ACCOUNT_CIRCLE",
                subtitle="设置账号信息",
                controls_config=ACCOUNT_CONTROLS,
                has_switch=True,
                on_change=on_change,
                theme_colors=theme_colors,
            )
            cards.append(card)
        
        return ft.Column(cards, spacing=USER_CARD_SPACING, scroll=ft.ScrollMode.AUTO, expand=True)
    
    @staticmethod
    def destroy():
        if AccountPage._card_group:
            AccountPage._card_group.destroy_all()
            AccountPage._card_group = None

if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    
    from 前端.V2.数据层.仓库.配置仓库 import ConfigRepository
    from 前端.V2.业务层.服务.配置服务 import ConfigService
    
    def main(page: ft.Page):
        page.title = "账号设置测试"
        
        repository = ConfigRepository()
        config_service = ConfigService(repository)
        
        account_page = AccountPage.create(page, config_service)
        page.add(account_page)
    
    ft.app(target=main)
