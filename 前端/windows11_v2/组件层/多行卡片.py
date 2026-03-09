# -*- coding: utf-8 -*-
"""
多行卡片 - 组件层

设计思路:
    本模块是组件层模块，提供多行布局容器。

功能:
    1. 左侧：图标+标题（上下排列），图标可点击切换启用/禁用状态
    2. 中间：发光分割线
    3. 右侧：多行控件，每行多个控件
    4. 通用性：接收任意控件列表
    5. 状态切换：双击图标切换启用/禁用，禁用时灰色显示

数据来源:
    主题颜色从界面配置获取。

使用场景:
    被建筑卡片等需要多行布局的模块调用。

可独立运行调试: python 多行卡片.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import flet as ft
from typing import List, Callable, Optional
from 原子层.界面配置 import 界面配置


# ==================== 用户指定变量区 ====================
ITEMS_PER_ROW = 6           # 每行控件数量
DIVIDER_WIDTH = 2           # 分割线宽度
DIVIDER_HEIGHT = 60         # 分割线高度
DIVIDER_OPACITY = 0.7       # 分割线透明度
DIVIDER_BLUR = 6            # 分割线模糊
LEFT_WIDTH = 60             # 左侧区域宽度
DIVIDER_LEFT = 90           # 分割线左边距
CONTENT_LEFT = 130          # 内容区域左边距
# ========================================================


class MultiRowCard:  # 多行卡片组件
    """多行卡片 - 左侧图标+标题，中间分割线，右侧多行控件"""
    
    @staticmethod
    def create(
        config: 界面配置,
        title: str,
        icon: str = None,
        controls: List[ft.Control] = None,
        on_click: Callable = None,
        enabled: bool = True,
        on_state_change: Callable[[bool], None] = None,
        **kwargs
    ) -> ft.Container:
        theme_colors = config.当前主题颜色
        
        font_config = config.定义尺寸.get("字体", {})
        weight_config = config.定义尺寸.get("字重", {})
        icon_config = config.定义尺寸.get("组件", {})
        spacing_config = config.定义尺寸.get("间距", {})
        radius_config = config.定义尺寸.get("圆角", {})
        ui_config = config.定义尺寸.get("界面", {})
        
        current_enabled = enabled
        
        icon_control = None
        if icon:
            if isinstance(icon, str):
                icon_name = icon.upper()
                actual_icon = getattr(ft.Icons, icon_name, ft.Icons.SETTINGS)
            else:
                actual_icon = icon
            icon_control = ft.Icon(
                actual_icon,
                size=icon_config.get("icon_size_large", 24),
                color=theme_colors.get("accent"),
                opacity=1.0 if current_enabled else 0.4,
            )
        
        title_control = ft.Text(
            title,
            size=font_config.get("font_size_md", 14),
            weight=weight_config.get("font_weight_medium", ft.FontWeight.W_500),
            color=theme_colors.get("text_primary"),
            opacity=1.0 if current_enabled else 0.4,
        )
        
        left_content = ft.Column(
            [
                icon_control,
                title_control,
            ],
            spacing=spacing_config.get("spacing_xs", 4),
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        )
        
        left_gesture = ft.GestureDetector(
            content=left_content,
            on_double_tap=None,
        )
        
        left_container = ft.Container(
            content=left_gesture,
            left=ui_config.get("card_padding", 16),
            top=0,
            bottom=0,
            width=LEFT_WIDTH,
            alignment=ft.Alignment(0, 0),
        )
        
        divider = ft.Container(
            width=DIVIDER_WIDTH,
            height=DIVIDER_HEIGHT,
            bgcolor=theme_colors.get("accent"),
            opacity=DIVIDER_OPACITY if current_enabled else 0.2,
            shadow=ft.BoxShadow(
                blur_radius=DIVIDER_BLUR,
                color=theme_colors.get("accent"),
                spread_radius=0,
            ) if current_enabled else None,
            left=DIVIDER_LEFT,
            top=0,
            bottom=0,
        )
        
        rows = []
        if controls:
            for i in range(0, len(controls), ITEMS_PER_ROW):
                row_items = controls[i:i+ITEMS_PER_ROW]
                row = ft.Row(
                    row_items,
                    spacing=spacing_config.get("spacing_md", 12),
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                )
                rows.append(row)
        
        row_count = len(rows)
        row_height = 32
        row_spacing = spacing_config.get("spacing_sm", 8)
        padding_vertical = ui_config.get("item_padding", 12) * 2
        content_height = row_count * row_height + (row_count - 1) * row_spacing if row_count > 0 else 0
        card_height = content_height + padding_vertical
        
        right_content = ft.Column(
            rows,
            spacing=row_spacing,
            opacity=1.0 if current_enabled else 0.5,
        )
        
        right_container = ft.Container(
            content=right_content,
            left=CONTENT_LEFT,
            right=ui_config.get("card_padding", 16),
            top=ui_config.get("item_padding", 12),
            height=content_height,
            alignment=ft.Alignment(-1, 0),
        )
        
        main_stack = ft.Stack(
            [
                left_container,
                divider,
                right_container,
            ],
            height=card_height,
            clip_behavior=ft.ClipBehavior.NONE,
        )
        
        container = ft.Container(
            content=main_stack,
            bgcolor=theme_colors.get("bg_card"),
            border_radius=radius_config.get("radius_lg", 12),
            padding=ft.Padding(
                left=ui_config.get("card_padding", 16),
                right=ui_config.get("card_padding", 16),
                top=ui_config.get("item_padding", 12),
                bottom=ui_config.get("item_padding", 12)
            ),
            border=ft.Border.all(1, theme_colors.get("border_light")),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=4,
                color=theme_colors.get("shadow"),
            ),
            animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
            clip_behavior=ft.ClipBehavior.NONE,
        )
        
        def toggle_state(e):  # 切换启用/禁用状态
            nonlocal current_enabled
            current_enabled = not current_enabled
            
            if icon_control:
                icon_control.opacity = 1.0 if current_enabled else 0.4
                icon_control.update()
            title_control.opacity = 1.0 if current_enabled else 0.4
            title_control.update()
            divider.opacity = DIVIDER_OPACITY if current_enabled else 0.2
            divider.update()
            right_content.opacity = 1.0 if current_enabled else 0.5
            right_content.update()
            
            if on_state_change:
                on_state_change(current_enabled)
        
        if left_gesture:
            left_gesture.on_double_tap = toggle_state
        
        def on_hover(e):  # 悬停效果
            if e.data == "true":
                container.bgcolor = theme_colors.get("bg_hover")
                container.border = ft.Border.all(1, theme_colors.get("border"))
                container.shadow = ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=8,
                    color=theme_colors.get("shadow"),
                )
            else:
                container.bgcolor = theme_colors.get("bg_card")
                container.border = ft.Border.all(1, theme_colors.get("border_light"))
                container.shadow = ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=4,
                    color=theme_colors.get("shadow"),
                )
            container.update()
        
        container.on_hover = on_hover
        
        return container


# 兼容别名
多行卡片 = MultiRowCard


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    config = 界面配置()
    
    def main(page: ft.Page):
        page.padding = 20
        page.bgcolor = config.获取颜色("bg_primary")
        
        controls = [
            ft.Text("控件1", color="white"),
            ft.Text("控件2", color="white"),
            ft.Text("控件3", color="white"),
        ]
        
        def on_state_change(enabled):
            print(f"状态变化: {'启用' if enabled else '禁用'}")
        
        page.add(MultiRowCard.create(
            config=config,
            title="测试卡片",
            icon="HOME",
            controls=controls,
            enabled=True,
            on_state_change=on_state_change,
        ))
    
    ft.run(main)
