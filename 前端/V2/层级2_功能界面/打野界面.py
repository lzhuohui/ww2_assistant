# -*- coding: utf-8 -*-

"""
模块名称：打野界面.py
模块功能：打野设置界面

职责：
- 从配置服务获取section列表
- 调用卡片组创建卡片
- 销毁功能

不负责：
- 卡片信息获取（由卡片开关负责）
- 控件创建（由卡片控件负责）
- 开关逻辑（由卡片开关负责）

设计原则（符合V2版本模块化设计补充共识）：
- 从配置服务获取数据，不硬编码
- 只传递section，不传递具体数据
- 数据归属原则：界面配置.json是唯一数据源
"""

import flet as ft
from typing import Callable, Dict, Any

from 前端.V2.层级3_卡片组.卡片组 import CardGroup

USER_CARD_SPACING = 10

class HuntingPage:
    """
    打野设置界面（层级2：功能界面）
    
    职责：
    - 从配置服务获取section列表
    - 调用卡片组创建卡片
    - 销毁功能
    
    不负责：
    - 卡片信息获取（由卡片开关负责）
    - 控件创建（由卡片控件负责）
    - 开关逻辑（由卡片开关负责）
    """
    
    _card_group: CardGroup = None
    
    @staticmethod
    def create(
        page: ft.Page,
        config_service,
        on_change: Callable = None,
        theme_colors: Dict = None,
    ) -> ft.Control:
        """
        创建打野设置界面
        
        参数：
        - page: 页面实例
        - config_service: 配置服务实例
        - on_change: 控件值变更回调
        - theme_colors: 主题颜色
        
        返回：
        - ft.Control: 界面内容
        """
        if theme_colors is None:
            theme_colors = config_service.get_theme_colors()
        
        CardGroup.set_config_service(config_service)
        HuntingPage._card_group = CardGroup(page, config_service)
        cards = []
        
        sections = config_service.get_sections_by_interface("打野界面")
        for section in sections:
            card = HuntingPage._card_group.create(
                section=section,
                on_control_change=on_change,
                theme_colors=theme_colors,
            )
            cards.append(card)
        
        return ft.Column(cards, spacing=USER_CARD_SPACING, scroll=ft.ScrollMode.AUTO, expand=True)
    
    @staticmethod
    def destroy():
        """销毁所有卡片"""
        if HuntingPage._card_group:
            HuntingPage._card_group.destroy_all()
            HuntingPage._card_group = None

if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    
    from 前端.V2.业务层.服务.配置服务 import ConfigService
    
    def main(page: ft.Page):
        page.title = "打野设置测试"
        
        config_service = ConfigService()
        CardGroup.set_config_service(config_service)
        
        hunting_page = HuntingPage.create(page, config_service)
        page.add(hunting_page)
    
    ft.run(main)
