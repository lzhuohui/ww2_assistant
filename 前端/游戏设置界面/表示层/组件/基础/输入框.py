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

import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

try:
    from 核心层.配置.界面配置 import UIConfig
except ImportError:
    # 尝试相对导入
    from ..核心层.配置.界面配置 import UIConfig


# *** 用户指定变量: 变量值必须生效,AI不得更改数据 ***
USER_WIDTH = 120  # 输入框宽度
USER_HEIGHT = 30  # 输入框高度
# *********************************


class InputBox:
    """输入框组件"""
    
    @staticmethod
    def create(
        config: UIConfig = None,
        hint_text: str = "",
        value: str = "",
        width: int = USER_WIDTH,
        height: int = USER_HEIGHT,
        enabled: bool = True,
        password_mode: bool = False,
        max_length: int = None,
        on_change: Callable[[str], None] = None,
    ) -> ft.TextField:
        if config is None:
            config = UIConfig()
        
        theme_colors = config.当前主题颜色
        
        def handle_change(e):
            new_value = e.control.value
            if max_length and new_value and len(new_value) > max_length:
                e.control.value = new_value[:max_length]
                new_value = e.control.value
            if on_change:
                on_change(new_value)
        
        return ft.TextField(
            value=value,
            hint_text=hint_text,
            width=width,
            height=height,
            disabled=not enabled,
            password=password_mode,
            can_reveal_password=password_mode,
            on_change=handle_change,
            border_color=theme_colors.get("border"),
            focused_border_color=theme_colors.get("accent"),
            text_style=ft.TextStyle(color=theme_colors.get("text_primary")),
            hint_style=ft.TextStyle(color=theme_colors.get("text_disabled")),
            text_align=ft.TextAlign.LEFT,
            content_padding=ft.padding.symmetric(horizontal=10, vertical=5),
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
