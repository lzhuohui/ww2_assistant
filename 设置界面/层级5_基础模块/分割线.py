# -*- coding: utf-8 -*-

"""
模块名称：分割线.py
模块功能：分割线组件

职责：
- 分隔显示

不负责：
- 布局
- 销毁（不需要销毁）
"""

import flet as ft
from typing import Dict

from 设置界面.层级0_数据管理.配置管理 import ConfigManager


class Divider:
    """
    分割线组件 - V3版本
    
    职责：
    - 分隔显示
    
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
        if Divider._config_manager is None:
            raise RuntimeError(
                "Divider模块未设置config_manager，"
                "请先调用 Divider.set_config_manager(config_manager)"
            )
    
    @staticmethod
    def _get_theme_colors() -> Dict[str, str]:
        """获取主题颜色"""
        Divider._check_config_manager()
        return Divider._config_manager.get_theme_colors()
    
    @staticmethod
    def create_horizontal(
        height: int = 1,
        color_type: str = "divider",
        theme_colors: Dict[str, str] = None,
    ) -> ft.Divider:
        """
        创建水平分割线
        
        参数：
        - height: 分割线高度（粗细）
        - color_type: 颜色类型 (divider/accent)
        - theme_colors: 主题颜色
        """
        if theme_colors is None:
            theme_colors = Divider._get_theme_colors()
        
        color = theme_colors.get(color_type, theme_colors.get("divider"))
        
        return ft.Divider(
            height=height,
            thickness=height,
            color=color,
        )
    
    @staticmethod
    def create_vertical(
        width: int = 1,
        color_type: str = "divider",
        theme_colors: Dict[str, str] = None,
    ) -> ft.VerticalDivider:
        """
        创建垂直分割线
        
        参数：
        - width: 分割线宽度（粗细）
        - color_type: 颜色类型 (divider/accent)
        - theme_colors: 主题颜色
        """
        if theme_colors is None:
            theme_colors = Divider._get_theme_colors()
        
        color = theme_colors.get(color_type, theme_colors.get("divider"))
        
        return ft.VerticalDivider(
            width=width,
            thickness=width,
            color=color,
        )
