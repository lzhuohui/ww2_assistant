# -*- coding: utf-8 -*-
"""
椭圆开关 - 组件层

设计思路：
- 自定义Win11风格开关，支持尺寸调整
- 通过Container构建控件，实现平滑动画过渡
- 匹配Win11设置界面的开关风格

功能：
- 支持自定义宽度和高度
- 支持开关状态切换
- 支持点击回调
- 支持悬停效果（关闭状态悬停时边框变蓝）
- 按钮颜色随状态变化（开启白色，关闭灰色）
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
import flet as ft
from typing import Callable, Optional
from 原子层.界面配置 import 界面配置

# *** 用户指定变量 - AI不得修改 ***
DEFAULT_WIDTH = 60       # 开关默认宽度（Win11风格）
DEFAULT_HEIGHT = 26      # 开关默认高度（Win11风格）
# *********************************


class EllipseSwitch:  # 椭圆开关组件
    
    def __init__(
        self,
        config: 界面配置,
        value: bool = False,
        width: int = DEFAULT_WIDTH,
        height: int = DEFAULT_HEIGHT,
        on_change: Optional[Callable[[bool], None]] = None,
    ):
        self._config = config
        self._value = value
        self._width = width
        self._height = height
        self._on_change = on_change
        
        theme_colors = config.当前主题颜色
        self._accent_color = theme_colors.get("accent", "#0078D4")
        self._track_off_color = theme_colors.get("switch_track_off", "#333333")
        self._thumb_on_color = theme_colors.get("switch_thumb_on", "#FFFFFF")
        self._thumb_off_color = theme_colors.get("switch_thumb_off", "#AAAAAA")
        self._border_color = theme_colors.get("switch_border", "#555555")
        
        thumb_diameter = height - 4
        thumb_padding = 2
        
        self._track = ft.Container(
            width=width,
            height=height,
            border_radius=height / 2,
            bgcolor=self._accent_color if value else self._track_off_color,
            animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
            border=ft.Border.all(1, self._border_color) if not value else None,
        )
        
        self._thumb = ft.Container(
            width=thumb_diameter,
            height=thumb_diameter,
            border_radius=thumb_diameter / 2,
            bgcolor=self._thumb_on_color if value else self._thumb_off_color,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=2,
                offset=ft.Offset(0, 1),
                color="#00000030",
            ),
            animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
        )
        
        self._thumb_container = ft.Container(
            content=self._thumb,
            alignment=ft.Alignment(1.0 if value else -1.0, 0),
            padding=ft.Padding(left=thumb_padding, right=thumb_padding, top=0, bottom=0),
            animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
        )
        
        self._stack = ft.Stack(
            [
                self._track,
                self._thumb_container,
            ],
            width=width,
            height=height,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
        )
        
        self._container = ft.Container(
            content=self._stack,
            on_click=self._handle_click,
            on_hover=self._handle_hover,
            border_radius=height / 2,
        )
    
    def _handle_hover(self, e):  # 悬停效果：关闭状态时边框变蓝
        if self._value:
            return
        if e.data == "true":
            self._track.border = ft.Border.all(1, self._accent_color)
        else:
            self._track.border = ft.Border.all(1, self._border_color)
        self._track.update()
    
    def _handle_click(self, e):  # 点击切换状态
        self._value = not self._value
        self._track.bgcolor = self._accent_color if self._value else self._track_off_color
        self._track.border = None if self._value else ft.Border.all(1, self._border_color)
        self._track.update()
        self._thumb.bgcolor = self._thumb_on_color if self._value else self._thumb_off_color
        self._thumb.update()
        self._thumb_container.alignment = ft.Alignment(1.0 if self._value else -1.0, 0)
        self._thumb_container.update()
        if self._on_change:
            self._on_change(self._value)
    
    def create(self):
        return self._container
    
    @property
    def value(self) -> bool:  # 获取当前值
        return self._value
    
    def set_value(self, value: bool, update: bool = True):  # 设置值
        if self._value == value:
            return
        self._value = value
        self._track.bgcolor = self._accent_color if value else self._track_off_color
        self._track.border = None if value else ft.Border.all(1, self._border_color)
        self._thumb.bgcolor = self._thumb_on_color if value else self._thumb_off_color
        self._thumb_container.alignment = ft.Alignment(1.0 if value else -1.0, 0)
        if update:
            self._track.update()
            self._thumb.update()
            self._thumb_container.update()


if __name__ == "__main__":
    config = 界面配置()
    
    def main(page: ft.Page):
        page.padding = 20
        page.bgcolor = config.当前主题颜色["bg_primary"]
        page.add(ft.Column([
            ft.Text("Win11风格开关测试", size=16, weight=ft.FontWeight.W_500, color=config.获取颜色("text_primary")),
            ft.Divider(height=20, color="transparent"),
            ft.Row([
                ft.Text("关闭状态:", color=config.获取颜色("text_primary")),
                EllipseSwitch(config=config, value=False).create(),
            ], spacing=10),
            ft.Divider(height=10, color="transparent"),
            ft.Row([
                ft.Text("开启状态:", color=config.获取颜色("text_primary")),
                EllipseSwitch(config=config, value=True).create(),
            ], spacing=10),
        ], spacing=10))
    
    ft.run(main)


# 兼容别名
椭圆开关 = EllipseSwitch
