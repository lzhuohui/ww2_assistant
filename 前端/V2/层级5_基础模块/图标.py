# -*- coding: utf-8 -*-

"""
模块名称：图标.py
模块功能：图标组件

实现步骤：
- 创建图标
- 支持主题颜色
- 支持不同大小

职责：
- 图标显示

不负责：
- 布局
- 销毁（不需要销毁）
"""

import flet as ft
from typing import Dict, Optional

# ============================================
# 数据和文件接口（前置，方便查看和修改）
# ============================================

DEFAULT_SIZE = 20

# ============================================
# 公开接口
# ============================================

class Icon:
    """
    图标组件
    
    职责：
    - 图标显示
    
    不负责：
    - 布局
    - 销毁（不需要销毁）
    """
    
    @staticmethod
    def create(
        icon_name: str = "HOME",
        size: int = DEFAULT_SIZE,
        color_type: str = "accent",
        theme_colors: Dict[str, str] = None,
        opacity: float = 1.0,
    ) -> ft.Icon:
        """
        创建图标
        
        参数：
        - icon_name: 图标名称
        - size: 图标大小
        - color_type: 颜色类型 (accent/primary/secondary)
        - theme_colors: 主题颜色
        - opacity: 透明度
        """
        if theme_colors is None:
            theme_colors = {
                "text_primary": "#FFFFFF",
                "text_secondary": "#C5C5C5",
                "accent": "#0078D4",
            }
        
        color = theme_colors.get(color_type, theme_colors.get("accent"))
        
        icon_attr = getattr(ft.Icons, icon_name.upper(), ft.Icons.HOME)
        
        return ft.Icon(
            icon_attr,
            size=size,
            color=color,
            opacity=opacity,
        )

# *** 标准测试格式: 仅调用被测模块,AI不得添加数据 ***
if __name__ == "__main__":
    def main(page: ft.Page):
        page.title = "图标测试"
        
        row = ft.Row([
            Icon.create("SETTINGS", color_type="accent"),
            Icon.create("HOME", color_type="primary"),
            Icon.create("INFO", color_type="secondary"),
        ])
        page.add(row)
    
    ft.app(target=main)
