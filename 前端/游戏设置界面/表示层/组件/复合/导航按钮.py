# -*- coding: utf-8 -*-
"""
模块名称：NavigationButton
模块功能：导航按钮组件，支持选中状态和点击回调
实现步骤：
- 创建导航按钮布局
- 支持图标和文字
- 支持选中状态切换
- 支持点击回调
"""

import flet as ft
from typing import Callable, Optional, Any, Dict, List

import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

try:
    from 核心层.配置.界面配置 import UIConfig
except ImportError:
    # 尝试相对导入
    from ..核心层.配置.界面配置 import UIConfig


# *** 用户指定变量: 变量值必须生效,AI不得更改数据 ***
USER_BUTTON_HEIGHT = 36  # 按钮高度
USER_BUTTON_WIDTH = 220  # 按钮宽度
USER_ICON_SIZE = 18  # 图标大小
USER_TEXT_SIZE = 13  # 文字大小
USER_LEFT_PADDING = 10  # 左侧内边距
# *********************************


class NavigationButton:
    """导航按钮组件"""
    
    @staticmethod
    def create(
        label: str = "导航项",
        icon: str = "HOME",
        selected: bool = False,
        on_click: Callable[[str], None] = None,
        config: UIConfig = None,
    ) -> ft.Container:
        if config is None:
            config = UIConfig()
        
        theme_colors = config.当前主题颜色
        
        is_selected = [selected]
        
        icon_control = ft.Icon(
            getattr(ft.Icons, icon.upper(), ft.Icons.HOME),
            size=USER_ICON_SIZE,
            color=theme_colors.get("accent"),
        )
        
        text_control = ft.Text(
            label,
            size=USER_TEXT_SIZE,
            color=theme_colors.get("accent") if selected else theme_colors.get("text_secondary"),
            weight=ft.FontWeight.W_500 if selected else ft.FontWeight.NORMAL,
        )
        
        left_indicator = ft.Container(
            width=3,
            height=USER_BUTTON_HEIGHT - 8,
            bgcolor=theme_colors.get("accent") if selected else "transparent",
            border_radius=ft.border_radius.all(2),
        )
        
        content = ft.Row(
            controls=[
                ft.Container(width=USER_LEFT_PADDING - 3),
                left_indicator,
                ft.Container(width=USER_LEFT_PADDING - 3),
                icon_control,
                ft.Container(width=8),
                text_control,
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
        )
        
        container = ft.Container(
            content=content,
            width=USER_BUTTON_WIDTH,
            height=USER_BUTTON_HEIGHT,
            bgcolor=theme_colors.get("bg_secondary") if selected else "transparent",
            border_radius=ft.border_radius.all(6),
            on_click=lambda e: handle_click(),
            on_hover=lambda e: handle_hover(e),
            animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
        )
        
        def handle_click():
            if on_click:
                on_click(label)
        
        def handle_hover(e):
            if is_selected[0]:
                return
            if e.data == "true":
                container.bgcolor = theme_colors.get("bg_tertiary")
            else:
                container.bgcolor = "transparent"
            try:
                if container.page:
                    container.update()
            except:
                pass
        
        def set_selected(selected_state: bool):
            is_selected[0] = selected_state
            if selected_state:
                container.bgcolor = theme_colors.get("bg_secondary")
                text_control.color = theme_colors.get("accent")
                text_control.weight = ft.FontWeight.W_500
                left_indicator.bgcolor = theme_colors.get("accent")
            else:
                container.bgcolor = "transparent"
                text_control.color = theme_colors.get("text_secondary")
                text_control.weight = ft.FontWeight.NORMAL
                left_indicator.bgcolor = "transparent"
            try:
                if container.page:
                    container.update()
            except:
                pass
        
        container.set_selected = set_selected
        container.label = label
        
        return container


class NavigationButtonGroup:
    """导航按钮组"""
    
    @staticmethod
    def create(
        items: List[Dict[str, Any]] = None,
        selected_index: int = 0,
        on_change: Callable[[str, int], None] = None,
        config: UIConfig = None,
    ) -> ft.Column:
        if config is None:
            config = UIConfig()
        
        if items is None:
            items = [
                {"label": "系统配置", "icon": "SETTINGS"},
                {"label": "策略配置", "icon": "ROCKET_LAUNCH"},
            ]
        
        buttons = []
        current_selected = [selected_index]
        
        def handle_click(label: str):
            for i, btn in enumerate(buttons):
                if btn.label == label:
                    btn.set_selected(True)
                    current_selected[0] = i
                    if on_change:
                        on_change(label, i)
                else:
                    btn.set_selected(False)
        
        for i, item in enumerate(items):
            btn = NavigationButton.create(
                label=item.get("label", f"导航{i}"),
                icon=item.get("icon", "HOME"),
                selected=(i == selected_index),
                on_click=handle_click,
                config=config,
            )
            buttons.append(btn)
        
        column = ft.Column(
            controls=buttons,
            spacing=2,
        )
        
        def get_selected_index() -> int:
            return current_selected[0]
        
        def get_selected_label() -> str:
            return items[current_selected[0]].get("label", "")
        
        column.get_selected_index = get_selected_index
        column.get_selected_label = get_selected_label
        column.buttons = buttons
        
        return column


# *** 标准测试格式: 仅调用被测模块,AI不得添加数据 ***
if __name__ == "__main__":
    def main(page: ft.Page):
        config = UIConfig()
        
        items = [
            {"label": "系统配置", "icon": "SETTINGS"},
            {"label": "策略配置", "icon": "ROCKET_LAUNCH"},
            {"label": "账号设置", "icon": "ACCOUNT_CIRCLE"},
        ]
        
        def on_change(label, index):
            print(f"选中: {label} (索引: {index})")
        
        nav_group = NavigationButtonGroup.create(
            items=items,
            selected_index=0,
            on_change=on_change,
            config=config,
        )
        page.add(nav_group)
    
    ft.app(target=main)
