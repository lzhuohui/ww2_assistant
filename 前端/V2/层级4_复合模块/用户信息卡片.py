# -*- coding: utf-8 -*-

"""
模块名称：用户信息卡片.py
模块功能：用户信息卡片组件，紧凑左右布局

实现步骤：
- 从配置服务获取用户信息
- 创建头像（左）
- 创建用户名、授权信息、到期时间（右）
- 左右布局

职责：
- 用户信息显示
- 从配置服务获取数据
- 更新授权数量

不负责：
- 销毁（不需要销毁）
"""

import flet as ft
from typing import Dict, Optional, Any

# ============================================
# 数据和文件接口（前置，方便查看和修改）
# ============================================

DEFAULT_CARD_HEIGHT = 70
DEFAULT_AVATAR_SIZE = 44
DEFAULT_NAME_SIZE = 14
DEFAULT_STATUS_SIZE = 11
DEFAULT_PADDING = 16

DEFAULT_USERNAME = "二战风云玩家"
DEFAULT_AUTHORIZED_COUNT = 0
DEFAULT_MAX_ACCOUNTS = 15
DEFAULT_EXPIRE_DAYS = 30

# ============================================
# 公开接口
# ============================================

class UserCard:
    """
    用户信息卡片组件 - 紧凑左右布局
    
    职责：
    - 用户信息显示
    - 从配置服务获取数据
    - 更新授权数量
    
    不负责：
    - 销毁（不需要销毁）
    """
    
    def __init__(self, config_service=None):
        self._config_service = config_service
        self._container = None
        self._account_text = None
        self._expire_text = None
        self._name_text = None
        self._max_accounts = DEFAULT_MAX_ACCOUNTS
    
    def create(self, theme_colors: Dict[str, str] = None) -> ft.Container:
        """
        创建用户信息卡片
        
        参数：
        - theme_colors: 主题颜色
        """
        if theme_colors is None:
            theme_colors = {
                "text_primary": "#000000",
                "text_secondary": "#666666",
                "bg_primary": "#FFFFFF",
                "bg_tertiary": "#F5F5F5",
                "accent": "#0078D4",
            }
        
        username = self._get_username()
        authorized_count = self._get_authorized_count()
        self._max_accounts = self._get_max_accounts()
        expire_days = self._get_expire_days()
        
        avatar = ft.Container(
            content=ft.Icon(
                ft.Icons.ACCOUNT_CIRCLE,
                size=DEFAULT_AVATAR_SIZE,
                color=theme_colors.get("accent"),
            ),
            width=DEFAULT_AVATAR_SIZE,
            height=DEFAULT_AVATAR_SIZE,
            border_radius=ft.border_radius.all(24),
            bgcolor=theme_colors.get("bg_tertiary"),
            alignment=ft.alignment.Alignment(0.5, 0.5),
        )
        
        self._name_text = ft.Text(
            username,
            size=DEFAULT_NAME_SIZE,
            weight=ft.FontWeight.BOLD,
            color=theme_colors.get("text_primary"),
            text_align=ft.TextAlign.LEFT,
        )
        
        self._account_text = ft.Text(
            f"授权账号: {authorized_count}/{self._max_accounts}",
            size=DEFAULT_STATUS_SIZE,
            color=theme_colors.get("text_secondary"),
            text_align=ft.TextAlign.LEFT,
        )
        
        self._expire_text = ft.Text(
            f"到期时间: {expire_days} 天",
            size=DEFAULT_STATUS_SIZE,
            color=theme_colors.get("text_secondary"),
            text_align=ft.TextAlign.LEFT,
        )
        
        right_info_column = ft.Column(
            controls=[
                self._name_text,
                ft.Container(height=2),
                self._account_text,
                ft.Container(height=2),
                self._expire_text,
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
        
        self._container = ft.Container(
            content=content,
            height=DEFAULT_CARD_HEIGHT,
            padding=DEFAULT_PADDING,
            bgcolor=theme_colors.get("bg_primary"),
            alignment=ft.alignment.Alignment(0, 0.5),
        )
        
        return self._container
    
    def update_authorized_count(self, count: int):
        """更新授权账号数量"""
        if self._account_text:
            self._account_text.value = f"授权账号: {count}/{self._max_accounts}"
            self._update()
    
    def update_expire_days(self, days: int):
        """更新到期天数"""
        if self._expire_text:
            self._expire_text.value = f"到期时间: {days} 天"
            self._update()
    
    def update_name(self, name: str):
        """更新用户名"""
        if self._name_text:
            self._name_text.value = name
            self._update()
    
    def _update(self):
        """更新显示"""
        if self._container:
            try:
                if self._container.page:
                    self._container.update()
            except:
                pass
    
    def _get_username(self) -> str:
        """获取用户名"""
        if self._config_service:
            return self._config_service.get_user_preference("username", DEFAULT_USERNAME)
        return DEFAULT_USERNAME
    
    def _get_authorized_count(self) -> int:
        """获取已授权账号数"""
        if self._config_service:
            return self._config_service.get_user_preference("authorized_count", DEFAULT_AUTHORIZED_COUNT)
        return DEFAULT_AUTHORIZED_COUNT
    
    def _get_max_accounts(self) -> int:
        """获取最大账号数"""
        if self._config_service:
            return self._config_service.get_user_preference("max_accounts", DEFAULT_MAX_ACCOUNTS)
        return DEFAULT_MAX_ACCOUNTS
    
    def _get_expire_days(self) -> int:
        """获取到期天数"""
        if self._config_service:
            return self._config_service.get_user_preference("expire_days", DEFAULT_EXPIRE_DAYS)
        return DEFAULT_EXPIRE_DAYS

# *** 标准测试格式: 仅调用被测模块,AI不得添加数据 ***
if __name__ == "__main__":
    def main(page: ft.Page):
        page.title = "用户信息卡片测试"
        
        user_card = UserCard()
        card = user_card.create()
        page.add(card)
    
    ft.app(target=main)
