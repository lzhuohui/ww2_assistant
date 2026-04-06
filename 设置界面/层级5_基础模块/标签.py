# -*- coding: utf-8 -*-

"""
模块名称：标签.py
模块功能：文本标签组件

职责：
- 文本显示
- 从用户偏好.yaml获取基础字体大小

不负责：
- 布局
- 销毁（不需要销毁）
"""

import flet as ft
from typing import Dict

from 设置界面.层级0_数据管理.配置管理 import ConfigManager


class Label:
    """
    标签组件 - V3版本
    
    职责：
    - 文本显示
    - 从用户偏好.yaml获取基础字体大小
    
    不负责：
    - 布局
    - 销毁（不需要销毁）
    """
    
    _config_manager: ConfigManager = None
    
    @classmethod
    def set_config_manager(cls, config_manager: ConfigManager):
        """
        设置配置管理实例（类级别）
        
        注意：此方法必须在创建任何Label实例之前调用
        通常在MainEntry的_init_modules方法中调用
        
        参数:
            config_manager: 配置管理实例
        """
        cls._config_manager = config_manager
    
    @staticmethod
    def _check_config_manager():
        """检查配置管理是否已设置"""
        if Label._config_manager is None:
            raise RuntimeError(
                "Label模块未设置config_manager。\n"
                "解决方案：\n"
                "1. 确保在创建Label实例之前调用 Label.set_config_manager(config_manager)\n"
                "2. 通常在MainEntry的_init_modules方法中调用\n"
                "3. 检查初始化顺序是否正确"
            )
    
    @staticmethod
    def get_base_size() -> int:
        """获取基础字体大小（从用户偏好.yaml获取）"""
        Label._check_config_manager()
        size = Label._config_manager.get_ui_size("字体", "正文字体")
        if size is None:
            size = 16
        return size
    
    @staticmethod
    def _get_theme_colors() -> Dict[str, str]:
        """获取主题颜色"""
        Label._check_config_manager()
        return Label._config_manager.get_theme_colors()
    
    @staticmethod
    def create(
        text: str = "",
        size: int = None,
        weight: ft.FontWeight = ft.FontWeight.NORMAL,
        color_type: str = "primary",
        theme_colors: Dict[str, str] = None,
        no_wrap: bool = True,
        overflow: ft.TextOverflow = ft.TextOverflow.ELLIPSIS,
    ) -> ft.Text:
        """
        创建标签
        
        参数：
        - text: 文本内容
        - size: 字体大小（可选，默认从用户偏好.yaml获取基础大小）
        - weight: 字体粗细
        - color_type: 颜色类型 (primary/secondary/disabled)
        - theme_colors: 主题颜色
        - no_wrap: 是否不换行
        - overflow: 溢出处理
        """
        if size is None:
            size = Label.get_base_size()
        
        if theme_colors is None:
            theme_colors = Label._get_theme_colors()
        
        color_key = f"text_{color_type}" if color_type != "primary" else "text_primary"
        color = theme_colors.get(color_key, theme_colors.get("text_primary"))
        
        return ft.Text(
            text,
            size=size,
            weight=weight,
            color=color,
            no_wrap=no_wrap,
            overflow=overflow,
        )
