# -*- coding: utf-8 -*-
"""
模块名称：功能通用界面
设计思路及联动逻辑:
    通用的内容区域容器，用于承载各种具体页面。
    1. 使用通用容器统一风格
    2. 支持动态内容切换
模块隔离原则:
    1. 不直接创建被调用模块的内容
    2. 不覆盖被调用模块的计算结果
    3. 用户指定变量除外
"""

from typing import Callable

import flet as ft

from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider
from 前端.用户设置界面.单元模块.通用容器 import GenericContainer
from 前端.用户设置界面.单元模块.文本标签 import LabelText
from 前端.用户设置界面.配置.界面配置 import 界面配置


# *** 用户指定变量 - AI不得修改, 变量值必须生效 ***
USER_WIDTH = 920  # 默认宽度
USER_HEIGHT = 540  # 默认高度
# *********************************


class ContentArea:
    """功能通用界面 - 界面模块"""
    
    @staticmethod
    def create(
        title: str="设置",
        icon: str="SETTINGS",
        content: ft.Control=None,
        width: int=USER_WIDTH,
        height: int=USER_HEIGHT,
        **kwargs
    ) -> ft.Container:
        配置 = 界面配置()
        theme_colors = 配置.当前主题颜色
        sizes = 配置.定义尺寸
        
        text_primary = theme_colors.get("text_primary", "#FFFFFF")
        spacing_sm = sizes.get("间距", {}).get("spacing_sm", 8)
        icon_size_medium = sizes.get("图标", {}).get("icon_size_md", 20)
        
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
            width=width,
            height=height,
            padding=16,
        )


# *** 调试逻辑 ***
if __name__ == "__main__":
    ft.run(lambda page: page.add(ContentArea.create()))
