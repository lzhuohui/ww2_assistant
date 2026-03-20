# -*- coding: utf-8 -*-
"""
模块名称：功能通用界面 | 层级：界面模块层
设计思路：
    通用的内容区域容器，用于承载各种具体页面。
    使用通用容器统一风格。
    使用统一的文本样式管理，确保文字视觉效果一致。
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
from 前端.用户设置界面.单元模块.文本标签 import LabelText
from 前端.用户设置界面.配置.界面配置 import 界面配置

DEFAULT_WIDTH = 920
DEFAULT_HEIGHT = 540


class ContentArea:
    """功能通用界面 - 界面模块层"""
    
    @staticmethod
    def create(
        title: str = "设置",
        icon: str = "SETTINGS",
        content: ft.Control = None,
        width: int = None,
        height: int = None,
        **kwargs
    ) -> ft.Container:
        """
        创建功能通用界面
        
        参数:
            title: 标题
            icon: 图标名称
            content: 内容控件
            width: 宽度
            height: 高度
        
        返回:
            ft.Container: 功能通用界面容器
        """
        配置 = 界面配置()
        theme_colors = 配置.当前主题颜色
        sizes = 配置.定义尺寸
        
        text_primary = theme_colors.get("text_primary", "#FFFFFF")
        text_secondary = theme_colors.get("text_secondary", "#CCCCCC")
        
        font_size_lg = sizes.get("字体", {}).get("font_size_lg", 16)
        font_size_md = sizes.get("字体", {}).get("font_size_md", 14)
        font_size_sm = sizes.get("字体", {}).get("font_size_sm", 12)
        icon_size_medium = sizes.get("图标", {}).get("icon_size_md", 20)
        spacing_sm = sizes.get("间距", {}).get("spacing_sm", 8)
        
        # 创建标题行
        title_row = ft.Row(
            [
                ft.Icon(ft.Icons.SETTINGS, color=text_primary, size=icon_size_medium),
                LabelText.create(
                    text=title,
                    role="h3",
                    win11_style=True
                ),
            ],
            spacing=spacing_sm,
        )
        
        if content is None:
            content = ft.Column(
                [
                    LabelText.create(
                        text="功能区域",
                        role="body",
                        win11_style=True
                    ),
                    LabelText.create(
                        text="请选择左侧导航项查看具体设置",
                        role="caption",
                        win11_style=True
                    ),
                ],
                spacing=spacing_sm,
            )
        
        main_content = ft.Column(
            [
                title_row,
                content,
            ],
            spacing=spacing_sm,
            expand=True,
        )
        
        return GenericContainer.create(
            content=main_content,
            width=width or DEFAULT_WIDTH,
            height=height or DEFAULT_HEIGHT,
            padding=16,
        )


if __name__ == "__main__":
    from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider
    
    配置 = 界面配置()
    ThemeProvider.initialize(配置)
    
    def main(page: ft.Page):
        page.add(ContentArea.create())
    
    ft.run(main)