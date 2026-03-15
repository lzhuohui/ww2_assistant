# -*- coding: utf-8 -*-
"""
标签输入框 - 零件层（新思路）

设计思路:
    独立功能模块，轻量级设计。
    标签文本 + 输入框组合。

功能:
    1. 标签文本显示
    2. 输入框
    3. 水平排列布局
    4. 值变化回调

数据来源:
    所有配置数据从配置目录获取。

使用场景:
    被组件层模块调用，也可独立使用。

可独立运行调试: python 标签输入框.py
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


class LabelInput:
    """标签输入框 - 独立功能模块"""
    
    @staticmethod
    def create(
        config: 界面配置,
        label: str,
        value: str = "",
        width: int = None,
        on_change: Callable[[str], None] = None,
        hint_text: str = None,
        **kwargs
    ) -> ft.Row:
        """
        创建标签输入框
        
        参数:
            config: 界面配置对象
            label: 标签文本
            value: 初始值
            width: 输入框宽度（可选，默认从配置中获取）
            on_change: 值变化回调
            hint_text: 提示文本（可选）
        
        返回:
            ft.Row: 标签输入框容器
        """
        theme_colors = config.当前主题颜色
        
        # 创建标签文本（自适应宽度）
        label_control = ft.Text(
            label,
            size=14,
            color=theme_colors.get("text_primary"),
            no_wrap=True,
        )
        
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
        )
        
        # 创建行容器（标签紧靠输入框）
        row = ft.Row(
            [
                label_control,
                input_control,
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=4,
        )
        
        # 暴露控制接口
        row.get_value = lambda: input_control.value
        row.set_value = lambda v: setattr(input_control, "value", v) or input_control.update()
        
        def set_state(enabled: bool):
            """设置启用状态 - 只改变透明度，不改变可操作性"""
            label_control.opacity = 1.0 if enabled else 0.4
            if label_control.page:
                label_control.update()
        
        row.set_state = set_state
        
        return row


# 兼容别名
标签输入框 = LabelInput


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    # 1. 界面配置初始化
    配置 = 界面配置()
    
    # 2. 自动加载用户数据覆盖默认值（在界面配置.__init__中自动完成）
    
    # 3. 正常启动被测模块
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        page.add(LabelInput.create(配置, label="尝试次数", value="3"))  # 只能更改此处**被测调用模块名称**
    
    ft.run(main)
