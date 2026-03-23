# -*- coding: utf-8 -*-
"""模块名称：集资界面 | 设计思路：集资配置界面，使用折叠卡片模式 | 模块隔离原则"""

import flet as ft
from typing import Dict, Any, List, Callable

from 前端.新界面.核心接口.界面配置 import 界面配置
from 前端.新界面.核心接口.主题提供者 import ThemeProvider
from 前端.新界面.组件模块.折叠卡片 import CollapsibleCard


# *** 用户指定变量 - AI不得修改, 变量值必须生效 ***
USER_CARD_WIDTH = 500
USER_CARD_HEIGHT = 70
USER_CARD_SPACING = 8
# *********************************


class 集资界面:
    """集资配置界面"""
    
    @staticmethod
    def create(
        config: 界面配置=None,
        on_save: Callable[[str, str, str], None]=None,
        width: int=USER_CARD_WIDTH,
    ) -> ft.Column:
        if config is None:
            config = 界面配置()
        
        ThemeProvider.initialize(config)
        theme_colors = config.当前主题颜色
        
        cards: List[ft.Control] = []
        card_data: Dict[str, Dict[str, Any]] = {}
        
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
                
                if on_save:
                    on_save(card_id, config_key, value)
            
            card = CollapsibleCard.create(
                title=title,
                icon=icon,
                subtitle=subtitle,
                enabled=enabled,
                controls_config=controls_config,
                controls_per_row=4,
                width=width,
                on_save=handle_save,
            )
            
            cards.append(card)
            return card
        
        create_card(
            card_id="small_account",
            title="小号上贡",
            icon="UPLOAD",
            subtitle="设置小号上贡相关参数",
            controls_config=[
                {"type": "dropdown", "config_key": "tribute_level", "label": "上贡限级", "value": "05", "options": [f"{i:02d}级" for i in range(5, 16)]},
                {"type": "dropdown", "config_key": "tribute_limit", "label": "上贡限量", "value": "2万", "options": [f"{i}万" for i in range(2, 21)]},
            ],
        )
        
        create_card(
            card_id="branch_city",
            title="分城纳租",
            icon="ATTACH_MONEY",
            subtitle="设置分城纳租相关参数",
            controls_config=[
                {"type": "dropdown", "config_key": "rent_level", "label": "纳租限级", "value": "05", "options": [f"{i:02d}级" for i in range(5, 16)]},
                {"type": "dropdown", "config_key": "rent_limit", "label": "纳租限量", "value": "2万", "options": [f"{i}万" for i in range(2, 21)]},
            ],
        )
        
        content = ft.Column(
            controls=cards,
            spacing=USER_CARD_SPACING,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )
        
        def get_all_values() -> Dict[str, Dict[str, str]]:
            result = {}
            for i, card in enumerate(cards):
                if hasattr(card, 'get_values'):
                    card_id = list(card_data.keys())[i] if i < len(card_data) else f"card_{i}"
                    result[card_id] = card.get_values()
            return result
        
        def set_all_values(values: Dict[str, Dict[str, str]]):
            for i, card in enumerate(cards):
                if hasattr(card, 'set_values'):
                    card_id = list(card_data.keys())[i] if i < len(card_data) else f"card_{i}"
                    if card_id in values:
                        card.set_values(values[card_id])
        
        def dispose():
            for card in cards:
                if hasattr(card, 'dispose'):
                    card.dispose()
        
        content.get_all_values = get_all_values
        content.set_all_values = set_all_values
        content.dispose = dispose
        
        return content


if __name__ == "__main__":
    config = 界面配置()
    ThemeProvider.initialize(config)
    
    def on_save(card_id, key, value):
        print(f"保存: {card_id}.{key} = {value}")
    
    ft.run(lambda page: page.add(集资界面.create(config=config, on_save=on_save)))
