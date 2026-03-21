# -*- coding: utf-8 -*-
"""
模块名称：导航按钮
设计思路及联动逻辑:
    导航按钮组件，基于通用按钮的导航专用封装。
    1. 复用通用按钮的 style="nav" 样式
    2. 提供导航场景的默认参数配置
    3. 用卡片容器包装，增加立体感
模块隔离原则:
    1. 不直接创建被调用模块的内容
    2. 不覆盖被调用模块的计算结果
    3. 用户指定变量除外
"""

from typing import Callable, Optional

import flet as ft

from 前端.用户设置界面.单元模块.通用按钮 import Button, DEFAULT_WIDTH as BUTTON_DEFAULT_WIDTH, DEFAULT_HEIGHT as BUTTON_DEFAULT_HEIGHT
from 前端.用户设置界面.单元模块.卡片容器 import CardContainer, DEFAULT_WIDTH as CARD_DEFAULT_WIDTH, DEFAULT_HEIGHT as CARD_DEFAULT_HEIGHT


# *** 用户指定变量 - AI不得修改, 变量值必须生效 ***
USER_CARD_WIDTH = 200
USER_CARD_HEIGHT = 50
# *********************************

# 默认值常量 - 供调用者获取
DEFAULT_CARD_WIDTH = USER_CARD_WIDTH
DEFAULT_CARD_HEIGHT = USER_CARD_HEIGHT


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
    """导航按钮 - 基于通用按钮的导航专用封装，带卡片包装"""
    
    @staticmethod
    def create(
        text: str="导航项",
        icon: str="SETTINGS",
        selected: bool=False,
        on_click: Optional[Callable]=None,
        card_width: int=DEFAULT_CARD_WIDTH,
        card_height: int=DEFAULT_CARD_HEIGHT,
        **kwargs
    ) -> NavButtonWrapper:
        card_padding = 8
        button_width = card_width - card_padding * 2
        button_height = card_height - card_padding * 2
        
        button = Button.create(
            text=text,
            icon=icon,
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
            alignment=ft.alignment.center,
        )
        
        return NavButtonWrapper(container, button)


# *** 调试逻辑 ***
if __name__ == "__main__":
    ft.run(lambda page: page.add(NavButton.create().container))
