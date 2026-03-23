# -*- coding: utf-8 -*-
"""
模块名称：通用功能容器
设计思路及联动逻辑:
    作为页面层的通用容器，包含通用容器、图标、标签、水平灰色隔断和卡片列表。
    只接收已创建的卡片控件，不创建卡片，不处理配置。
模块隔离原则:
    1. 不直接创建被调用模块的内容
    2. 不覆盖被调用模块的计算结果
    3. 用户指定变量除外
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft
from typing import List, Optional, Dict, Any
from 前端.用户设置界面.配置.界面配置 import 界面配置
from 前端.用户设置界面.单元模块.通用容器 import GenericContainer, USER_WIDTH, USER_HEIGHT
from 前端.用户设置界面.单元模块.文本标签 import LabelText


# *** 用户指定变量 - AI不得修改, 变量值必须生效 ***
# （用户未指定变量）
# *********************************


class GenericFunctionContainer:
    """通用功能容器 - 接收已创建的卡片，只负责包装布局"""
    
    @staticmethod
    def create(
        config: 界面配置,
        title: str="功能标题",
        icon: str="SETTINGS",
        cards: List[ft.Control]=None,
        width: int=USER_WIDTH,
        height: int=USER_HEIGHT,
        expand: bool=False,
        card_margin: int=0,
        **kwargs
    ) -> ft.Container:
        final_cards = cards if cards else []
        
        content_width = width - card_margin * 2
        for card in final_cards:
            if hasattr(card, 'width'):
                card.width = content_width
        
        icon_control = None
        if icon:
            if isinstance(icon, str):
                icon_upper = icon.upper()
                actual_icon = getattr(ft.Icons, icon_upper, ft.Icons.SETTINGS)
            else:
                actual_icon = icon
            icon_control = ft.Icon(
                actual_icon,
                size=20,
                color=config.当前主题颜色.get("accent"),
            )
        
        label_text = LabelText.create(
            text=title,
            role="h3",
            win11_style=True
        )
        
        header_content = ft.Row(
            [
                icon_control,
                ft.Container(width=8),
                label_text,
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ) if icon_control else label_text
        
        divider = ft.Container(
            content=ft.Divider(
                height=1,
                thickness=1,
                color=config.当前主题颜色.get("border"),
            ),
            opacity=0.5,
        )
        
        card_list = ft.Column(
            controls=final_cards,
            spacing=5,
            expand=expand,
            scroll=ft.ScrollMode.HIDDEN if expand else None,
        )
        
        content = ft.Column(
            controls=[
                header_content,
                divider,
                card_list,
            ],
            spacing=8,
            expand=expand,
        )
        
        return GenericContainer.create(
            content=content,
            width=width,
            height=height,
            expand=expand,
            padding=card_margin,
            **kwargs
        )


# *** 调试逻辑 ***
if __name__ == "__main__":
    ft.run(lambda page: page.add(GenericFunctionContainer.create(config=界面配置())))
