# -*- coding: utf-8 -*-

"""
模块名称：图标标题.py
模块功能：图标+标题+分割线组合组件

实现步骤：
- 创建图标
- 创建标题
- 创建分割线
- 组合布局

职责：
- 左侧标题区显示

不负责：
- 导航逻辑
- 销毁（不需要销毁）
"""

import flet as ft
from typing import Dict, Optional

from 前端.V2.层级5_基础模块.图标 import Icon
from 前端.V2.层级5_基础模块.标签 import Label
from 前端.V2.层级5_基础模块.分割线 import Divider

# ============================================
# 数据和文件接口（前置，方便查看和修改）
# ============================================

DEFAULT_ICON_SIZE = 20
DEFAULT_TITLE_SIZE = 16
DEFAULT_SPACING = 8

# ============================================
# 公开接口
# ============================================

class IconTitle:
    """
    图标标题组件 - 图标+标题+分割线
    
    职责：
    - 左侧标题区显示
    
    不负责：
    - 导航逻辑
    - 销毁（不需要销毁）
    """
    
    @staticmethod
    def create(
        title: str = "标题",
        icon_name: str = "HOME",
        show_divider: bool = True,
        theme_colors: Dict[str, str] = None,
    ) -> ft.Row:
        """
        创建图标标题
        
        参数：
        - title: 标题文本
        - icon_name: 图标名称
        - show_divider: 是否显示分割线
        - theme_colors: 主题颜色
        """
        if theme_colors is None:
            theme_colors = {
                "text_primary": "#000000",
                "accent": "#0078D4",
                "divider": "#E5E5E5",
            }
        
        icon = Icon.create(
            icon_name=icon_name,
            size=DEFAULT_ICON_SIZE,
            color_type="accent",
            theme_colors=theme_colors,
        )
        
        title_text = Label.create(
            text=title,
            size=DEFAULT_TITLE_SIZE,
            weight=ft.FontWeight.BOLD,
            color_type="primary",
            theme_colors=theme_colors,
        )
        
        row_controls = [
            icon,
            ft.Container(width=DEFAULT_SPACING),
            title_text,
        ]
        
        if show_divider:
            row_controls.append(ft.Container(expand=True))
            row_controls.append(Divider.create_horizontal(theme_colors=theme_colors))
        
        return ft.Row(
            row_controls,
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

# *** 标准测试格式: 仅调用被测模块,AI不得添加数据 ***
if __name__ == "__main__":
    def main(page: ft.Page):
        page.title = "图标标题测试"
        
        icon_title = IconTitle.create(
            title="系统设置",
            icon_name="SETTINGS",
        )
        page.add(icon_title)
    
    ft.app(target=main)
