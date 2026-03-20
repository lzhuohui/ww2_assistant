# -*- coding: utf-8 -*-
"""
模块名称：懒加载UI渲染器 | 层级：组件模块层
设计思路：
    单一职责：渲染懒加载卡片的UI。
    分离未加载状态和已加载状态的渲染逻辑。

功能：
    1. 渲染未加载状态UI
    2. 渲染已加载状态UI
    3. 提供UI更新接口

对外接口：
    - render_lazy_state(): 渲染未加载状态
    - render_loaded_state(): 渲染已加载状态
"""

import flet as ft
from typing import Dict, Any, Callable, Optional, List
from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider
from 前端.用户设置界面.单元模块.卡片容器 import CardContainer
from 前端.用户设置界面.组件模块.图标标题 import IconTitle
from 前端.用户设置界面.组件模块.通用卡片 import UniversalCard
from 前端.用户设置界面.组件模块.懒加载资源加载器 import LazyLoader
from 前端.用户设置界面.配置.界面配置 import 界面配置


LAZY_HEIGHT = 60
DEFAULT_CONTROL_MARGIN_RIGHT = 20


class LazyRenderer:
    """懒加载UI渲染器 - 负责渲染懒加载卡片的UI"""
    
    @staticmethod
    def render_lazy_state(
        card_config: Dict[str, Any],
        enabled: bool = True,
        on_state_change: Callable[[bool], None] = None,
    ) -> Dict[str, Any]:
        """
        渲染未加载状态
        
        参数:
            card_config: 卡片配置
            enabled: 是否启用
            on_state_change: 状态变化回调
        
        返回:
            包含container和hint_controls的字典
        """
        配置 = 界面配置()
        theme_colors = 配置.当前主题颜色
        ui_config = 配置.定义尺寸.get("界面", {})
        card_padding = ui_config.get("card_padding", 16)
        card_width = LazyRenderer._get_card_width()
        
        title = card_config.get("title", "")
        icon = card_config.get("icon", "DOMAIN")
        subtitle = card_config.get("subtitle")
        
        icon_title = IconTitle.create(
            title=title,
            icon=icon,
            enabled=enabled,
            on_state_change=on_state_change,
            subtitle=subtitle,
            divider_height=LAZY_HEIGHT,
        )
        
        left_container = ft.Container(content=icon_title)
        
        lazy_hint_icon = ft.Icon(
            ft.Icons.FOLDER_OPEN,
            size=18,
            color=theme_colors.get("text_secondary"),
        )
        lazy_hint_text = ft.Text(
            "点击加载数据",
            size=14,
            color=theme_colors.get("text_secondary"),
        )
        
        if not enabled:
            lazy_hint_icon.opacity = 0.4
            lazy_hint_text.opacity = 0.4
        
        lazy_hint = ft.Row(
            [lazy_hint_icon, ft.Container(width=8), lazy_hint_text],
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
            height=LAZY_HEIGHT,
            width=card_width,
            clip_behavior=ft.ClipBehavior.NONE,
        )
        
        container = CardContainer.create(
            config=配置,
            content=main_stack,
            height=LAZY_HEIGHT,
            width=card_width,
        )
        
        return {
            "container": container,
            "hint_controls": {
                "icon": lazy_hint_icon,
                "text": lazy_hint_text,
            },
            "icon_title": icon_title,
        }
    
    @staticmethod
    def render_loaded_state(
        card_config: Dict[str, Any],
        card_name: str,
        config_manager: Any = None,
        on_value_change: Callable[[str, Any], None] = None,
    ) -> ft.Container:
        """
        渲染已加载状态
        
        参数:
            card_config: 卡片配置
            card_name: 卡片名称
            config_manager: 配置管理器
            on_value_change: 值变化回调
        
        返回:
            已加载状态的容器
        """
        title = card_config.get("title", card_name)
        icon = card_config.get("icon", "DOMAIN")
        subtitle = card_config.get("subtitle")
        enabled = card_config.get("enabled", True)
        controls_per_row = card_config.get("controls_per_row", 1)
        controls_config = card_config.get("controls", [])
        
        controls = LazyLoader.create_controls(
            controls_config=controls_config,
            card_name=card_name,
            config_manager=config_manager,
            on_value_change=on_value_change,
        )
        
        container = UniversalCard.create(
            title=title,
            icon=icon,
            enabled=enabled,
            subtitle=subtitle,
            controls=controls,
            controls_per_row=controls_per_row,
        )
        
        return container
    
    @staticmethod
    def update_hint_state(
        hint_controls: Dict[str, ft.Control],
        enabled: bool,
    ):
        """
        更新提示控件状态
        
        参数:
            hint_controls: 提示控件字典
            enabled: 是否启用
        """
        opacity = 1.0 if enabled else 0.4
        for control in hint_controls.values():
            if control:
                control.opacity = opacity
                try:
                    if control.page:
                        control.update()
                except RuntimeError:
                    pass
    
    @staticmethod
    def _get_card_width() -> int:
        """计算卡片宽度"""
        配置 = 界面配置()
        ui_config = 配置.定义尺寸.get("界面", {})
        window_width = ui_config.get("window_width", 1200)
        left_panel_width = ui_config.get("left_panel_width", 280)
        page_padding = ui_config.get("page_padding", 10)
        return window_width - left_panel_width - 20 - page_padding * 2


懒加载渲染器 = LazyRenderer
