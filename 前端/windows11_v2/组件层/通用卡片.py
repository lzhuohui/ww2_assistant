# -*- coding: utf-8 -*-
"""
通用卡片 - 组件层

设计思路:
    最小模块化的卡片容器，只包含左侧布局。
    - 容器：外轮廓+悬浮内轮廓阴影
    - 左侧：图标+标题（上下排列居中）+?标签（上对齐）+分割线
    - 右侧：空着，由扩展卡片模块填充

功能:
    1. 容器：统一的边距、阴影、圆角、边框
    2. 左侧：图标+标题+帮助标签+分割线
    3. 状态切换：单击左侧区域切换启用/禁用状态
    4. 悬停效果：统一的悬停视觉反馈

数据来源:
    所有配置数据从界面配置获取。

使用场景:
    被扩展卡片模块调用，不直接使用。

可独立运行调试: python 通用卡片.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import flet as ft
from typing import Callable, Optional
from 原子层.界面配置 import 界面配置


class UniversalCard:
    """通用卡片 - 最小模块化的卡片容器"""
    
    @staticmethod
    def create(
        config: 界面配置,
        title: str,
        icon: str = None,
        enabled: bool = True,
        on_state_change: Callable[[bool], None] = None,
        help_text: str = None,
        height: int = None,
        width: int = None,
        **kwargs
    ) -> ft.Container:
        theme_colors = config.当前主题颜色
        
        weight_config = config.定义尺寸.get("字重", {})
        spacing_config = config.定义尺寸.get("间距", {})
        ui_config = config.定义尺寸.get("界面", {})
        card_config = config.定义尺寸.get("卡片", {})
        multirow_config = config.定义尺寸.get("多行卡片", {})
        shadow_config = config.定义尺寸.get("阴影", {})
        
        default_icon_size = card_config.get("icon_size", 24)
        default_title_size = card_config.get("title_size", 14)
        
        divider_width = multirow_config.get("divider_width", 2)
        divider_height = multirow_config.get("divider_height", 60)
        divider_opacity = multirow_config.get("divider_opacity", 0.7)
        divider_blur = multirow_config.get("divider_blur", 6)
        left_width = multirow_config.get("left_width", 60)
        divider_left = multirow_config.get("divider_left", 90)
        
        shadow_blur_default = shadow_config.get("blur_default", 4)
        shadow_blur_hover = shadow_config.get("blur_hover", 8)
        shadow_spread = shadow_config.get("spread", 0)
        shadow_offset_y = shadow_config.get("offset_y", 2)
        shadow_offset_y_hover = shadow_config.get("offset_y_hover", 3)
        
        card_border_radius = ui_config.get("card_radius", 8)
        card_border_width = ui_config.get("card_border_width", 1)
        card_padding = ui_config.get("card_padding", 16)
        
        current_enabled = enabled
        
        card_height = height or card_config.get("default_height", 70)
        card_width = width or 800
        
        icon_value = None
        if icon:
            if isinstance(icon, str):
                icon_name = icon.upper()
                icon_value = getattr(ft.Icons, icon_name, ft.Icons.SETTINGS)
            else:
                icon_value = icon
        
        icon_control = None
        if icon_value:
            icon_control = ft.Icon(
                icon_value,
                size=default_icon_size,
                color=theme_colors.get("accent"),
                opacity=1.0 if current_enabled else 0.4,
            )
        
        title_control = ft.Text(
            title,
            size=default_title_size,
            weight=weight_config.get("font_weight_medium", ft.FontWeight.W_500),
            color=theme_colors.get("text_primary"),
            opacity=1.0 if current_enabled else 0.4,
        )
        
        help_icon = None
        if help_text:
            help_icon = ft.IconButton(
                icon=ft.Icons.HELP_OUTLINE,
                icon_size=14,
                icon_color=theme_colors.get("text_secondary"),
                tooltip=help_text,
                opacity=0.7 if current_enabled else 0.3,
                style=ft.ButtonStyle(padding=0),
            )
        
        left_column_items = []
        if help_icon:
            left_column_items.append(help_icon)
        if icon_control:
            left_column_items.append(icon_control)
        left_column_items.append(title_control)
        
        left_content = ft.Column(
            left_column_items,
            spacing=spacing_config.get("spacing_xs", 4),
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        )
        
        left_container = ft.Container(
            content=left_content,
            left=card_padding,
            top=0,
            bottom=0,
            width=left_width,
            alignment=ft.Alignment(0, 0),
            on_click=lambda e: toggle_state(e),
        )
        
        divider = ft.Container(
            width=divider_width,
            height=divider_height,
            bgcolor=theme_colors.get("accent"),
            opacity=divider_opacity if current_enabled else 0.2,
            shadow=ft.BoxShadow(
                blur_radius=divider_blur,
                color=theme_colors.get("accent"),
                spread_radius=0,
            ) if current_enabled else None,
            left=divider_left,
            top=0,
            bottom=0,
        )
        
        stack_children = [
            left_container,
            divider,
        ]
        
        main_stack = ft.Stack(
            stack_children,
            height=card_height,
            width=card_width,
            clip_behavior=ft.ClipBehavior.NONE,
        )
        
        container = ft.Container(
            content=main_stack,
            bgcolor=theme_colors.get("bg_card"),
            border_radius=card_border_radius,
            border=ft.Border.all(card_border_width, theme_colors.get("border_light")),
            shadow=ft.BoxShadow(
                spread_radius=shadow_spread,
                blur_radius=shadow_blur_default,
                color=theme_colors.get("shadow"),
                offset=ft.Offset(0, shadow_offset_y),
            ),
            animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
            clip_behavior=ft.ClipBehavior.NONE,
        )
        
        def toggle_state(e):
            nonlocal current_enabled
            current_enabled = not current_enabled
            
            if icon_control:
                icon_control.opacity = 1.0 if current_enabled else 0.4
                icon_control.update()
            title_control.opacity = 1.0 if current_enabled else 0.4
            title_control.update()
            
            if help_icon:
                help_icon.opacity = 0.7 if current_enabled else 0.3
                help_icon.update()
            
            if divider:
                divider.opacity = divider_opacity if current_enabled else 0.2
                divider.update()
            
            if on_state_change:
                on_state_change(current_enabled)
        
        def on_hover(e):
            if e.data == "true":
                container.bgcolor = theme_colors.get("bg_hover")
                container.border = ft.Border.all(card_border_width, theme_colors.get("border"))
                container.shadow = ft.BoxShadow(
                    spread_radius=shadow_spread,
                    blur_radius=shadow_blur_hover,
                    color=theme_colors.get("shadow"),
                    offset=ft.Offset(0, shadow_offset_y_hover),
                )
            else:
                container.bgcolor = theme_colors.get("bg_card")
                container.border = ft.Border.all(card_border_width, theme_colors.get("border_light"))
                container.shadow = ft.BoxShadow(
                    spread_radius=shadow_spread,
                    blur_radius=shadow_blur_default,
                    color=theme_colors.get("shadow"),
                    offset=ft.Offset(0, shadow_offset_y),
                )
            container.update()
        
        container.on_hover = on_hover
        
        return container


# 兼容别名
通用卡片 = UniversalCard


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    config = 界面配置()
    
    def main(page: ft.Page):
        page.padding = 20
        page.bgcolor = config.获取颜色("bg_primary")
        
        page.add(ft.Text("通用卡片测试（最小模块化）:", color=config.获取颜色("text_secondary")))
        page.add(ft.Divider(height=20, color="transparent"))
        
        def on_state_change(enabled):
            print(f"状态变化: {'启用' if enabled else '禁用'}")
        
        page.add(UniversalCard.create(
            config=config,
            title="测试卡片",
            icon="HOME",
            enabled=True,
            on_state_change=on_state_change,
            help_text="点击切换启用/禁用状态",
        ))
        
        page.add(ft.Divider(height=20, color="transparent"))
        
        page.add(UniversalCard.create(
            config=config,
            title="设置卡片",
            icon="SETTINGS",
            enabled=True,
            help_text="这是设置卡片的帮助提示",
        ))
    
    ft.run(main)
