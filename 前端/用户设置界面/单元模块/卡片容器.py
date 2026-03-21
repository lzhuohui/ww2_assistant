# -*- coding: utf-8 -*-
"""
模块名称：卡片容器

设计思路及联动逻辑:
    最小模块化的卡片容器，只负责外轮廓、阴影、边框。
    1. 从配置获取主题颜色、尺寸参数
    2. 创建带圆角、边框、阴影的容器
    3. 添加悬停和点击交互效果

模块隔离原则:
    1. 不直接创建被调用模块的内容
    2. 不覆盖被调用模块的计算结果
    3. 用户指定变量除外
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft
from 前端.用户设置界面.配置.界面配置 import 界面配置


# *** 用户指定变量 - AI不得修改, 变量值必须生效 ***
USER_WIDTH = 500  # 默认卡片宽度
USER_HEIGHT = 150  # 默认卡片高度
# *********************************

# 默认值常量 - 供调用者获取
DEFAULT_WIDTH = USER_WIDTH
DEFAULT_HEIGHT = USER_HEIGHT


class CardContainer:
    """卡片容器 - 外轮廓+阴影+边框"""
    
    @staticmethod
    def create(
        content: ft.Control=None,
        config: 界面配置=None,
        height: int=DEFAULT_HEIGHT,
        width: int=DEFAULT_WIDTH,
        expand: bool=False,
        enabled: bool=True,
        on_hover_enabled: bool=True,
        **kwargs
    ) -> ft.Container:
        try:
            if config is None:
                config = 界面配置()
        except:
            config = None
        
        try:
            theme_colors = config.当前主题颜色 if config else {}
        except:
            theme_colors = {}
        
        try:
            ui_config = config.定义尺寸.get("界面", {}) if config else {}
        except:
            ui_config = {}
        
        try:
            shadow_config = config.定义尺寸.get("阴影", {}) if config else {}
        except:
            shadow_config = {}
        shadow_blur_default = shadow_config.get("blur_default", 4)
        shadow_blur_hover = shadow_config.get("blur_hover", 8)
        shadow_spread = shadow_config.get("spread", 0)
        shadow_spread_hover = shadow_config.get("spread_hover", 1)
        shadow_offset_y = shadow_config.get("offset_y", 2)
        shadow_offset_y_hover = shadow_config.get("offset_y_hover", 3)
        
        try:
            animation_config = config.定义尺寸.get("动画", {}) if config else {}
        except:
            animation_config = {}
        animation_duration = animation_config.get("duration_fast", 167)
        animation_curve = getattr(ft.AnimationCurve, animation_config.get("curve_direct_out", "EASE_OUT"), ft.AnimationCurve.EASE_OUT)
        
        card_border_radius = ui_config.get("card_radius", 8)
        card_border_width = ui_config.get("card_border_width", 1)
        
        try:
            风格配置 = config.获取风格配置() if config else {}
        except:
            风格配置 = {}
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
                try:
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
                except:
                    pass
            
            def on_click_down(e):
                try:
                    container.bgcolor = theme_colors.get("bg_pressed", "#4A4A4A")
                    container.shadow = ft.BoxShadow(
                        spread_radius=shadow_spread,
                        blur_radius=shadow_blur_hover - 2,
                        color=theme_colors.get("shadow"),
                        offset=ft.Offset(0, shadow_offset_y_hover),
                    ) if final_shadow_blur > 0 else None
                    container.update()
                except:
                    pass
            
            def on_click_up(e):
                try:
                    container.bgcolor = theme_colors.get("bg_card")
                    container.shadow = ft.BoxShadow(
                        spread_radius=shadow_spread,
                        blur_radius=final_shadow_blur,
                        color=theme_colors.get("shadow"),
                        offset=ft.Offset(0, final_shadow_offset_y),
                    ) if final_shadow_blur > 0 else None
                    container.update()
                except:
                    pass
            
            container.on_hover = on_hover
            container.on_tap_down = on_click_down
            container.on_tap_up = on_click_up
        
        return container


# *** 调试逻辑 ***
if __name__ == "__main__":
    ft.run(lambda page: page.add(CardContainer.create(content=ft.Text("卡片内容"), height=USER_HEIGHT, width=USER_WIDTH)))
