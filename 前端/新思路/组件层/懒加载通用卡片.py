# -*- coding: utf-8 -*-
"""
懒加载通用卡片 - 组件层

设计思路:
    未加载时：左侧图标+标题+分割线，右侧显示"点击加载数据"
    加载后：直接调用通用卡片显示控件

功能:
    1. 未加载状态：左侧与通用卡片一致，右侧显示"点击加载数据"
    2. 已加载状态：调用通用卡片显示控件
    3. 点击时：保存上一个卡片 + 销毁上一个卡片 + 加载当前卡片

使用场景:
    被建筑设置页面调用。
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft
from typing import Callable, Dict, Any, Optional, List

DEFAULT_CONTROL_MARGIN_RIGHT = 20


class LazyCardManager:
    """懒加载卡片管理器（单例）"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self.current_card_name: Optional[str] = None
        self.config_manager: Optional[Any] = None
        self.cards: Dict[str, 'LazyUniversalCard'] = {}
        self._initialized = True
    
    def register_card(self, card_name: str, card: 'LazyUniversalCard'):
        """注册卡片"""
        self.cards[card_name] = card
    
    def switch_to(self, card_name: str):
        """切换到指定卡片"""
        if self.current_card_name and self.config_manager:
            self.config_manager.save_all()
        
        if self.current_card_name and self.current_card_name in self.cards:
            self.cards[self.current_card_name].destroy()
        
        if card_name in self.cards:
            self.cards[card_name].load()
            self.current_card_name = card_name
    
    def save_current(self):
        """保存当前卡片数据"""
        if self.current_card_name and self.config_manager:
            self.config_manager.save_all()


