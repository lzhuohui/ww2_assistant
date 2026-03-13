# -*- coding: utf-8 -*-
"""
懒加载建筑卡片 - 组件层

设计思路:
    懒加载建筑卡片，点击后才加载实际控件。
    切换时销毁上一个卡片，保持内存低占用。

功能:
    1. 未加载状态：显示"📁 点击加载XX数据"
    2. 已加载状态：显示实际的建筑设置控件
    3. 点击时：保存上一个卡片 + 销毁上一个卡片 + 加载当前卡片

使用场景:
    被建筑设置页面调用。
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft
from typing import Callable, Dict, Any, Optional, List


class LazyBuildingCardManager:
    """懒加载建筑卡片管理器（单例）"""
    
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
        self.current_card_container: Optional[ft.Container] = None
        self.config_manager: Optional[Any] = None
        self.cards: Dict[str, 'LazyBuildingCard'] = {}
        self._initialized = True
    
    def register_card(self, card_name: str, card: 'LazyBuildingCard'):
        """注册卡片"""
        self.cards[card_name] = card
    
    def switch_to(self, card_name: str):
        """切换到指定卡片"""
        # 保存当前卡片数据
        if self.current_card_name and self.config_manager:
            self.config_manager.save_all()
        
        # 销毁当前卡片
        if self.current_card_name and self.current_card_name in self.cards:
            self.cards[self.current_card_name].destroy()
        
        # 加载新卡片
        if card_name in self.cards:
            self.cards[card_name].load()
            self.current_card_name = card_name
    
    def save_current(self):
        """保存当前卡片数据"""
        if self.current_card_name and self.config_manager:
            self.config_manager.save_all()


class LazyBuildingCard:
    """懒加载建筑卡片"""
    
    def __init__(
        self,
        config,
        card_name: str,
        card_config: Dict[str, Any],
        config_manager: Any,
        on_value_change: Callable[[str, Any], None] = None,
        is_default: bool = False,
    ):
        """
        初始化懒加载建筑卡片
        
        参数:
            config: 界面配置对象
            card_name: 卡片名称
            card_config: 卡片配置
            config_manager: 配置管理器
            on_value_change: 值变化回调
            is_default: 是否默认加载
        """
        self.config = config
        self.card_name = card_name
        self.card_config = card_config
        self.config_manager = config_manager
        self.on_value_change = on_value_change
        self.is_default = is_default
        
        self.is_loaded = False
        self.container: Optional[ft.Container] = None
        
        # 注册到管理器
        manager = LazyBuildingCardManager()
        manager.register_card(card_name, self)
        if is_default:
            manager.config_manager = config_manager
    
    def create(self) -> ft.Container:
        """创建卡片容器"""
        theme_colors = self.config.当前主题颜色
        
        # 创建容器
        self.container = ft.Container(
            bgcolor=theme_colors.get("bg_secondary"),
            border_radius=8,
            padding=ft.Padding.all(16),
            border=ft.Border.all(1, theme_colors.get("border")),
            on_click=self._on_click if not self.is_default else None,
        )
        
        # 如果是默认加载，直接设置内容
        if self.is_default:
            self.container.content = self._create_loaded_content()
            self.is_loaded = True
            # 更新管理器状态
            manager = LazyBuildingCardManager()
            manager.current_card_name = self.card_name
        else:
            self.container.content = self._create_unloaded_content()
        
        return self.container
    
    def _create_unloaded_content(self) -> ft.Control:
        """创建未加载状态的内容"""
        theme_colors = self.config.当前主题颜色
        
        return ft.Row(
            [
                ft.Icon(ft.Icons.FOLDER_OPEN, size=24, color=theme_colors.get("accent")),
                ft.Container(width=12),
                ft.Text(
                    f"点击加载 {self.card_name} 数据",
                    size=16,
                    color=theme_colors.get("text_primary"),
                ),
                ft.Container(expand=True),
                ft.Icon(ft.Icons.KEYBOARD_ARROW_RIGHT, size=20, color=theme_colors.get("text_secondary")),
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
    
    def _create_loaded_content(self) -> ft.Control:
        """创建已加载状态的内容"""
        from 新思路.零件层.控件工厂 import ControlFactory
        
        # 创建控件
        controls = ControlFactory.create_controls(
            config=self.config,
            card_config=self.card_config,
            config_manager=self.config_manager,
            on_value_change=self.on_value_change,
        )
        
        theme_colors = self.config.当前主题颜色
        
        # 获取卡片配置
        title = self.card_config.get("title", self.card_name)
        icon = self.card_config.get("icon", "DOMAIN")
        subtitle = self.card_config.get("subtitle")
        
        # 创建标题行
        title_row = ft.Row(
            [
                ft.Icon(getattr(ft.Icons, icon, ft.Icons.DOMAIN), size=20, color=theme_colors.get("accent")),
                ft.Container(width=8),
                ft.Text(title, size=16, weight=ft.FontWeight.BOLD, color=theme_colors.get("text_primary")),
            ],
            alignment=ft.MainAxisAlignment.START,
        )
        
        # 创建控件行
        controls_row = ft.Row(
            controls,
            alignment=ft.MainAxisAlignment.START,
            spacing=16,
            wrap=True,
        )
        
        # 创建内容
        content = ft.Column(
            [
                title_row,
                ft.Container(height=12),
                controls_row,
            ],
            spacing=0,
        )
        
        if subtitle:
            content.controls.insert(1, ft.Container(height=4))
            content.controls.insert(2, ft.Text(subtitle, size=12, color=theme_colors.get("text_secondary")))
        
        return content
    
    def _on_click(self, e):
        """点击卡片时"""
        if self.is_loaded:
            return
        
        # 通过管理器切换
        manager = LazyBuildingCardManager()
        manager.switch_to(self.card_name)
    
    def load(self):
        """加载卡片内容"""
        if self.is_loaded:
            return
        
        # 创建已加载内容
        content = self._create_loaded_content()
        
        # 更新容器
        self.container.content = content
        self.container.on_click = None  # 移除点击事件
        
        self.is_loaded = True
        
        # 更新管理器状态
        manager = LazyBuildingCardManager()
        manager.current_card_name = self.card_name
        
        # 更新界面
        if self.container.page:
            self.container.update()
    
    def destroy(self):
        """销毁卡片内容"""
        if not self.is_loaded:
            return
        
        # 清空内容
        self.container.content = self._create_unloaded_content()
        self.container.on_click = self._on_click  # 恢复点击事件
        
        self.is_loaded = False
        
        # 更新界面
        if self.container.page:
            self.container.update()


懒加载建筑卡片 = LazyBuildingCard
