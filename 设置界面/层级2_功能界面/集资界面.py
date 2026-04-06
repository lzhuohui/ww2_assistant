# -*- coding: utf-8 -*-

import flet as ft
from typing import Callable, Dict, Any, List

from 设置界面.层级0_数据管理.配置管理 import ConfigManager
from 设置界面.层级3_功能卡片.功能卡片 import FunctionCard
from 设置界面.层级3_功能卡片.界面容器 import InterfaceContainer
from 设置界面.层级5_基础模块.下拉框 import DropdownOptimized


class FundraiseInterface:
    """集资界面 - V3版本"""
    
    INTERFACE_NAME = "集资界面"
    INTERFACE_TITLE = "集资设置"
    INTERFACE_HINT = "点击卡片标题栏可启用/禁用功能"
    
    def __init__(self, page: ft.Page, config_manager: ConfigManager, on_scheme_change: Callable[[str], None] = None):
        self._page = page
        self._config_manager = config_manager
        self._on_scheme_change = on_scheme_change
        self._function_card = FunctionCard(page, config_manager)
        self._interface_container = InterfaceContainer(page, config_manager)
        self._cards: Dict[str, ft.Container] = {}
        self._container: ft.Container = None
        self._primary_commander: str = ""
    
    def build(self) -> ft.Container:
        theme_colors = self._config_manager.get_theme_colors()
        card_names = self._config_manager.get_card_names(self.INTERFACE_NAME)
        
        self._primary_commander = self._config_manager.get_raw_value(self.INTERFACE_NAME, "小号上贡", "主要统帅") or ""
        
        self._update_exclude_values()
        
        cards = []
        for card_name in card_names:
            card = self._function_card.create(
                interface=self.INTERFACE_NAME,
                card=card_name,
                on_change=self._on_change,
                on_toggle=self._on_toggle,
                theme_colors=theme_colors,
            )
            cards.append(card)
            self._cards[card_name] = card
        
        self._container = self._interface_container.create(
            title=self.INTERFACE_TITLE,
            hint=self.INTERFACE_HINT,
            cards=cards,
            on_scheme_change=self._on_scheme_change,
            on_load_defaults=self._on_load_defaults,
        )
        return self._container
    
    def _update_exclude_values(self):
        if self._primary_commander:
            self._config_manager.set_exclude_value(
                self.INTERFACE_NAME, "小号上贡", "主要统帅", [self._primary_commander]
            )
        else:
            self._config_manager.clear_exclude_value(
                self.INTERFACE_NAME, "小号上贡", "主要统帅"
            )
    
    def _on_change(self, interface: str, card: str, control_id: str, value: Any):
        if control_id == "主要统帅":
            if isinstance(value, dict):
                self._primary_commander = value.get("value", "")
            else:
                self._primary_commander = value
            self._update_exclude_values()
            self._refresh_card(card)
    
    def _refresh_card(self, card: str):
        if card in self._cards:
            DropdownOptimized.clear_dropdown_cache(self.INTERFACE_NAME, f"{card}.次要统帅")
            
            theme_colors = self._config_manager.get_theme_colors()
            new_card = self._function_card.create(
                interface=self.INTERFACE_NAME,
                card=card,
                on_change=self._on_change,
                on_toggle=self._on_toggle,
                theme_colors=theme_colors,
            )
            self._cards[card] = new_card
            
            if self._container:
                main_column = self._container.content
                cards_column = main_column.controls[1]
                for i, c in enumerate(cards_column.controls):
                    if hasattr(c, 'key') and c.key == f"{self.INTERFACE_NAME}.{card}":
                        cards_column.controls[i] = new_card
                        break
                self._page.update()
    
    def _on_toggle(self, interface: str, card: str, enabled: bool):
        self._refresh_card(card)
    
    def _on_load_defaults(self):
        theme_colors = self._config_manager.get_theme_colors()
        self._primary_commander = self._config_manager.get_default(self.INTERFACE_NAME, "小号上贡", "主要统帅") or ""
        
        self._update_exclude_values()
        
        card_names = self._config_manager.get_card_names(self.INTERFACE_NAME)
        new_cards = []
        for card_name in card_names:
            card = self._function_card.create(
                interface=self.INTERFACE_NAME,
                card=card_name,
                on_change=self._on_change,
                on_toggle=self._on_toggle,
                theme_colors=theme_colors,
                use_defaults=True,
            )
            new_cards.append(card)
            self._cards[card_name] = card
        if self._container:
            main_column = self._container.content
            cards_column = main_column.controls[1]
            cards_column.controls = new_cards
            self._page.update()
    
    def destroy(self):
        self._config_manager.clear_exclude_value(self.INTERFACE_NAME)
        self._function_card.destroy()
        self._cards.clear()
        self._container = None