class LazyUniversalCard:
    """懒加载通用卡片"""
    
    def __init__(
        self,
        config,
        card_name: str,
        card_config: Dict[str, Any],
        config_manager: Any,
        on_value_change: Callable[[str, Any], None] = None,
        is_default: bool = False,
    ):
        self.config = config
        self.card_name = card_name
        self.card_config = card_config
        self.config_manager = config_manager
        self.on_value_change = on_value_change
        self.is_default = is_default
        
        self.is_loaded = False
        self.container: Optional[ft.Container] = None
        self.current_enabled = True
        
        manager = LazyCardManager()
        manager.register_card(card_name, self)
        if is_default:
            manager.config_manager = config_manager
    
    def create(self) -> ft.Container:
        """创建卡片容器"""
        from 新思路.零件层.卡片容器 import CardContainer
        from 新思路.零件层.图标标题 import IconTitle
        
        theme_colors = self.config.当前主题颜色
        ui_config = self.config.定义尺寸.get("界面", {})
        card_padding = ui_config.get("card_padding", 16)
        
        window_width = ui_config.get("window_width", 1200)
        left_panel_width = ui_config.get("left_panel_width", 280)
        page_padding = ui_config.get("page_padding", 10)
        card_width = window_width - left_panel_width - page_padding * 3
        
        title = self.card_config.get("title", self.card_name)
        icon = self.card_config.get("icon", "DOMAIN")
        subtitle = self.card_config.get("subtitle")
        
        if self.is_default:
            self.container = self._create_loaded_container()
            self.is_loaded = True
            manager = LazyCardManager()
            manager.current_card_name = self.card_name
        else:
            lazy_height = 60
            
            def on_state_change(new_enabled: bool):
                self.current_enabled = new_enabled
                self._sync_lazy_hint_state(new_enabled)
            
            icon_title = IconTitle.create(
                config=self.config,
                title=title,
                icon=icon,
                enabled=self.current_enabled,
                on_state_change=on_state_change,
                subtitle=subtitle,
                divider_height=lazy_height,
            )
            
            left_container = ft.Container(content=icon_title)
            
            self.lazy_hint_icon = ft.Icon(ft.Icons.FOLDER_OPEN, size=18, color=theme_colors.get("text_secondary"))
            self.lazy_hint_text = ft.Text("点击加载数据", size=14, color=theme_colors.get("text_secondary"))
            
            lazy_hint = ft.Row(
                [
                    self.lazy_hint_icon,
                    ft.Container(width=8),
                    self.lazy_hint_text,
                ],
                alignment=ft.MainAxisAlignment.END,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            )
            
            right_container = ft.Container(
                content=lazy_hint,
                right=DEFAULT_CONTROL_MARGIN_RIGHT,
                top=card_padding,
            )
            
            main_stack = ft.Stack(
                [left_container, right_container],
                height=lazy_height,
                width=card_width,
                clip_behavior=ft.ClipBehavior.NONE,
            )
            
            self.container = CardContainer.create(
                config=self.config,
                content=main_stack,
                height=lazy_height,
                width=card_width,
            )
            self.container.on_click = self._on_click
            self.icon_title = icon_title
        
        return self.container
    
    def _sync_lazy_hint_state(self, enabled: bool):
        """同步懒加载提示的状态"""
        if hasattr(self, 'lazy_hint_icon') and self.lazy_hint_icon:
            self.lazy_hint_icon.opacity = 1.0 if enabled else 0.4
            try:
                if self.lazy_hint_icon.page:
                    self.lazy_hint_icon.update()
            except RuntimeError:
                pass
        
        if hasattr(self, 'lazy_hint_text') and self.lazy_hint_text:
            self.lazy_hint_text.opacity = 1.0 if enabled else 0.4
            try:
                if self.lazy_hint_text.page:
                    self.lazy_hint_text.update()
            except RuntimeError:
                pass
    
    def _create_loaded_container(self) -> ft.Container:
        """创建已加载状态的容器 - 直接调用通用卡片"""
        from 新思路.组件层.通用卡片 import UniversalCard
        
        container = UniversalCard.create_from_config(
            config=self.config,
            card_name=self.card_name,
            config_manager=self.config_manager,
            on_value_change=self.on_value_change,
        )
        
        self.icon_title = container
        
        return container
    
    def _on_click(self, e):
        """点击卡片时"""
        if self.is_loaded:
            return
        
        if not self.current_enabled:
            return
        
        manager = LazyCardManager()
        manager.switch_to(self.card_name)
    
    def load(self):
        """加载卡片内容"""
        if self.is_loaded:
            return
        
        new_container = self._create_loaded_container()
        
        self.container.content = new_container.content
        self.container.on_click = None
        self.container.height = new_container.height
        
        self.is_loaded = True
        
        manager = LazyCardManager()
        manager.current_card_name = self.card_name
        
        try:
            if self.container.page:
                self.container.update()
        except RuntimeError:
            pass
    
    def destroy(self):
        """销毁卡片内容"""
        if not self.is_loaded:
            return
        
        from 新思路.零件层.图标标题 import IconTitle
        
        theme_colors = self.config.当前主题颜色
        ui_config = self.config.定义尺寸.get("界面", {})
        card_padding = ui_config.get("card_padding", 16)
        
        window_width = ui_config.get("window_width", 1200)
        left_panel_width = ui_config.get("left_panel_width", 280)
        page_padding = ui_config.get("page_padding", 10)
        card_width = window_width - left_panel_width - page_padding * 3
        
        title = self.card_config.get("title", self.card_name)
        icon = self.card_config.get("icon", "DOMAIN")
        subtitle = self.card_config.get("subtitle")
        
        lazy_height = 60
        
        icon_title = IconTitle.create(
            config=self.config,
            title=title,
            icon=icon,
            enabled=True,
            on_state_change=None,
            subtitle=subtitle,
            divider_height=lazy_height,
        )
        
        left_container = ft.Container(content=icon_title)
        
        lazy_hint = ft.Row(
            [
                ft.Icon(ft.Icons.FOLDER_OPEN, size=18, color=theme_colors.get("text_secondary")),
                ft.Container(width=8),
                ft.Text("点击加载数据", size=14, color=theme_colors.get("text_secondary")),
            ],
            alignment=ft.MainAxisAlignment.END,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        
        right_container = ft.Container(
            content=lazy_hint,
            right=DEFAULT_CONTROL_MARGIN_RIGHT,
            top=card_padding,
        )
        
        main_stack = ft.Stack(
            [left_container, right_container],
            height=lazy_height,
            width=card_width,
            clip_behavior=ft.ClipBehavior.NONE,
        )
        
        self.container.content = main_stack
        self.container.on_click = self._on_click
        self.container.height = lazy_height
        
        self.is_loaded = False
        
        try:
            if self.container.page:
                self.container.update()
        except RuntimeError:
            pass


懒加载通用卡片 = LazyUniversalCard
