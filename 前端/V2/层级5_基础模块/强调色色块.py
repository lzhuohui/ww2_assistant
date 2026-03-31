# -*- coding: utf-8 -*-

"""
模块名称：强调色色块.py
模块功能：强调色选择块

实现步骤：
- 创建强调色块
- 支持选中状态
- 支持点击选择

职责：
- 强调色显示
- 强调色选择

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

class AccentBlock:
    """
    强调色色块组件
    
    职责：
    - 强调色显示
    - 强调色选择
    
    不负责：
    - 布局
    - 销毁（不需要销毁）
    """
    
    @staticmethod
    def create(
        accent_name: str = "blue",
        selected: bool = False,
        on_click: Callable[[str], None] = None,
        size: int = DEFAULT_SIZE,
        accent_colors: Dict = None,
    ) -> ft.Container:
        """
        创建强调色块
        
        参数：
        - accent_name: 强调色名称
        - selected: 是否选中
        - on_click: 点击回调
        - size: 色块大小
        - accent_colors: 强调色配置字典（可选，默认使用DEFAULT_ACCENT_COLORS）
        """
        if accent_colors is None:
            accent_colors = {
                "blue": {"name": "蓝色", "value": "#0078D4"},
            }
        
        accent = accent_colors.get(accent_name, {"name": accent_name, "value": "#0078D4"})
        
        border = ft.border.all(2, accent.get("value")) if selected else ft.border.all(1, "#CCCCCC")
        
        container = ft.Container(
            bgcolor=accent.get("value"),
            width=size,
            height=size,
            border_radius=DEFAULT_BORDER_RADIUS,
            border=border,
            tooltip=accent.get("name", accent_name),
            on_click=lambda e: on_click(accent_name) if on_click else None,
        )
        
        return container

# *** 标准测试格式: 仅调用被测模块,AI不得添加数据 ***
if __name__ == "__main__":
    def main(page: ft.Page):
        page.title = "强调色色块测试"
        
        def on_accent_click(accent_name):
            print(f"选择强调色: {accent_name}")
        
        row = ft.Row([
            AccentBlock.create(name, name == "blue", on_accent_click)
            for name in DEFAULT_ACCENT_COLORS.keys()
        ])
        page.add(row)
    
    ft.app(target=main)
