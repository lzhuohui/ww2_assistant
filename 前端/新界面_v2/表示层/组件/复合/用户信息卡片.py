# -*- coding: utf-8 -*-
"""
模块名称：UserInfoCard
设计思路: 显示用户头像和基本信息
模块隔离: 复合组件，依赖基础组件
"""

import flet as ft
from typing import Dict, Any

from 前端.新界面_v2.核心.配置.界面配置 import UIConfig
from 前端.新界面_v2.表示层.组件.基础.卡片容器 import CardContainer


# *** 用户指定变量 - AI不得修改, 变量值必须生效 ***
USER_INFO_HEIGHT = 80  # 用户信息卡片高度
# *********************************


class UserInfoCard:
    """用户信息卡片 - 显示用户头像和基本信息"""
    
    @staticmethod
    def create(
        config: UIConfig=None,
        username: str="试用用户",
        status: str="试用剩余 7 天",
        avatar_text: str="帅",
    ) -> ft.Container:
        if config is None:
            config = UIConfig()
        
        theme_colors = config.当前主题颜色
        
        avatar = ft.Container(
            content=ft.Text(avatar_text, size=24, weight=ft.FontWeight.BOLD, color="#FFD700"),
            width=48,
            height=48,
            bgcolor=theme_colors.get("bg_secondary"),
            border_radius=24,
            alignment=ft.Alignment(0, 0),
        )
        
        name_text = ft.Text(username, size=14, weight=ft.FontWeight.BOLD, color=theme_colors.get("text_primary"))
        status_text = ft.Text(status, size=12, color=theme_colors.get("text_secondary"))
        
        content = ft.Row([
            avatar,
            ft.Container(width=12),
            ft.Column([name_text, status_text], spacing=4, alignment=ft.MainAxisAlignment.CENTER),
        ], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER)
        
        return CardContainer.create(
            content=content,
            config=config,
            height=USER_INFO_HEIGHT,
            hover_effect=False,
        )


# *** 调试逻辑 ***
if __name__ == "__main__":
    ft.run(lambda page: page.add(UserInfoCard.create()))
