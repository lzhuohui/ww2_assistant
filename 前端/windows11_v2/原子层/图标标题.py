# -*- coding: utf-8 -*-
"""
图标标题 - 原子层

设计思路:
    最小模块化的图标+标题组件，垂直排列居中。

功能:
    1. 图标：上方居中
    2. 标题：下方居中
    3. 状态切换：启用/禁用透明度变化

数据来源:
    所有配置数据从界面配置获取。

使用场景:
    被组件层模块调用。

可独立运行调试: python 图标标题.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import flet as ft
from typing import Optional, Tuple
from 原子层.界面配置 import 界面配置


class IconTitle:
    """图标标题 - 图标+标题垂直排列居中"""
    
    @staticmethod
    def create(
        config: 界面配置,
        title: str,
        icon: str = None,
        enabled: bool = True,
        **kwargs
    ) -> Tuple[ft.Column, Optional[ft.Icon], ft.Text]:
        theme_colors = config.当前主题颜色
        
        weight_config = config.定义尺寸.get("字重", {})
        spacing_config = config.定义尺寸.get("间距", {})
        card_config = config.定义尺寸.get("卡片", {})
        
        default_icon_size = card_config.get("icon_size", 24)
        default_title_size = card_config.get("title_size", 14)
        
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
                opacity=1.0 if enabled else 0.4,
            )
        
        title_control = ft.Text(
            title,
            size=default_title_size,
            weight=weight_config.get("font_weight_medium", ft.FontWeight.W_500),
            color=theme_colors.get("text_primary"),
            opacity=1.0 if enabled else 0.4,
        )
        
        column_items = [icon_control, title_control] if icon_control else [title_control]
        
        content = ft.Column(
            column_items,
            spacing=spacing_config.get("spacing_xs", 4),
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        )
        
        return content, icon_control, title_control


# 兼容别名
图标标题 = IconTitle


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    config = 界面配置()
    
    def main(page: ft.Page):
        page.padding = 20
        page.bgcolor = config.获取颜色("bg_primary")
        
        page.add(ft.Text("图标标题测试:", color=config.获取颜色("text_secondary")))
        page.add(ft.Divider(height=20, color="transparent"))
        
        content, _, _ = IconTitle.create(
            config=config,
            title="测试标题",
            icon="HOME",
            enabled=True,
        )
        
        page.add(ft.Container(
            content=content,
            padding=20,
            bgcolor=config.获取颜色("bg_card"),
            border_radius=8,
        ))
    
    ft.run(main)
