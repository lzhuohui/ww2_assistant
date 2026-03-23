# -*- coding: utf-8 -*-
"""
模块名称：设置面板 | 设计思路：通用模块，接收卡片配置列表，动态创建卡片 | 模块隔离原则：不直接创建被调用模块的内容，不覆盖被调用模块的计算结果，用户指定变量除外
"""

import flet as ft

from 前端.用户设置界面.配置.界面配置 import 界面配置
from 前端.用户设置界面.组件模块.通用功能容器 import GenericFunctionContainer, USER_WIDTH
from 前端.用户设置界面.组件模块.通用卡片 import UniversalCard
from 前端.用户设置界面.单元模块.下拉框 import Dropdown
from 前端.用户设置界面.配置.卡片配置 import 卡片配置
from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider


# *** 用户指定变量 - AI不得修改, 变量值必须生效 ***
USER_CARD_MARGIN = 5  # 卡片边缘到容器边缘的边距
# *********************************


class SettingsPanel:
    """设置面板 - 通用模块"""
    
    @staticmethod
    def create(
        config: 界面配置=None,
        title: str="设置",
        icon: str="SETTINGS",
        card_names: list=None,
        width: int=USER_WIDTH,
        expand: bool=False
    ) -> ft.Container:
        if config is None:
            config = 界面配置()
        
        if card_names is None:
            card_names = ["挂机模式", "指令速度"]
        
        配置 = config
        
        cards = []
        for card_name in card_names:
            card_config = 卡片配置.get(card_name)
            if card_config:
                card = SettingsPanel._create_card(配置, card_config)
                cards.append(card)
        
        return GenericFunctionContainer.create(
            config=配置,
            title=title,
            icon=icon,
            cards=cards,
            width=width,
            card_margin=USER_CARD_MARGIN,
            expand=expand,
        )
    
    @staticmethod
    def _create_card(配置: 界面配置, card_config: dict) -> ft.Container:
        card_type = card_config.get("card_type", "switch_dropdown")
        
        if card_type == "switch_dropdown":
            return SettingsPanel._create_switch_dropdown_card(配置, card_config)
        elif card_type == "color_blocks":
            return SettingsPanel._create_color_blocks_card(配置, card_config)
        else:
            return UniversalCard.create(
                title=card_config.get("title", "未知卡片"),
                icon=card_config.get("icon", "HELP"),
                subtitle=card_config.get("subtitle", ""),
            )
    
    @staticmethod
    def _create_switch_dropdown_card(配置: 界面配置, card_config: dict) -> ft.Container:
        dropdown_configs = card_config.get("dropdown_configs", [])
        
        controls = []
        for dropdown_config in dropdown_configs:
            options = dropdown_config.get("options", [])
            default_value = dropdown_config.get("default_value", options[0] if options else "")
            label = dropdown_config.get("label", "")
            
            dropdown = Dropdown.create(
                options=options,
                value=default_value,
            )
            
            if label:
                label_text = ft.Text(
                    label,
                    size=14,
                    color=ThemeProvider.get_color("text_secondary"),
                )
                row = ft.Row(
                    [label_text, dropdown],
                    spacing=8,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                )
                row.height = 32
                controls.append(row)
            else:
                controls.append(dropdown)
        
        return UniversalCard.create(
            title=card_config.get("title", ""),
            icon=card_config.get("icon", "SETTINGS"),
            subtitle=card_config.get("subtitle", ""),
            enabled=card_config.get("enabled", True),
            controls=controls,
        )
    
    @staticmethod
    def _create_color_blocks_card(配置: 界面配置, card_config: dict) -> ft.Container:
        return UniversalCard.create(
            title=card_config.get("title", ""),
            icon=card_config.get("icon", "PALETTE"),
            subtitle=card_config.get("subtitle", ""),
        )


# *** 调试逻辑 ***
if __name__ == "__main__":
    ft.run(lambda page: page.add(SettingsPanel.create()))
