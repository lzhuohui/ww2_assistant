# -*- coding: utf-8 -*-
"""
关于通用卡片 - 组件层

设计思路:
    复刻通用卡片风格，左侧图标+标题+分割线，右侧文本内容。
    无开关功能，适合展示信息类卡片。

布局规则:
    0. 全部控件边距为0
    1. 除分割线外，所有控件自适应
    2. 以分割线为基准
    3. 图标/主标题上下布置且中间对齐，交线与分割线中点水平对齐

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
from 新思路.零件层.分割线 import Divider, CONTAINER_WIDTH, LINE_WIDTH


DEFAULT_ICON_SIZE = 24
DEFAULT_TITLE_SIZE = 14
ICON_TITLE_SPACING = 4
ICON_AREA_WIDTH = DEFAULT_ICON_SIZE + ICON_TITLE_SPACING + 5 * DEFAULT_TITLE_SIZE


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
        
        icon_name = getattr(ft.Icons, icon.upper(), ft.Icons.INFO)
        
        icon_height = DEFAULT_ICON_SIZE
        title_height = DEFAULT_TITLE_SIZE
        icon_title_total_height = icon_height + ICON_TITLE_SPACING + title_height
        icon_title_center_y = height / 2
        icon_title_top = icon_title_center_y - icon_title_total_height / 2
        title_top = icon_title_top + icon_height + ICON_TITLE_SPACING
        
        divider = Divider.create(config, height, enabled=True)
        
        stack_children = []
        
        divider_container = ft.Container(
            content=divider,
            left=ICON_AREA_WIDTH,
            top=0,
        )
        stack_children.append(divider_container)
        
        title_text_width = len(title) * DEFAULT_TITLE_SIZE
        title_center_to_divider = 50
        title_container_left = ICON_AREA_WIDTH - title_text_width / 2 - title_center_to_divider
        
        title_control = ft.Text(
            title,
            size=DEFAULT_TITLE_SIZE,
            weight=ft.FontWeight.BOLD,
            color=theme_colors.get("text_primary"),
        )
        
        title_column = ft.Column(
            [title_control],
            spacing=ICON_TITLE_SPACING,
            horizontal_alignment=ft.CrossAxisAlignment.END,
            alignment=ft.MainAxisAlignment.START,
            tight=True,
        )
        
        icon_title_container = ft.Container(
            content=title_column,
            left=title_container_left,
            top=title_top,
        )
        stack_children.append(icon_title_container)
        
        icon_control = ft.Icon(
            icon_name,
            size=DEFAULT_ICON_SIZE,
            color=theme_colors.get("accent"),
        )
        
        icon_center_to_divider = 50
        icon_left = ICON_AREA_WIDTH - DEFAULT_ICON_SIZE / 2 - icon_center_to_divider
        icon_top = title_top - DEFAULT_ICON_SIZE - ICON_TITLE_SPACING
        
        icon_container = ft.Container(
            content=icon_control,
            left=icon_left,
            top=icon_top,
        )
        stack_children.append(icon_container)
        
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
            left=ICON_AREA_WIDTH + CONTAINER_WIDTH + CONTAINER_WIDTH,
            top=card_padding,
        )
        stack_children.append(right_container)
        
        main_stack = ft.Stack(
            stack_children,
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
