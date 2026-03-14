# -*- coding: utf-8 -*-
"""
用户信息卡片 - 组件层（新思路）

设计思路:
    组装零件，构建用户信息卡片。
    采用装配模式，协调各零件交互。

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
            status_color = "#D13438"  # 红色
        elif not is_registered:
            # 试用用户
            status_text = f"试用剩余：{expire_days}天"
            status_color = "#0078D4"  # 蓝色
        elif expire_days > 30:
            # 正常
            status_text = f"授权剩余：{expire_days}天"
            status_color = "#107C10"  # 绿色
        elif expire_days > 7:
            # 提醒
            status_text = f"授权剩余：{expire_days}天"
            status_color = "#FFB900"  # 黄色
        else:
            # 警告
            status_text = "授权即将到期"
            status_color = "#FF8C00"  # 橙色
        
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
        user_info = ft.Container(
            content=ft.Row(
                [
                    avatar,
                    ft.Container(width=12),
                    user_info_right,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.Padding(left=12, right=12, top=12, bottom=12),
        )
        
        # 卡片容器
        风格配置 = config.获取风格配置()
        border_radius = 风格配置.get("border_radius", 8)
        shadow_blur = 风格配置.get("shadow_blur", 8)
        shadow_offset_y = 风格配置.get("shadow_offset_y", 2)
        
        container = ft.Container(
            content=user_info,
            bgcolor=theme_colors.get("bg_secondary"),
            width=280,
            border_radius=border_radius,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=shadow_blur,
                color="#00000020",
                offset=ft.Offset(0, shadow_offset_y),
            ) if shadow_blur > 0 else None,
            on_click=lambda e: on_click() if on_click else None,
            on_hover=lambda e: UserInfoCard._on_hover(e, container, theme_colors),
        )
        
        return container
    
    @staticmethod
    def _on_hover(e, container, theme_colors):
        """鼠标悬停效果"""
        if e.data == "true":
            container.bgcolor = theme_colors.get("bg_tertiary", theme_colors.get("bg_secondary"))
        else:
            container.bgcolor = theme_colors.get("bg_secondary")
        container.update()


# 兼容别名
用户信息卡片 = UserInfoCard


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    # 1. 界面配置初始化
    配置 = 界面配置()
    
    # 2. 自动加载用户数据覆盖默认值（在界面配置.__init__中自动完成）
    
    # 3. 正常启动被测模块
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        page.add(UserInfoCard.create(配置))  # 只能更改此处**被测调用模块名称**
    
    ft.run(main)
