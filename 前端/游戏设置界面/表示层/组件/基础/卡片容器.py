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
from typing import Optional, Callable

import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

try:
    from 核心层.配置.界面配置 import UIConfig
except ImportError:
    # 尝试相对导入
    from ..核心层.配置.界面配置 import UIConfig


# *** 用户指定变量: 变量值必须生效,AI不得更改数据 ***
USER_WIDTH = None  # 卡片宽度(None表示自适应)
USER_HEIGHT = 100  # 卡片高度
USER_PADDING = 6  # 卡片内边距
USER_BORDER_RADIUS = 8  # 卡片圆角
# *********************************


class CardContainer:
    """基础卡片容器 - 支持阴影立体效果"""
    
    @staticmethod
    def create(
        config: UIConfig = None,
        content: ft.Control = None,
        height: int = USER_HEIGHT,
        width: int = USER_WIDTH,
        padding: int = USER_PADDING,
        on_click: Callable = None,
        elevation: int = 1,
    ) -> ft.Container:
        if config is None:
            config = UIConfig()
        
        theme_colors = config.当前主题颜色
        
        shadow = ft.BoxShadow(
            spread_radius=0,
            blur_radius=4 * elevation,
            color="#26000000",
            offset=ft.Offset(0, 2 * elevation),
        )
        
        container = ft.Container(
            content=content,
            width=width,
            height=height,
            padding=padding,
            bgcolor=theme_colors.get("bg_card"),
            border_radius=USER_BORDER_RADIUS,
            on_click=on_click,
            shadow=shadow,
            animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
        )
        
        def handle_hover(e):
            if e.data == "true":
                container.shadow = ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=8,
                    color="#33000000",
                    offset=ft.Offset(0, 4),
                )
            else:
                container.shadow = shadow
            try:
                if container.page:
                    container.update()
            except:
                pass
        
        container.on_hover = handle_hover
        
        return container


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
