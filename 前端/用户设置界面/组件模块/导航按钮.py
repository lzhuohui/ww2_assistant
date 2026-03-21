# -*- coding: utf-8 -*-
"""
模块名称：导航按钮
设计思路及联动逻辑:
    导航按钮组件，负责组装图标+文本并包装为卡片。
    1. 使用容器图标、文本标签单元模块组装内容
    2. 调用通用按钮(nav样式)处理选中状态和点击交互
    3. 用卡片容器包装，增加立体感
模块隔离原则:
    1. 不直接创建被调用模块的内容
    2. 不覆盖被调用模块的计算结果
    3. 用户指定变量除外
"""

from typing import Callable, Optional

import flet as ft

from 前端.用户设置界面.单元模块.通用按钮 import Button, USER_WIDTH as BUTTON_USER_WIDTH, USER_HEIGHT as BUTTON_USER_HEIGHT
from 前端.用户设置界面.单元模块.卡片容器 import CardContainer, USER_WIDTH as CARD_USER_WIDTH, USER_HEIGHT as CARD_USER_HEIGHT
from 前端.用户设置界面.单元模块.容器图标 import ContainerIcon, DEFAULT_ICON_SIZE as ICON_DEFAULT_SIZE
from 前端.用户设置界面.单元模块.文本标签 import LabelText, DEFAULT_SIZE as TEXT_DEFAULT_SIZE
from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider
from 前端.用户设置界面.配置.界面配置 import 界面配置


# *** 用户指定变量 - AI不得修改, 变量值必须生效 ***
USER_CARD_WIDTH = 300
USER_CARD_HEIGHT =40
USER_CONTENT_LEFT_MARGIN = 5  # 图标+标签距离按钮左侧的距离
# *********************************

# 导出默认值供调用者使用
__all__ = ['NavButton', 'NavButtonWrapper', 'USER_CARD_WIDTH', 'USER_CARD_HEIGHT']


class NavButtonWrapper:
    """导航按钮包装器 - 提供set_selected方法"""
    
    def __init__(self, container: ft.Container, button: ft.Container):
        self.container = container
        self.button = button
    
    def set_selected(self, selected: bool):
        """设置选中状态"""
        if hasattr(self.button, 'set_selected'):
            self.button.set_selected(selected)
    
    def __getattr__(self, name):
        return getattr(self.container, name)


class NavButton:
    """导航按钮 - 组装图标+文本，使用通用按钮和卡片包装"""
    
    @staticmethod
    def create(
        text: str="导航项",
        icon: str="SETTINGS",
        selected: bool=False,
        on_click: Optional[Callable]=None,
        card_width: int=USER_CARD_WIDTH,
        card_height: int=USER_CARD_HEIGHT,
        **kwargs
    ) -> NavButtonWrapper:
        card_padding = 4
        button_width = card_width - card_padding * 2
        button_height = card_height - card_padding * 2
        
        配置 = 界面配置()
        ThemeProvider.initialize(配置)
        accent_color = ThemeProvider.get_color("accent")
        text_secondary = ThemeProvider.get_color("text_secondary")
        selected_color = "#FFFFFF"
        font_weight_semibold = 配置.获取尺寸("字重", "font_weight_semibold") or ft.FontWeight.W_500
        
        icon_control = None
        if icon:
            if isinstance(icon, str):
                icon_upper = icon.upper()
                actual_icon = getattr(ft.Icons, icon_upper, ft.Icons.SETTINGS)
            else:
                actual_icon = icon
            icon_obj = ft.Icon(actual_icon, size=ICON_DEFAULT_SIZE, color=accent_color)
            icon_control = ContainerIcon.create(
                icon=icon_obj,
                icon_size=ICON_DEFAULT_SIZE,
                padding=0,
            )
        
        text_control = LabelText.create(
            text=text,
            role="body",
            size=TEXT_DEFAULT_SIZE,
            weight=font_weight_semibold,
            enabled=True,
            win11_style=True,
            expand=True,
        )
        if selected:
            text_control.color = selected_color
        else:
            text_control.color = text_secondary
        
        if icon_control:
            row_controls = [
                ft.Container(width=USER_CONTENT_LEFT_MARGIN),
                icon_control,
                ft.Container(width=12),
                text_control,
            ]
        else:
            row_controls = [
                ft.Container(width=USER_CONTENT_LEFT_MARGIN),
                text_control,
            ]
        
        content_row = ft.Row(
            row_controls,
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            width=button_width,
            height=button_height,
        )
        
        button = Button.create(
            content=content_row,
            style="nav",
            selected=selected,
            on_click=on_click,
            width=button_width,
            height=button_height,
            toggle_mode=True,
            **kwargs
        )
        
        container = CardContainer.create(
            content=button,
            width=card_width,
            height=card_height,
            padding=card_padding,
            on_hover_enabled=False,
            alignment=ft.Alignment(-1, 0),
        )
        
        return NavButtonWrapper(container, button)


# *** 调试逻辑 ***
if __name__ == "__main__":
    ft.run(lambda page: page.add(NavButton.create().container))
