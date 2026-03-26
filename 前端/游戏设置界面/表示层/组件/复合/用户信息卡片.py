# -*- coding: utf-8 -*-
"""
模块名称：UserInfoCard
模块功能：用户信息卡片组件，显示用户头像、名称、授权信息
布局结构：紧凑左右布局（头像左，信息右）
数据对接：
  - 授权账号数量: AccountConfigSection.当前参与数量 / AccountConfigSection.授权数量
  - 到期时间: 授权服务（待对接）
  - 用户名称: 用户配置
共识记录：#011 紧凑左右布局
"""

import flet as ft
from typing import Optional

from 前端.游戏设置界面.核心层.配置.界面配置 import UIConfig
from 前端.游戏设置界面.核心层.常量.全局常量 import GlobalConstants


# *** 用户指定变量: 变量值必须生效,AI不得更改数据 ***
USER_CARD_HEIGHT = 70  # 卡片高度
USER_AVATAR_SIZE = 44  # 头像大小
USER_NAME_SIZE = 14  # 名称字体大小
USER_STATUS_SIZE = 11  # 状态字体大小
# *********************************


class UserInfoCard:
    """用户信息卡片组件 - 紧凑左右布局（共识#011）"""
    
    @staticmethod
    def create(
        config: UIConfig = None,
        user_name: str = "二战风云玩家",
        authorized_count: int = 0,
        max_count: int = None,
        expire_days: int = 30,
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
            border_radius=ft.border_radius.all(24),
            bgcolor=theme_colors.get("bg_tertiary"),
            alignment=ft.alignment.Alignment(0.5, 0.5),
        )
        
        name_text = ft.Text(
            user_name,
            size=USER_NAME_SIZE,
            weight=ft.FontWeight.BOLD,
            color=theme_colors.get("text_primary"),
            text_align=ft.TextAlign.LEFT,
        )
        
        account_text = ft.Text(
            f"授权账号: {authorized_count}/{max_count}",
            size=USER_STATUS_SIZE,
            color=theme_colors.get("text_secondary"),
            text_align=ft.TextAlign.LEFT,
        )
        
        expire_text = ft.Text(
            f"到期时间: {expire_days} 天",
            size=USER_STATUS_SIZE,
            color=theme_colors.get("text_secondary"),
            text_align=ft.TextAlign.LEFT,
        )
        
        right_info_column = ft.Column(
            controls=[
                name_text,
                ft.Container(height=2),
                account_text,
                ft.Container(height=2),
                expire_text,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.START,
            spacing=0,
        )
        
        content = ft.Row(
            controls=[
                avatar,
                ft.Container(width=12),
                right_info_column,
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
        )
        
        container = ft.Container(
            content=content,
            height=USER_CARD_HEIGHT,
            padding=ft.padding.all(16),
            bgcolor=theme_colors.get("bg_primary"),
            alignment=ft.alignment.Alignment(0, 0.5),
        )
        
        def update_authorized_count(count: int):
            account_text.value = f"授权账号: {count}/{max_count}"
            try:
                if container.page:
                    container.update()
            except:
                pass
        
        def update_expire_days(days: int):
            expire_text.value = f"到期时间: {days} 天"
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
        
        container.update_authorized_count = update_authorized_count
        container.update_expire_days = update_expire_days
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
