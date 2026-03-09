# -*- coding: utf-8 -*-
"""
导航栏模块 - 部件层

设计思路:
    本模块是部件层模块，调用容器组件、装饰框线组件和导航按钮组件创建导航栏。

功能:
    1. 调用容器组件创建导航栏容器
    2. 调用装饰框线组件创建内框线
    3. 调用导航按钮组件创建导航菜单
    4. 支持两级导航（分组 + 导航项）
    5. 支持滚动条

数据来源:
    主题颜色从界面配置获取。
    菜单项从界面配置获取。

使用场景:
    被设备层界面调用，提供导航栏区域。

可独立运行调试: python 导航栏模块.py
"""

import flet as ft
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from 原子层.界面配置 import 界面配置
from 组件层.容器样式 import ContainerStyle
from 组件层.装饰框线 import DecorativeBorder
from 组件层.导航按钮 import NavButton
from typing import List, Callable, Dict, Any


class NavBar:  # 导航栏模块
    """导航栏模块 - 调用容器+框线+导航按钮"""
    
    def __init__(self, config: 界面配置, page: ft.Page, **kwargs):
        self._config = config
        self._page = page
        self._width = kwargs.get("width", 240)
        ui_config = config.定义尺寸.get("界面", {})
        self._margin = ui_config.get("peripheral_margin", 10)
        self._button_spacing = 3
        self._button_height = 36
        self._nav_buttons: List[NavButton] = []
        self._current_index = 0
        self._callbacks: List[Callable] = []
        self._menu_items = [
            {"name": "系统设置", "icon": "SETTINGS", "subtitle": "系统相关设置"},
            {"name": "通用设置", "icon": "TUNE", "subtitle": "全局通用控制设置"},
            {"name": "策略设置", "icon": "TRENDING_UP", "subtitle": "策略相关配置"},
            {"name": "任务设置", "icon": "FLAG", "subtitle": "任务相关配置"},
            {"name": "建筑设置", "icon": "HOME", "subtitle": "建筑相关配置"},
            {"name": "集资设置", "icon": "ATTACH_MONEY", "subtitle": "集资相关配置"},
            {"name": "打扫战场", "icon": "CLEANING_SERVICES", "subtitle": "打扫战场配置"},
            {"name": "打野设置", "icon": "FOREST", "subtitle": "打野相关配置"},
            {"name": "账号设置", "icon": "ACCOUNT_CIRCLE", "subtitle": "账号相关配置"},
            {"name": "个性化设置", "icon": "PALETTE", "subtitle": "界面个性化配置"},
            {"name": "关于", "icon": "INFO", "subtitle": "关于本程序"},
        ]
    
    def add_callback(self, callback: Callable):  # 添加联动回调函数
        self._callbacks.append(callback)
    
    def render(self) -> ft.Container:
        nav_menu = self._create_nav_menu()
        
        nav_content = ft.Column(
            controls=nav_menu,
            spacing=self._button_spacing,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.HIDDEN,
        )
        
        inner_border = DecorativeBorder.inner_border(
            self._config,
            content=nav_content,
            padding=self._margin,
        )
        
        if self._nav_buttons:
            self._nav_buttons[0].set_selected(True)
        
        return ContainerStyle.nav_container(
            self._config,
            content=inner_border,
            width=self._width,
            padding=self._margin,
        )
    
    def _create_nav_menu(self):  # 创建导航菜单按钮列表
        nav_controls = []
        button_width = self._width - self._margin * 2 - 25
        
        for i, item in enumerate(self._menu_items):
            btn = NavButton(
                self._config,
                name=item["name"],
                icon=item["icon"],
                width=button_width,
                on_click=lambda e, index=i: self._on_nav_click(index),
            )
            self._nav_buttons.append(btn)
            nav_controls.append(btn.render())
        
        return nav_controls
    
    def _on_nav_click(self, index: int):  # 导航按钮点击处理：更新选中状态
        if index == self._current_index:
            return
        self._current_index = index
        
        for i, btn in enumerate(self._nav_buttons):
            btn.set_selected(i == index)
        
        menu_item = self._menu_items[index]
        for callback in self._callbacks:
            callback(menu_item["name"], menu_item["subtitle"])
    
    @property
    def width(self):
        return self._width


# 兼容别名
导航栏模块 = NavBar


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    config = 界面配置()
    
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = config.获取颜色("bg_primary")
        navbar = NavBar(config, page)
        
        def callback(title, subtitle):
            print(f"导航到: {title} - {subtitle}")
        
        navbar.add_callback(callback)
        page.add(navbar.render())
    
    ft.run(main)
