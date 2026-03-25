# -*- coding: utf-8 -*-
"""
模块名称：InputBox
模块功能：输入框组件
实现步骤：
- 创建文本输入框
- 支持密码模式
- 支持值变更回调
"""

import flet as ft
from typing import Callable, Optional

from 前端.游戏设置界面.核心层.配置.界面配置 import UIConfig


USER_WIDTH = 200


class InputBox:
    """输入框组件"""
    
    @staticmethod
    def create(
        config: UIConfig = None,
        hint_text: str = "",
        value: str = "",
        width: int = USER_WIDTH,
        enabled: bool = True,
        password_mode: bool = False,
        on_change: Callable[[str], None] = None,
    ) -> ft.TextField:
        if config is None:
            config = UIConfig()
        
        theme_colors = config.当前主题颜色
        
        def handle_change(e):
            if on_change:
                on_change(e.control.value)
        
        return ft.TextField(
            value=value,
            hint_text=hint_text,
            width=width,
            disabled=not enabled,
            password=password_mode,
            can_reveal_password=password_mode,
            on_change=handle_change,
            border_color=theme_colors.get("border"),
            focused_border_color=theme_colors.get("accent"),
            text_style=ft.TextStyle(color=theme_colors.get("text_primary")),
            hint_style=ft.TextStyle(color=theme_colors.get("text_disabled")),
        )
    
    @staticmethod
    def get_value(input_box: ft.TextField) -> str:
        """获取输入框当前值"""
        return input_box.value if input_box else ""
    
    @staticmethod
    def set_value(input_box: ft.TextField, value: str) -> None:
        """设置输入框值"""
        if input_box:
            input_box.value = value
    
    @staticmethod
    def set_enabled(input_box: ft.TextField, enabled: bool) -> None:
        """设置启用状态"""
        if input_box:
            input_box.disabled = not enabled


# *** 标准测试格式: 仅调用被测模块,AI不得添加数据 ***
if __name__ == "__main__":
    def main(page: ft.Page):
        config = UIConfig()
        
        def on_change(value):
            print(f"输入: {value}")
        
        input_box = InputBox.create(
            config=config,
            hint_text="请输入内容",
            on_change=on_change,
        )
        page.add(input_box)
    
    ft.app(target=main)
