# -*- coding: utf-8 -*-

"""
模块名称：主题色块.py
模块功能：主题颜色选择块

实现步骤：
- 创建主题颜色块
- 支持选中状态
- 支持点击选择

职责：
- 主题颜色显示
- 主题选择

不负责：
- 布局
- 销毁（不需要销毁）
"""

import flet as ft
from typing import Callable, Dict, Optional

# ============================================
# 数据和文件接口（前置，方便查看和修改）
# ============================================

DEFAULT_SIZE = 24
DEFAULT_BORDER_RADIUS = 4

# ============================================
# 公开接口
# ============================================

class ThemeBlock:
    """
    主题色块组件
    
    职责：
    - 主题颜色显示
    - 主题选择
    
    不负责：
    - 布局
    - 销毁（不需要销毁）
    """
    
    @staticmethod
    def create(
        theme_name: str = "light",
        selected: bool = False,
        on_click: Callable[[str], None] = None,
        size: int = DEFAULT_SIZE,
        theme_data: Dict = None,
    ) -> ft.Container:
        """
        创建主题色块
        
        参数：
        - theme_name: 主题名称
        - selected: 是否选中
        - on_click: 点击回调
        - size: 色块大小
        - theme_data: 主题数据（由上层从配置服务获取）
        """
        if theme_data is None:
            theme_data = {
                "name": "默认",
                "bg_primary": "#202020",
                "border": "#3D3D3D",
                "accent": "#0078D4",
            }
        
        border = ft.border.all(2, theme_data.get("accent")) if selected else ft.border.all(1, theme_data.get("border"))
        
        container = ft.Container(
            content=ft.Container(
                bgcolor=theme_data.get("bg_primary"),
                border_radius=DEFAULT_BORDER_RADIUS,
                expand=True,
            ),
            width=size,
            height=size,
            border_radius=DEFAULT_BORDER_RADIUS,
            border=border,
            tooltip=theme_data.get("name", theme_name),
            on_click=lambda e: on_click(theme_name) if on_click else None,
        )
        
        return container

# *** 标准测试格式: 仅调用被测模块,AI不得添加数据 ***
if __name__ == "__main__":
    def main(page: ft.Page):
        page.title = "主题色块测试"
        
        def on_theme_click(theme_name):
            print(f"选择主题: {theme_name}")
        
        row = ft.Row([
            ThemeBlock.create("light", True, on_theme_click),
            ThemeBlock.create("dark", False, on_theme_click),
        ])
        page.add(row)
    
    ft.app(target=main)
