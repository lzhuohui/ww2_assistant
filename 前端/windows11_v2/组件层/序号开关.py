# -*- coding: utf-8 -*-
"""
序号开�?- 组件�?
设计思路�?- 圆形开关，中心显示序号
- 通过Container构建控件，实现平滑动画过�?- 匹配Win11风格

功能�?- 支持自定义序号文�?- 支持开关状态切�?- 支持点击回调
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
import flet as ft
from typing import Callable, Optional
from 原子�?界面配置 import 界面配置

# *** 用户指定变量 - AI不得修改 ***
DEFAULT_SIZE = 32          # 开关默认尺寸（直径�?DEFAULT_FONT_SIZE = 12     # 序号字体大小
# *********************************


class NumberSwitch:  # 序号开关组�?    
    def __init__(
        self,
        config: 界面配置,
        number: str = "01",
        value: bool = False,
        size: int = DEFAULT_SIZE,
        on_change: Optional[Callable[[bool], None]] = None,
    ):
        self._config = config
        self._number = number
        self._value = value
        self._size = size
        self._on_change = on_change
        
        theme_colors = config.当前主题颜色
        self._active_color = theme_colors.get("accent", "#0078D4")
        self._inactive_color = theme_colors.get("bg_secondary", "#E5E5E5")
        self._text_off_color = theme_colors.get("text_secondary", "#666666")
        
        self._number_text = ft.Text(
            number,
            size=DEFAULT_FONT_SIZE,
            color="#FFFFFF" if value else self._text_off_color,
            weight=ft.FontWeight.W_500,
        )
        
        self._circle = ft.Container(
            width=size,
            height=size,
            border_radius=size / 2,
            bgcolor=self._active_color if value else self._inactive_color,
            content=self._number_text,
            alignment=ft.Alignment(0, 0),
            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
            on_click=self._handle_click,
        )
    
    def _handle_click(self, e):
        self._value = not self._value
        self._circle.bgcolor = self._active_color if self._value else self._inactive_color
        self._number_text.color = "#FFFFFF" if self._value else self._text_off_color
        self._circle.update()
        if self._on_change:
            self._on_change(self._value)
    
    def create(self):
        return self._circle


if __name__ == "__main__":
    config = 界面配置()
    
    def main(page: ft.Page):
        page.padding = 20
        page.bgcolor = config.当前主题颜色["bg_primary"]
        page.add(ft.Column([
            ft.Text("序号开�?, size=16, weight=ft.FontWeight.W_500),
            ft.Row([
                NumberSwitch(config=config, number="01", value=False).create(),
                NumberSwitch(config=config, number="02", value=True).create(),
                NumberSwitch(config=config, number="03", value=False).create(),
            ], spacing=10),
        ], spacing=20))
    
    ft.run(main)


# 兼容性别�?序号开�?= NumberSwitch

