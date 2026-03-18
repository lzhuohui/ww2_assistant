# -*- coding: utf-8 -*-
"""
输入框 - 单元模块

设计思路:
    独立功能模块，轻量级设计。
    只提供输入框功能，不包含标签。

功能:
    1. 输入框
    2. 值变化回调

数据来源:
    所有配置数据从配置目录获取。

使用场景:
    被组件层模块调用，也可独立使用。

可独立运行调试: python 输入框.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft
from typing import Callable, Optional
from 前端.配置.界面配置 import 界面配置


# *** 用户指定变量 - AI不得修改 ***
# (用户指定的变量放在这里，用户没有指定之前就空着)
# *********************************


class Input:
    """输入框 - 独立功能模块"""
    
    @staticmethod
    def create(
        config: 界面配置,
        value: str = "",
        width: int = None,
        on_change: Callable[[str], None] = None,
        hint_text: str = None,
        password: bool = False,
        **kwargs
    ) -> ft.TextField:
        """
        创建输入框
        
        参数:
            config: 界面配置对象
            value: 初始值
            width: 输入框宽度（可选，默认从配置中获取）
            on_change: 值变化回调
            hint_text: 提示文本（可选）
            password: 是否为密码输入框（可选，默认False）
        
        返回:
            ft.TextField: 输入框控件
        """
        theme_colors = config.当前主题颜色
        
        # 创建输入框（宽度由调用者决定，或使用默认值120）
        input_control = ft.TextField(
            value=value,
            text_size=14,
            color=theme_colors.get("text_primary"),
            bgcolor=theme_colors.get("bg_input"),
            border_color=theme_colors.get("border"),
            focused_border_color=theme_colors.get("accent"),
            border_radius=4,
            dense=True,
            content_padding=ft.Padding(left=8, right=8, top=8, bottom=8),
            width=width if width is not None else 120,
            on_change=lambda e: on_change(e.control.value) if on_change else None,
            on_submit=lambda e: on_change(e.control.value) if on_change else None,
            on_blur=lambda e: on_change(e.control.value) if on_change else None,
            hint_text=hint_text,
            password=password,
            can_reveal_password=password,
        )
        
        # 暴露控制接口
        input_control.get_value = lambda: input_control.value
        input_control.set_value = lambda v: setattr(input_control, "value", v) or input_control.update()
        
        def set_state(enabled: bool):
            """设置启用状态 - 只改变透明度，不改变可操作性"""
            input_control.opacity = 1.0 if enabled else 0.4
            try:
                if input_control.page:
                    input_control.update()
            except RuntimeError:
                pass
        
        input_control.set_state = set_state
        
        return input_control


# 兼容别名
输入框 = Input


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    # 1. 界面配置初始化
    配置 = 界面配置()
    
    # 2. 自动加载用户数据覆盖默认值（在界面配置.__init__中自动完成）
    
    # 3. 正常启动被测模块
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        page.add(Input.create(配置, value="3"))  # 只能更改此处**被测调用模块名称**
    
    ft.run(main)
