# -*- coding: utf-8 -*-
"""
主题色块 - 零件层（新思路）

设计思路:
    独立功能模块，轻量级设计。
    主题预览色块，包含竖排文字和色块。

功能:
    1. 显示主题名称（竖排文字）
    2. 显示主题预览色块
    3. 支持选中状态边框
    4. 支持点击事件

数据来源:
    所有配置数据从配置目录获取。

使用场景:
    被组件层模块调用，也可独立使用。

可独立运行调试: python 主题色块.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft
from typing import Callable, Optional
from 配置.界面配置 import 界面配置


# *** 用户指定变量 - AI不得修改 ***
# (用户指定的变量放在这里，用户没有指定之前就空着)
# *********************************


class ThemeColorBlock:
    """主题色块 - 独立功能模块"""
    
    @staticmethod
    def create(
        config: 界面配置,
        theme_name: str,
        bg_color: str,
        accent_color: str = None,
        is_selected: bool = False,
        block_size: int = None,
        text_size: int = None,
        on_click: Callable[[str], None] = None,
        **kwargs
    ) -> ft.Container:
        """
        创建主题色块
        
        参数:
            config: 界面配置对象
            theme_name: 主题名称
            bg_color: 背景颜色
            accent_color: 强调色（选中边框颜色）
            is_selected: 是否选中
            block_size: 色块大小（可选，默认从配置中获取）
            text_size: 文字大小（可选，默认从配置中获取）
            on_click: 点击回调
        
        返回:
            ft.Container: 主题色块容器
        """
        theme_colors = config.当前主题颜色
        ui_config = config.定义尺寸.get("组件", {})
        font_config = config.定义尺寸.get("字体", {})
        
        # 从配置文件获取默认值
        default_block_size = ui_config.get("theme_block_size", 48)
        default_text_size = font_config.get("font_size_sm", 12)
        current_block_size = block_size if block_size is not None else default_block_size
        current_text_size = text_size if text_size is not None else default_text_size
        
        # 创建竖排文字
        vertical_text = ft.Column(
            [ft.Text(char, size=current_text_size, color=theme_colors.get("text_primary")) for char in theme_name],
            spacing=0,
            alignment=ft.MainAxisAlignment.CENTER,
        )
        
        # 创建色块
        color_block = ft.Container(
            width=current_block_size,
            height=current_block_size,
            bgcolor=bg_color,
            border_radius=8,
            border=ft.Border.all(3, accent_color if is_selected else "transparent"),
            ink=True,
        )
        
        # 创建完整卡片（文字在左，色块在右）
        card = ft.Container(
            content=ft.Row(
                [
                    ft.Container(
                        content=vertical_text,
                        width=20,
                        alignment=ft.Alignment(0, 0),
                    ),
                    color_block,
                ],
                spacing=4,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            on_click=lambda e: on_click(theme_name) if on_click else None,
            height=current_block_size,  # 设置高度，与色块高度一致
        )
        
        # 暴露控制接口
        def set_selected(selected: bool):
            """设置选中状态"""
            color_block.border = ft.Border.all(3, accent_color if selected else "transparent")
            if card.page:
                card.update()
        
        def set_state(enabled: bool):
            """设置启用状态"""
            card.opacity = 1.0 if enabled else 0.4
            card.disabled = not enabled
            if card.page:
                card.update()
        
        card.set_selected = set_selected
        card.set_state = set_state
        card._enabled = True
        
        return card


# 兼容别名
主题色块 = ThemeColorBlock


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    # 1. 界面配置初始化
    配置 = 界面配置()
    
    # 2. 自动加载用户数据覆盖默认值（在界面配置.__init__中自动完成）
    
    # 3. 正常启动被测模块
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        page.add(ThemeColorBlock.create(配置, "浅色", "#FFFFFF", "#0078D4", True))  # 只能更改此处**被测调用模块名称**
    
    ft.run(main)
