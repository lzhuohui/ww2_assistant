# -*- coding: utf-8 -*-
"""
模块名称：用户界面
设计思路及联动逻辑:
    在统一风格用户界面基础上，使用可编辑的头像组件。
    1. 支持头像文字编辑，保持与原始界面相同的风格
    2. 使用统一的文本样式管理，确保文字视觉效果一致
模块隔离原则:
    1. 不直接创建被调用模块的内容
    2. 不覆盖被调用模块的计算结果
    3. 用户指定变量除外
"""

from typing import Callable, Optional

import flet as ft

from 前端.用户设置界面.单元模块.通用容器 import GenericContainer
from 前端.用户设置界面.单元模块.卡片容器 import CardContainer
from 前端.用户设置界面.单元模块.用户头像 import Avatar
from 前端.用户设置界面.单元模块.文本标签 import LabelText
from 前端.用户设置界面.配置.界面配置 import 界面配置


# *** 用户指定变量 - AI不得修改, 变量值必须生效 ***
USER_WIDTH = 280  # 默认宽度
USER_HEIGHT = 90  # 默认高度
USER_CARD_MARGIN =5  # 卡片容器距离通用容器的边距
# *********************************


class UserInfoCard:
    """可编辑统一风格用户界面"""
    
    @staticmethod
    def create(
        username: str="试用用户",
        is_registered: bool=False,
        expire_days: int=7,
        on_click: Optional[Callable[[], None]]=None,
        on_avatar_text_change: Optional[Callable[[str], None]]=None,
        width: int=USER_WIDTH,
        height: int=USER_HEIGHT,
        **kwargs
    ) -> ft.Container:
        配置 = 界面配置()
        
        theme_colors = 配置.当前主题颜色
        bg_card = theme_colors.get("bg_card", "#2D2D2D")
        
        sizes = 配置.定义尺寸
        spacing_md = sizes.get("间距", {}).get("spacing_md", 12)
        spacing_xs = sizes.get("间距", {}).get("spacing_sm", 8)
        card_radius = sizes.get("圆角", {}).get("radius_md", 8)
        
        container_width = width
        container_height = height
        card_width = container_width - USER_CARD_MARGIN * 2
        card_height = container_height - USER_CARD_MARGIN * 2
        item_padding = USER_CARD_MARGIN
        avatar_size_medium = 48
        
        status_text = "已注册" if is_registered else f"试用剩余 {expire_days} 天"
        
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
        
        card_container = CardContainer.create(
            content=content,
            width=card_width,
            height=card_height,
            padding=item_padding,
        )
        
        outer_container = GenericContainer.create(
            content=card_container,
            width=container_width,
            height=container_height,
            padding=0,
            alignment=ft.Alignment(0, 0),
        )
        
        if on_click:
            outer_container.on_click = on_click
        
        return outer_container


# *** 调试逻辑 ***
if __name__ == "__main__":
    ft.run(lambda page: page.add(UserInfoCard.create()))
