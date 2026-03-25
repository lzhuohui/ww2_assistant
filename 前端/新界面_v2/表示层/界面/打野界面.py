# -*- coding: utf-8 -*-
"""
模块名称：HuntingPage
设计思路: 打野配置界面，使用折叠卡片模式
模块隔离: 界面层依赖组件层和业务层
"""

import flet as ft
from typing import Dict, Any, List, Callable, Optional

from 前端.新界面_v2.核心.配置.界面配置 import UIConfig
from 前端.新界面_v2.表示层.组件.复合.折叠卡片 import CollapsibleCard
from 前端.新界面_v2.核心.常量.全局常量 import USER_SPACING, USER_CARD_SPACING


# *** 用户指定变量 - AI不得修改, 变量值必须生效 ***
# （用户未指定变量）
# *********************************


class HuntingPage:
    """打野配置界面"""
    
    current_loaded_card: Optional[ft.Container] = None
    
    @staticmethod
    def create(
        config: UIConfig=None,
        save_callback: Callable[[str, str, str], None]=None,
    ) -> ft.Container:
        if config is None:
            config = UIConfig()
        
        theme_colors = config.当前主题颜色
        card_list: List[ft.Control] = []
        card_data: Dict[str, Dict[str, Any]] = {}
        current_loaded_card = [None]
        
        def destroy_loaded_card():
            if current_loaded_card[0] and hasattr(current_loaded_card[0], 'is_loaded'):
                if current_loaded_card[0].is_loaded():
                    current_loaded_card[0].destroy_controls()
            current_loaded_card[0] = None
        
        def create_card(
            card_id: str,
            title: str,
            icon: str,
            subtitle: str,
            controls_config: List[Dict[str, Any]],
            enabled: bool=True,
        ) -> ft.Container:
            def handle_save(config_key: str, value: str):
                if card_id not in card_data:
                    card_data[card_id] = {}
                card_data[card_id][config_key] = value
                if save_callback:
                    save_callback(card_id, config_key, value)
            
            def handle_expand():
                if current_loaded_card[0] and current_loaded_card[0] != card:
                    if current_loaded_card[0].is_loaded():
                        current_loaded_card[0].destroy_controls()
                current_loaded_card[0] = card
            
            card = CollapsibleCard.create(
                title=title,
                icon=icon,
                subtitle=subtitle,
                enabled=enabled,
                controls_config=controls_config,
                controls_per_row=1,
                on_save=handle_save,
                on_expand=handle_expand,
                config=config,
            )
            card_list.append(card)
            return card
        
        create_card(
            card_id="auto_hunting",
            title="自动打野",
            icon="EXPLORE",
            subtitle="自动搜索并攻击野怪",
            controls_config=[
                {"type": "dropdown", "config_key": "level", "label": "野怪等级选择:", "value": "全部", "options": ["全部", "1-3级", "4-6级", "7-9级", "10级以上"]},
                {"type": "dropdown", "config_key": "frequency", "label": "搜索频率选择:", "value": "每小时", "options": ["每30分钟", "每小时", "每2小时", "每4小时"]},
            ],
        )
        
        title_bar = ft.Row([
            ft.Icon(ft.Icons.EXPLORE, size=20, color=theme_colors.get("accent")),
            ft.Container(width=6),
            ft.Text("打野设置", size=16, weight=ft.FontWeight.BOLD, color=theme_colors.get("text_primary")),
        ], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER)
        
        card_column = ft.Column(
            controls=card_list,
            spacing=USER_CARD_SPACING,
            scroll=ft.ScrollMode.HIDDEN,
            expand=True,
        )
        
        content_column = ft.Column(
            controls=[
                title_bar,
                ft.Container(height=USER_SPACING),
                card_column,
            ],
            spacing=0,
            expand=True,
        )
        
        content_column.destroy_loaded_card = destroy_loaded_card
        
        return ft.Container(
            content=content_column,
            expand=True,
        )


# *** 调试逻辑 ***
if __name__ == "__main__":
    ft.run(lambda page: page.add(HuntingPage.create()))
