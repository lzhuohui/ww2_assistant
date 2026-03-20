# -*- coding: utf-8 -*-
"""
模块名称：可编辑统一风格用户界面 | 层级：组件层
设计思路：
    在统一风格用户界面基础上，使用可编辑的头像组件。
    使用可编辑的头像组件，支持头像文字编辑。
    保持与原始界面相同的风格和功能。
    使用统一的文本样式管理，确保文字视觉效果一致。
"""

import flet as ft
from typing import Optional, Callable

from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider
from 前端.用户设置界面.单元模块.通用容器 import GenericContainer
from 前端.用户设置界面.单元模块.用户头像 import Avatar
from 前端.用户设置界面.单元模块.文本标签 import LabelText
from 前端.用户设置界面.配置.界面配置 import 界面配置

DEFAULT_WIDTH = 280
DEFAULT_HEIGHT = 80


class UserInfoCard:
    """可编辑统一风格用户界面"""
    
    @staticmethod
    def create(
        username: str = "试用用户",
        is_registered: bool = False,
        expire_days: int = 7,
        on_click: Optional[Callable[[], None]] = None,
        on_avatar_text_change: Optional[Callable[[str], None]] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        **kwargs
    ) -> ft.Container:
        """
        创建用户信息卡片
        
        参数:
            username: 用户名
            is_registered: 是否已注册
            expire_days: 过期天数
            on_click: 点击回调
            on_avatar_text_change: 头像文字变化回调
            width: 宽度
            height: 高度
        
        返回:
            ft.Container: 用户信息卡片容器
        """
        配置 = 界面配置()
        
        theme_colors = 配置.当前主题颜色
        text_primary = theme_colors.get("text_primary", "#FFFFFF")
        text_secondary = theme_colors.get("text_secondary", "#CCCCCC")
        accent = theme_colors.get("accent", "#0078D4")
        bg_card = theme_colors.get("bg_card", "#2D2D2D")
        
        sizes = 配置.定义尺寸
        font_size_md = sizes.get("字体", {}).get("font_size_md", 14)
        font_size_xs = sizes.get("字体", {}).get("font_size_xs", 12)
        spacing_md = sizes.get("间距", {}).get("spacing_md", 12)
        spacing_xs = sizes.get("间距", {}).get("spacing_sm", 8)
        card_radius = sizes.get("圆角", {}).get("radius_md", 8)
        
        container_width = width or DEFAULT_WIDTH
        container_height = height or DEFAULT_HEIGHT
        item_padding = spacing_md
        avatar_size_medium = 48
        
        status_text = "已注册" if is_registered else f"试用剩余 {expire_days} 天"
        status_color = accent if is_registered else text_secondary
        
        def handle_avatar_text_change(new_text: str):
            if on_avatar_text_change:
                on_avatar_text_change(new_text)
        
        avatar = Avatar.create(
            size=avatar_size_medium,
            text=username[0] if username else "帅",
            show_glow=True,
            bg_color=bg_card,
            text_color="#FFD700",
            on_text_change=on_avatar_text_change,
        )
        
        name_label = LabelText.create(
            text=username,
            role="h3",
            win11_style=True
        )
        
        status_label = LabelText.create(
            text=status_text,
            role="caption",
            win11_style=True
        )
        
        labels = ft.Column(
            [
                name_label,
                status_label,
            ],
            spacing=spacing_xs,
            alignment=ft.MainAxisAlignment.CENTER,
        )
        
        content = ft.Row(
            [
                avatar,
                ft.Container(width=spacing_md),
                labels,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        
        card_container = GenericContainer.create(
            content=content,
            width=container_width,
            height=container_height,
            padding=item_padding,
            bgcolor=bg_card,
            border_radius=card_radius,
            alignment=ft.Alignment(0, 0),
        )
        
        if on_click:
            card_container.on_click = on_click
        
        return card_container


if __name__ == "__main__":
    from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider
    
    配置 = 界面配置()
    ThemeProvider.initialize(配置)
    
    def main(page: ft.Page):
        page.add(UserInfoCard.create())
    
    ft.run(main)