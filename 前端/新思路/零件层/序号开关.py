# -*- coding: utf-8 -*-
"""
序号开关 - 零件层（新思路）

设计思路:
    独立功能模块，轻量级设计。
    圆形开关，中心显示序号。

功能:
    1. 圆形开关
    2. 序号显示
    3. 状态切换
    4. 外部控制接口

数据来源:
    所有配置数据从配置目录获取。

使用场景:
    被组件层模块调用，也可独立使用。

可独立运行调试: python 序号开关.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft
from typing import Callable, Optional
from 配置.界面配置 import 界面配置


class NumberSwitch:
    """序号开关 - 独立功能模块"""
    
    @staticmethod
    def create(
        config: 界面配置,
        number: str = "01",
        value: bool = False,
        size: int = 32,
        on_change: Callable[[bool], None] = None,
        **kwargs
    ) -> ft.Container:
        """
        创建序号开关组件
        
        参数:
            config: 界面配置对象
            number: 序号文字
            value: 初始状态
            size: 开关尺寸（直径）
            on_change: 状态变化回调函数
        
        返回:
            ft.Container: 包含序号开关的容器，具备状态切换能力
        """
        theme_colors = config.当前主题颜色
        
        active_color = theme_colors.get("accent", "#0078D4")
        inactive_color = theme_colors.get("bg_secondary", "#E5E5E5")
        text_off_color = theme_colors.get("text_secondary", "#666666")
        
        # 内部状态
        current_value = value
        
        # 创建序号文字
        number_text = ft.Text(
            number,
            size=12,
            color="#FFFFFF" if current_value else text_off_color,
            weight=ft.FontWeight.W_500,
        )
        
        # 创建圆形容器
        circle = ft.Container(
            width=size,
            height=size,
            border_radius=size / 2,
            bgcolor=active_color if current_value else inactive_color,
            content=number_text,
            alignment=ft.Alignment(0, 0),
            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
        )
        
        def set_value(new_value: bool, notify: bool = True):
            """设置状态"""
            nonlocal current_value
            current_value = new_value
            
            circle.bgcolor = active_color if current_value else inactive_color
            number_text.color = "#FFFFFF" if current_value else text_off_color
            circle.update()
            
            if notify and on_change:
                on_change(current_value)
        
        def toggle_value():
            """切换状态"""
            set_value(not current_value)
        
        def handle_click(e):
            """处理点击事件"""
            toggle_value()
        
        circle.on_click = handle_click
        
        # 暴露控制接口
        circle.set_value = set_value
        circle.toggle_value = toggle_value
        circle.get_value = lambda: current_value
        
        return circle


# 兼容别名
序号开关 = NumberSwitch


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    # 1. 界面配置初始化
    配置 = 界面配置()
    
    # 2. 自动加载用户数据覆盖默认值（在界面配置.__init__中自动完成）
    
    # 3. 正常启动被测模块
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        page.add(NumberSwitch.create(配置, number="01", value=False))  # 只能更改此处**被测调用模块名称**
    
    ft.run(main)
