# -*- coding: utf-8 -*-
"""
模块名称：关于卡片 | 层级：组件模块层
设计思路：
    专门用于"关于"页面的卡片组件。
    展示键值对信息，支持可选的点击事件。

功能：
    1. 展示键值对信息
    2. 支持可点击链接

对外接口：
    - create(): 创建关于卡片
"""

import flet as ft
from typing import Callable, List, Tuple
from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider
from 前端.用户设置界面.配置.界面配置 import 界面配置


class AboutCard:
    """关于卡片 - 组件模块层"""
    
    @staticmethod
    def create(
        config: 界面配置,
        title: str,
        icon: str,
        content_items: List[Tuple[str, str, Callable]],
        **kwargs
    ) -> ft.Container:
        """
        创建关于卡片
        
        参数:
            config: 界面配置对象
            title: 卡片标题
            icon: 图标名称
            content_items: 内容项列表，每项为 (标签, 值, 点击回调)
            **kwargs: 其他参数
        
        返回:
            ft.Container: 关于卡片容器
        """
        theme_colors = config.当前主题颜色
        
        icon_control = ft.Icon(
            getattr(ft.Icons, icon, ft.Icons.INFO),
            size=20,
            color=theme_colors.get("accent"),
        )
        
        title_control = ft.Text(
            title,
            size=16,
            weight=ft.FontWeight.BOLD,
            color=theme_colors.get("text_primary"),
        )
        
        header = ft.Row(
            [icon_control, ft.Container(width=8), title_control],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        
        content_controls = []
        for label, value, on_click in content_items:
            if label == "" and value in ["授权价格", "授权流程", ""]:
                content_controls.append(
                    ft.Container(
                        content=ft.Text(
                            value,
                            size=14,
                            weight=ft.FontWeight.BOLD,
                            color=theme_colors.get("text_primary"),
                        ),
                        margin=ft.Margin(top=8, bottom=4, left=0, right=0),
                    )
                )
            elif label == "":
                content_controls.append(
                    ft.Container(
                        content=ft.Text(
                            value,
                            size=13,
                            color=theme_colors.get("text_secondary"),
                        ),
                        margin=ft.Margin(top=2, bottom=2, left=16, right=0),
                    )
                )
            else:
                value_control = ft.Text(
                    value,
                    size=14,
                    color=theme_colors.get("accent") if on_click else theme_colors.get("text_primary"),
                )
                
                if on_click:
                    value_control = ft.GestureDetector(
                        content=value_control,
                        on_tap=on_click,
                    )
                
                row = ft.Row(
                    [
                        ft.Text(
                            label,
                            size=14,
                            color=theme_colors.get("text_secondary"),
                            width=80,
                        ),
                        value_control,
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                )
                content_controls.append(row)
        
        content = ft.Column(
            [header, ft.Container(height=12)] + content_controls,
            spacing=4,
        )
        
        return ft.Container(
            content=content,
            bgcolor=theme_colors.get("bg_card"),
            border_radius=8,
            padding=16,
            border=ft.border.all(1, theme_colors.get("border")),
        )


# *** 调试逻辑 ***
if __name__ == "__main__":
    配置 = 界面配置()
    ThemeProvider.initialize(配置)
    
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        page.add(AboutCard.create(
            config=配置,
            title="版本信息",
            icon="INFO",
            content_items=[
                ("软件名称", "二战风云辅助工具", None),
                ("当前版本", "v1.0.0", None),
            ],
        ))
    ft.run(main)
