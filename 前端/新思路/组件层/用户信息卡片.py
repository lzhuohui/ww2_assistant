# -*- coding: utf-8 -*-
"""
用户信息卡片 - 组件层（新思路）

设计思路:
    组装零件，构建用户信息卡片。
    采用装配模式，协调各零件交互。
    使用卡片容器统一风格。

功能:
    1. 组装头像
    2. 组装用户文本
    3. 显示试用/授权状态
    4. 根据天数显示不同颜色

数据来源:
    所有配置数据从配置目录获取。

使用场景:
    被页面层模块调用。

可独立运行调试: python 用户信息卡片.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft
from 配置.界面配置 import 界面配置
from 新思路.零件层.头像 import Avatar
from 新思路.零件层.卡片容器 import CardContainer


class UserInfoCard:
    """用户信息卡片 - 组件层"""
    
    @staticmethod
    def create(
        config: 界面配置,
        username: str = "试用用户",
        is_registered: bool = False,
        expire_days: int = 7,
        on_click: callable = None,
        **kwargs
    ) -> ft.Container:
        """
        创建用户信息卡片
        
        参数:
            config: 界面配置对象
            username: 用户名
            is_registered: 是否注册
            expire_days: 剩余天数
            on_click: 点击回调
        
        返回:
            ft.Container: 用户信息卡片容器
        """
        theme_colors = config.当前主题颜色
        
        # 创建头像（暂时禁用动画，避免控件未添加到页面时的错误）
        avatar = Avatar.create(
            config=config,
            diameter=50,
            text="帅",
            show_glow=False,
            show_scan=False,
        )
        
        # 用户名文本
        username_text = ft.Text(
            username,
            size=16,
            weight=ft.FontWeight.W_600,
            color=theme_colors.get("text_primary"),
        )
        
        # 状态+天数+颜色联动逻辑
        if expire_days <= 0:
            # 已过期
            status_text = "已过期"
            status_color = "#D13438"
        elif not is_registered:
            # 试用用户
            status_text = f"试用剩余：{expire_days}天"
            status_color = "#0078D4"
        elif expire_days > 30:
            # 正常
            status_text = f"授权剩余：{expire_days}天"
            status_color = "#107C10"
        elif expire_days > 7:
            # 提醒
            status_text = f"授权剩余：{expire_days}天"
            status_color = "#FFB900"
        else:
            # 警告
            status_text = "授权即将到期"
            status_color = "#FF8C00"
        
        # 状态文本
        status_text_control = ft.Text(
            status_text,
            size=12,
            color=status_color,
        )
        
        # 用户信息右侧（用户名 + 状态）
        user_info_right = ft.Column(
            [
                username_text,
                ft.Container(height=2),
                status_text_control,
            ],
            spacing=0,
            alignment=ft.MainAxisAlignment.CENTER,
        )
        
        # 用户信息容器（水平排列，居中）
        user_info_content = ft.Row(
            [
                avatar,
                ft.Container(width=12),
                user_info_right,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        
        # 使用卡片容器统一风格
        container = CardContainer.create(
            config=config,
            content=user_info_content,
            on_hover_enabled=True,
        )
        
        # 添加点击事件
        if on_click:
            container.on_click = lambda e: on_click()
        
        return container


用户信息卡片 = UserInfoCard


if __name__ == "__main__":
    配置 = 界面配置()
    
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        page.add(UserInfoCard.create(配置))
    
    ft.run(main)
