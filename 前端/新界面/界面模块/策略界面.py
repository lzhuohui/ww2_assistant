# -*- coding: utf-8 -*-
"""模块名称：策略界面 | 设计思路：策略配置界面，使用折叠卡片模式 | 模块隔离原则"""

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


class 策略界面:
    """策略配置界面"""
    
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
            card_id="main_city",
            title="主帅主城",
            icon="HOME",
            subtitle="设置主帅主城建筑等级",
            controls_config=[
                {"type": "dropdown", "config_key": "city_level", "label": "城市", "value": "17", "options": [f"{i:02d}级" for i in range(1, 21)]},
                {"type": "dropdown", "config_key": "barracks_level", "label": "兵营", "value": "15", "options": [f"{i:02d}级" for i in range(1, 21)]},
                {"type": "dropdown", "config_key": "factory_level", "label": "兵工", "value": "12", "options": [f"{i:02d}级" for i in range(1, 21)]},
                {"type": "dropdown", "config_key": "army_level", "label": "陆军", "value": "14", "options": [f"{i:02d}级" for i in range(1, 21)]},
            ],
        )
        
        create_card(
            card_id="resource",
            title="资源采集",
            icon="INVENTORY_2",
            subtitle="设置资源采集策略",
            controls_config=[
                {"type": "dropdown", "config_key": "collect_level", "label": "采集等级", "value": "10", "options": [f"{i:02d}级" for i in range(1, 21)]},
                {"type": "dropdown", "config_key": "collect_count", "label": "采集数量", "value": "5", "options": [f"{i}个" for i in range(1, 11)]},
            ],
        )
        
        create_card(
            card_id="battle",
            title="战斗策略",
            icon="SWORD_FIGHT",
            subtitle="设置战斗相关策略",
            controls_config=[
                {"type": "dropdown", "config_key": "attack_mode", "label": "攻击模式", "value": "主动", "options": ["主动", "被动", "防守"]},
                {"type": "dropdown", "config_key": "retreat_hp", "label": "撤退血量", "value": "30%", "options": [f"{i}%" for i in range(10, 60, 10)]},
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
    
    ft.run(lambda page: page.add(策略界面.create(config=config, on_save=on_save)))
