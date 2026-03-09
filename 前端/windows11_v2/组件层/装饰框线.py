# -*- coding: utf-8 -*-
"""
装饰框线 - 组件层

设计思路:
    本模块是组件层模块，提供装饰框线组件。

功能:
    1. 提供内框线样式
    2. 提供外框线样式
    3. 提供分隔线样式

数据来源:
    主题颜色从界面配置获取。

使用场景:
    被部件层模块调用，提供装饰框线组件。

可独立运行调试: python 装饰框线.py
"""

import flet as ft
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from 原子层.界面配置 import 界面配置


# ==================== 用户指定变量区 ====================
# （暂无用户指定的默认值）


class DecorativeBorder:  # 装饰框线组件
    """装饰框线类 - 提供装饰框线组件"""
    
    @staticmethod
    def inner_border(config: 界面配置, content: ft.Control, **kwargs) -> ft.Container:  # 创建内框线
        padding = kwargs.get("padding", config.获取尺寸("间距", "spacing_md"))
        border_radius = config.获取尺寸("界面", "card_radius") or 8
        
        return ft.Container(
            content=content,
            padding=padding,
            border_radius=border_radius,
            bgcolor=config.获取颜色("bg_secondary"),
            border=ft.Border.all(1, config.获取颜色("border_light")),
        )
    
    @staticmethod
    def outer_border(config: 界面配置, content: ft.Control, **kwargs) -> ft.Container:  # 创建外框线
        padding = kwargs.get("padding", config.获取尺寸("间距", "spacing_lg"))
        border_radius = config.获取尺寸("界面", "card_radius") or 8
        
        return ft.Container(
            content=content,
            padding=padding,
            border_radius=border_radius,
            bgcolor=config.获取颜色("bg_primary"),
            border=ft.Border.all(1, config.获取颜色("border_light")),
        )
    
    @staticmethod
    def divider(config: 界面配置, **kwargs) -> ft.Divider:  # 创建分隔线
        height = kwargs.get("height", config.获取尺寸("间距", "spacing_md"))
        color = kwargs.get("color", config.获取颜色("divider"))
        
        return ft.Divider(height=height, color=color)


# 兼容别名
装饰框线 = DecorativeBorder


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    config = 界面配置()
    
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = config.获取颜色("bg_primary")
        
        inner = DecorativeBorder.inner_border(
            config,
            content=ft.Text("内框线", color=config.获取颜色("text_primary")),
            width=200,
            height=100
        )
        
        outer = DecorativeBorder.outer_border(
            config,
            content=ft.Text("外框线", color=config.获取颜色("text_primary")),
            width=200,
            height=100
        )
        
        div = DecorativeBorder.divider(config)
        
        page.add(ft.Column([inner, div, outer], spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER))
    
    ft.run(main)
