# -*- coding: utf-8 -*-

"""
模块名称：导航按钮.py
模块功能：导航按钮组件，卡片+按钮组合

实现步骤：
- 创建卡片容器
- 创建图标
- 创建标签
- 组合布局
- 支持选中状态

职责：
- 导航按钮显示
- 导航切换

不负责：
- 销毁（不需要销毁）
"""

import flet as ft
from typing import Callable, Dict, List, Optional

from 前端.V2.层级5_基础模块.卡片容器 import CardContainer
from 前端.V2.层级5_基础模块.图标 import Icon
from 前端.V2.层级5_基础模块.标签 import Label

# ============================================
# 数据和文件接口（前置，方便查看和修改）
# ============================================

DEFAULT_HEIGHT = 36
DEFAULT_ICON_SIZE = 18
DEFAULT_TITLE_SIZE = 14
DEFAULT_PADDING = 8
DEFAULT_SPACING = 2

# ============================================
# 公开接口
# ============================================

class NavigationButton:
    """
    导航按钮组件 - 卡片+按钮组合
    
    职责：
    - 导航按钮显示
    - 导航切换
    
    不负责：
    - 销毁（不需要销毁）
    """
    
    @staticmethod
    def create(
        label: str = "导航",
        icon_name: str = "HOME",
        selected: bool = False,
        on_click: Callable[[str, int], None] = None,
        index: int = 0,
        theme_colors: Dict[str, str] = None,
    ) -> ft.Container:
        """
        创建导航按钮
        
        参数：
        - label: 按钮文本
        - icon_name: 图标名称
        - selected: 是否选中
        - on_click: 点击回调
        - index: 按钮索引
        - theme_colors: 主题颜色
        """
        if theme_colors is None:
            theme_colors = {
                "text_primary": "#000000",
                "text_secondary": "#666666",
                "bg_card": "#FFFFFF",
                "bg_selected": "#0078D4",
                "accent": "#0078D4",
            }
        
        icon_color = theme_colors.get("accent") if selected else theme_colors.get("text_secondary")
        text_color = theme_colors.get("accent") if selected else theme_colors.get("text_primary")
        
        icon = Icon.create(
            icon_name=icon_name,
            size=DEFAULT_ICON_SIZE,
            theme_colors={"accent": icon_color, "text_secondary": icon_color},
        )
        
        text = Label.create(
            text=label,
            size=DEFAULT_TITLE_SIZE,
            weight=ft.FontWeight.BOLD if selected else ft.FontWeight.NORMAL,
            theme_colors={"text_primary": text_color},
        )
        
        content = ft.Row(
            [icon, ft.Container(width=8), text],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        
        container = ft.Container(
            content=content,
            height=DEFAULT_HEIGHT,
            padding=ft.padding.symmetric(horizontal=DEFAULT_PADDING),
            bgcolor=theme_colors.get("bg_selected") if selected else "transparent",
            border_radius=6,
            on_click=lambda e: on_click(label, index) if on_click else None,
        )
        
        def handle_hover(e):
            if not selected:
                if e.data == "true":
                    container.bgcolor = theme_colors.get("bg_card")
                else:
                    container.bgcolor = "transparent"
                try:
                    if container.page:
                        container.update()
                except:
                    pass
        
        container.on_hover = handle_hover
        
        return container


class NavigationButtonGroup:
    """
    导航按钮组 - 管理多个导航按钮
    
    职责：
    - 创建导航按钮组
    - 管理选中状态
    - 导航切换
    """
    
    @staticmethod
    def create(
        items: List[Dict[str, str]] = None,
        selected_index: int = 0,
        on_change: Callable[[str, int], None] = None,
        theme_colors: Dict[str, str] = None,
    ) -> ft.Column:
        """
        创建导航按钮组
        
        参数：
        - items: 导航项列表 [{"label": "系统", "icon": "SETTINGS"}, ...]
        - selected_index: 当前选中索引
        - on_change: 切换回调
        - theme_colors: 主题颜色
        """
        if items is None:
            items = [
                {"label": "系统", "icon": "SETTINGS"},
                {"label": "策略", "icon": "ROCKET_LAUNCH"},
            ]
        
        if theme_colors is None:
            theme_colors = {
                "text_primary": "#000000",
                "text_secondary": "#666666",
                "bg_card": "#FFFFFF",
                "bg_selected": "#0078D4",
                "accent": "#0078D4",
            }
        
        current_selected = [selected_index]
        buttons = []
        
        def handle_click(label: str, index: int):
            if index == current_selected[0]:
                return
            
            old_index = current_selected[0]
            current_selected[0] = index
            
            if on_change:
                on_change(label, index)
        
        for i, item in enumerate(items):
            btn = NavigationButton.create(
                label=item.get("label", ""),
                icon_name=item.get("icon", "HOME"),
                selected=i == selected_index,
                on_click=handle_click,
                index=i,
                theme_colors=theme_colors,
            )
            buttons.append(btn)
        
        return ft.Column(buttons, spacing=DEFAULT_SPACING)

# *** 标准测试格式: 仅调用被测模块,AI不得添加数据 ***
if __name__ == "__main__":
    def main(page: ft.Page):
        page.title = "导航按钮测试"
        
        def on_change(label, index):
            print(f"导航切换: {label}, 索引: {index}")
        
        nav_items = [
            {"label": "系统", "icon": "SETTINGS"},
            {"label": "策略", "icon": "ROCKET_LAUNCH"},
            {"label": "建筑", "icon": "APARTMENT"},
        ]
        
        nav_group = NavigationButtonGroup.create(
            items=nav_items,
            selected_index=0,
            on_change=on_change,
        )
        page.add(nav_group)
    
    ft.app(target=main)
