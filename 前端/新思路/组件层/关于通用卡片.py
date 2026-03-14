# -*- coding: utf-8 -*-
"""
关于通用卡片 - 组件层

设计思路:
    复刻通用卡片风格，左侧图标+标题+分割线，右侧文本内容。
    无开关功能，适合展示信息类卡片。

功能:
    1. 左侧：图标+标题+分割线
    2. 右侧：文本内容

使用场景:
    被关于设置页面调用。
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft
from typing import List
from 新思路.零件层.卡片容器 import CardContainer
from 新思路.零件层.分割线 import Divider


class AboutCard:
    """关于通用卡片"""
    
    @staticmethod
    def create(
        config,
        title: str,
        icon: str,
        content_lines: List[str],
        height: int = 80,
    ) -> ft.Container:
        """
        创建关于卡片
        
        参数:
            config: 界面配置对象
            title: 卡片标题
            icon: 图标名称
            content_lines: 右侧文本行列表
            height: 卡片高度
        
        返回:
            ft.Container: 卡片容器
        """
        theme_colors = config.当前主题颜色
        ui_config = config.定义尺寸.get("界面", {})
        card_padding = ui_config.get("card_padding", 16)
        
        window_width = ui_config.get("window_width", 1200)
        left_panel_width = ui_config.get("left_panel_width", 280)
        page_padding = ui_config.get("page_padding", 10)
        card_width = window_width - left_panel_width - 20 - page_padding * 2
        
        icon_name = getattr(ft.Icons, icon, ft.Icons.INFO)
        
        left_content = ft.Column(
            [
                ft.Icon(icon_name, color=theme_colors.get("accent"), size=24),
                ft.Text(title, size=14, weight=ft.FontWeight.BOLD, color=theme_colors.get("text_primary")),
                Divider.create(config, height),
            ],
            spacing=4,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        
        left_container = ft.Container(
            content=left_content,
            left=card_padding,
            top=card_padding,
        )
        
        content_controls = [
            ft.Text(line, size=14, color=theme_colors.get("text_secondary"))
            for line in content_lines
        ]
        
        content_column = ft.Column(
            content_controls,
            spacing=4,
        )
        
        right_container = ft.Container(
            content=content_column,
            right=20,
            top=card_padding,
        )
        
        main_stack = ft.Stack(
            [left_container, right_container],
            height=height,
            width=card_width,
            clip_behavior=ft.ClipBehavior.NONE,
        )
        
        container = CardContainer.create(
            config=config,
            content=main_stack,
            height=height,
            width=card_width,
        )
        
        return container


关于通用卡片 = AboutCard
