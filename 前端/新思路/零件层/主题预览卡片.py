# -*- coding: utf-8 -*-
"""
主题预览卡片 - 零件层（新思路）

设计思路:
    独立功能模块，轻量级设计。
    主题预览卡片，点击切换主题。

功能:
    1. 显示主题预览效果
    2. 点击切换主题
    3. 当前主题选中标记

数据来源:
    所有配置数据从配置目录获取。

使用场景:
    被组件层模块调用，也可独立使用。

可独立运行调试: python 主题预览卡片.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft
from typing import Callable, Optional, List
from 配置.界面配置 import 界面配置


class ThemePreviewCard:
    """主题预览卡片 - 独立功能模块"""
    
    @staticmethod
    def create(
        config: 界面配置,
        theme_name: str = "浅色",
        is_selected: bool = False,
        on_click: Callable[[str], None] = None,
        **kwargs
    ) -> ft.Container:
        """
        创建主题预览卡片
        
        参数:
            config: 界面配置对象
            theme_name: 主题名称
            is_selected: 是否选中
            on_click: 点击回调
        
        返回:
            ft.Container: 主题预览卡片容器
        """
        # 主题颜色定义
        themes = {
            "浅色": {
                "bg": "#FFFFFF",
                "panel": "#F3F3F3",
                "text": "#1A1A1A",
                "accent": "#0078D4",
            },
            "深色": {
                "bg": "#1A1A1A",
                "panel": "#2D2D2D",
                "text": "#FFFFFF",
                "accent": "#60CDFF",
            },
        }
        
        theme = themes.get(theme_name, themes["浅色"])
        
        # 创建预览内容
        preview_content = ft.Column(
            [
                # 模拟标题栏
                ft.Container(
                    content=ft.Text(
                        "标题",
                        size=8,
                        color=theme["text"],
                    ),
                    bgcolor=theme["panel"],
                    padding=2,
                ),
                # 模拟内容区
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Container(
                                content=ft.Text("内容行", size=6, color=theme["text"]),
                                bgcolor=theme["panel"],
                                padding=1,
                            ),
                            ft.Container(
                                content=ft.Text("内容行", size=6, color=theme["text"]),
                                bgcolor=theme["panel"],
                                padding=1,
                            ),
                        ],
                        spacing=2,
                    ),
                    padding=2,
                ),
            ],
            spacing=0,
        )
        
        # 创建预览卡片
        preview_card = ft.Container(
            content=preview_content,
            width=80,
            height=60,
            bgcolor=theme["bg"],
            border_radius=4,
            border=ft.Border.all(2, theme["accent"] if is_selected else "transparent"),
        )
        
        # 主题名称
        theme_label = ft.Text(
            theme_name,
            size=12,
            color=config.当前主题颜色.get("text_primary"),
        )
        
        # 选中标记
        check_icon = ft.Icon(
            ft.Icons.CHECK_CIRCLE,
            size=16,
            color=theme["accent"],
            visible=is_selected,
        )
        
        # 完整卡片
        card = ft.Container(
            content=ft.Column(
                [
                    preview_card,
                    ft.Container(height=4),
                    ft.Row(
                        [theme_label, check_icon],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=4,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
            ),
            on_click=lambda e: on_click(theme_name) if on_click else None,
            ink=True,
            border_radius=8,
        )
        
        return card


class ThemeSelector:
    """主题选择器 - 组合多个主题预览卡片"""
    
    @staticmethod
    def create(
        config: 界面配置,
        current_theme: str = "浅色",
        on_theme_change: Callable[[str], None] = None,
        **kwargs
    ) -> ft.Container:
        """
        创建主题选择器
        
        参数:
            config: 界面配置对象
            current_theme: 当前主题
            on_theme_change: 主题变化回调
        
        返回:
            ft.Container: 主题选择器容器
        """
        theme_names = ["浅色", "深色"]
        theme_cards = []
        
        def handle_theme_click(theme_name: str):
            if on_theme_change:
                on_theme_change(theme_name)
        
        for theme_name in theme_names:
            card = ThemePreviewCard.create(
                config=config,
                theme_name=theme_name,
                is_selected=(theme_name == current_theme),
                on_click=handle_theme_click,
            )
            theme_cards.append(card)
        
        # 创建选择器容器
        selector = ft.Container(
            content=ft.Row(
                theme_cards,
                alignment=ft.MainAxisAlignment.START,
                spacing=20,
            ),
            padding=10,
        )
        
        return selector


# 兼容别名
主题预览卡片 = ThemePreviewCard
主题选择器 = ThemeSelector


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    # 1. 界面配置初始化
    配置 = 界面配置()
    
    # 2. 自动加载用户数据覆盖默认值（在界面配置.__init__中自动完成）
    
    # 3. 正常启动被测模块
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        
        def on_theme_change(theme_name: str):
            print(f"主题切换: {theme_name}")
        
        page.add(ThemeSelector.create(配置, current_theme="浅色", on_theme_change=on_theme_change))  # 只能更改此处**被测调用模块名称**
    
    ft.run(main)
