# -*- coding: utf-8 -*-
"""
模块名称：通用容器 | 层级：零件层
设计思路：
    提供基础的容器功能，作为其他容器的基类。
    纯UI控件，无业务逻辑。
    通过ThemeProvider获取主题，无需传入config。
功能列表：
    1. 基础容器功能
    2. 主题颜色支持
    3. 状态切换（透明度）
    4. 灵活的布局选项
对外接口：
    - create(): 创建通用容器
"""

import flet as ft
from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider
from 前端.配置.界面配置 import 界面配置

# *** 用户指定变量 - AI不得修改 ***
# *********************************


class GenericContainer:
    """通用容器 - 纯UI控件，基础容器基类"""
    
    @staticmethod
    def create(
        content: ft.Control = None,
        height: int = None,
        width: int = None,
        padding: int = None,
        margin: int = None,
        bgcolor: str = None,
        border_color: str = None,
        border_width: int = None,
        border_radius: int = None,
        alignment: ft.Alignment = None,
        enabled: bool = True,
        **kwargs
    ) -> ft.Container:
        """
        创建通用容器
        
        参数:
            content: 容器内容（默认为示例文本）
            height: 容器高度（可选）
            width: 容器宽度（可选）
            padding: 内边距（可选）
            margin: 外边距（可选）
            bgcolor: 背景颜色（可选，默认使用主题颜色）
            border_color: 边框颜色（可选，默认使用主题颜色）
            border_width: 边框宽度（可选，默认使用主题尺寸）
            border_radius: 边框圆角（可选，默认使用主题尺寸）
            alignment: 内容对齐方式（可选）
            enabled: 启用状态
        
        返回:
            ft.Container: 通用容器
        """
        配置 = 界面配置()
        
        if bgcolor is None:
            bgcolor = ThemeProvider.get_color("bg_secondary")
        if border_color is None:
            border_color = ThemeProvider.get_color("border")
        if border_width is None:
            border_width = 配置.获取尺寸("界面", "card_border_width") or 1
        
        if border_radius is None:
            border_radius = 配置.获取尺寸("界面", "card_radius") or 8
        
        if content is None:
            content = ft.Text("通用容器内容", color=ThemeProvider.get_color("text_primary"))
        
        # Win11风格阴影：更柔和、更自然
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
            content=content,
            height=height,
            width=width,
            padding=padding,
            margin=margin,
            bgcolor=bgcolor,
            border=ft.border.all(border_width, border_color) if border_width > 0 else None,
            border_radius=border_radius,
            alignment=alignment,
            opacity=1.0 if enabled else 0.4,
            shadow=shadow,  # Win11风格阴影
            **kwargs
        )
        
        # 添加状态切换方法
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
    配置 = 界面配置()
    ThemeProvider.initialize(配置)
    def main(page: ft.Page):
        page.add(GenericContainer.create())
    ft.run(main)
