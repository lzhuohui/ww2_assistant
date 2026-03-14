# -*- coding: utf-8 -*-
"""
信息卡片 - 组件层

设计思路:
    专门用于展示静态信息，保持与通用卡片一致的视觉风格。
    不需要开关和控件功能，支持自定义内容。

功能:
    1. 标题+图标
    2. 自定义内容区域
    3. 悬停效果（阴影增强）
    4. 与通用卡片视觉一致

使用场景:
    被关于设置页面调用。
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft
from typing import Optional
from 配置.界面配置 import 界面配置


class InfoCard:
    """信息卡片 - 展示静态信息，视觉风格与通用卡片一致"""
    
    @staticmethod
    def create(
        config: 界面配置,
        title: str,
        icon: str = None,
        content: ft.Control = None,
        width: int = None,
    ) -> ft.Container:
        """
        创建信息卡片
        
        参数:
            config: 界面配置对象
            title: 卡片标题
            icon: 图标名称（可选）
            content: 自定义内容控件
            width: 卡片宽度（可选，默认自适应）
        
        返回:
            ft.Container: 信息卡片容器
        """
        theme_colors = config.当前主题颜色
        ui_config = config.定义尺寸.get("界面", {})
        
        shadow_config = config.定义尺寸.get("阴影", {})
        shadow_blur_default = shadow_config.get("blur_default", 4)
        shadow_blur_hover = shadow_config.get("blur_hover", 12)
        shadow_spread = shadow_config.get("spread", 0)
        shadow_spread_hover = shadow_config.get("spread_hover", 0)
        shadow_offset_y = shadow_config.get("offset_y", 2)
        shadow_offset_y_hover = shadow_config.get("offset_y_hover", 4)
        
        animation_config = config.定义尺寸.get("动画", {})
        animation_duration = animation_config.get("duration_fast", 150)
        animation_curve = getattr(ft.AnimationCurve, animation_config.get("curve", "EASE_OUT"), ft.AnimationCurve.EASE_OUT)
        
        card_border_radius = ui_config.get("card_radius", 8)
        card_border_width = ui_config.get("card_border_width", 1)
        
        window_width = ui_config.get("window_width", 1200)
        left_panel_width = ui_config.get("left_panel_width", 280)
        page_padding = ui_config.get("page_padding", 10)
        card_width = width if width else (window_width - left_panel_width - 20 - page_padding * 2)
        
        icon_map = {
            "INFO": ft.Icons.INFO,
            "CONTACTS": ft.Icons.CONTACTS,
            "WARNING_AMBER": ft.Icons.WARNING_AMBER,
            "PAYMENT": ft.Icons.PAYMENT,
        }
        
        icon_widget = None
        if icon:
            icon_widget = ft.Icon(
                icon_map.get(icon, ft.Icons.INFO),
                color=theme_colors.get("accent"),
                size=24,
            )
        
        title_row = ft.Row(
            [
                icon_widget,
                ft.Text(
                    title,
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color=theme_colors.get("text_primary"),
                ),
            ] if icon_widget else [
                ft.Text(
                    title,
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color=theme_colors.get("text_primary"),
                ),
            ],
            spacing=10,
        )
        
        card_content = ft.Column(
            [
                title_row,
                ft.Container(height=10),
                content,
            ] if content else [title_row],
            spacing=5,
        )
        
        container = ft.Container(
            content=card_content,
            width=card_width,
            padding=ft.Padding.all(16),
            bgcolor=theme_colors.get("bg_card"),
            border_radius=card_border_radius,
            border=ft.Border.all(card_border_width, theme_colors.get("border_light")) if card_border_width > 0 else None,
            shadow=ft.BoxShadow(
                spread_radius=shadow_spread,
                blur_radius=shadow_blur_default,
                color=theme_colors.get("shadow"),
                offset=ft.Offset(0, shadow_offset_y),
            ) if shadow_blur_default > 0 else None,
            animate=ft.Animation(animation_duration, animation_curve),
        )
        
        def on_hover(e):
            if e.data == "true":
                container.bgcolor = theme_colors.get("bg_hover")
                container.border = ft.Border.all(card_border_width, theme_colors.get("border")) if card_border_width > 0 else None
                container.shadow = ft.BoxShadow(
                    spread_radius=shadow_spread_hover,
                    blur_radius=shadow_blur_hover,
                    color=theme_colors.get("shadow"),
                    offset=ft.Offset(0, shadow_offset_y_hover),
                ) if shadow_blur_default > 0 else None
            else:
                container.bgcolor = theme_colors.get("bg_card")
                container.border = ft.Border.all(card_border_width, theme_colors.get("border_light")) if card_border_width > 0 else None
                container.shadow = ft.BoxShadow(
                    spread_radius=shadow_spread,
                    blur_radius=shadow_blur_default,
                    color=theme_colors.get("shadow"),
                    offset=ft.Offset(0, shadow_offset_y),
                ) if shadow_blur_default > 0 else None
            container.update()
        
        container.on_hover = on_hover
        
        return container


信息卡片 = InfoCard
