# -*- coding: utf-8 -*-
"""
模块名称：CardGroupManager
设计思路: 统一管理卡片组的展开/折叠行为，支持不同的销毁策略
模块隔离: 复合组件，依赖折叠卡片组件

销毁策略:
    - NONE: 不销毁（个性化界面、账号界面）
    - UNLOAD_OPTIONS: 只卸载选项（系统界面、策略界面）
    - DESTROY_CONTROLS: 销毁控件（预留）

使用方式:
    manager = CardGroupManager(destroy_strategy="unload_options")
    manager.add_card(card, on_expand=callback, on_collapse=callback)
    manager.expand_card(card)  # 自动折叠其他卡片
"""

import flet as ft
from typing import Callable, Dict, Any, List, Optional
from enum import Enum


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
    config = None,
) -> ft.Container:
    from 前端.新界面_v2.表示层.组件.复合.折叠卡片 import CollapsibleCard
    
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


if __name__ == "__main__":
    import flet as ft
    from 前端.新界面_v2.核心.配置.界面配置 import UIConfig
    
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
