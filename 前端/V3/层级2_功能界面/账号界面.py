# -*- coding: utf-8 -*-

"""
模块名称：账号界面.py
模块功能：账号管理界面

职责：
- 管理账号卡片
- 界面布局
- 响应配置变更

不负责：
- 数据存储
"""

import flet as ft
from typing import Callable, Dict, Any, List

from 前端.V3.层级0_数据管理.配置管理 import ConfigManager
from 前端.V3.层级3_功能卡片.功能卡片 import FunctionCard

# ============================================
# 公开接口
# ============================================

class AccountInterface:
    """
    账号界面 - V3版本
    
    职责：
    - 管理账号卡片
    - 界面布局
    - 响应配置变更
    
    不负责：
    - 数据存储
    """
    
    INTERFACE_NAME = "账号界面"
    INTERFACE_TITLE = "账号管理"
    INTERFACE_HINT = "配置账号信息后点击标题栏启用"
    
    def __init__(self, page: ft.Page, config_manager: ConfigManager):
        self._page = page
        self._config_manager = config_manager
        self._function_card = FunctionCard(page, config_manager)
        self._cards: Dict[str, ft.Container] = {}
        self._container: ft.Container = None
    
    def build(self) -> ft.Container:
        """构建账号界面"""
        theme_colors = self._config_manager.get_theme_colors()
        
        title_row = self._create_title_row(theme_colors)
        
        card_names = self._config_manager.get_card_names(self.INTERFACE_NAME)
        
        card_spacing = self._config_manager.get_ui_size("边距", "卡片间距")
        
        cards_column = ft.Column(
            spacing=card_spacing,
            scroll=ft.ScrollMode.HIDDEN,
            expand=True,
        )
        
        for card_name in card_names:
            card = self._function_card.create(
                interface=self.INTERFACE_NAME,
                card=card_name,
                on_change=self._on_change,
                on_toggle=self._on_toggle,
                theme_colors=theme_colors,
            )
            cards_column.controls.append(card)
            self._cards[card_name] = card
        
        title_spacing = self._config_manager.get_ui_size("边距", "卡片间距")
        
        main_column = ft.Column(
            controls=[title_row, cards_column],
            spacing=title_spacing,
            expand=True,
        )
        
        bg_primary = theme_colors.get("bg_primary", "#202020")
        
        padding = self._config_manager.get_ui_size("边距", "界面内边距")
        
        self._container = ft.Container(
            content=main_column,
            bgcolor=bg_primary,
            padding=padding,
            expand=True,
            alignment=ft.Alignment(-1, -1),
        )
        
        return self._container
    
    def _create_title_row(self, theme_colors: Dict[str, str]) -> ft.Row:
        """创建标题行"""
        text_primary = theme_colors.get("text_primary", "#FFFFFF")
        text_secondary = theme_colors.get("text_secondary", "#B0B0B0")
        
        title = ft.Text(
            value=self.INTERFACE_TITLE,
            size=24,
            weight=ft.FontWeight.BOLD,
            color=text_primary,
        )
        
        hint = ft.Text(
            value=self.INTERFACE_HINT,
            size=12,
            color=text_secondary,
        )
        
        return ft.Row(
            controls=[title, ft.VerticalDivider(width=1, color=text_secondary), hint],
            vertical_alignment=ft.CrossAxisAlignment.END,
            spacing=12,
        )
    
    def _on_change(self, interface: str, card: str, control_id: str, value: Any):
        """控件值变更回调"""
        pass
    
    def _on_toggle(self, interface: str, card: str, enabled: bool):
        """开关状态变更回调"""
        if card in self._cards:
            theme_colors = self._config_manager.get_theme_colors()
            new_card = self._function_card.create(
                interface=interface,
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
                    if hasattr(c, 'key') and c.key == f"{interface}.{card}":
                        cards_column.controls[i] = new_card
                        break
                self._page.update()
    
    def destroy(self):
        """销毁界面（只清理界面级缓存，下拉框销毁由层级1负责）"""
        self._cards.clear()
        self._container = None
