# -*- coding: utf-8 -*-
"""
模块名称：CardGroupManager
模块功能：卡片组管理器，统一管理卡片展开/折叠行为
实现步骤：
- 管理卡片列表
- 支持不同销毁策略
- 自动折叠其他卡片
"""

import flet as ft
from typing import Callable, Dict, Any, List, Optional
from enum import Enum

from 前端.游戏设置界面.核心层.配置.界面配置 import UIConfig


class DestroyStrategy(Enum):
    """销毁策略枚举"""
    NONE = "none"
    UNLOAD_OPTIONS = "unload_options"
    DESTROY_CONTROLS = "destroy_controls"


class CardGroupManager:
    """卡片组管理器 - 统一管理卡片的展开/折叠行为"""
    
    def __init__(self, destroy_strategy: str = "unload_options"):
        self.cards: List[ft.Container] = []
        self.card_callbacks: Dict[ft.Container, Dict[str, Callable]] = {}
        self.current_expanded_card: Optional[ft.Container] = None
        self.destroy_strategy = DestroyStrategy(destroy_strategy)
    
    def add_card(
        self,
        card: ft.Container,
        on_expand: Callable[[], None] = None,
        on_collapse: Callable[[], None] = None,
    ) -> None:
        self.cards.append(card)
        self.card_callbacks[card] = {
            "on_expand": on_expand,
            "on_collapse": on_collapse,
        }
    
    def _execute_destroy_strategy(self, card: ft.Container) -> None:
        if not card or not hasattr(card, 'is_loaded'):
            return
        
        if not card.is_loaded():
            return
        
        if self.destroy_strategy == DestroyStrategy.NONE:
            return
        
        if self.destroy_strategy == DestroyStrategy.UNLOAD_OPTIONS:
            if hasattr(card, 'unload_options_only'):
                card.unload_options_only()
        
        if self.destroy_strategy == DestroyStrategy.DESTROY_CONTROLS:
            if hasattr(card, 'destroy_controls'):
                card.destroy_controls()
    
    def expand_card(self, card: ft.Container) -> None:
        if self.current_expanded_card and self.current_expanded_card != card:
            self._execute_destroy_strategy(self.current_expanded_card)
            old_callbacks = self.card_callbacks.get(self.current_expanded_card, {})
            if old_callbacks.get("on_collapse"):
                old_callbacks["on_collapse"]()
        
        self.current_expanded_card = card
        
        callbacks = self.card_callbacks.get(card, {})
        if callbacks.get("on_expand"):
            callbacks["on_expand"]()
    
    def collapse_all(self) -> None:
        for card in self.cards:
            if hasattr(card, 'is_loaded') and card.is_loaded():
                self._execute_destroy_strategy(card)
                callbacks = self.card_callbacks.get(card, {})
                if callbacks.get("on_collapse"):
                    callbacks["on_collapse"]()
        
        self.current_expanded_card = None
    
    def get_current_expanded_card(self) -> Optional[ft.Container]:
        return self.current_expanded_card
    
    def is_card_expanded(self, card: ft.Container) -> bool:
        return self.current_expanded_card == card
    
    def get_all_cards(self) -> List[ft.Container]:
        return self.cards.copy()
    
    def clear(self) -> None:
        self.collapse_all()
        self.cards.clear()
        self.card_callbacks.clear()
        self.current_expanded_card = None


def create_managed_card(
    manager: CardGroupManager,
    title: str,
    icon: str,
    subtitle: str,
    enabled: bool = True,
    controls: List[ft.Control] = None,
    controls_config: List[Dict[str, Any]] = None,
    controls_per_row: int = 6,
    width: int = None,
    on_value_change: Callable[[str, Any], None] = None,
    on_save: Callable[[str, str], None] = None,
    on_expand: Callable[[], None] = None,
    on_collapse: Callable[[], None] = None,
    config: UIConfig = None,
) -> ft.Container:
    from 前端.游戏设置界面.表示层.组件.复合.折叠卡片 import CollapsibleCard
    
    def handle_expand():
        manager.expand_card(card)
        if on_expand:
            on_expand()
    
    card = CollapsibleCard.create(
        title=title,
        icon=icon,
        subtitle=subtitle,
        enabled=enabled,
        controls=controls,
        controls_config=controls_config,
        controls_per_row=controls_per_row,
        width=width,
        on_value_change=on_value_change,
        on_save=on_save,
        on_expand=handle_expand,
        on_collapse=on_collapse,
        config=config,
    )
    
    manager.add_card(card, on_expand=on_expand, on_collapse=on_collapse)
    
    return card


# *** 标准测试格式: 仅调用被测模块,AI不得添加数据 ***
if __name__ == "__main__":
    def main(page: ft.Page):
        config = UIConfig()
        manager = CardGroupManager(destroy_strategy="unload_options")
        
        card1 = create_managed_card(
            manager=manager,
            title="测试卡片1",
            icon="SETTINGS",
            subtitle="这是测试卡片1",
            config=config,
        )
        
        card2 = create_managed_card(
            manager=manager,
            title="测试卡片2",
            icon="ACCOUNT",
            subtitle="这是测试卡片2",
            config=config,
        )
        
        page.add(ft.Column([card1, card2], spacing=10))
    
    ft.app(target=main)
