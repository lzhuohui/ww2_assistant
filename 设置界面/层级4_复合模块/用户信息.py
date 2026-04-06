# -*- coding: utf-8 -*-

"""
模块名称：用户信息.py
模块功能：用户信息组件，显示头像和用户信息

职责：
- 头像显示（金色字可编辑)
- 注册名称显示
- 扩展信息显示
- 基础信息显示
- 点击跳转注册界面

不负责：
- 数据持久化
"""

import flet as ft
from typing import Dict, Callable, Optional

from 设置界面.层级0_数据管理.配置管理 import ConfigManager
from 设置界面.层级5_基础模块.头像 import Avatar
from 设置界面.层级5_基础模块.标签 import Label


class UserInfoCard:
    """
    用户信息 - V3版本
    
    职责：
    - 头像显示（金色字可编辑）
    - 注册名称显示
    - 扩展信息显示
    - 基础信息显示
    - 点击跳转注册界面
    
    不负责：
    - 数据持久化
    """
    
    _config_manager: ConfigManager = None
    _instance: ft.Container = None
    _on_click_callback: Optional[Callable] = None
    _extension_text: ft.Text = None
    _basic_text: ft.Text = None
    
    @classmethod
    def set_config_manager(cls, config_manager: ConfigManager):
        """设置配置管理实例"""
        cls._config_manager = config_manager
        Avatar.set_config_manager(config_manager)
        Label.set_config_manager(config_manager)
    
    @classmethod
    def set_on_click_callback(cls, callback: Callable):
        """设置点击回调函数"""
        cls._on_click_callback = callback
    
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
        UserInfoCard._check_config_manager()
        spacing = UserInfoCard._config_manager.get_ui_size("边距", "控件间距")
        if spacing is None:
            spacing = 6
        return spacing
    
    @staticmethod
    def get_card_padding() -> int:
        UserInfoCard._check_config_manager()
        padding = UserInfoCard._config_manager.get_ui_size("边距", "控件区内边距")
        if padding is None:
            padding = 6
        return padding
    
    @staticmethod
    def get_avatar_spacing() -> int:
        UserInfoCard._check_config_manager()
        spacing = UserInfoCard._config_manager.get_ui_size("边距", "控件间距")
        if spacing is None:
            spacing = 6
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
        
        extension_used = user_info.get("extension_used", 0)
        extension_total = user_info.get("extension_total", 0)
        remaining_days = user_info.get("remaining_days", 0)
        
        title_size = UserInfoCard._config_manager.get_ui_size("字体", "正文字体")
        info_size = UserInfoCard._config_manager.get_ui_size("字体", "副标题字体")
        card_padding = UserInfoCard.get_card_padding()
        
        avatar = Avatar.create(
            text=avatar_text,
            text_color="#FFD700",
            size=50,
            theme_colors=theme_colors,
        )
        
        text_primary = theme_colors.get("text_primary", "#FFFFFF")
        text_secondary = theme_colors.get("text_secondary", "#B0B0B0")
        accent = theme_colors.get("accent", "#0078D4")
        bg_card = theme_colors.get("bg_card", "#2D2D2D")
        bg_hover = theme_colors.get("bg_hover", "#3D3D3D")
        
        arrow_icon = ft.Icon(
            ft.Icons.CHEVRON_RIGHT,
            size=14,
            color=text_secondary,
        )
        
        def create_clickable_row(content: ft.Control, on_click_callback: Callable, show_arrow: bool = True) -> ft.Container:
            """创建可点击的行"""
            controls = [content]
            if show_arrow:
                controls.append(arrow_icon)
            container = ft.Container(
                content=ft.Row(controls, spacing=4, alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                on_click=lambda e: on_click_callback() if on_click_callback else None,
                border_radius=4,
                padding=ft.Padding(4, 2, 4, 2),
            )
            
            def on_hover(e):
                if e.data == "true":
                    e.control.bgcolor = bg_hover
                    if hasattr(content, 'color'):
                        content.color = accent
                else:
                    e.control.bgcolor = None
                    if hasattr(content, 'color'):
                        content.color = text_secondary
                e.control.update()
            
            container.on_hover = on_hover
            return container
        
        username_text = Label.create(
            text=username,
            size=title_size,
            weight=ft.FontWeight.BOLD,
            color_type="primary",
            theme_colors=theme_colors,
        )
        
        UserInfoCard._extension_text = Label.create(
            text=f"扩展信息: {extension_used}/{extension_total}",
            size=info_size,
            color_type="secondary",
            theme_colors=theme_colors,
        )
        
        UserInfoCard._basic_text = Label.create(
            text=f"基础信息: {remaining_days}",
            size=info_size,
            color_type="secondary",
            theme_colors=theme_colors,
        )
        
        username_row = create_clickable_row(username_text, UserInfoCard._on_click_callback, show_arrow=False)
        extension_row = create_clickable_row(UserInfoCard._extension_text, UserInfoCard._on_click_callback)
        basic_row = create_clickable_row(UserInfoCard._basic_text, UserInfoCard._on_click_callback)
        
        right_column = ft.Column([
            username_row,
            extension_row,
            basic_row,
        ], spacing=2, alignment=ft.MainAxisAlignment.CENTER)
        
        avatar_container = ft.Container(
            content=avatar,
            margin=ft.Margin(8, 0, 0, 0),
        )
        
        content = ft.Row([
            avatar_container,
            right_column,
        ], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER)
        
        UserInfoCard._instance = ft.Container(
            content=content,
            bgcolor=bg_card,
            padding=0,
            border_radius=UserInfoCard._config_manager.get_ui_size("圆角", "卡片圆角"),
        )
        
        return UserInfoCard._instance
    
    @classmethod
    def update_extension_info(cls, used: int, total: int):
        """更新扩展信息显示"""
        if cls._extension_text:
            cls._extension_text.value = f"扩展信息: {used}/{total}"
            try:
                cls._extension_text.update()
            except:
                pass
    
    @classmethod
    def update_basic_info(cls, remaining_days: int):
        """更新基础信息显示"""
        if cls._basic_text:
            cls._basic_text.value = f"基础信息: {remaining_days}"
            try:
                cls._basic_text.update()
            except:
                pass
    
    @classmethod
    def update_theme(cls, theme_colors: Dict[str, str] = None):
        """更新主题颜色"""
        if theme_colors is None:
            theme_colors = cls._config_manager.get_theme_colors()
        
        text_primary = theme_colors.get("text_primary", "#FFFFFF")
        text_secondary = theme_colors.get("text_secondary", "#B0B0B0")
        bg_card = theme_colors.get("bg_card", "#2D2D2D")
        
        if cls._instance:
            cls._instance.bgcolor = bg_card
            cls._instance.update()


if __name__ == "__main__":
    def main(page: ft.Page):
        from 设置界面.层级0_数据管理.配置管理 import ConfigManager
        config_manager = ConfigManager()
        UserInfoCard.set_config_manager(config_manager)
        
        def on_user_info_click():
            print("用户信息被点击")
        
        UserInfoCard.set_on_click_callback(on_user_info_click)
        
        user_info = UserInfoCard.create()
        
        page.add(user_info)
    
    ft.app(target=main)
