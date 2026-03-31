# -*- coding: utf-8 -*-

"""
模块名称：系统界面.py
模块功能：系统设置界面 - 4个卡片

卡片配置：
1. 挂机模式 - 模式选择
2. 指令速度 - 速度选择
3. 尝试次数 - 次数选择
4. 清缓限量 - 限量选择
"""

import flet as ft
from typing import Callable, Dict, Any

from 前端.V2.层级3_卡片组.卡片组 import CardGroup

USER_CARD_SPACING = 10

CARDS_CONFIG = [
    {
        "section": "系统设置.挂机模式",
        "title": "挂机模式",
        "icon": "POWER_SETTINGS_NEW",
        "subtitle": "全自动:自动挂机,无需人为干预 | 半自动:点击头像,自动切换账号",
        "controls": [
            {"id": "挂机模式", "type": "dropdown", "label": "模式选择"},
        ],
    },
    {
        "section": "系统设置.指令速度",
        "title": "指令速度",
        "icon": "SPEED",
        "subtitle": "运行指令间隔频率(毫秒)，数值越小速度越快",
        "controls": [
            {"id": "指令速度", "type": "dropdown", "label": "速度选择"},
        ],
    },
    {
        "section": "系统设置.尝试次数",
        "title": "尝试次数",
        "icon": "REFRESH",
        "subtitle": "连续操作失败达到最大尝试次数后,触发自动纠错系统",
        "controls": [
            {"id": "尝试次数", "type": "dropdown", "label": "次数选择"},
        ],
    },
    {
        "section": "系统设置.清缓限量",
        "title": "清缓限量",
        "icon": "DELETE_SWEEP",
        "subtitle": "达到设置系统缓存清理阈值(M)后,自动清理缓存",
        "controls": [
            {"id": "清缓限量", "type": "dropdown", "label": "限量选择"},
        ],
    },
]

class SystemPage:
    _card_group: CardGroup = None
    
    @staticmethod
    def create(page: ft.Page, config_service, on_change: Callable = None, theme_colors: Dict = None) -> ft.Control:
        if theme_colors is None:
            theme_colors = {"text_primary": "#000000", "text_secondary": "#666666", "text_disabled": "#999999", "bg_card": "#FFFFFF", "accent": "#0078D4", "border": "#CCCCCC"}
        
        SystemPage._card_group = CardGroup(page, config_service)
        cards = []
        for card_config in CARDS_CONFIG:
            card = SystemPage._card_group.create(
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
        if SystemPage._card_group:
            SystemPage._card_group.destroy_all()
            SystemPage._card_group = None

if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    
    from 前端.V2.数据层.仓库.配置仓库 import ConfigRepository
    from 前端.V2.业务层.服务.配置服务 import ConfigService
    
    def main(page: ft.Page):
        page.title = "系统设置测试"
        
        repository = ConfigRepository()
        config_service = ConfigService(repository)
        
        system_page = SystemPage.create(page, config_service)
        page.add(system_page)
    
    ft.app(target=main)
