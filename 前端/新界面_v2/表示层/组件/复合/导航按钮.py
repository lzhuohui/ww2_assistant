# -*- coding: utf-8 -*-
"""
模块名称：NavigationButton
设计思路: 可点击的导航按钮，支持选中状态，Win11风格背景块
模块隔离: 复合组件，依赖基础组件
"""

import flet as ft
from typing import Dict, Any, Callable

from 前端.新界面_v2.核心.配置.界面配置 import UIConfig


# *** 用户指定变量 - AI不得修改, 变量值必须生效 ***
# （用户未指定变量）
# *********************************


class NavigationButton:
    """导航按钮 - 可点击的导航按钮，支持选中状态，Win11风格背景块"""
    
    @staticmethod
    def create(
        config: UIConfig=None,
        item: Dict[str, Any]=None,
        index: int=0,
        current_selection: list=None,
        on_navigate: Callable=None,
        selected: bool=False,
        auto_height: bool=False,
    ) -> ft.Container:
        if config is None:
            config = UIConfig()
        
        if item is None:
            item = {"id": "未命名", "icon": "INFO"}
        
        if current_selection is None:
            current_selection = [0]
        
        theme_colors = config.当前主题颜色
        icon_name = item.get("icon", "INFO")
        
        selected_color = theme_colors.get("text_primary")
        unselected_color = theme_colors.get("text_secondary")
        selected_bg = theme_colors.get("accent")
        hover_bg = theme_colors.get("bg_card")
        
        icon_control = ft.Icon(
            getattr(ft.Icons, icon_name, ft.Icons.INFO),
            size=18,
            color=selected_color if selected else unselected_color,
        )
        
        text_control = ft.Text(
            item["id"],
            size=13,
            color=selected_color if selected else unselected_color,
        )
        
        button_content = ft.Row([
            icon_control,
            ft.Container(width=8),
            text_control,
        ], spacing=0, vertical_alignment=ft.CrossAxisAlignment.CENTER)
        
        background_block = ft.Container(
            bgcolor=selected_bg if selected else "transparent",
            border_radius=6,
            animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
            width=float("inf") if selected else 0,
            height=float("inf"),
        )
        
        content_container = ft.Container(
            content=button_content,
            padding=ft.Padding(left=12, right=12, top=8, bottom=8),
            alignment=ft.Alignment(-1, 0),
        )
        
        stack = ft.Stack([
            background_block,
            content_container,
        ], alignment=ft.Alignment(-1, 0))
        
        button = ft.Container(
            content=stack,
            bgcolor=theme_colors.get("bg_secondary"),
            border_radius=6,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
        )
        
        if auto_height:
            button.expand = True
        
        selected_state = [selected]
        
        def update_selected(is_selected: bool):
            selected_state[0] = is_selected
            if is_selected:
                background_block.bgcolor = selected_bg
                background_block.width = float("inf")
                icon_control.color = selected_color
                text_control.color = selected_color
            else:
                background_block.bgcolor = "transparent"
                background_block.width = 0
                icon_control.color = unselected_color
                text_control.color = unselected_color
            try:
                if button.page:
                    button.update()
            except:
                pass
        
        def handle_hover(e):
            if not selected_state[0]:
                if e.data == "true":
                    background_block.bgcolor = hover_bg
                    background_block.width = float("inf")
                else:
                    background_block.bgcolor = "transparent"
                    background_block.width = 0
                try:
                    if button.page:
                        button.update()
                except:
                    pass
        
        button.on_hover = handle_hover
        
        if on_navigate:
            button.on_click = lambda e, idx=index: on_navigate(idx)
        
        button.update_selected = update_selected
        
        return button
    
    @staticmethod
    def update_selection(button: ft.Container, selected: bool, config: UIConfig=None) -> None:
        """更新按钮的选中状态"""
        if hasattr(button, 'update_selected'):
            button.update_selected(selected)


# *** 调试逻辑 ***
if __name__ == "__main__":
    ft.run(lambda page: page.add(NavigationButton.create()))
