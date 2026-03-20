# -*- coding: utf-8 -*-
"""
模块名称：导航界面
设计思路及联动逻辑:
    提供导航功能，切换不同的设置页面。
    1. 使用通用容器统一风格
    2. 支持选中状态高亮和点击切换
模块隔离原则:
    1. 不直接创建被调用模块的内容
    2. 不覆盖被调用模块的计算结果
    3. 用户指定变量除外
"""

from typing import Callable, Dict, List

import flet as ft

from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider
from 前端.用户设置界面.单元模块.通用容器 import GenericContainer
from 前端.用户设置界面.组件模块.导航按钮 import NavButton
from 前端.用户设置界面.配置.界面配置 import 界面配置


# *** 用户指定变量 - AI不得修改, 变量值必须生效 ***
USER_WIDTH = 280  # 默认宽度
USER_HEIGHT = 400  # 默认高度
# *********************************


class NavBar:
    """导航界面 - 组件模块"""
    
    @staticmethod
    def create(
        items: List[Dict]=None,
        selected_index: int=0,
        on_select: Callable[[int], None]=None,
        width: int=USER_WIDTH,
        height: int=USER_HEIGHT,
        **kwargs
    ) -> ft.Container:
        配置 = 界面配置()
        
        spacing_xs = 配置.获取尺寸("间距", "spacing_xs")
        spacing_sm = 配置.获取尺寸("间距", "spacing_sm")
        nav_padding = 配置.获取尺寸("间距", "spacing_sm")
        nav_button_spacing = 配置.获取尺寸("间距", "spacing_xs") or 4
        
        if items is None:
            items = [
                {"text": "系统", "icon": ft.Icons.SETTINGS},
                {"text": "策略", "icon": ft.Icons.ROCKET_LAUNCH},
                {"text": "任务", "icon": ft.Icons.ASSIGNMENT},
                {"text": "建筑", "icon": ft.Icons.DOMAIN},
                {"text": "集资", "icon": ft.Icons.SHOPPING_CART},
                {"text": "账号", "icon": ft.Icons.ACCOUNT_CIRCLE},
                {"text": "打扫", "icon": ft.Icons.CLEANING_SERVICES},
                {"text": "打野", "icon": ft.Icons.EXPLORE},
                {"text": "个性化", "icon": ft.Icons.PALETTE},
                {"text": "关于", "icon": ft.Icons.INFO},
            ]
        
        current_selected = [selected_index]
        nav_buttons = []
        
        def handle_nav_click(index: int):
            current_selected[0] = index
            for i, btn in enumerate(nav_buttons):
                btn.set_selected(i == index)
            if on_select:
                on_select(index)
        
        for i, item in enumerate(items):
            btn = NavButton.create(
                text=item.get("text", f"导航项{i+1}"),
                icon=item.get("icon", ft.Icons.CHEVRON_RIGHT),
                selected=(i == selected_index),
                on_click=lambda e, idx=i: handle_nav_click(idx),
                width=width - spacing_sm * 2,
            )
            nav_buttons.append(btn)
        
        content = ft.Column(
            [btn.container for btn in nav_buttons],
            spacing=nav_button_spacing,
        )
        
        container = GenericContainer.create(
            content=content,
            width=width,
            height=height,
            padding=nav_padding,
            **kwargs
        )
        
        return container


# *** 调试逻辑 ***
if __name__ == "__main__":
    ft.run(lambda page: page.add(NavBar.create()))
