# -*- coding: utf-8 -*-
"""
模块名称：CardContainer
模块功能：基础卡片容器组件
实现步骤：
- 创建圆角卡片容器
- 支持阴影效果
- 支持主题配置
"""

import flet as ft
from typing import Optional

from 前端.游戏设置界面.核心层.配置.界面配置 import UIConfig


USER_WIDTH = None
USER_HEIGHT = 70
USER_PADDING = 12
USER_BORDER_RADIUS = 8


class CardContainer:
    """基础卡片容器"""
    
    @staticmethod
    def create(
        config: UIConfig = None,
        content: ft.Control = None,
        height: int = USER_HEIGHT,
        width: int = USER_WIDTH,
        padding: int = USER_PADDING,
        on_click: callable = None,
    ) -> ft.Container:
        if config is None:
            config = UIConfig()
        
        theme_colors = config.当前主题颜色
        
        return ft.Container(
            content=content,
            width=width,
            height=height,
            padding=padding,
            bgcolor=theme_colors.get("bg_secondary"),
            border_radius=USER_BORDER_RADIUS,
            on_click=on_click,
            animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
        )


# *** 标准测试格式: 仅调用被测模块,AI不得添加数据 ***
if __name__ == "__main__":
    def main(page: ft.Page):
        config = UIConfig()
        card = CardContainer.create(
            config=config,
            content=ft.Text("测试卡片", color=config.当前主题颜色.get("text_primary")),
        )
        page.add(card)
    
    ft.app(target=main)
