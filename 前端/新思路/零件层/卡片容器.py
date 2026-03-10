# -*- coding: utf-8 -*-
"""
卡片容器 - 零件层（新思路）

设计思路:
    最小模块化的卡片容器，只负责外轮廓、阴影、边框。

功能:
    1. 外轮廓：圆角边框
    2. 阴影：默认阴影+悬停阴影
    3. 悬停效果：背景色变化+阴影增强

数据来源:
    所有配置数据从配置目录获取。

使用场景:
    被组件层模块调用。

可独立运行调试: python 卡片容器.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft
from typing import Optional
from 配置.界面配置 import 界面配置


# *** 用户指定变量 - AI不得修改 ***
# (用户指定的变量放在这里，用户没有指定之前就空着)
# *********************************


class CardContainer:
    """卡片容器 - 外轮廓+阴影+边框"""
    
    @staticmethod
    def create(
        config: 界面配置,
        content: ft.Control,
        height: int = None,
        width: int = None,
        enabled: bool = True,
        **kwargs
    ) -> ft.Container:
        theme_colors = config.当前主题颜色
        
        ui_config = config.定义尺寸.get("界面", {})
        shadow_config = config.定义尺寸.get("阴影", {})
        animation_config = config.定义尺寸.get("动画", {})
        
        shadow_blur_default = shadow_config.get("blur_default", 4)
        shadow_blur_hover = shadow_config.get("blur_hover", 12)
        shadow_spread = shadow_config.get("spread", 1)
        shadow_spread_hover = shadow_config.get("spread_hover", 2)
        shadow_offset_y = shadow_config.get("offset_y", 2)
        shadow_offset_y_hover = shadow_config.get("offset_y_hover", 4)
        
        animation_duration = animation_config.get("duration_fast", 150)
        animation_curve = getattr(ft.AnimationCurve, animation_config.get("curve", "EASE_OUT"), ft.AnimationCurve.EASE_OUT)
        
        card_border_radius = ui_config.get("card_radius", 8)
        card_border_width = ui_config.get("card_border_width", 1)
        
        container = ft.Container(
            content=content,
            height=height,
            width=width,
            bgcolor=theme_colors.get("bg_card"),
            border_radius=card_border_radius,
            border=ft.Border.all(card_border_width, theme_colors.get("border_light")),
            shadow=ft.BoxShadow(
                spread_radius=shadow_spread,
                blur_radius=shadow_blur_default,
                color=theme_colors.get("shadow"),
                offset=ft.Offset(0, shadow_offset_y),
            ),
            animate=ft.Animation(animation_duration, animation_curve),
            clip_behavior=ft.ClipBehavior.NONE,
        )
        
        def on_hover(e):
            if e.data == "true":
                container.bgcolor = theme_colors.get("bg_hover")
                container.border = ft.Border.all(card_border_width, theme_colors.get("border"))
                container.shadow = ft.BoxShadow(
                    spread_radius=shadow_spread_hover,
                    blur_radius=shadow_blur_hover,
                    color=theme_colors.get("shadow"),
                    offset=ft.Offset(0, shadow_offset_y_hover),
                )
                # 添加轻微上浮效果，模拟Win11动画
                container.margin = ft.Margin(0, -2, 0, 2)
            else:
                container.bgcolor = theme_colors.get("bg_card")
                container.border = ft.Border.all(card_border_width, theme_colors.get("border_light"))
                container.shadow = ft.BoxShadow(
                    spread_radius=shadow_spread,
                    blur_radius=shadow_blur_default,
                    color=theme_colors.get("shadow"),
                    offset=ft.Offset(0, shadow_offset_y),
                )
                # 恢复默认边距
                container.margin = ft.Margin(0, 0, 0, 0)
            container.update()
        
        container.on_hover = on_hover
        
        return container


# 兼容别名
卡片容器 = CardContainer


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    # 1. 界面配置初始化
    配置 = 界面配置()
    
    # 2. 自动加载用户数据覆盖默认值（在界面配置.__init__中自动完成）
    
    # 3. 正常启动被测模块
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        page.add(CardContainer.create(配置, content=ft.Text("卡片内容"), height=100, width=400))  # 只能更改此处**被测调用模块名称**
    
    ft.run(main)
