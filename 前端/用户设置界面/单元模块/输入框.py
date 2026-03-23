# -*- coding: utf-8 -*-
"""
模块名称：输入框
设计思路及联动逻辑:
    独立功能模块，轻量级设计。
    1. 提供输入框功能，不包含标签
    2. 支持值变化回调和统一高度控制
模块隔离原则:
    1. 不直接创建被调用模块的内容
    2. 不覆盖被调用模块的计算结果
    3. 用户指定变量除外
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from typing import Callable, Optional

import flet as ft

from 前端.用户设置界面.配置.界面配置 import 界面配置


# *** 用户指定变量 - AI不得修改, 变量值必须生效 ***
USER_WIDTH = 120  # 默认输入框宽度
USER_HEIGHT = 32  # 默认输入框高度
# *********************************


class Input:
    """输入框 - 独立功能模块"""
    
    @staticmethod
    def create(
        config: 界面配置,
        value: str="",
        width: int=120,
        height: int=32,
        on_change: Callable[[str], None]=None,
        hint_text: str="",
        password: bool=False,
        **kwargs
    ) -> ft.Container:
        theme_colors = config.当前主题颜色
        
        input_control = ft.TextField(
            value=value,
            text_size=14,
            color=theme_colors.get("text_primary"),
            bgcolor=theme_colors.get("bg_secondary"),
            border_color=theme_colors.get("border"),
            focused_border_color=theme_colors.get("accent"),
            border_radius=6,
            dense=True,
            content_padding=ft.Padding(left=12, right=8, top=8, bottom=8),
            width=width,
            on_change=lambda e: on_change(e.control.value) if on_change else None,
            on_submit=lambda e: on_change(e.control.value) if on_change else None,
            on_blur=lambda e: on_change(e.control.value) if on_change else None,
            hint_text=hint_text,
            password=password,
            can_reveal_password=password,
        )
        
        container = ft.Container(
            content=input_control,
            width=width,
            height=height,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
        )
        
        container.get_value = lambda: input_control.value
        container.set_value = lambda v: setattr(input_control, "value", v) or input_control.update()
        
        def set_state(enabled: bool):
            input_control.opacity = 1.0 if enabled else 0.4
            try:
                if input_control.page:
                    input_control.update()
            except RuntimeError:
                pass
        
        container.set_state = set_state
        
        return container


# *** 调试逻辑 ***
if __name__ == "__main__":
    ft.run(lambda page: page.add(Input.create(界面配置())))
