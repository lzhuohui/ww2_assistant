# -*- coding: utf-8 -*-
"""模块名称：主题提供者 | 设计思路：提供主题相关的统一访问接口 | 模块隔离原则"""

import flet as ft
from typing import Dict, Any, Optional
from .界面配置 import 界面配置


class ThemeProvider:
    """主题提供者 - 核心接口"""
    
    _instance = None
    _config = None
    _default_text_style: Optional[Dict[str, Any]] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ThemeProvider, cls).__new__(cls)
        return cls._instance
    
    @classmethod
    def initialize(cls, config: 界面配置):
        cls._config = config
        cls._init_default_text_style()
    
    @classmethod
    def _init_default_text_style(cls):
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
        if not cls._config:
            cls._config = 界面配置()
        theme_colors = cls._config.当前主题颜色
        return theme_colors.get(color_key, "#000000")
    
    @classmethod
    def get_size(cls, category: str, size_key: str) -> int:
        if not cls._config:
            cls._config = 界面配置()
        sizes = cls._config.定义尺寸.get(category, {})
        return sizes.get(size_key, 0)
    
    @classmethod
    def get_theme(cls) -> dict:
        if not cls._config:
            cls._config = 界面配置()
        return {
            "colors": cls._config.当前主题颜色,
            "sizes": cls._config.定义尺寸,
        }
    
    @classmethod
    def get_default_text_style(cls) -> Dict[str, Any]:
        if not cls._default_text_style:
            cls._init_default_text_style()
        return cls._default_text_style.copy()
    
    @classmethod
    def merge_text_style(cls, custom_style: Dict[str, Any]) -> Dict[str, Any]:
        default_style = cls.get_default_text_style()
        merged_style = default_style.copy()
        merged_style.update(custom_style)
        return merged_style
    
    @classmethod
    def get_win11_text_style(cls, role: str="body", size: Optional[int]=None, weight: Optional[ft.FontWeight]=None) -> Dict[str, Any]:
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


if __name__ == "__main__":
    配置 = 界面配置()
    ThemeProvider.initialize(配置)
    print(f"获取颜色 'text_primary': {ThemeProvider.get_color('text_primary')}")
    print(f"获取尺寸 '间距.spacing_md': {ThemeProvider.get_size('间距', 'spacing_md')}")
