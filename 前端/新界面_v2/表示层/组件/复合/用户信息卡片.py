# -*- coding: utf-8 -*-
"""
模块名称：用户信息卡片
设计思路: 显示用户头像和基本信息
模块隔离: 复合组件，依赖基础组件
"""

import flet as ft
from typing import Dict, Any

from 前端.新界面_v2.核心.配置.界面配置 import 界面配置
from 前端.新界面_v2.表示层.组件.基础.卡片容器 import 卡片容器


# *** 用户指定变量 - AI不得修改 ***
USER_INFO_HEIGHT = 80
# *********************************


class 用户信息卡片:
    """用户信息卡片 - 显示用户头像和基本信息"""
    
    @staticmethod
    def 创建(
        配置: 界面配置=None,
        用户名: str="试用用户",
        状态: str="试用剩余 7 天",
        头像文字: str="帅",
    ) -> ft.Container:
        if 配置 is None:
            配置 = 界面配置()
        
        主题颜色 = 配置.当前主题颜色
        
        头像 = ft.Container(
            content=ft.Text(头像文字, size=24, weight=ft.FontWeight.BOLD, color="#FFD700"),
            width=48,
            height=48,
            bgcolor=主题颜色.get("bg_secondary"),
            border_radius=24,
            alignment=ft.Alignment(0, 0),
        )
        
        名称文本 = ft.Text(用户名, size=14, weight=ft.FontWeight.BOLD, color=主题颜色.get("text_primary"))
        状态文本 = ft.Text(状态, size=12, color=主题颜色.get("text_secondary"))
        
        内容 = ft.Row([
            头像,
            ft.Container(width=12),
            ft.Column([名称文本, 状态文本], spacing=4, alignment=ft.MainAxisAlignment.CENTER),
        ], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER)
        
        return 卡片容器.创建(
            内容=内容,
            配置=配置,
            高度=USER_INFO_HEIGHT,
            悬停效果=False,
        )


# *** 调试逻辑 ***
if __name__ == "__main__":
    ft.run(lambda page: page.add(用户信息卡片.创建()))
