# -*- coding: utf-8 -*-

"""
模块名称：输入框.py
模块功能：输入框组件，支持文本输入和配置保存

职责：
- 从配置管理获取当前值
- 从用户偏好.yaml获取UI配置
- 文本输入
- 自动保存到配置

不负责：
- 布局
- 销毁（不需要销毁）
"""

import flet as ft
from typing import Callable, Dict, Optional

from 设置界面.层级0_数据管理.配置管理 import ConfigManager


class InputBox:
    """
    输入框组件 - V3版本
    
    职责：
    - 从配置管理获取当前值
    - 从用户偏好.yaml获取UI配置
    - 文本输入
    - 自动保存到配置
    
    不负责：
    - 布局
    - 销毁（不需要销毁）
    """
    
    _config_manager: ConfigManager = None
    
    @classmethod
    def set_config_manager(cls, config_manager: ConfigManager):
        """设置配置管理实例"""
        cls._config_manager = config_manager
    
    @staticmethod
    def _check_config_manager():
        """检查配置管理是否已设置"""
        if InputBox._config_manager is None:
            raise RuntimeError(
                "InputBox模块未设置config_manager，"
                "请先调用 InputBox.set_config_manager(config_manager)"
            )
    
    @staticmethod
    def get_width() -> int:
        InputBox._check_config_manager()
        width = InputBox._config_manager.get_ui_config("控件", "输入框宽度")
        if width is None:
            width = 120
        return width
    
    @staticmethod
    def get_height() -> int:
        InputBox._check_config_manager()
        height = InputBox._config_manager.get_ui_config("控件", "输入框高度")
        if height is None:
            height = 30
        return height
    
    @staticmethod
    def get_border_radius() -> int:
        InputBox._check_config_manager()
        radius = InputBox._config_manager.get_radius("小")
        if radius is None:
            radius = 3
        return radius
    
    @staticmethod
    def get_text_size() -> int:
        InputBox._check_config_manager()
        size = InputBox._config_manager.get_ui_size("字体", "正文字体")
        if size is None:
            size = 16
        return size
    
    def __init__(self, page: ft.Page = None, config_manager: ConfigManager = None):
        self._page = page
        self._config_manager = config_manager or InputBox._config_manager
        self._inputs: Dict[str, ft.TextField] = {}
    
    def create(
        self,
        interface: str = "",
        card: str = "",
        control_id: str = "",
        enabled: bool = True,
        max_length: int = None,
        on_change: Callable[[str, str, str, str], None] = None,
        theme_colors: Dict[str, str] = None,
        hint_text: str = None,
        password_mode: Optional[bool] = None,
        width: int = None,
        height: int = None,
        use_defaults: bool = False,
    ) -> ft.TextField:
        """
        创建输入框
        
        参数：
        - interface: 界面名称
        - card: 卡片名称
        - control_id: 控件ID
        - enabled: 是否启用
        - max_length: 最大长度
        - on_change: 值变更回调
        - theme_colors: 主题颜色
        - hint_text: 提示文本
        - password_mode: 密码模式
        - width: 宽度（可选）
        - height: 高度（可选）
        - use_defaults: 是否使用默认值（True时忽略方案值）
        """
        if width is None:
            width = InputBox.get_width()
        if height is None:
            height = InputBox.get_height()
        border_radius = InputBox.get_border_radius()
        
        if theme_colors is None:
            theme_colors = self._get_theme_colors()
        
        current_value = self._get_current_value(interface, card, control_id, use_defaults)
        
        if hint_text is None:
            hint_text = self._get_hint(interface, card, control_id)
        
        if password_mode is None:
            password_mode = self._get_password_mode(interface, card, control_id)
        
        text_field = self._build_text_field(
            current_value, enabled, width, height, border_radius,
            theme_colors, hint_text, password_mode,
            max_length, interface, card, control_id, on_change
        )
        
        key = f"{interface}.{card}.{control_id}" if interface and card and control_id else f"input_{len(self._inputs)}"
        self._inputs[key] = text_field
        
        return text_field
    
    def _get_theme_colors(self) -> Dict[str, str]:
        """获取主题颜色"""
        if self._config_manager is None:
            raise RuntimeError("InputBox模块未设置config_manager")
        return self._config_manager.get_theme_colors()
    
    def _get_current_value(self, interface: str, card: str, control_id: str, use_defaults: bool = False) -> str:
        """从配置管理获取当前值"""
        if self._config_manager:
            if use_defaults:
                return self._config_manager.get_default(interface, card, control_id) or ""
            else:
                return self._config_manager.get_value(interface, card, control_id, "")
        return ""
    
    def _get_hint(self, interface: str, card: str, control_id: str) -> str:
        """从配置管理获取提示文本"""
        if self._config_manager:
            config = self._config_manager.get_control_config(interface, card, control_id)
            return config.get("hint", "")
        return ""
    
    def _get_password_mode(self, interface: str, card: str, control_id: str) -> bool:
        """从配置管理获取密码模式"""
        if self._config_manager:
            config = self._config_manager.get_control_config(interface, card, control_id)
            return config.get("password", False)
        return False
    
    def _build_text_field(
        self,
        current_value: str,
        enabled: bool,
        width: int,
        height: int,
        border_radius: int,
        theme_colors: Dict,
        hint_text: str,
        password_mode: bool,
        max_length: int,
        interface: str,
        card: str,
        control_id: str,
        on_change: Callable,
    ) -> ft.TextField:
        """构建文本输入框"""
        
        text_color = theme_colors.get("text_primary", "#FFFFFF")
        disabled_color = theme_colors.get("text_disabled", "#666666")
        bg_card = theme_colors.get("bg_card", "#2D2D2D")
        border_color = theme_colors.get("border", "#3D3D3D")
        text_size = InputBox.get_text_size()
        padding = InputBox._config_manager.get_ui_size("边距", "输入框内边距") or 6
        
        def handle_change(e):
            self._save_value(interface, card, control_id, e.control.value)
            if on_change:
                on_change(interface, card, control_id, e.control.value)
        
        text_field = ft.TextField(
            value=current_value,
            width=width,
            height=height,
            text_size=text_size,
            color=text_color if enabled else disabled_color,
            bgcolor=bg_card,
            border_color=border_color,
            border_radius=border_radius,
            hint_text=hint_text,
            hint_style=ft.TextStyle(color=disabled_color),
            password=password_mode,
            can_reveal_password=password_mode,
            max_length=max_length,
            on_change=handle_change,
            disabled=not enabled,
            content_padding=ft.Padding.symmetric(horizontal=padding, vertical=padding // 2),
        )
        
        return text_field
    
    def _save_value(self, interface: str, card: str, control_id: str, value: str):
        """保存值到配置"""
        if self._config_manager:
            self._config_manager.set_value(interface, card, control_id, value)
    
    def get_value(self, interface: str, card: str, control_id: str) -> str:
        """获取输入框当前值"""
        key = f"{interface}.{card}.{control_id}"
        if key in self._inputs:
            return self._inputs[key].value or ""
        return ""
