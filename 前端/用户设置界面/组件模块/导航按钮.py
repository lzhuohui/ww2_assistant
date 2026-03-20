# -*- coding: utf-8 -*-
"""
模块名称：导航按钮
设计思路及联动逻辑:
    导航按钮组件，基于通用按钮的导航专用封装。
    1. 复用通用按钮的 style="nav" 样式
    2. 提供导航场景的默认参数配置
模块隔离原则:
    1. 不直接创建被调用模块的内容
    2. 不覆盖被调用模块的计算结果
    3. 用户指定变量除外
"""

from typing import Callable, Optional

import flet as ft

from 前端.用户设置界面.单元模块.通用按钮 import Button


# *** 用户指定变量 - AI不得修改, 变量值必须生效 ***
DEFAULT_WIDTH = 240  # 默认宽度
DEFAULT_HEIGHT = 34  # 默认高度
# *********************************


class NavButton:
    """导航按钮 - 基于通用按钮的导航专用封装"""
    
    @staticmethod
    def create(
        text: str="导航项",
        icon: str="SETTINGS",
        selected: bool=False,
        on_click: Optional[Callable]=None,
        width: int=DEFAULT_WIDTH,
        height: int=DEFAULT_HEIGHT,
        **kwargs
    ) -> ft.Container:
        return Button.create(
            text=text,
            icon=icon,
            style="nav",
            selected=selected,
            on_click=on_click,
            width=width,
            height=height,
            toggle_mode=True,
            **kwargs
        )


# *** 调试逻辑 ***
if __name__ == "__main__":
    ft.run(lambda page: page.add(NavButton.create()))
