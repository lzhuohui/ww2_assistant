# -*- coding: utf-8 -*-
"""
策略界面 - 设备层

设计思路:
    本模块是设备层模块，提供策略界面。

功能:
    1. 继承基础界面
    2. 提供策略相关功能
    3. 包含建筑速建、资源速产、策点保留

数据来源:
    主题颜色从界面配置获取。

使用场景:
    被系统层调用，提供策略界面。

可独立运行调试: python 策略界面.py
"""

import flet as ft
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from 原子层.界面配置 import 界面配置
from 设备层.基础界面 import BaseInterface
from 组件层.下拉卡片 import DropDownCard
from 组件层.开关卡片 import SwitchCard


def create_mixed_card_list(config: 界面配置, card_configs: list) -> ft.Column:  # 创建混合卡片列表（下拉框+开关）
    card_spacing = config.获取尺寸("界面", "card_spacing")
    controls = []
    
    for i, card_config in enumerate(card_configs):
        card_type = card_config.get("type", "dropdown")
        
        if card_type == "switch":
            card = SwitchCard.create(
                config=config,
                title=card_config.get("title", ""),
                description=card_config.get("description"),
                icon=card_config.get("icon"),
                value=card_config.get("value", False),
                on_change=card_config.get("on_change"),
            )
        else:
            card = DropDownCard.create(
                config=config,
                title=card_config.get("title", ""),
                description=card_config.get("description"),
                icon=card_config.get("icon"),
                options=card_config.get("options", []),
                value=card_config.get("value"),
                on_change=card_config.get("on_change"),
            )
        
        controls.append(card)
        
        if i < len(card_configs) - 1:
            controls.append(ft.Divider(height=card_spacing, color="transparent"))
    
    return ft.Column(controls, spacing=0)


class StrategyInterface(BaseInterface):  # 策略界面
    """策略界面 - 提供策略功能"""
    
    def __init__(self, config: 界面配置, page: ft.Page):
        super().__init__(config, page, title="策略设置", subtitle="策略相关配置")
    
    def _create_content_area(self) -> ft.Control:  # 创建内容区域
        return create_mixed_card_list(
            config=self._config,
            card_configs=[
                {
                    "type": "switch",
                    "title": "开启速建",
                    "description": "自动加速建筑建造",
                    "icon": "CONSTRUCTION",
                    "value": True
                },
                {
                    "type": "dropdown",
                    "title": "速建限级",
                    "description": "建筑等级低于此值时自动加速",
                    "icon": "STAIRS",
                    "options": [f"{i:02d}" for i in range(5, 16)],
                    "value": "08"
                },
                {
                    "type": "dropdown",
                    "title": "建筑类型",
                    "description": "选择加速的建筑类型",
                    "icon": "DOMAIN",
                    "options": ["城资建筑", "城市建筑", "资源建筑"],
                    "value": "城资建筑"
                },
                {
                    "type": "switch",
                    "title": "开启速产",
                    "description": "自动施放资源策略",
                    "icon": "FACTORY",
                    "value": True
                },
                {
                    "type": "dropdown",
                    "title": "速产限级",
                    "description": "主城等级低于此值时自动施策",
                    "icon": "TRENDING_UP",
                    "options": [f"{i:02d}" for i in range(5, 16)],
                    "value": "07"
                },
                {
                    "type": "dropdown",
                    "title": "策略类型",
                    "description": "选择施放的资源策略",
                    "icon": "SCIENCE",
                    "options": ["平衡资源", "战时经济", "钢铁熔炉", "橡胶采集", "石油开采"],
                    "value": "平衡资源"
                },
                {
                    "type": "dropdown",
                    "title": "保留点数",
                    "description": "策略点数低于此值时停止施策",
                    "icon": "SAVINGS",
                    "options": ["30", "60", "90", "120", "150", "180", "210", "240"],
                    "value": "60"
                },
            ]
        )


# 兼容别名
策略界面 = StrategyInterface


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    config = 界面配置()
    
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = config.获取颜色("bg_primary")
        interface = StrategyInterface(config, page)
        page.add(interface.render())
    
    ft.run(main)
