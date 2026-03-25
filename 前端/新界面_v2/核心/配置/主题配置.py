# -*- coding: utf-8 -*-
"""
模块名称：ThemeConfig
设计思路: 管理主题颜色配置，支持深色/浅色主题切换
模块隔离: 纯配置模块，无外部依赖
"""

from typing import Dict, Any


# *** 用户指定变量 - AI不得修改, 变量值必须生效 ***
USER_DEFAULT_THEME = "dark"  # 默认主题
# *********************************


class ThemeConfig:
    """主题配置类 - 提供主题颜色管理"""
    
    themes = {
        "dark": {
            "bg_primary": "#202020",
            "bg_secondary": "#252525",
            "bg_card": "#2D2D2D",
            "bg_input": "#2D2D2D",
            "bg_selected": "#4D4D4D",
            "bg_hover": "#3D3D3D",
            "text_primary": "#FFFFFF",
            "text_secondary": "#C5C5C5",
            "text_hint": "#8A8A8A",
            "border": "#3D3D3D",
            "accent": "#0078D4",
            "success": "#6CCB5F",
            "warning": "#FCE100",
            "error": "#FF6B6B",
            "shadow": "rgba(0, 0, 0, 0.25)",
        },
        "light": {
            "bg_primary": "#F3F3F3",
            "bg_secondary": "#FFFFFF",
            "bg_card": "#FFFFFF",
            "bg_input": "#FFFFFF",
            "bg_selected": "#0078D4",
            "bg_hover": "#E5E5E5",
            "text_primary": "#1A1A1A",
            "text_secondary": "#666666",
            "text_hint": "#999999",
            "border": "#D0D0D0",
            "accent": "#0078D4",
            "success": "#6CCB5F",
            "warning": "#FCE100",
            "error": "#FF6B6B",
            "shadow": "rgba(0, 0, 0, 0.1)",
        },
    }
    
    palettes = {
        "水生": "#006994",
        "沙漠": "#C19A6B",
        "黄昏": "#FF6B6B",
        "夜空": "#2C3E50",
    }
    
    styles = {
        "普通平铺": "flat",
        "3D立体": "3d",
    }
    
    def __init__(self, theme_name: str=USER_DEFAULT_THEME):
        self._theme_name = theme_name
        self._palette_name = "水生"
        self._style_name = "普通平铺"
        self.current_colors = self.themes.get(theme_name, self.themes["dark"])
    
    def switch_theme(self, theme_name: str) -> bool:
        if theme_name in self.themes:
            self._theme_name = theme_name
            self.current_colors = self.themes[theme_name]
            return True
        return False
    
    def switch_palette(self, palette_name: str) -> bool:
        if palette_name in self.palettes:
            self._palette_name = palette_name
            # 这里可以根据调色板名称更新颜色
            return True
        return False
    
    def switch_style(self, style_name: str) -> bool:
        if style_name in self.styles:
            self._style_name = style_name
            return True
        return False
    
    def get_color(self, color_name: str) -> str:
        return self.current_colors.get(color_name, "#000000")
    
    @property
    def theme_name(self) -> str:
        return self._theme_name
    
    @property
    def palette_name(self) -> str:
        return self._palette_name
    
    @property
    def style_name(self) -> str:
        return self._style_name


# *** 调试逻辑 ***
if __name__ == "__main__":
    config = ThemeConfig()
    print(f"当前主题: {config.theme_name}")
    print(f"主背景色: {config.get_color('bg_primary')}")
