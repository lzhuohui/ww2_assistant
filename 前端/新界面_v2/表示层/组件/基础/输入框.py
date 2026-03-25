# -*- coding: utf-8 -*-
"""
模块名称：InputBox
设计思路: 独立功能模块，提供输入框功能
模块隔离: 基础组件，不依赖其他业务组件
"""

import flet as ft
from typing import Callable

from 前端.新界面_v2.核心.配置.界面配置 import UIConfig


# *** 用户指定变量 - AI不得修改, 变量值必须生效 ***
USER_WIDTH = 120  # 默认输入框宽度
USER_HEIGHT = 32  # 默认输入框高度
# *********************************


class InputBox:
    """输入框组件"""
    
    @staticmethod
    def create(
        config: UIConfig=None,
        value: str="",
        width: int=USER_WIDTH,
        height: int=USER_HEIGHT,
        hint_text: str="请输入内容",
        password_mode: bool=False,
        enabled: bool=True,
        on_change: Callable[[str], None]=None,
    ) -> ft.Container:
        if config is None:
            config = UIConfig()
        
        theme_colors = config.当前主题颜色
        current_value = [value]
        
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
            hint_text=hint_text,
            password=password_mode,
            can_reveal_password=password_mode,
            opacity=1.0 if enabled else 0.4,
            on_change=lambda e: InputBox._handle_change(current_value, e.control.value, on_change),
            on_submit=lambda e: InputBox._handle_change(current_value, e.control.value, on_change),
            on_blur=lambda e: InputBox._handle_change(current_value, e.control.value, on_change),
        )
        
        container = ft.Container(
            content=input_control,
            width=width,
            height=height,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
        )
        
        def get_value() -> str:
            return current_value[0]
        
        def set_value(new_value: str):
            current_value[0] = new_value
            input_control.value = new_value
            try:
                if input_control.page:
                    input_control.update()
            except:
                pass
        
        def set_enabled(state: bool):
            input_control.opacity = 1.0 if state else 0.4
            try:
                if input_control.page:
                    input_control.update()
            except:
                pass
        
        container.get_value = get_value
        container.set_value = set_value
        container.set_enabled = set_enabled
        
        return container
    
    @staticmethod
    def _handle_change(current_value: list, new_value: str, callback: Callable):
        current_value[0] = new_value
        if callback:
            callback(new_value)


# *** 调试逻辑 ***
if __name__ == "__main__":
    ft.run(lambda page: page.add(InputBox.create()))
