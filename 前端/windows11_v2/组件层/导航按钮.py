# -*- coding: utf-8 -*-
"""
导航按钮 - 组件�?
设计思路:
    本模块是组件层模块，提供导航按钮组件�?
功能:
    1. 样式：透明背景，悬停时显示背景色，选中时高�?    2. 结构：图�?+ 文字水平排列
    3. 交互：悬停时背景从中心扩散，选中时保持高�?    4. 动画：背景宽度从0�?00%的扩散动�?
数据来源:
    主题颜色从界面配置动态获取�?    默认配置从界面配置获取�?
使用场景:
    被导航栏模块调用，用于页面切换�?
可独立运行调�? python 导航按钮.py
"""

import flet as ft
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from 原子�?界面配置 import 界面配置
from typing import Callable, Optional


# ==================== 用户指定变量�?====================
# （暂无用户指定的默认值）


class NavButton:  # 导航按钮组件
    """导航按钮组件 - 提供统一的导航按钮功�?""
    
    def __init__(self, config: 界面配置, name: str = "通用设置", icon: str = "SETTINGS", on_click: Callable = None, width: float = 200):
        self._config = config
        self._theme_colors = config.当前主题颜色
        self.name = name
        self._icon = icon
        self._on_click = on_click
        self._width = width
        self._is_selected = False
        self._is_hovering = False
        self._bg_container = None
        self._container_ref = None
        self._icon_control = None
        self._text_control = None
        
        font_config = config.定义尺寸.get("字体", {})
        weight_config = config.定义尺寸.get("字重", {})
        component_config = config.定义尺寸.get("组件", {})
        spacing_config = config.定义尺寸.get("间距", {})
        radius_config = config.定义尺寸.get("圆角", {})
        
        self._font_size = font_config.get("font_size_md", 14)
        self._font_weight = weight_config.get("font_weight_normal", ft.FontWeight.NORMAL)
        self._icon_size = component_config.get("icon_size_medium", 20)
        self._button_height = component_config.get("button_height", 36)
        self._spacing = spacing_config.get("spacing_md", 12)
        self._padding = spacing_config.get("spacing_xs", 4)
        self._border_radius = radius_config.get("radius_sm", 8)
    
    def _get_icon(self, icon_name: str):  # 获取图标控件
        if isinstance(icon_name, str):
            icon_upper = icon_name.upper()
            actual_icon = getattr(ft.Icons, icon_upper, ft.Icons.SETTINGS)
            return ft.Icon(actual_icon, size=self._icon_size, color=self._theme_colors["accent"])
        return ft.Icon(ft.Icons.SETTINGS, size=self._icon_size, color=self._theme_colors["accent"])
    
    def render(self) -> ft.Container:
        self._icon_control = self._get_icon(self._icon)
        self._text_control = ft.Text(self.name, size=self._font_size, weight=self._font_weight, color=self._theme_colors["text_secondary"])
        
        content = ft.Row([
            self._icon_control,
            ft.Container(width=self._spacing),
            self._text_control
        ], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER)

        self._bg_container = ft.Container(
            bgcolor="transparent",
            border_radius=self._border_radius,
            animate=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
            width=0,
            height=self._button_height,
        )

        content_container = ft.Container(
            content=content,
            padding=self._padding,
            width=self._width,
        )

        self._container_ref = ft.Container(
            content=ft.Stack([
                self._bg_container,
                content_container,
            ], alignment=ft.Alignment(0, 0)),
            border_radius=self._border_radius,
            ink=True,
            bgcolor="transparent",
            on_click=self._on_click_handler,
            on_hover=self._on_hover_handler,
            width=self._width,
            height=self._button_height,
        )
        
        return self._container_ref
    
    def _on_click_handler(self, e):  # 点击处理：触发回调，由导航栏模块管理选中状�?        if self._on_click:
            self._on_click(e)
    
    def _update_appearance(self):  # 更新按钮外观
        if self._is_selected:
            self._bg_container.width = self._width
            self._bg_container.bgcolor = self._theme_colors["bg_selected"]
            if self._icon_control:
                self._icon_control.color = "#FFFFFF"
            if self._text_control:
                self._text_control.color = "#FFFFFF"
        elif self._is_hovering:
            self._bg_container.width = self._width
            self._bg_container.bgcolor = self._theme_colors["bg_hover"]
            if self._icon_control:
                self._icon_control.color = self._theme_colors["accent"]
            if self._text_control:
                self._text_control.color = self._theme_colors["text_primary"]
        else:
            self._bg_container.width = 0
            self._bg_container.bgcolor = "transparent"
            if self._icon_control:
                self._icon_control.color = self._theme_colors["accent"]
            if self._text_control:
                self._text_control.color = self._theme_colors["text_secondary"]
        
        try:
            if self._container_ref and self._container_ref.page:
                self._container_ref.update()
        except RuntimeError:
            pass
    
    def _on_hover_handler(self, e):
        self._is_hovering = (e.data == "true")
        self._update_appearance()
    
    def set_selected(self, selected: bool):
        self._is_selected = selected
        self._update_appearance()


# 兼容别名
导航按钮 = NavButton


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    config = 界面配置()
    
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = config.获取颜色("bg_primary")
        
        btn = NavButton(config, name="通用设置", icon="SETTINGS")
        page.add(btn.render())
    
    ft.run(main)

