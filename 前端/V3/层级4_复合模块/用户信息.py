# -*- coding: utf-8 -*-

"""
模块名称：用户信息.py
模块功能：用户信息组件，显示头像和用户信息

职责：
- 头像显示（金色字可编辑）
- 注册名称显示
- 注册数量显示
- 注册天数显示

不负责：
- 数据持久化
"""

import flet as ft
from typing import Dict

from 前端.V3.层级0_数据管理.配置管理 import ConfigManager
from 前端.V3.层级5_基础模块.头像 import Avatar

class UserInfoCard:
    """
    用户信息 - V3版本
    
    职责：
    - 头像显示（金色字可编辑）
    - 注册名称显示
    - 注册数量显示
    - 注册天数显示
    
    不负责：
    - 数据持久化
    """
    
    _config_manager: ConfigManager = None
    
    @classmethod
    def set_config_manager(cls, config_manager: ConfigManager):
        """设置配置管理实例"""
        cls._config_manager = config_manager
        Avatar.set_config_manager(config_manager)
    
    @staticmethod
    def _check_config_manager():
        """检查配置管理是否已设置"""
        if UserInfoCard._config_manager is None:
            raise RuntimeError(
                "UserInfoCard模块未设置config_manager，"
                "请先调用 UserInfoCard.set_config_manager(config_manager)"
            )
    
    @staticmethod
    def get_info_spacing() -> int:
        """获取信息行间距"""
        UserInfoCard._check_config_manager()
        spacing = UserInfoCard._config_manager.get_ui_size("边距", "小")
        if spacing is None:
            spacing = 2
        return spacing
    
    @staticmethod
    def get_card_padding() -> int:
        """获取卡片内边距"""
        UserInfoCard._check_config_manager()
        padding = UserInfoCard._config_manager.get_ui_size("边距", "中")
        if padding is None:
            padding = 6
        return padding
    
    @staticmethod
    def get_avatar_spacing() -> int:
        """获取头像与信息区间距"""
        UserInfoCard._check_config_manager()
        spacing = UserInfoCard._config_manager.get_ui_size("边距", "小")
        if spacing is None:
            spacing = 4
        return spacing
    
    @staticmethod
    def create(
        theme_colors: Dict[str, str] = None,
        width: int = None,
    ) -> ft.Container:
        """
        创建用户信息
        
        参数:
        - theme_colors: 主题颜色
        - width: 宽度
        
        返回:
        - ft.Container: 用户信息
        """
        if UserInfoCard._config_manager is None:
            raise RuntimeError("UserInfoCard模块未设置config_manager")
        
        if theme_colors is None:
            theme_colors = UserInfoCard._config_manager.get_theme_colors()
        
        prefs = UserInfoCard._config_manager._data.load_user_preference()
        user_info = prefs.get("用户信息", {})
        
        avatar_text = user_info.get("avatar_text", "帅")
        username = user_info.get("username", "试用用户")
        account_count = user_info.get("account_count", "0/15")
        remaining_days = user_info.get("remaining_days", "0天")
        
        title_size = UserInfoCard._config_manager.get_ui_size("字体", "正文字体")
        info_size = UserInfoCard._config_manager.get_ui_size("字体", "副标题字体")
        info_spacing = UserInfoCard.get_info_spacing()
        card_padding = UserInfoCard.get_card_padding()
        avatar_spacing = UserInfoCard.get_avatar_spacing()
        
        avatar = Avatar.create(
            text=avatar_text,
            text_color="#FFD700",
            size=50,
            theme_colors=theme_colors,
        )
        
        text_primary = theme_colors.get("text_primary", "#FFFFFF")
        text_secondary = theme_colors.get("text_secondary", "#B0B0B0")
        bg_card = theme_colors.get("bg_card", "#2D2D2D")
        
        username_text = ft.Text(
            username,
            size=title_size,
            weight=ft.FontWeight.BOLD,
            color=text_primary,
        )
        
        count_text = ft.Text(
            f"注册数量: {account_count}",
            size=info_size,
            color=text_secondary,
        )
        
        days_text = ft.Text(
            f"剩余天数: {remaining_days}",
            size=info_size,
            color=text_secondary,
        )
        
        right_column = ft.Column([
            username_text,
            count_text,
            days_text,
        ], spacing=info_spacing, alignment=ft.MainAxisAlignment.CENTER)
        
        content = ft.Row([
            avatar,
            ft.Container(width=avatar_spacing),
            right_column,
        ], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER)
        
        return ft.Container(
            content=content,
            bgcolor=bg_card,
            padding=card_padding,
            border_radius=UserInfoCard._config_manager.get_ui_size("圆角", "卡片圆角"),
        )
