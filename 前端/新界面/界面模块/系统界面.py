# -*- coding: utf-8 -*-
"""模块名称：系统界面 | 设计思路：系统配置界面，使用折叠卡片模式 | 模块隔离原则"""

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


class 系统界面:
    """系统配置界面"""
    
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
            card_id="hangup_mode",
            title="挂机模式",
            icon="POWER_SETTINGS_NEW",
            subtitle="全自动:自动挂机,无需人为干预 | 半自动:点击头像,自动切换账号",
            controls_config=[
                {"type": "dropdown", "config_key": "mode", "label": "模式选择", "value": "自动", "options": ["自动", "手动"]},
            ],
        )
        
        create_card(
            card_id="command_speed",
            title="指令速度",
            icon="SPEED",
            subtitle="运行指令间隔频率(毫秒)，数值越小速度越快",
            controls_config=[
                {"type": "dropdown", "config_key": "speed", "label": "速度选择", "value": "100毫秒", "options": ["100毫秒", "150毫秒", "200毫秒", "250毫秒", "300毫秒", "350毫秒", "400毫秒", "450毫秒", "500毫秒"]},
            ],
        )
        
        create_card(
            card_id="retry_count",
            title="尝试次数",
            icon="REFRESH",
            subtitle="连续操作失败达到最大尝试次数后,触发自动纠错系统",
            controls_config=[
                {"type": "dropdown", "config_key": "count", "label": "次数选择", "value": "10次", "options": ["10次", "15次", "20次", "25次", "30次"]},
            ],
        )
        
        create_card(
            card_id="cache_limit",
            title="清缓限量",
            icon="DELETE_SWEEP",
            subtitle="达到设置系统缓存清理阈值(M)后,自动清理缓存",
            controls_config=[
                {"type": "dropdown", "config_key": "limit", "label": "限量选择", "value": "1.0M", "options": ["1.0M", "1.5M", "2.0M", "2.5M", "3.0M", "3.5M", "4.0M", "4.5M", "5.0M"]},
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
    
    ft.run(lambda page: page.add(系统界面.create(config=config, on_save=on_save)))
