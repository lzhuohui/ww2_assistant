# -*- coding: utf-8 -*-
"""
模块名称：输入框
设计思路: 独立功能模块，提供输入框功能
模块隔离: 基础组件，不依赖其他业务组件
"""

import flet as ft
from typing import Callable

from 前端.新界面_v2.核心.配置.界面配置 import 界面配置


# *** 用户指定变量 - AI不得修改 ***
USER_WIDTH = 120
USER_HEIGHT = 32
# *********************************


class 输入框:
    """输入框组件"""
    
    @staticmethod
    def 创建(
        配置: 界面配置=None,
        值: str="",
        宽度: int=USER_WIDTH,
        高度: int=USER_HEIGHT,
        提示文本: str="请输入内容",
        密码模式: bool=False,
        启用: bool=True,
        变更回调: Callable[[str], None]=None,
    ) -> ft.Container:
        if 配置 is None:
            配置 = 界面配置()
        
        主题颜色 = 配置.当前主题颜色
        当前值 = [值]
        
        输入控件 = ft.TextField(
            value=值,
            text_size=14,
            color=主题颜色.get("text_primary"),
            bgcolor=主题颜色.get("bg_secondary"),
            border_color=主题颜色.get("border"),
            focused_border_color=主题颜色.get("accent"),
            border_radius=6,
            dense=True,
            content_padding=ft.Padding(left=12, right=8, top=8, bottom=8),
            width=宽度,
            hint_text=提示文本,
            password=密码模式,
            can_reveal_password=密码模式,
            opacity=1.0 if 启用 else 0.4,
            on_change=lambda e: 输入框._处理变更(当前值, e.control.value, 变更回调),
            on_submit=lambda e: 输入框._处理变更(当前值, e.control.value, 变更回调),
            on_blur=lambda e: 输入框._处理变更(当前值, e.control.value, 变更回调),
        )
        
        容器 = ft.Container(
            content=输入控件,
            width=宽度,
            height=高度,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
        )
        
        def 获取值() -> str:
            return 当前值[0]
        
        def 设置值(新值: str):
            当前值[0] = 新值
            输入控件.value = 新值
            try:
                if 输入控件.page:
                    输入控件.update()
            except:
                pass
        
        def 设置启用(状态: bool):
            输入控件.opacity = 1.0 if 状态 else 0.4
            try:
                if 输入控件.page:
                    输入控件.update()
            except:
                pass
        
        容器.获取值 = 获取值
        容器.设置值 = 设置值
        容器.设置启用 = 设置启用
        
        return 容器
    
    @staticmethod
    def _处理变更(当前值: list, 新值: str, 回调: Callable):
        当前值[0] = 新值
        if 回调:
            回调(新值)


# *** 调试逻辑 ***
if __name__ == "__main__":
    ft.run(lambda page: page.add(输入框.创建()))
