# -*- coding: utf-8 -*-
"""
模块名称：导航界面 | 层级：组件层
设计思路：
    提供导航功能，切换不同的设置页面。
    使用通用容器统一风格。
功能列表：
    1. 显示导航项列表
    2. 支持选中状态高亮
    3. 支持点击切换
对外接口：
    - create(): 创建导航界面
"""

import flet as ft
from typing import List, Dict, Callable
from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider
from 前端.用户设置界面.单元模块.通用容器 import GenericContainer
from 前端.用户设置界面.组件模块.导航按钮 import NavButton
from 前端.用户设置界面.配置.界面配置 import 界面配置

# *** 用户指定变量 - AI不得修改 ***
DEFAULT_WIDTH = 280
DEFAULT_HEIGHT = 400
# *********************************


class NavBar:
    """导航界面 - 组件层"""
    
    @staticmethod
    def create(
        items: List[Dict] = None,
        selected_index: int = 0,
        on_select: Callable[[int], None] = None,
        width: int = None,
        height: int = None,
        **kwargs
    ) -> ft.Container:
        """
        创建导航界面
        
        参数:
            items: 导航项列表，每项为字典 {"text": "显示文字", "icon": "图标名称"}
            selected_index: 当前选中项索引
            on_select: 选择回调，参数为索引
            width: 宽度（默认280）
            height: 高度（默认390）
        
        返回:
            ft.Container: 导航界面容器
        """
        配置 = 界面配置()
        
        container_width = width if width is not None else DEFAULT_WIDTH
        container_height = height if height is not None else DEFAULT_HEIGHT
        
        spacing_xs = 配置.获取尺寸("间距", "spacing_xs")
        spacing_sm = 配置.获取尺寸("间距", "spacing_sm")
        # Win11风格：导航按钮间距更紧凑
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
            nonlocal current_selected
            current_selected = index
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
                width=container_width - spacing_sm * 2,
            )
            nav_buttons.append(btn)
        
        # Win11风格：导航按钮列表，间距紧凑
        content = ft.Column(
            nav_buttons,
            spacing=nav_button_spacing,
        )
        
        container = GenericContainer.create(
            content=content,
            width=container_width,
            height=container_height,
            padding=nav_padding,
            **kwargs
        )
        
        return container


# *** 调试逻辑 ***
if __name__ == "__main__":
    配置 = 界面配置()
    ThemeProvider.initialize(配置)
    def main(page: ft.Page):
        page.add(NavBar.create())
    ft.run(main)
