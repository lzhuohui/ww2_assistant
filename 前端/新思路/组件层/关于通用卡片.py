# -*- coding: utf-8 -*-
"""
关于通用卡片 - 组件层

设计思路:
    复刻通用卡片风格，左侧图标+标题+分割线，右侧内容区域。
    无开关功能，适合展示信息类卡片。

功能:
    1. 左侧：图标+标题+副标题+分割线
    2. 右侧：内容区域（可自定义）
    3. 无开关功能

使用场景:
    被关于设置页面调用。
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft
from typing import List, Optional
from 新思路.零件层.卡片容器 import CardContainer
from 新思路.零件层.图标标题 import IconTitle


class AboutCard:
    """关于通用卡片"""
    
    @staticmethod
    def create(
        config,
        title: str,
        icon: str,
        content_controls: List[ft.Control],
        subtitle: str = None,
        height: int = None,
    ) -> ft.Container:
        """
        创建关于卡片
        
        参数:
            config: 界面配置对象
            title: 卡片标题
            icon: 图标名称
            content_controls: 右侧内容控件列表
            subtitle: 副标题（可选）
            height: 卡片高度（可选，自动计算）
        
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
        
        icon_title = IconTitle.create(
            config=config,
            title=title,
            icon=icon,
            enabled=True,
            on_state_change=None,
            subtitle=subtitle,
            divider_height=height,
        )
        
        left_container = ft.Container(content=icon_title)
        
        content_column = ft.Column(
            content_controls,
            spacing=4,
            alignment=ft.MainAxisAlignment.CENTER,
        )
        
        right_container = ft.Container(
            content=content_column,
            right=20,
            top=card_padding,
        )
        
        if height is None:
            content_height = sum(
                getattr(c, 'height', 20) if hasattr(c, 'height') else 20
                for c in content_controls
            ) + (len(content_controls) - 1) * 4
            height = max(60, content_height + card_padding * 2)
        
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
