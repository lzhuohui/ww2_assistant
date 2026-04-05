# -*- coding: utf-8 -*-

"""
模块名称：账号界面.py
模块功能：账号管理界面

职责：
- 管理账号卡片
- 响应配置变更
- 加载默认值
- 动态副标题显示账号状态

不负责：
- 数据存储
- 界面布局（由界面容器负责）
"""

import flet as ft
from typing import Callable, Dict, Any, List

from 前端.V3.层级0_数据管理.配置管理 import ConfigManager
from 前端.V3.层级3_功能卡片.功能卡片 import FunctionCard
from 前端.V3.层级3_功能卡片.界面容器 import InterfaceContainer


class AccountInterface:
    """账号界面 - V3版本"""
    
    INTERFACE_NAME = "账号界面"
    INTERFACE_TITLE = "账号管理"
    INTERFACE_HINT = "管理多个游戏账号信息"
    
    SUBTITLE_INCOMPLETE = "请完善账号信息"
    SUBTITLE_ACTIVE = "已完善账号信息"
    SUBTITLE_DISABLED = "账号已禁用"
    
    def __init__(self, page: ft.Page, config_manager: ConfigManager, on_scheme_change: Callable[[str], None] = None, on_start: Callable[[], None] = None):
        self._page = page
        self._config_manager = config_manager
        self._on_scheme_change = on_scheme_change
        self._on_start: Callable[[], None] = None
        self._on_start = on_start
        self._function_card = FunctionCard(page, config_manager)
        self._interface_container = InterfaceContainer(page, config_manager)
        self._cards: Dict[str, ft.Container] = {}
        self._container: ft.Container = None
        self._subtitle_text: ft.Text = None
    
    def build(self) -> ft.Container:
        """构建账号界面"""
        theme_colors = self._config_manager.get_theme_colors()
        
        card_names = self._config_manager.get_card_names(self.INTERFACE_NAME)
        
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
            
            self._update_card_subtitle(card_name)
        
        self._container = self._interface_container.create(
            title=self.INTERFACE_TITLE,
            hint=self.INTERFACE_HINT,
            cards=cards,
            on_scheme_change=self._on_scheme_change,
            on_load_defaults=self._on_load_defaults,
            on_start=self._on_start,
        )
        
        return self._container
    
    def _calculate_card_subtitle(self, card: str) -> str:
        """计算卡片副标题"""
        enabled = self._config_manager.get_enabled(self.INTERFACE_NAME, card)
        
        if not enabled:
            return self.SUBTITLE_DISABLED
        
        name = self._config_manager.get_raw_value(self.INTERFACE_NAME, card, "名称") or ""
        account = self._config_manager.get_raw_value(self.INTERFACE_NAME, card, "账号") or ""
        password = self._config_manager.get_raw_value(self.INTERFACE_NAME, card, "密码") or ""
        
        if not name or not account or not password:
            return self.SUBTITLE_INCOMPLETE
        
        return self.SUBTITLE_ACTIVE
    
    def _update_card_subtitle(self, card: str):
        """更新卡片副标题"""
        subtitle = self._calculate_card_subtitle(card)
        self._function_card.set_subtitle(self.INTERFACE_NAME, card, subtitle)
    
    def _on_change(self, interface: str, card: str, control_id: str, value: Any):
        """控件值变更回调"""
        if control_id in ["名称", "账号", "密码"]:
            self._update_card_subtitle(card)
    
    def _on_toggle(self, interface: str, card: str, enabled: bool):
        """开关状态变更回调"""
        self._update_card_subtitle(card)
    
    def _on_load_defaults(self):
        """加载默认值回调"""
        theme_colors = self._config_manager.get_theme_colors()
        
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
            
            self._update_card_subtitle(card_name)
        
        if self._container:
            main_column = self._container.content
            cards_column = main_column.controls[1]
            cards_column.controls = new_cards
            self._page.update()
    
    def destroy(self):
        """销毁界面（只清理界面级缓存，下拉框销毁由层级1负责）"""
        self._function_card.destroy()
        self._cards.clear()
        self._container = None
