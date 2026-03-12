# -*- coding: utf-8 -*-
"""
圆形开关 - 零件层（新思路）

设计思路:
    独立功能模块，轻量级设计。
    圆形开关，开启时填充主题色，关闭时空心灰色。

功能:
    1. 圆形开关
    2. 状态切换动画
    3. 悬停效果
    4. 外部控制接口

数据来源:
    所有配置数据从配置目录获取。

使用场景:
    被组件层模块调用，也可独立使用。

可独立运行调试: python 圆形开关.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft
from typing import Callable, Optional
from 配置.界面配置 import 界面配置


class CircleSwitch:
    """圆形开关 - 独立功能模块"""
    
    @staticmethod
    def create(
        config: 界面配置,
        value: bool = False,
        size: int = 24,
        on_change: Callable[[bool], None] = None,
        enabled: bool = True,
        **kwargs
    ) -> ft.Container:
        """
        创建圆形开关组件
        
        参数:
            config: 界面配置对象
            value: 初始状态
            size: 开关尺寸（直径）
            on_change: 状态变化回调函数
            enabled: 是否可操作
        
        返回:
            ft.Container: 包含圆形开关的容器，具备状态切换能力
        """
        theme_colors = config.当前主题颜色
        
        active_color = theme_colors.get("accent", "#0078D4")
        inactive_border_color = theme_colors.get("text_secondary", "#888888")
        disabled_color = theme_colors.get("text_disabled", "#555555")
        
        # 内部状态
        current_value = value
        current_enabled = enabled
        
        # 创建圆形容器
        circle = ft.Container(
            width=size,
            height=size,
            border_radius=size / 2,
            bgcolor=active_color if current_value else "transparent",
            border=ft.Border.all(2, inactive_border_color if not current_value else "transparent"),
            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
        )
        
        def update_visual():
            """更新视觉状态"""
            if not current_enabled:
                circle.bgcolor = disabled_color if current_value else "transparent"
                circle.border = ft.Border.all(2, disabled_color)
            else:
                circle.bgcolor = active_color if current_value else "transparent"
                circle.border = ft.Border.all(2, inactive_border_color if not current_value else "transparent")
            circle.update()
        
        def set_value(new_value: bool, notify: bool = True):
            """设置状态"""
            nonlocal current_value
            current_value = new_value
            update_visual()
            if notify and on_change and current_enabled:
                on_change(current_value)
        
        def toggle_value():
            """切换状态"""
            if current_enabled:
                set_value(not current_value)
        
        def set_enabled(new_enabled: bool):
            """设置启用状态"""
            nonlocal current_enabled
            current_enabled = new_enabled
            update_visual()
        
        def handle_click(e):
            """处理点击事件"""
            toggle_value()
        
        def handle_hover(e):
            """处理悬停效果"""
            if not current_enabled:
                return
            if e.data == "true":
                if not current_value:
                    circle.border = ft.Border.all(2, active_color)
            else:
                if not current_value:
                    circle.border = ft.Border.all(2, inactive_border_color)
            circle.update()
        
        circle.on_click = handle_click
        circle.on_hover = handle_hover
        
        # 暴露控制接口
        circle.set_value = set_value
        circle.toggle_value = toggle_value
        circle.get_value = lambda: current_value
        circle.set_enabled = set_enabled
        circle.get_enabled = lambda: current_enabled
        
        return circle


# 兼容别名
圆形开关 = CircleSwitch


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    # 1. 界面配置初始化
    配置 = 界面配置()
    
    # 2. 自动加载用户数据覆盖默认值（在界面配置.__init__中自动完成）
    
    # 3. 正常启动被测模块
    def main(page: ft.Page):
        page.padding = 20
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        
        # 测试多个圆形开关
        row = ft.Row([
            CircleSwitch.create(配置, value=False),
            ft.Container(width=20),
            CircleSwitch.create(配置, value=True),
            ft.Container(width=20),
            CircleSwitch.create(配置, value=False, enabled=False),
        ])
        page.add(row)
    
    ft.run(main)
