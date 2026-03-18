# -*- coding: utf-8 -*-
"""
模块名称：功能通用界面 | 层级：界面模块层
设计思路：
    通用的内容区域容器，用于承载各种具体页面。
    使用通用容器统一风格。
功能列表：
    1. 显示标题
    2. 显示内容区域
    3. 支持动态内容切换
对外接口：
    - create(): 创建功能通用界面
"""

import flet as ft
from typing import Callable
from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider
from 前端.用户设置界面.单元模块.通用容器 import GenericContainer
from 前端.配置.界面配置 import 界面配置

# *** 用户指定变量 - AI不得修改 ***
DEFAULT_WIDTH = 920
DEFAULT_HEIGHT = 540
# *********************************


class ContentArea:
    """功能通用界面 - 界面模块层"""
    
    @staticmethod
    def create(
        title: str = "设置",
        content: ft.Control = None,
        on_back: Callable = None,
        width: int = None,
        height: int = None,
        **kwargs
    ) -> ft.Container:
        """
        创建功能通用界面
        
        参数:
            title: 标题
            content: 内容控件
            on_back: 返回回调
            width: 宽度（默认920）
            height: 高度（默认540）
        
        返回:
            ft.Container: 功能通用界面容器
        """
        配置 = 界面配置()
        
        container_width = width if width is not None else DEFAULT_WIDTH
        container_height = height if height is not None else DEFAULT_HEIGHT
        
        text_primary = ThemeProvider.get_color("text_primary")
        text_secondary = ThemeProvider.get_color("text_secondary")
        border_color = ThemeProvider.get_color("border")
        
        font_size_lg = 配置.获取尺寸("字体", "font_size_lg")
        font_size_md = 配置.获取尺寸("字体", "font_size_md")
        font_size_sm = 配置.获取尺寸("字体", "font_size_sm")
        icon_size_medium = 配置.获取尺寸("图标", "size_medium") or 20
        spacing_sm = 配置.获取尺寸("间距", "spacing_sm")
        spacing_md = 配置.获取尺寸("间距", "spacing_md")
        content_padding = 配置.获取尺寸("界面", "card_padding") or 16
        
        title_row = ft.Row(
            [
                ft.Icon(ft.Icons.SETTINGS, color=text_primary, size=icon_size_medium),
                ft.Text(title, color=text_primary, size=font_size_lg, weight=ft.FontWeight.W_600),
            ],
            spacing=spacing_sm,
        )
        
        if content is None:
            content = ft.Column(
                [
                    ft.Text("功能区域", color=text_secondary, size=font_size_md),
                    ft.Text("请选择左侧导航项查看具体设置", color=text_secondary, size=font_size_sm),
                ],
                spacing=spacing_sm,
            )
        
        main_content = ft.Column(
            [
                content,
            ],
            spacing=0,
        )
        
        container = GenericContainer.create(
            content=main_content,
            width=container_width,
            height=container_height,
            padding=content_padding,
            bgcolor=ThemeProvider.get_color("bg_secondary"),
            border_radius=配置.获取尺寸("界面", "card_radius") or 8,
        )
        
        return container


# *** 调试逻辑 ***
if __name__ == "__main__":
    配置 = 界面配置()
    ThemeProvider.initialize(配置)
    def main(page: ft.Page):
        page.add(ContentArea.create())
    ft.run(main)
