# -*- coding: utf-8 -*-
"""
模块名称：设置容器
设计思路及联动逻辑:
    配置驱动的设置容器，接收卡片名称列表，自动从ConfigManager获取配置创建卡片。
    支持多种卡片类型：switch_dropdown、color_blocks等。
模块隔离原则:
    1. 不直接创建被调用模块的内容
    2. 不覆盖被调用模块的计算结果
    3. 用户指定变量除外
"""

import flet as ft
from typing import List, Optional, Dict, Any, Callable

from 前端.用户设置界面.配置.界面配置 import 界面配置
from 前端.用户设置界面.配置.配置管理器 import ConfigManager
from 前端.用户设置界面.组件模块.通用功能容器 import GenericFunctionContainer, DEFAULT_WIDTH, DEFAULT_HEIGHT, USER_MARGIN
from 前端.用户设置界面.组件模块.通用卡片 import UniversalCard
from 前端.用户设置界面.单元模块.下拉框 import Dropdown
from 前端.用户设置界面.单元模块.文本标签 import LabelText


# *** 用户指定变量 - AI不得修改, 变量值必须生效 ***
# （用户未指定变量）
# *********************************

# 默认值常量 - 供调用者获取
DEFAULT_TITLE = "设置"
DEFAULT_ICON = "SETTINGS"


class SettingsContainer:
    """设置容器 - 配置驱动，自动创建卡片"""
    
    @staticmethod
    def create(
        config: 界面配置,
        title: str=DEFAULT_TITLE,
        icon: str=DEFAULT_ICON,
        card_names: List[str]=None,
        cards: List[ft.Control]=None,
        width: int=DEFAULT_WIDTH,
        height: int=DEFAULT_HEIGHT,
        expand: bool=False,
        **kwargs
    ) -> ft.Container:
        final_cards = []
        card_width = width - USER_MARGIN * 2
        
        try:
            config_manager = ConfigManager()
        except:
            config_manager = None
        
        if card_names:
            for card_name in card_names:
                card = SettingsContainer._create_card_from_config(
                    card_name=card_name,
                    config_manager=config_manager,
                    card_width=card_width,
                )
                if card:
                    final_cards.append(card)
        
        if cards:
            final_cards.extend(cards)
        
        return GenericFunctionContainer.create(
            config=config,
            title=title,
            icon=icon,
            cards=final_cards,
            width=width,
            height=height,
            expand=expand,
            **kwargs
        )
    
    @staticmethod
    def _create_card_from_config(
        card_name: str,
        config_manager: ConfigManager,
        card_width: int,
    ) -> Optional[ft.Container]:
        if not config_manager:
            return None
        
        card_config = config_manager.get_card_config(card_name)
        if not card_config:
            return None
        
        card_type = card_config.get("card_type", "switch_dropdown")
        
        if card_type == "switch_dropdown":
            return SettingsContainer._create_switch_dropdown_card(
                card_name=card_name,
                card_config=card_config,
                config_manager=config_manager,
                card_width=card_width,
            )
        elif card_type == "color_blocks":
            return SettingsContainer._create_color_blocks_card(
                card_name=card_name,
                card_config=card_config,
                config_manager=config_manager,
                card_width=card_width,
            )
        
        return None
    
    @staticmethod
    def _create_switch_dropdown_card(
        card_name: str,
        card_config: Dict[str, Any],
        config_manager: ConfigManager,
        card_width: int,
    ) -> ft.Container:
        controls = []
        dropdown_configs = card_config.get("dropdown_configs", [])
        controls_per_row = card_config.get("controls_per_row", 1)
        
        for dd_config in dropdown_configs:
            config_key = dd_config.get("config_key")
            label = dd_config.get("label", "")
            options = dd_config.get("options", [])
            default_value = dd_config.get("default_value", "")
            unit = dd_config.get("unit", "")
            
            value = config_manager.get_value(card_name, config_key, default_value)
            if unit and not value.endswith(unit):
                value = f"{value}{unit}"
            
            def make_on_change(cn, ck):
                def on_change(v):
                    config_manager.set_value(cn, ck, v)
                return on_change
            
            dropdown = Dropdown.create(
                options=options,
                value=value,
                width=120,
                on_change=make_on_change(card_name, config_key),
            )
            
            label_text = LabelText.create(
                text=label,
                role="secondary",
                size=14,
                enabled=True
            )
            
            control_row = ft.Row(
                [label_text, dropdown],
                alignment=ft.MainAxisAlignment.END,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8,
                expand=True,
            )
            controls.append(control_row)
        
        switch_config = card_config.get("switch_config", {})
        switch_key = switch_config.get("config_key")
        enabled = config_manager.get_value(card_name, switch_key, card_config.get("enabled", True)) if switch_key else card_config.get("enabled", True)
        
        def make_on_state_change(cn, sk):
            def on_state_change(new_enabled: bool):
                if sk:
                    config_manager.set_value(cn, sk, new_enabled)
            return on_state_change
        
        return UniversalCard.create(
            title=card_config.get("title", card_name),
            icon=card_config.get("icon", "SETTINGS"),
            enabled=enabled,
            on_state_change=make_on_state_change(card_name, switch_key) if switch_key else None,
            subtitle=card_config.get("subtitle", ""),
            controls=controls if controls else None,
            controls_per_row=controls_per_row,
            width=card_width,
        )
    
    @staticmethod
    def _create_color_blocks_card(
        card_name: str,
        card_config: Dict[str, Any],
        config_manager: ConfigManager,
        card_width: int,
    ) -> ft.Container:
        from 前端.用户设置界面.组件模块.主题色块 import ThemeColorBlock
        
        blocks_config = card_config.get("blocks_config", {})
        items = blocks_config.get("items", [])
        selected = config_manager.get_value(card_name, blocks_config.get("config_key"), blocks_config.get("selected"))
        supports_deselect = blocks_config.get("supports_deselect", False)
        
        def on_select(name: str):
            config_manager.set_value(card_name, blocks_config.get("config_key"), name)
        
        return UniversalCard.create(
            title=card_config.get("title", card_name),
            icon=card_config.get("icon", "PALETTE"),
            enabled=True,
            subtitle=card_config.get("subtitle", ""),
            controls=[
                ThemeColorBlock.create(
                    items=items,
                    selected=selected,
                    on_select=on_select,
                    supports_deselect=supports_deselect,
                )
            ],
            controls_per_row=card_config.get("controls_per_row", 4),
            width=card_width,
        )


# *** 调试逻辑 ***
if __name__ == "__main__":
    from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider
    
    配置 = 界面配置()
    ThemeProvider.initialize(配置)
    
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        page.add(SettingsContainer.create(
            config=配置,
            title="系统设置",
            icon="SETTINGS",
            card_names=["挂机模式", "指令速度"],
        ))
    
    ft.run(main)
