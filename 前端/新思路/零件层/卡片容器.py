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
DEFAULT_WIDTH = 800
DEFAULT_HEIGHT = 100
# *********************************


class CardContainer:
    """卡片容器 - 外轮廓+阴影+边框"""
    
    @staticmethod
    def create(
        config: 界面配置,
        content: ft.Control,
        height: int = None,
        width: int = None,
        expand: bool = False,
        enabled: bool = True,
        on_hover_enabled: bool = True,
        **kwargs
    ) -> ft.Container:
        theme_colors = config.当前主题颜色
        
        ui_config = config.定义尺寸.get("界面", {})
        
        shadow_config = config.定义尺寸.get("阴影", {})
        shadow_blur_default = shadow_config.get("blur_default", 4)
        shadow_blur_hover = shadow_config.get("blur_hover", 12)
        shadow_spread = shadow_config.get("spread", 0)
        shadow_spread_hover = shadow_config.get("spread_hover", 0)
        shadow_offset_y = shadow_config.get("offset_y", 2)
        shadow_offset_y_hover = shadow_config.get("offset_y_hover", 4)
        
        animation_config = config.定义尺寸.get("动画", {})
        animation_duration = animation_config.get("duration_fast", 150)
        animation_curve = getattr(ft.AnimationCurve, animation_config.get("curve", "EASE_OUT"), ft.AnimationCurve.EASE_OUT)
        
        card_border_radius = ui_config.get("card_radius", 8)
        card_border_width = ui_config.get("card_border_width", 1)
        
        风格配置 = config.获取风格配置()
        style_border_radius = 风格配置.get("border_radius", 8)
        style_shadow_blur = 风格配置.get("shadow_blur", 8)
        style_shadow_offset_y = 风格配置.get("shadow_offset_y", 2)
        style_border_width = 风格配置.get("border_width", 1)
        
        final_border_radius = style_border_radius if style_border_radius > 0 else card_border_radius
        final_shadow_blur = style_shadow_blur if style_shadow_blur > 0 else shadow_blur_default
        final_shadow_offset_y = style_shadow_offset_y if style_shadow_blur > 0 else shadow_offset_y
        final_border_width = style_border_width if style_border_width > 0 else card_border_width
        
        container = ft.Container(
            content=content,
            height=height,
            width=width,
            expand=expand,
            bgcolor=theme_colors.get("bg_card"),
            border_radius=final_border_radius,
            border=ft.Border.all(final_border_width, theme_colors.get("border_light")) if final_border_width > 0 else None,
            shadow=ft.BoxShadow(
                spread_radius=shadow_spread,
                blur_radius=final_shadow_blur,
                color=theme_colors.get("shadow"),
                offset=ft.Offset(0, final_shadow_offset_y),
            ) if final_shadow_blur > 0 else None,
            animate=ft.Animation(animation_duration, animation_curve),
            clip_behavior=ft.ClipBehavior.NONE,
        )
        
        if on_hover_enabled:
            def on_hover(e):
                if e.data == "true":
                    container.bgcolor = theme_colors.get("bg_hover")
                    container.border = ft.Border.all(final_border_width, theme_colors.get("border")) if final_border_width > 0 else None
                    container.shadow = ft.BoxShadow(
                        spread_radius=shadow_spread_hover,
                        blur_radius=shadow_blur_hover,
                        color=theme_colors.get("shadow"),
                        offset=ft.Offset(0, shadow_offset_y_hover),
                    ) if final_shadow_blur > 0 else None
                else:
                    container.bgcolor = theme_colors.get("bg_card")
                    container.border = ft.Border.all(final_border_width, theme_colors.get("border_light")) if final_border_width > 0 else None
                    container.shadow = ft.BoxShadow(
                        spread_radius=shadow_spread,
                        blur_radius=final_shadow_blur,
                        color=theme_colors.get("shadow"),
                        offset=ft.Offset(0, final_shadow_offset_y),
                    ) if final_shadow_blur > 0 else None
                container.update()
            
            def on_click_down(e):
                container.bgcolor = theme_colors.get("bg_pressed", "#4A4A4A")
                container.shadow = ft.BoxShadow(
                    spread_radius=shadow_spread_hover,
                    blur_radius=shadow_blur_hover - 2,
                    color=theme_colors.get("shadow"),
                    offset=ft.Offset(0, shadow_offset_y_hover + 1),
                ) if final_shadow_blur > 0 else None
                container.update()
            
            def on_click_up(e):
                container.bgcolor = theme_colors.get("bg_card")
                container.shadow = ft.BoxShadow(
                    spread_radius=shadow_spread,
                    blur_radius=final_shadow_blur,
                    color=theme_colors.get("shadow"),
                    offset=ft.Offset(0, final_shadow_offset_y),
                ) if final_shadow_blur > 0 else None
                container.update()
            
            container.on_hover = on_hover
            container.on_tap_down = on_click_down
            container.on_tap_up = on_click_up
        
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
        page.add(CardContainer.create(配置, content=ft.Text("卡片内容"), height=DEFAULT_HEIGHT, width=DEFAULT_WIDTH))
    
    ft.run(main)
