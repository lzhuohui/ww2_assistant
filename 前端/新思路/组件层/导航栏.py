# -*- coding: utf-8 -*-
"""
导航栏 - 组件层（新思路）

设计思路:
    组装零件，构建导航栏。
    采用装配模式，协调各零件交互。

功能:
    1. 组装导航按钮列表
    2. 协调导航状态
    3. 切换内容区域

数据来源:
    所有配置数据从配置目录获取。

使用场景:
    被页面层模块调用。

可独立运行调试: python 导航栏.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft
from typing import Callable, List, Dict
from 配置.界面配置 import 界面配置
from 新思路.零件层.导航按钮 import NavButton


class NavBar:
    """导航栏 - 组件层"""
    
    @staticmethod
    def create(
        config: 界面配置,
        nav_items: List[Dict] = None,
        on_nav_change: Callable[[str], None] = None,
        padding: ft.Padding = None,
        **kwargs
    ) -> ft.Column:
        """
        创建导航栏
        
        参数:
            config: 界面配置对象
            nav_items: 导航项列表 [{"name": "系统设置", "icon": "SETTINGS"}, ...]
            on_nav_change: 导航切换回调
            padding: 内边距（可选，默认从配置中获取）
        
        返回:
            ft.Column: 导航栏容器
        """
        theme_colors = config.当前主题颜色
        ui_config = config.定义尺寸.get("界面", {})
        
        # 默认导航项（8个，不需要滚动）
        default_nav_items = [
            {"name": "系统", "icon": "SETTINGS"},
            {"name": "策略", "icon": "ROCKET_LAUNCH"},
            {"name": "任务", "icon": "ASSIGNMENT"},
            {"name": "建筑", "icon": "DOMAIN"},
            {"name": "集资", "icon": "SHOPPING_CART"},
            {"name": "账号", "icon": "ACCOUNT_CIRCLE"},
            {"name": "打扫", "icon": "CLEANING_SERVICES"},
            {"name": "打野", "icon": "EXPLORE"},
            {"name": "个性化", "icon": "PALETTE"},
            {"name": "关于", "icon": "INFO"},
        ]
        
        current_nav_items = nav_items if nav_items else default_nav_items
        
        # 默认内边距（从配置中获取）
        if padding is None:
            padding = ft.Padding(
                left=ui_config.get("nav_padding_left", 8),
                right=ui_config.get("nav_padding_right", 8),
                top=ui_config.get("nav_padding_top", 8),
                bottom=ui_config.get("nav_padding_bottom", 8),
            )
        
        # 内部状态
        current_selected = 0
        nav_buttons = []
        
        def handle_nav_click(index: int, name: str):
            nonlocal current_selected
            
            # 更新选中状态
            for i, btn in enumerate(nav_buttons):
                btn.set_selected(i == index)
            
            current_selected = index
            
            if on_nav_change:
                on_nav_change(name)
        
        # 创建导航按钮
        for i, item in enumerate(current_nav_items):
            btn = NavButton.create(
                config=config,
                name=item["name"],
                icon=item["icon"],
                on_click=lambda e, idx=i, name=item["name"]: handle_nav_click(idx, name),
            )
            # 默认选中第一个（通过暴露的接口设置）
            if i == 0:
                btn.set_selected(True)
            nav_buttons.append(btn)
        
        # 导航栏容器
        nav_column = ft.Column(
            nav_buttons,
            spacing=4,
            expand=True,
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
        )
        
        # 导航栏容器（带内边距）
        nav_container = ft.Container(
            content=nav_column,
            padding=padding,
            expand=True,
        )
        
        return nav_container


# 兼容别名
导航栏 = NavBar


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    # 1. 界面配置初始化
    配置 = 界面配置()
    
    # 2. 自动加载用户数据覆盖默认值（在界面配置.__init__中自动完成）
    
    # 3. 正常启动被测模块
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        page.add(NavBar.create(配置))  # 只能更改此处**被测调用模块名称**
    
    ft.run(main)
