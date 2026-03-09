# -*- coding: utf-8 -*-
"""
下拉卡片 - 组件层组合组件

设计思路：
- 使用 Stack 绝对定位，左侧显示标题/描述/图标，右侧显示下拉框
- 下拉框尺寸由下拉框自身决定，卡片高度自适应

功能：
- 支持自定义标题、描述、图标
- 支持自定义下拉框选项
- 支持自定义卡片尺寸
"""

import sys
from pathlib import Path
from typing import Callable, List, Optional

sys.path.insert(0, str(Path(__file__).parent.parent))

import flet as ft
from 原子层.界面配置 import 界面配置
from 组件层.自定义下拉框 import CustomDropDown

# *** 用户指定变量 - AI不得修改 ***
DEFAULT_CARD_HEIGHT = 70      # 卡片默认高度
DEFAULT_CARD_SPACING = 10     # 卡片之间的间距
# *********************************


class DropDownCard:  # 下拉卡片组件
    
    @staticmethod
    def create(
        config: 界面配置,
        title: str = "功能设置",
        description: str = "请选择一个选项",
        icon: str = "SETTINGS",
        options: List[str] = None,
        value: str = None,
        on_change: Callable[[str], None] = None,
        height: int = None,
        width: int = None,
    ) -> ft.Container:
        theme_colors = config.当前主题颜色
        card_radius = config.获取尺寸("界面", "card_radius") or 8
        card_height = height or config.获取尺寸("界面", "card_height") or DEFAULT_CARD_HEIGHT
        card_width = width or config.获取尺寸("界面", "card_width") or 800
        
        dropdown = CustomDropDown(
            config=config,
            options=options or ["选项一", "选项二", "选项三"],
            value=value,
            on_change=on_change,
        )
        dropdown_control = dropdown.create()
        
        icon_value = None
        if icon:
            if isinstance(icon, str):
                icon_name = icon.upper()
                icon_value = getattr(ft.Icons, icon_name, ft.Icons.SETTINGS)
            else:
                icon_value = icon
        
        left_content = ft.Container(
            content=ft.Row(
                [
                    ft.Icon(icon_value, size=20, color=theme_colors["accent"]) if icon_value else ft.Container(),
                    ft.Column(
                        [
                            ft.Text(title, size=14, weight=ft.FontWeight.W_500, color=theme_colors["text_primary"]),
                            ft.Text(description, size=12, color=theme_colors["text_secondary"]) if description else ft.Container(),
                        ],
                        spacing=4,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
                spacing=12,
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            left=16,
            top=0,
            bottom=0,
            alignment=ft.Alignment(-1, 0),
        )
        
        right_dropdown = ft.Container(
            content=dropdown_control,
            width=dropdown._width,
            height=dropdown._height,
            right=16,
            top=(card_height - dropdown._height) / 2,
        )
        
        stack = ft.Stack(
            [
                left_content,
                right_dropdown,
            ],
            height=card_height,
            width=card_width,
            clip_behavior=ft.ClipBehavior.NONE,
        )
        
        card = ft.Container(
            content=stack,
            bgcolor=theme_colors["bg_card"],
            border_radius=card_radius,
            border=ft.Border.all(1, theme_colors.get("border_light", theme_colors["border"])),
            height=card_height,
            width=card_width,
        )
        
        return card
    
    @staticmethod
    def create_list(
        config: 界面配置,
        card_configs: List[dict],
    ) -> ft.Column:
        card_spacing = config.获取尺寸("界面", "card_spacing") or DEFAULT_CARD_SPACING
        controls = []
        
        for i, card_config in enumerate(card_configs):
            card = DropDownCard.create(
                config=config,
                title=card_config.get("title"),
                description=card_config.get("description"),
                icon=card_config.get("icon"),
                options=card_config.get("options"),
                value=card_config.get("value"),
                on_change=card_config.get("on_change"),
                height=card_config.get("height"),
                width=card_config.get("width"),
            )
            controls.append(card)
            
            if i < len(card_configs) - 1:
                controls.append(ft.Divider(height=card_spacing, color="transparent"))
        
        return ft.Column(controls, spacing=0)


if __name__ == "__main__":
    config = 界面配置()
    
    def main(page: ft.Page):
        page.padding = 20
        page.bgcolor = config.当前主题颜色["bg_primary"]
        page.add(DropDownCard.create(config=config))
    
    ft.run(main)


# 兼容性别名
下拉卡片 = DropDownCard
