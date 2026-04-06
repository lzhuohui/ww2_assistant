# -*- coding: utf-8 -*-

"""
模块名称：图标.py
模块功能：图标组件

职责：
- 图标显示
- 从用户偏好.yaml获取基础图标大小

不负责：
- 布局
- 销毁（不需要销毁）
"""

import flet as ft
from typing import Dict

from 设置界面.层级0_数据管理.配置管理 import ConfigManager


class Icon:
    """
    图标组件 - V3版本
    
    职责：
    - 图标显示
    - 从用户偏好.yaml获取基础图标大小
    
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
        if Icon._config_manager is None:
            raise RuntimeError(
                "Icon模块未设置config_manager，"
                "请先调用 Icon.set_config_manager(config_manager)"
            )
    
    @staticmethod
    def get_base_size() -> int:
        """获取基础图标大小（从用户偏好.yaml获取）"""
        Icon._check_config_manager()
        size = Icon._config_manager.get_ui_size("字体", "图标大小")
        if size is None:
            size = 18
        return size
    
    @staticmethod
    def _get_theme_colors() -> Dict[str, str]:
        """获取主题颜色"""
        Icon._check_config_manager()
        return Icon._config_manager.get_theme_colors()
    
    @staticmethod
    def create(
        icon_name: str = "HOME",
        size: int = None,
        color_type: str = "accent",
        theme_colors: Dict[str, str] = None,
        opacity: float = 1.0,
    ) -> ft.Icon:
        """
        创建图标
        
        参数：
        - icon_name: 图标名称
        - size: 图标大小（可选，默认从用户偏好.yaml获取基础大小）
        - color_type: 颜色类型 (accent/primary/secondary)
        - theme_colors: 主题颜色
        - opacity: 透明度
        """
        if size is None:
            size = Icon.get_base_size()
        
        if theme_colors is None:
            theme_colors = Icon._get_theme_colors()
        
        color = theme_colors.get(color_type, theme_colors.get("accent"))
        
        icon_attr = getattr(ft.Icons, icon_name.upper(), ft.Icons.HOME)
        
        return ft.Icon(
            icon_attr,
            size=size,
            color=color,
            opacity=opacity,
        )
