# -*- coding: utf-8 -*-
"""模块名称：卡片容器 | 设计思路：最小模块化的卡片容器，只负责外轮廓、阴影、边框 | 模块隔离原则"""

import flet as ft
from 前端.新界面.核心接口.界面配置 import 界面配置


# *** 用户指定变量 - AI不得修改, 变量值必须生效 ***
USER_WIDTH = 500
USER_HEIGHT = 100
USER_PADDING = 20
# *********************************


class CardContainer:
    """卡片容器 - 外轮廓+阴影+边框"""
    
    @staticmethod
    def create(
        content: ft.Control=None,
        config: 界面配置=None,
        height: int=USER_HEIGHT,
        width: int=USER_WIDTH,
        expand: bool=False,
        on_hover_enabled: bool=True,
        alignment: ft.Alignment=None,
        padding: int=USER_PADDING
    ) -> ft.Container:
        if config is None:
            config = 界面配置()
        
        theme_colors = config.当前主题颜色
        ui_config = config.定义尺寸.get("界面", {})
        shadow_config = config.定义尺寸.get("阴影", {})
        animation_config = config.定义尺寸.get("动画", {})
        
        shadow_blur_default = shadow_config.get("blur_default", 4)
        shadow_blur_hover = shadow_config.get("blur_hover", 8)
        shadow_spread = shadow_config.get("spread", 0)
        shadow_spread_hover = shadow_config.get("spread_hover", 1)
        shadow_offset_y = shadow_config.get("offset_y", 2)
        shadow_offset_y_hover = shadow_config.get("offset_y_hover", 3)
        
        animation_duration = animation_config.get("duration_fast", 167)
        animation_curve = getattr(ft.AnimationCurve, animation_config.get("curve_direct_out", "EASE_OUT"), ft.AnimationCurve.EASE_OUT)
        
        card_border_radius = ui_config.get("card_radius", 8)
        card_border_width = ui_config.get("card_border_width", 1)
        
        风格配置 = config.获取风格配置()
        final_border_radius = 风格配置.get("border_radius", card_border_radius)
        final_shadow_blur = 风格配置.get("shadow_blur", shadow_blur_default)
        final_shadow_offset_y = 风格配置.get("shadow_offset_y", shadow_offset_y)
        final_border_width = 风格配置.get("border_width", card_border_width)
        
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
            alignment=alignment,
            padding=padding,
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
            
            container.on_hover = on_hover
        
        return container


if __name__ == "__main__":
    ft.run(lambda page: page.add(CardContainer.create(content=ft.Text("卡片内容"), height=USER_HEIGHT, width=USER_WIDTH)))
