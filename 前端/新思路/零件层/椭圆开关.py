# -*- coding: utf-8 -*-
"""
椭圆开关 - 零件层（新思路）

设计思路:
    独立功能模块，轻量级设计。
    Win11风格椭圆开关，支持状态切换。

功能:
    1. 椭圆形开关
    2. 状态切换动画
    3. 悬停效果
    4. 外部控制接口

数据来源:
    所有配置数据从配置目录获取。

使用场景:
    被组件层模块调用，也可独立使用。

可独立运行调试: python 椭圆开关.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft
from typing import Callable, Optional
from 配置.界面配置 import 界面配置


# *** 用户指定变量 - AI不得修改 ***
# 开关尺寸
DEFAULT_WIDTH = 60
DEFAULT_HEIGHT = 26
# *********************************


class EllipseSwitch:
    """椭圆开关 - 独立功能模块"""
    
    @staticmethod
    def create(
        config: 界面配置,
        value: bool = False,
        width: int = None,
        height: int = None,
        on_change: Callable[[bool], None] = None,
        **kwargs
    ) -> ft.Container:
        """
        创建椭圆开关组件
        
        参数:
            config: 界面配置对象
            value: 初始状态
            width: 开关宽度（可选，默认从配置中获取）
            height: 开关高度（可选，默认从配置中获取）
            on_change: 状态变化回调
        
        返回:
            ft.Container: 开关容器
        """
        theme_colors = config.当前主题颜色
        
        # 使用用户指定的默认值
        current_width = width if width is not None else DEFAULT_WIDTH
        current_height = height if height is not None else DEFAULT_HEIGHT
        
        accent_color = theme_colors.get("accent", "#0078D4")
        track_off_color = theme_colors.get("switch_track_off", "#333333")
        thumb_on_color = theme_colors.get("switch_thumb_on", "#FFFFFF")
        thumb_off_color = theme_colors.get("switch_thumb_off", "#AAAAAA")
        border_color = theme_colors.get("switch_border", "#555555")
        
        thumb_diameter = current_height - 4
        thumb_padding = 2
        
        # 内部状态
        current_value = value
        
        # 创建轨道
        track = ft.Container(
            width=current_width,
            height=current_height,
            border_radius=current_height / 2,
            bgcolor=accent_color if value else track_off_color,
            animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
            border=ft.Border.all(1, border_color) if not value else None,
        )
        
        # 创建滑块
        thumb = ft.Container(
            width=thumb_diameter,
            height=thumb_diameter,
            border_radius=thumb_diameter / 2,
            bgcolor=thumb_on_color if value else thumb_off_color,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=2,
                offset=ft.Offset(0, 1),
                color="#00000030",
            ),
            animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
        )
        
        # 创建滑块容器
        thumb_container = ft.Container(
            content=thumb,
            alignment=ft.Alignment(1.0 if value else -1.0, 0),
            padding=ft.Padding(left=thumb_padding, right=thumb_padding, top=0, bottom=0),
            animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
        )
        
        # 创建Stack
        stack = ft.Stack(
            [track, thumb_container],
            width=current_width,
            height=current_height,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
        )
        
        def set_value(new_value: bool, notify: bool = True):
            """设置状态"""
            nonlocal current_value
            current_value = new_value
            
            track.bgcolor = accent_color if new_value else track_off_color
            track.border = None if new_value else ft.Border.all(1, border_color)
            track.update()
            
            thumb.bgcolor = thumb_on_color if new_value else thumb_off_color
            thumb.update()
            
            thumb_container.alignment = ft.Alignment(1.0 if new_value else -1.0, 0)
            thumb_container.update()
            
            if notify and on_change:
                on_change(current_value)
        
        def toggle_value():
            """切换状态"""
            set_value(not current_value)
        
        def handle_click(e):
            """处理点击"""
            toggle_value()
        
        def handle_hover(e):
            """处理悬停"""
            if current_value:
                return
            if e.data == "true":
                track.border = ft.Border.all(1, accent_color)
            else:
                track.border = ft.Border.all(1, border_color)
            track.update()
        
        container = ft.Container(
            content=stack,
            on_click=handle_click,
            on_hover=handle_hover,
            border_radius=height / 2,
        )
        
        # 暴露控制接口
        container.set_value = set_value
        container.toggle_value = toggle_value
        container.get_value = lambda: current_value
        
        return container


# 兼容别名
椭圆开关 = EllipseSwitch


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    # 1. 界面配置初始化
    配置 = 界面配置()
    
    # 2. 自动加载用户数据覆盖默认值（在界面配置.__init__中自动完成）
    
    # 3. 正常启动被测模块
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        page.add(EllipseSwitch.create(配置, value=False))  # 只能更改此处**被测调用模块名称**
    
    ft.run(main)
