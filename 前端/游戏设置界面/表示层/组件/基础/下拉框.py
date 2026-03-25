# -*- coding: utf-8 -*-
"""
模块名称：Dropdown
模块功能：下拉框组件
实现步骤：
- 创建下拉选择框
- 支持选项列表
- 支持值变更回调
"""

import flet as ft
from typing import List, Callable, Optional, Any

from 前端.游戏设置界面.核心层.配置.界面配置 import UIConfig


USER_WIDTH = 100


class Dropdown:
    """下拉框组件"""
    
    @staticmethod
    def create(
        options: List[str] = None,
        current_value: str = "",
        width: int = USER_WIDTH,
        enabled: bool = True,
        on_change: Callable[[str], None] = None,
        config: UIConfig = None,
    ) -> ft.Dropdown:
        if config is None:
            config = UIConfig()
        
        if options is None:
            options = ["选项1", "选项2"]
        
        theme_colors = config.当前主题颜色
        
        def handle_change(e):
            if on_change and e.control.value:
                on_change(e.control.value)
        
        return ft.Dropdown(
            options=[ft.dropdown.Option(opt) for opt in options],
            value=current_value if current_value in options else (options[0] if options else ""),
            width=width,
            disabled=not enabled,
            on_change=handle_change,
            border_color=theme_colors.get("border"),
            focused_border_color=theme_colors.get("accent"),
            text_style=ft.TextStyle(color=theme_colors.get("text_primary")),
        )
    
    @staticmethod
    def get_value(dropdown: ft.Dropdown) -> str:
        """获取下拉框当前值"""
        return dropdown.value if dropdown else ""
    
    @staticmethod
    def set_value(dropdown: ft.Dropdown, value: str) -> None:
        """设置下拉框值"""
        if dropdown:
            dropdown.value = value
    
    @staticmethod
    def set_enabled(dropdown: ft.Dropdown, enabled: bool) -> None:
        """设置启用状态"""
        if dropdown:
            dropdown.disabled = not enabled
    
    @staticmethod
    def unload_options(dropdown: ft.Dropdown) -> None:
        """卸载选项（保留当前值）"""
        if dropdown:
            current = dropdown.value
            dropdown.options = [ft.dropdown.Option(current)] if current else []


# *** 标准测试格式: 仅调用被测模块,AI不得添加数据 ***
if __name__ == "__main__":
    def main(page: ft.Page):
        config = UIConfig()
        
        def on_change(value):
            print(f"选择: {value}")
        
        dropdown = Dropdown.create(
            options=["选项A", "选项B", "选项C"],
            current_value="选项A",
            on_change=on_change,
            config=config,
        )
        page.add(dropdown)
    
    ft.app(target=main)
