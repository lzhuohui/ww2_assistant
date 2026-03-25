# -*- coding: utf-8 -*-
"""
模块名称：UIConfig
模块功能：界面配置管理，主题、颜色、尺寸
实现步骤：
- 定义主题颜色方案
- 支持主题切换
- 提供尺寸配置
"""

from typing import Dict, Any


USER_DEFAULT_THEME = "dark"
USER_DEFAULT_PALETTE = "水生"
USER_DEFAULT_STYLE = "3D立体"


THEMES = {
    "light": {
        "bg_primary": "#FFFFFF",
        "bg_secondary": "#F5F5F5",
        "text_primary": "#1A1A2E",
        "text_secondary": "#666666",
        "text_disabled": "#999999",
        "accent": "#0078D4",
        "border": "#E0E0E0",
        "success": "#107C10",
        "error": "#D13438",
        "warning": "#FFB900",
    },
    "dark": {
        "bg_primary": "#1A1A2E",
        "bg_secondary": "#252542",
        "text_primary": "#FFFFFF",
        "text_secondary": "#B0B0B0",
        "text_disabled": "#666666",
        "accent": "#0078D4",
        "border": "#3D3D5C",
        "success": "#107C10",
        "error": "#D13438",
        "warning": "#FFB900",
    },
}

PALETTES = {
    "水生": {"accent": "#006994"},
    "沙漠": {"accent": "#C19A6B"},
    "黄昏": {"accent": "#FF6B6B"},
    "夜空": {"accent": "#2C3E50"},
}

SIZES = {
    "spacing_xs": 4,
    "spacing_sm": 8,
    "spacing_md": 12,
    "spacing_lg": 16,
    "spacing_xl": 24,
    "card_height": 70,
    "card_padding": 12,
    "icon_sm": 16,
    "icon_md": 20,
    "icon_lg": 24,
    "font_sm": 10,
    "font_md": 12,
    "font_lg": 14,
    "font_xl": 16,
}


class UIConfig:
    """界面配置"""
    
    def __init__(
        self,
        theme_name: str = USER_DEFAULT_THEME,
        palette_name: str = USER_DEFAULT_PALETTE,
        style_name: str = USER_DEFAULT_STYLE,
    ):
        self._theme_name = theme_name
        self._palette_name = palette_name
        self._style_name = style_name
        self._sizes = SIZES.copy()
    
    @property
    def theme_name(self) -> str:
        return self._theme_name
    
    @property
    def palette_name(self) -> str:
        return self._palette_name
    
    @property
    def current_style_name(self) -> str:
        return self._style_name
    
    @property
    def 当前主题颜色(self) -> Dict[str, str]:
        colors = THEMES.get(self._theme_name, THEMES["dark"]).copy()
        if self._palette_name in PALETTES:
            colors.update(PALETTES[self._palette_name])
        return colors
    
    def get_size(self, category: str, name: str) -> int:
        """获取尺寸配置"""
        return self._sizes.get(name, self._sizes.get(f"{category}_{name}", 0))
    
    def switch_theme(self, theme_name: str) -> None:
        """切换主题"""
        if theme_name in THEMES:
            self._theme_name = theme_name
    
    def switch_palette(self, palette_name: str) -> None:
        """切换调色板"""
        if palette_name in PALETTES:
            self._palette_name = palette_name
    
    def switch_style(self, style_name: str) -> None:
        """切换风格"""
        self._style_name = style_name


# *** 标准测试格式: 仅调用被测模块,AI不得添加数据 ***
if __name__ == "__main__":
    config = UIConfig()
    print(f"主题: {config.theme_name}")
    print(f"调色板: {config.palette_name}")
    print(f"颜色: {config.当前主题颜色}")
