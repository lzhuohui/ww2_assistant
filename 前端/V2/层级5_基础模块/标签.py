# -*- coding: utf-8 -*-

"""
模块名称：标签.py
模块功能：文本标签组件

实现步骤：
- 创建文本标签
- 支持主题颜色
- 支持不同大小

职责：
- 文本显示

不负责：
- 布局
- 销毁（不需要销毁）
"""

import flet as ft
from typing import Dict, Optional

# ============================================
# 数据和文件接口（前置，方便查看和修改）
# ============================================

DEFAULT_SIZE = 14
DEFAULT_WEIGHT = ft.FontWeight.NORMAL

# ============================================
# 公开接口
# ============================================

class Label:
    """
    标签组件
    
    职责：
    - 文本显示
    
    不负责：
    - 布局
    - 销毁（不需要销毁）
    """
    
    @staticmethod
    def create(
        text: str = "",
        size: int = DEFAULT_SIZE,
        weight: ft.FontWeight = DEFAULT_WEIGHT,
        color_type: str = "primary",
        theme_colors: Dict[str, str] = None,
        no_wrap: bool = True,
        overflow: ft.TextOverflow = ft.TextOverflow.ELLIPSIS,
    ) -> ft.Text:
        """
        创建标签
        
        参数：
        - text: 文本内容
        - size: 字体大小
        - weight: 字体粗细
        - color_type: 颜色类型 (primary/secondary/disabled)
        - theme_colors: 主题颜色
        - no_wrap: 是否不换行
        - overflow: 溢出处理
        """
        if theme_colors is None:
            theme_colors = {
                "text_primary": "#FFFFFF",
                "text_secondary": "#C5C5C5",
                "text_disabled": "#656565",
            }
        
        color_key = f"text_{color_type}" if color_type != "primary" else "text_primary"
        color = theme_colors.get(color_key, theme_colors.get("text_primary"))
        
        return ft.Text(
            text,
            size=size,
            weight=weight,
            color=color,
            no_wrap=no_wrap,
            overflow=overflow,
        )

# *** 标准测试格式: 仅调用被测模块,AI不得添加数据 ***
if __name__ == "__main__":
    def main(page: ft.Page):
        page.title = "标签测试"
        
        column = ft.Column([
            Label.create("主标题", size=16, weight=ft.FontWeight.BOLD),
            Label.create("副标题", size=14, color_type="secondary"),
            Label.create("禁用文本", size=12, color_type="disabled"),
        ])
        page.add(column)
    
    ft.app(target=main)
