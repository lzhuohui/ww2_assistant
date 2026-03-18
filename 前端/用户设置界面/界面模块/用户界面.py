# -*- coding: utf-8 -*-
"""
模块名称：可编辑统一风格用户界面 | 层级：组件层
设计思路：
    在统一风格用户界面基础上，使用可编辑的头像组件。
    保持原始风格，同时支持头像文字编辑功能。

功能：
    1. 显示用户头像（使用可编辑可靠头像）
    2. 显示用户名
    3. 显示授权状态
    4. 根据天数显示不同颜色
    5. Win11风格交互效果
    6. 头像文字可编辑

对外接口：
    - UserInfoCard.create(): 创建用户信息卡片
"""

import flet as ft
from typing import Callable, Optional
from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider
from 前端.用户设置界面.单元模块.通用容器 import GenericContainer
from 前端.用户设置界面.单元模块.用户头像 import Avatar
from 前端.配置.界面配置 import 界面配置

# *** 用户指定变量 - AI不得修改 ***
DEFAULT_WIDTH = 280
DEFAULT_HEIGHT = 80
# *********************************


class UserInfoCard:
    """
    可编辑统一风格用户界面 - 组件层
    
    使用可编辑的头像组件，支持头像文字编辑。
    保持与原始界面相同的风格和功能。
    """
    
    @staticmethod
    def create(
        username: str = "试用用户",
        is_registered: bool = False,
        expire_days: int = 7,
        on_click: Optional[Callable[[], None]] = None,
        on_avatar_text_change: Optional[Callable[[str], None]] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        **kwargs
    ) -> ft.Container:
        """
        创建用户界面
        
        参数:
            username: 用户名
            is_registered: 是否注册
            expire_days: 剩余天数
            on_click: 卡片点击回调
            on_avatar_text_change: 头像文字变化回调
            width: 宽度（默认280）
            height: 高度（默认80）
        
        返回:
            ft.Container: 用户界面容器
        """
        配置 = 界面配置()
        
        container_width = width if width is not None else DEFAULT_WIDTH
        container_height = height if height is not None else DEFAULT_HEIGHT
        
        text_primary = ThemeProvider.get_color("text_primary")
        bg_card = ThemeProvider.get_color("bg_card")
        bg_hover = ThemeProvider.get_color("bg_hover")
        accent = ThemeProvider.get_color("accent")
        
        font_size_md = 配置.获取尺寸("字体", "font_size_md")
        font_size_xs = 配置.获取尺寸("字体", "font_size_xs")
        spacing_md = 配置.获取尺寸("间距", "spacing_md")
        spacing_xs = 配置.获取尺寸("间距", "spacing_xs")
        item_padding = 配置.获取尺寸("界面", "item_padding")
        card_radius = 配置.获取尺寸("界面", "card_radius")
        avatar_size_medium = 配置.获取尺寸("头像", "avatar_size_medium") or 56
        
        if expire_days <= 0:
            status_text = "已过期"
            status_color = "#D13438"
        elif not is_registered:
            status_text = f"试用剩余：{expire_days}天"
            status_color = "#0078D4"
        elif expire_days > 30:
            status_text = f"授权剩余：{expire_days}天"
            status_color = "#107C10"
        elif expire_days > 7:
            status_text = f"授权剩余：{expire_days}天"
            status_color = "#FFB900"
        else:
            status_text = "授权即将到期"
            status_color = "#FF8C00"
        
        avatar = Avatar.create(
            size=avatar_size_medium,
            text=username[0] if username else "帅",
            show_glow=True,
            bg_color=bg_card,
            text_color="#FFD700",
            on_text_change=on_avatar_text_change,
        )
        
        name_label = ft.Text(
            username,
            color=text_primary,
            size=font_size_md,
            weight=ft.FontWeight.BOLD,
        )
        
        status_label = ft.Text(
            status_text,
            color=status_color,
            size=font_size_xs,
        )
        
        labels = ft.Column(
            [
                name_label,
                status_label,
            ],
            spacing=spacing_xs,
            alignment=ft.MainAxisAlignment.CENTER,
        )
        
        content = ft.Row(
            [
                avatar,
                ft.Container(width=spacing_md),
                labels,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        
        card_container = GenericContainer.create(
            content=content,
            width=container_width,
            height=container_height,
            padding=item_padding,
            bgcolor=bg_card,
            border_radius=card_radius,
            alignment=ft.Alignment(0, 0),
            clip_behavior=ft.ClipBehavior.NONE,
        )
        
        default_bg = bg_card
        hover_bg = bg_hover
        border_color = accent
        
        # 保持与其他界面一致的阴影效果和动画效果
        
        # 添加Win11风格悬停效果
        def handle_hover(e):
            if e.data == "true":
                card_container.bgcolor = hover_bg
                card_container.border = ft.border.all(1, border_color)
            else:
                card_container.bgcolor = default_bg
                card_container.border = None
            try:
                card_container.update()
            except:
                pass
        
        # 添加Win11风格点击效果
        def handle_click_down(e):
            # 轻微缩小阴影，模拟按下效果
            card_container.shadow = ft.BoxShadow(
                spread_radius=0,
                blur_radius=6,
                color=ThemeProvider.get_color("shadow"),
                offset=ft.Offset(0, 1),
            )
            try:
                card_container.update()
            except:
                pass
        
        def handle_click_up(e):
            # 恢复阴影效果
            card_container.shadow = ft.BoxShadow(
                spread_radius=1,
                blur_radius=8,
                color=ThemeProvider.get_color("shadow"),
                offset=ft.Offset(0, 3),
            )
            try:
                card_container.update()
            except:
                pass
        
        def handle_click(e):
            pass
        
        # 添加事件处理
        card_container.on_hover = handle_hover
        card_container.on_tap_down = handle_click_down
        card_container.on_tap_up = handle_click_up
        card_container.on_click = handle_click
        
        # 添加自定义点击事件
        if on_click:
            card_container.on_click = lambda e: on_click()
        
        # 添加头像控制方法
        def set_avatar_text(new_text: str):
            """设置头像文字"""
            avatar.set_text(new_text)
        
        def get_avatar_text() -> str:
            """获取头像文字"""
            return avatar.get_text()
        
        def set_avatar_image(url: str):
            """设置头像图片"""
            avatar.set_image(url)
        
        # 添加方法到卡片容器
        card_container.set_avatar_text = set_avatar_text  # type: ignore
        card_container.get_avatar_text = get_avatar_text  # type: ignore
        card_container.set_avatar_image = set_avatar_image  # type: ignore
        
        return card_container


# *** 调试逻辑 ***
if __name__ == "__main__":
    配置 = 界面配置()
    ThemeProvider.initialize(配置)
    def main(page: ft.Page):
        page.add(UserInfoCard.create())
    ft.run(main)