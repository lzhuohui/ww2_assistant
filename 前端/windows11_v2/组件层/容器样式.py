# -*- coding: utf-8 -*-
"""
容器样式 - 组件层

设计思路：
- 提供统一的容器样式，确保界面风格一致
- 所有样式从配置文件获取，便于主题切换
- 支持自定义参数覆盖默认值

功能：
- 用户信息容器样式
- 导航容器样式
- 内容容器样式
- 卡片容器样式
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
import flet as ft
from 原子层.界面配置 import 界面配置

# *** 用户指定变量 - AI不得修改 ***
# (用户指定的变量放在这里，用户没有指定之前就空着)
# *********************************


class ContainerStyle:  # 容器样式组件
    
    @staticmethod
    def user_info_container(config: 界面配置, content: ft.Control, **kwargs) -> ft.Container:
        theme_colors = config.当前主题颜色
        margin = config.获取尺寸("界面", "peripheral_margin")
        
        return ft.Container(
            content=content,
            width=kwargs.get("width", 240),
            height=kwargs.get("height", 80),
            padding=kwargs.get("padding", margin),
            bgcolor=theme_colors.get("bg_primary"),
        )
    
    @staticmethod
    def nav_container(config: 界面配置, content: ft.Control, **kwargs) -> ft.Container:
        theme_colors = config.当前主题颜色
        margin = config.获取尺寸("界面", "peripheral_margin")
        
        return ft.Container(
            content=content,
            width=kwargs.get("width", 240),
            padding=kwargs.get("padding", margin),
            bgcolor=theme_colors.get("bg_primary"),
        )
    
    @staticmethod
    def content_container(config: 界面配置, content: ft.Control, **kwargs) -> ft.Container:
        theme_colors = config.当前主题颜色
        margin = config.获取尺寸("界面", "peripheral_margin")
        
        return ft.Container(
            content=content,
            padding=kwargs.get("padding", margin),
            bgcolor=theme_colors.get("bg_primary"),
            expand=kwargs.get("expand", True),
            clip_behavior=ft.ClipBehavior.NONE,
        )
    
    @staticmethod
    def card_container(config: 界面配置, content: ft.Control, **kwargs) -> ft.Container:
        theme_colors = config.当前主题颜色
        radius = config.获取尺寸("界面", "card_radius")
        padding = config.获取尺寸("间距", "spacing_lg")
        
        return ft.Container(
            content=content,
            padding=kwargs.get("padding", padding),
            bgcolor=theme_colors.get("bg_card"),
            border_radius=kwargs.get("border_radius", radius),
            border=ft.Border.all(1, theme_colors.get("border_light")),
            width=kwargs.get("width"),
            height=kwargs.get("height"),
        )


if __name__ == "__main__":
    config = 界面配置()
    
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = config.当前主题颜色.get("bg_primary")
        
        user_info = ContainerStyle.user_info_container(
            config,
            content=ft.Text("用户信息", color=config.当前主题颜色.get("text_primary")),
            width=240,
            height=80
        )
        
        nav = ContainerStyle.nav_container(
            config,
            content=ft.Text("导航栏", color=config.当前主题颜色.get("text_primary")),
            width=240
        )
        
        content = ContainerStyle.content_container(
            config,
            content=ft.Text("内容区域", color=config.当前主题颜色.get("text_primary"))
        )
        
        page.add(ft.Row([user_info, nav, content]))
    
    ft.run(main)


# 兼容性别名
容器样式 = ContainerStyle
