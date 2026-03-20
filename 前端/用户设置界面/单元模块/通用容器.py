# -*- coding: utf-8 -*-
"""
模块名称：通用容器
设计思路及联动逻辑:
    提供基础的容器功能，作为其他容器的基类。
    1. 通过ThemeProvider获取主题，无需传入config
    2. 支持状态切换（透明度）和灵活的布局选项
模块隔离原则:
    1. 不直接创建被调用模块的内容
    2. 不覆盖被调用模块的计算结果
    3. 用户指定变量除外
"""

import flet as ft

from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider
from 前端.用户设置界面.配置.界面配置 import 界面配置


# *** 用户指定变量 - AI不得修改, 变量值必须生效 ***
# （用户未指定变量）
# *********************************


class GenericContainer:
    """通用容器 - 纯UI控件，基础容器基类"""
    
    @staticmethod
    def create(
        content: ft.Control=None,
        height: int=100,
        width: int=200,
        padding: int=8,
        margin: int=0,
        bgcolor: str="",
        border_color: str="",
        border_width: int=1,
        border_radius: int=8,
        alignment: ft.Alignment=None,
        enabled: bool=True,
        **kwargs
    ) -> ft.Container:
        配置 = 界面配置()
        
        actual_bgcolor = bgcolor if bgcolor else ThemeProvider.get_color("bg_secondary")
        actual_border_color = border_color if border_color else ThemeProvider.get_color("border")
        actual_border_width = border_width if border_width else 配置.获取尺寸("界面", "card_border_width") or 1
        actual_border_radius = border_radius if border_radius else 配置.获取尺寸("界面", "card_radius") or 8
        
        actual_content = content if content else ft.Text("通用容器内容", color=ThemeProvider.get_color("text_primary"))
        
        shadow_blur = 配置.获取尺寸("阴影", "blur_hover") or 8
        shadow_spread = 配置.获取尺寸("阴影", "spread_hover") or 1
        shadow_offset_y = 配置.获取尺寸("阴影", "offset_y_hover") or 3
        
        shadow = ft.BoxShadow(
            spread_radius=shadow_spread,
            blur_radius=shadow_blur,
            color=ThemeProvider.get_color("shadow"),
            offset=ft.Offset(0, shadow_offset_y),
        )
        
        container = ft.Container(
            content=actual_content,
            height=height,
            width=width,
            padding=padding,
            margin=margin,
            bgcolor=actual_bgcolor,
            border=ft.Border.all(actual_border_width, actual_border_color) if actual_border_width > 0 else None,
            border_radius=actual_border_radius,
            alignment=alignment,
            opacity=1.0 if enabled else 0.4,
            shadow=shadow,
            **kwargs
        )
        
        def set_state(new_enabled: bool):
            container.opacity = 1.0 if new_enabled else 0.4
            try:
                if container.page:
                    container.update()
            except RuntimeError:
                pass
        
        def get_state() -> bool:
            return container.opacity > 0.5
        
        container.set_state = set_state
        container.get_state = get_state
        
        return container


# *** 调试逻辑 ***
if __name__ == "__main__":
    ft.run(lambda page: page.add(GenericContainer.create()))
