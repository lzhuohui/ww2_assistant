# -*- coding: utf-8 -*-
"""
模块名称：UIConfig
设计思路: 管理界面尺寸和布局配置
模块隔离: 纯配置模块，依赖主题配置
"""

from typing import Dict, Any
from .主题配置 import ThemeConfig, USER_DEFAULT_THEME


# *** 用户指定变量 - AI不得修改, 变量值必须生效 ***
# （用户未指定变量）
# *********************************


class UIConfig:
    """界面配置类 - 提供界面尺寸和布局管理"""
    
    size_definitions = {
        "font": {
            "font_family": "Segoe UI Variable, Segoe UI, system-ui, sans-serif",
            "font_size_body": 14,
            "font_size_title": 16,
        },
        "spacing": {
            "spacing_xs": 4,
            "spacing_sm": 8,
            "spacing_md": 12,
            "spacing_lg": 16,
            "spacing_xl": 20,
        },
        "radius": {
            "radius_sm": 4,
            "radius_md": 8,
            "radius_lg": 12,
        },
        "component": {
            "button_height": 32,
            "input_height": 35,
            "icon_size": 20,
        },
        "card": {
            "default_height": 70,
            "default_spacing": 10,
        },
        "animation": {
            "duration_fast": 167,
            "duration_normal": 250,
        },
    }
    
    def __init__(self, theme_name: str=USER_DEFAULT_THEME):
        self._theme_config = ThemeConfig(theme_name)
    
    def switch_theme(self, theme_name: str) -> bool:
        return self._theme_config.switch_theme(theme_name)
    
    def switch_palette(self, palette_name: str) -> bool:
        return self._theme_config.switch_palette(palette_name)
    
    def switch_style(self, style_name: str) -> bool:
        return self._theme_config.switch_style(style_name)
    
    def get_color(self, color_name: str) -> str:
        return self._theme_config.get_color(color_name)
    
    def get_size(self, category: str, name: str) -> Any:
        category_data = self.size_definitions.get(category, {})
        return category_data.get(name)
    
    @property
    def theme_name(self) -> str:
        return self._theme_config.theme_name
    
    @property
    def palette_name(self) -> str:
        return self._theme_config.palette_name
    
    @property
    def current_style_name(self) -> str:
        return self._theme_config.style_name
    
    @property
    def 当前主题颜色(self) -> Dict[str, str]:
        return self._theme_config.current_colors


# *** 调试逻辑 ***
if __name__ == "__main__":
    config = UIConfig()
    print(f"当前主题: {config.theme_name}")
    print(f"字体: {config.get_size('font', 'font_family')}")
