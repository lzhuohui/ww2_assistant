# -*- coding: utf-8 -*-
"""
模块名称：UserInfoCard
模块功能：用户信息卡片组件，显示用户头像、名称、状态
实现步骤：
- 创建用户头像区域
- 显示用户名称和授权状态
- 支持主题配置
"""

import flet as ft
from typing import Optional

from 前端.游戏设置界面.核心层.配置.界面配置 import UIConfig
from 前端.游戏设置界面.核心层.常量.全局常量 import GlobalConstants


USER_CARD_HEIGHT = 100
USER_AVATAR_SIZE = 48
USER_NAME_SIZE = 14
USER_STATUS_SIZE = 12


class UserInfoCard:
    """用户信息卡片组件"""
    
    @staticmethod
    def create(
        config: UIConfig = None,
        user_name: str = "二战风云玩家",
        authorized_count: int = 0,
        max_count: int = None,
    ) -> ft.Container:
        if config is None:
            config = UIConfig()
        
        if max_count is None:
            max_count = GlobalConstants.AUTHORIZED_COUNT
        
        theme_colors = config.当前主题颜色
        
        avatar = ft.Container(
            content=ft.Icon(
                ft.Icons.ACCOUNT_CIRCLE,
                size=USER_AVATAR_SIZE,
                color=theme_colors.get("accent"),
            ),
            width=USER_AVATAR_SIZE,
            height=USER_AVATAR_SIZE,
            border_radius=8,
            bgcolor=theme_colors.get("bg_tertiary"),
            alignment=ft.alignment.Alignment(0.5, 0.5),
        )
        
        name_text = ft.Text(
            user_name,
            size=USER_NAME_SIZE,
            weight=ft.FontWeight.BOLD,
            color=theme_colors.get("text_primary"),
            text_align=ft.TextAlign.CENTER,
        )
        
        status_text = ft.Text(
            f"已授权 {authorized_count}/{max_count}",
            size=USER_STATUS_SIZE,
            color=theme_colors.get("text_secondary"),
            text_align=ft.TextAlign.CENTER,
        )
        
        content = ft.Column(
            controls=[
                avatar,
                ft.Container(height=8),
                name_text,
                ft.Container(height=4),
                status_text,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
        )
        
        container = ft.Container(
            content=content,
            height=USER_CARD_HEIGHT,
            padding=ft.padding.all(12),
            bgcolor=theme_colors.get("bg_primary"),
            alignment=ft.alignment.Alignment(0.5, 0.5),
        )
        
        def update_status(count: int):
            status_text.value = f"已授权 {count}/{max_count}"
            try:
                if container.page:
                    container.update()
            except:
                pass
        
        def update_name(name: str):
            name_text.value = name
            try:
                if container.page:
                    container.update()
            except:
                pass
        
        container.update_status = update_status
        container.update_name = update_name
        
        return container


# *** 标准测试格式: 仅调用被测模块,AI不得添加数据 ***
if __name__ == "__main__":
    def main(page: ft.Page):
        config = UIConfig()
        card = UserInfoCard.create(
            config=config,
            user_name="测试玩家",
            authorized_count=5,
        )
        page.add(card)
    
    ft.app(target=main)
