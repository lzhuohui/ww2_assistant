# -*- coding: utf-8 -*-
"""
主题提供者 - 核心接口

设计思路:
    提供主题相关的统一访问接口，负责颜色、尺寸和文本样式的管理。

功能:
    1. 颜色管理：获取主题颜色
    2. 尺寸管理：获取主题尺寸
    3. 文本样式管理：获取和合并文本样式
    4. Win11风格：提供Win11风格的文本样式
    5. 主题初始化：加载主题配置

数据来源:
    所有配置数据从配置目录获取。

使用场景:
    被界面层、组件层、单元层调用。

可独立运行调试: python 主题提供者.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft
from typing import Dict, Any, Optional
from 前端.用户设置界面.配置.界面配置 import 界面配置


class ThemeProvider:
    """主题提供者 - 核心接口"""
    
    _instance = None
    _config = None
    _default_text_style: Optional[Dict[str, Any]] = None
    
    def __new__(cls):
        """单例模式"""
        if cls._instance is None:
            cls._instance = super(ThemeProvider, cls).__new__(cls)
        return cls._instance
    
    @classmethod
    def initialize(cls, config: 界面配置):
        """
        初始化主题提供者
        
        参数:
            config: 界面配置对象
        """
        cls._config = config
        cls._init_default_text_style()
    
    @classmethod
    def _init_default_text_style(cls):
        """初始化默认文本样式"""
        font_family = cls.get_size("字体", "font_family") or "Segoe UI Variable, Segoe UI, sans-serif"
        cls._default_text_style = {
            "font_family": font_family,
            "size": 14,
            "weight": ft.FontWeight.W_400,
            "color": cls.get_color("text_primary"),
            "line_height": 21,
            "letter_spacing": 0.02,
        }
    
    @classmethod
    def get_color(cls, color_key: str) -> str:
        """
        获取主题颜色
        
        参数:
            color_key: 颜色键名
        
        返回:
            str: 颜色值
        """
        if not cls._config:
            cls._config = 界面配置()
        
        theme_colors = cls._config.当前主题颜色
        return theme_colors.get(color_key, "#000000")
    
    @classmethod
    def get_size(cls, category: str, size_key: str) -> int:
        """
        获取主题尺寸
        
        参数:
            category: 尺寸类别
            size_key: 尺寸键名
        
        返回:
            int: 尺寸值
        """
        if not cls._config:
            cls._config = 界面配置()
        
        sizes = cls._config.定义尺寸.get(category, {})
        return sizes.get(size_key, 0)
    
    @classmethod
    def get_theme(cls) -> dict:
        """
        获取当前主题配置
        
        返回:
            dict: 主题配置
        """
        if not cls._config:
            cls._config = 界面配置()
        
        return {
            "colors": cls._config.当前主题颜色,
            "sizes": cls._config.定义尺寸,
        }
    
    @classmethod
    def get_default_text_style(cls) -> Dict[str, Any]:
        """
        获取默认文本样式
        
        返回:
            Dict[str, Any]: 默认文本样式
        """
        if not cls._default_text_style:
            cls._init_default_text_style()
        return cls._default_text_style.copy()
    
    @classmethod
    def merge_text_style(cls, custom_style: Dict[str, Any]) -> Dict[str, Any]:
        """
        合并文本样式
        
        参数:
            custom_style: 自定义样式
        
        返回:
            Dict[str, Any]: 合并后的样式
        """
        default_style = cls.get_default_text_style()
        merged_style = default_style.copy()
        merged_style.update(custom_style)
        return merged_style
    
    @classmethod
    def get_win11_text_style(cls, role: str = "body", size: Optional[int] = None, weight: Optional[ft.FontWeight] = None) -> Dict[str, Any]:
        """
        获取Win11风格文本样式
        
        参数:
            role: 文本角色 (display, title_large, title, subtitle, body_large, body, caption)
            size: 自定义字体大小
            weight: 自定义字体粗细
        
        返回:
            Dict[str, Any]: Win11风格文本样式
        """
        font_family = cls.get_size("字体", "font_family") or "Segoe UI Variable, Segoe UI, sans-serif"
        
        style_map = {
            "display": {"size": 68, "weight": ft.FontWeight.W_600, "color": "text_primary", "line_height": 82},
            "title_large": {"size": 40, "weight": ft.FontWeight.W_600, "color": "text_primary", "line_height": 48},
            "title": {"size": 28, "weight": ft.FontWeight.W_600, "color": "text_primary", "line_height": 34},
            "subtitle": {"size": 20, "weight": ft.FontWeight.W_600, "color": "text_primary", "line_height": 24},
            "body_large": {"size": 18, "weight": ft.FontWeight.W_400, "color": "text_primary", "line_height": 22},
            "body": {"size": 14, "weight": ft.FontWeight.W_400, "color": "text_primary", "line_height": 21},
            "caption": {"size": 12, "weight": ft.FontWeight.W_400, "color": "text_secondary", "line_height": 18},
        }
        
        style = style_map.get(role, style_map["body"])
        custom_style = {
            "font_family": font_family,
            "size": size or style["size"],
            "weight": weight or style["weight"],
            "color": cls.get_color(style["color"]),
            "line_height": style["line_height"],
        }
        
        return custom_style


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    # 1. 界面配置初始化
    配置 = 界面配置()
    
    # 2. 初始化主题提供者
    ThemeProvider.initialize(配置)
    
    # 3. 测试获取颜色
    print("=== 测试获取颜色 ===")
    print(f"获取颜色 'text_primary': {ThemeProvider.get_color('text_primary')}")
    print(f"获取颜色 'bg_primary': {ThemeProvider.get_color('bg_primary')}")
    print(f"获取颜色 'accent': {ThemeProvider.get_color('accent')}")
    
    # 4. 测试获取尺寸
    print("\n=== 测试获取尺寸 ===")
    print(f"获取尺寸 '字体.font_family': {ThemeProvider.get_size('字体', 'font_family')}")
    print(f"获取尺寸 '字体.font_size_body': {ThemeProvider.get_size('字体', 'font_size_body')}")
    print(f"获取尺寸 '间距.spacing_md': {ThemeProvider.get_size('间距', 'spacing_md')}")
    print(f"获取尺寸 '圆角.radius_md': {ThemeProvider.get_size('圆角', 'radius_md')}")
    
    # 5. 测试获取主题
    print("\n=== 测试获取主题 ===")
    theme = ThemeProvider.get_theme()
    print(f"主题颜色数量: {len(theme['colors'])}")
    print(f"主题尺寸类别: {list(theme['sizes'].keys())}")
    
    # 6. 测试获取默认文本样式
    print("\n=== 测试获取默认文本样式 ===")
    default_style = ThemeProvider.get_default_text_style()
    print(f"默认文本样式: {default_style}")
    
    # 7. 测试获取Win11风格文本样式
    print("\n=== 测试获取Win11风格文本样式 ===")
    roles = ["display", "title_large", "title", "subtitle", "body_large", "body", "caption"]
    for role in roles:
        style = ThemeProvider.get_win11_text_style(role)
        print(f"{role}: size={style['size']}, weight={style['weight']}, color={style['color']}")