# -*- coding: utf-8 -*-
"""
任务界面 - 设备层

设计思路:
    本模块是设备层模块，提供任务界面。

功能:
    1. 继承基础界面
    2. 提供任务相关功能
    3. 包含主线任务和支线任务

数据来源:
    主题颜色从界面配置获取。

使用场景:
    被系统层调用，提供任务界面。

可独立运行调试: python 任务界面.py
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


class TaskInterface(BaseInterface):  # 任务界面
    """任务界面 - 提供任务功能"""
    
    def __init__(self, config: 界面配置, page: ft.Page):
        super().__init__(config, page, title="任务设置", subtitle="任务相关配置")
    
    def _create_content_area(self) -> ft.Control:  # 创建内容区域
        return create_mixed_card_list(
            config=self._config,
            card_configs=[
                {
                    "type": "switch",
                    "title": "开启主线",
                    "description": "自动执行主线任务",
                    "icon": "FLAG",
                    "value": True
                },
                {
                    "type": "dropdown",
                    "title": "主线限级",
                    "description": "主线任务等级上限",
                    "icon": "STAIRS",
                    "options": [f"{i:02d}" for i in range(1, 16)],
                    "value": "05"
                },
                {
                    "type": "switch",
                    "title": "开启支线",
                    "description": "自动执行支线任务",
                    "icon": "ASSIGNMENT",
                    "value": False
                },
                {
                    "type": "dropdown",
                    "title": "支线限级",
                    "description": "支线任务等级上限",
                    "icon": "TRENDING_UP",
                    "options": [f"{i:02d}" for i in range(5, 16)],
                    "value": "10"
                },
            ]
        )


# 兼容别名
任务界面 = TaskInterface


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    config = 界面配置()
    
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = config.获取颜色("bg_primary")
        interface = TaskInterface(config, page)
        page.add(interface.render())
    
    ft.run(main)
