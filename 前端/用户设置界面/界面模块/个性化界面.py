# -*- coding: utf-8 -*-
"""
模块名称：个性化界面 | 层级：界面模块层
设计思路：
    个性化界面，包含主题设置、调色板设置、风格设置等卡片。
    使用主题色块组件实现主题选择。

功能：
    1. 主题设置
    2. 调色板设置
    3. 风格设置

对外接口：
    - create(): 创建个性化界面
"""

import flet as ft
from typing import Callable
from 前端.用户设置界面.配置.界面配置 import 界面配置
from 前端.用户设置界面.组件模块.通用卡片 import UniversalCard
from 前端.用户设置界面.组件模块.功能容器 import FunctionContainer
from 前端.用户设置界面.单元模块.主题色块 import ThemeColorBlock


class PersonalizationInterface:
    """个性化界面 - 界面模块层"""
    
    @staticmethod
    def create(page: ft.Page = None, on_refresh: Callable[[], None] = None) -> ft.Container:
        """
        创建个性化界面
        
        参数：
            page: 页面对象（可选，用于更新页面显示）
            on_refresh: 刷新回调
        
        返回：
            ft.Container: 个性化界面容器
        """
        配置 = 界面配置()
        theme_colors = 配置.当前主题颜色
        
        current_theme = 配置.主题名称
        current_palette = 配置.调色板名称
        current_style = 配置.当前风格名称
        
        def on_theme_click(theme_name: str):
            if theme_name != current_theme:
                配置.切换主题(theme_name)
                if on_refresh:
                    on_refresh()
        
        def on_palette_click(palette_name: str):
            if palette_name != current_palette:
                配置.切换调色板(palette_name)
                if on_refresh:
                    on_refresh()
        
        def on_style_click(style_name: str):
            if style_name != current_style:
                配置.切换风格(style_name)
                if on_refresh:
                    on_refresh()
        
        theme_colors_list = [
            {"name": "浅色", "value": "#FFFFFF"},
            {"name": "深色", "value": "#1A1A2E"},
            {"name": "日出", "value": "#FFE4B5"},
            {"name": "捕捉", "value": "#98FB98"},
            {"name": "聚焦", "value": "#87CEEB"},
        ]
        
        theme_block = ThemeColorBlock.create_group(
            colors=theme_colors_list,
            selected_color=next((c["value"] for c in theme_colors_list if c["name"] == current_theme), ""),
            on_select=lambda v: on_theme_click(next((c["name"] for c in theme_colors_list if c["value"] == v), "")),
            size=40,
            spacing=10,
        )
        
        theme_card = UniversalCard.create(
            title="主题设置",
            icon="PALETTE",
            enabled=True,
            subtitle="选择界面主题风格",
            controls=[theme_block],
            controls_per_row=1,
        )
        
        palette_colors = [
            {"name": "水生", "value": "#006994"},
            {"name": "沙漠", "value": "#C19A6B"},
            {"name": "黄昏", "value": "#FF6B6B"},
            {"name": "夜空", "value": "#2C3E50"},
        ]
        
        palette_block = ThemeColorBlock.create_group(
            colors=palette_colors,
            selected_color=next((c["value"] for c in palette_colors if c["name"] == current_palette), ""),
            on_select=lambda v: on_palette_click(next((c["name"] for c in palette_colors if c["value"] == v), "")),
            size=40,
            spacing=10,
        )
        
        palette_card = UniversalCard.create(
            title="调色板设置",
            icon="CONTRAST",
            enabled=True,
            subtitle="选择高对比度调色板",
            controls=[palette_block],
            controls_per_row=1,
        )
        
        style_colors = [
            {"name": "平铺", "value": "#E0E0E0"},
            {"name": "立体", "value": "#FFFFFF"},
        ]
        
        style_block = ThemeColorBlock.create_group(
            colors=style_colors,
            selected_color=next((c["value"] for c in style_colors if c["name"] == ("立体" if current_style == "3D立体" else "平铺")), ""),
            on_select=lambda v: on_style_click("3D立体" if v == "#FFFFFF" else "普通平铺"),
            size=40,
            spacing=10,
        )
        
        style_card = UniversalCard.create(
            title="风格设置",
            icon="STYLE",
            enabled=True,
            subtitle="选择界面风格",
            controls=[style_block],
            controls_per_row=1,
        )
        
        return FunctionContainer.create(
            config=配置,
            title="个性化设置",
            icon="PALETTE",
            cards=[theme_card, palette_card, style_card],
            expand=True,
        )


# *** 调试逻辑 ***
if __name__ == "__main__":
    from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider
    ThemeProvider.initialize(配置)
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        page.add(PersonalizationInterface.create())
    ft.run(main)
