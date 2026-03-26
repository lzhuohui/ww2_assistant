# -*- coding: utf-8 -*-
"""
模块名称：UIConfig
模块功能：界面配置管理，主题、颜色、尺寸
实现步骤：
- 定义主题颜色方案（浅色/深色）
- 定义强调色系统
- 支持主题和强调色切换
- 遵循Windows 11 Fluent Design规范
"""

from typing import Dict, Any


# *** 用户指定变量: 变量值必须生效,AI不得更改数据 ***
USER_DEFAULT_THEME = "dark"
USER_DEFAULT_ACCENT = "blue"
# *********************************


THEMES = {
    "light": {
        "bg_primary": "#F3F3F3",
        "bg_secondary": "#FFFFFF",
        "bg_tertiary": "#F9F9F9",
        "bg_card": "#FFFFFF",
        "bg_input": "#FFFFFF",
        "bg_hover": "#E5E5E5",
        "bg_selected": "#0078D4",
        "bg_disabled": "#F3F3F3",
        "text_primary": "#1A1A1A",
        "text_secondary": "#5C5C5C",
        "text_tertiary": "#8A8A8A",
        "text_disabled": "#A0A0A0",
        "text_on_accent": "#FFFFFF",
        "border": "#D1D1D1",
        "border_hover": "#B4B4B4",
        "border_focus": "#0078D4",
        "border_error": "#C42B1C",
        "success": "#107C10",
        "success_bg": "#E6F4E6",
        "error": "#C42B1C",
        "error_bg": "#FDE7E7",
        "warning": "#FFB900",
        "warning_bg": "#FFF4CE",
        "info": "#0078D4",
        "info_bg": "#E5F1FB",
        "shadow": "rgba(0, 0, 0, 0.13)",
        "shadow_hover": "rgba(0, 0, 0, 0.18)",
        "divider": "#E5E5E5",
        "overlay": "rgba(0, 0, 0, 0.4)",
    },
    "dark": {
        "bg_primary": "#202020",
        "bg_secondary": "#282828",
        "bg_tertiary": "#2D2D2D",
        "bg_card": "#2D2D2D",
        "bg_input": "#2D2D2D",
        "bg_hover": "#3D3D3D",
        "bg_selected": "#0078D4",
        "bg_disabled": "#202020",
        "text_primary": "#FFFFFF",
        "text_secondary": "#C5C5C5",
        "text_tertiary": "#9A9A9A",
        "text_disabled": "#656565",
        "text_on_accent": "#FFFFFF",
        "border": "#3D3D3D",
        "border_hover": "#5C5C5C",
        "border_focus": "#60CDFF",
        "border_error": "#FF6B6B",
        "success": "#6CCB5F",
        "success_bg": "#1A3A1A",
        "error": "#FF6B6B",
        "error_bg": "#3A1A1A",
        "warning": "#FFB900",
        "warning_bg": "#3A3010",
        "info": "#60CDFF",
        "info_bg": "#1A2A3A",
        "shadow": "rgba(0, 0, 0, 0.25)",
        "shadow_hover": "rgba(0, 0, 0, 0.35)",
        "divider": "#3D3D3D",
        "overlay": "rgba(0, 0, 0, 0.6)",
    },
}

ACCENT_COLORS = {
    "blue": {
        "name": "蓝色",
        "value": "#0078D4",
        "light": "#1A86D9",
        "dark": "#0078D4",
    },
    "cyan": {
        "name": "青色",
        "value": "#00B7C3",
        "light": "#00C8D4",
        "dark": "#00B7C3",
    },
    "green": {
        "name": "绿色",
        "value": "#107C10",
        "light": "#0B8A0B",
        "dark": "#107C10",
    },
    "orange": {
        "name": "橙色",
        "value": "#FF8C00",
        "light": "#FFA500",
        "dark": "#FF8C00",
    },
    "pink": {
        "name": "粉色",
        "value": "#E3008C",
        "light": "#FF69B4",
        "dark": "#E3008C",
    },
    "purple": {
        "name": "紫色",
        "value": "#8764B8",
        "light": "#9F7AEA",
        "dark": "#8764B8",
    },
    "red": {
        "name": "红色",
        "value": "#D13438",
        "light": "#E81123",
        "dark": "#D13438",
    },
    "teal": {
        "name": "青绿",
        "value": "#00B294",
        "light": "#00C9A7",
        "dark": "#00B294",
    },
    "yellow": {
        "name": "黄色",
        "value": "#FFB900",
        "light": "#FFC107",
        "dark": "#FFB900",
    },
}

SIZES = {
    "spacing_xs": 4,
    "spacing_sm": 8,
    "spacing_md": 12,
    "spacing_lg": 16,
    "spacing_xl": 24,
    "spacing_xxl": 32,
    "card_height": 70,
    "card_height_sm": 48,
    "card_height_lg": 100,
    "card_padding": 12,
    "card_padding_sm": 8,
    "card_padding_lg": 16,
    "card_border_radius": 8,
    "card_border_radius_sm": 4,
    "card_border_radius_lg": 12,
    "icon_xs": 12,
    "icon_sm": 16,
    "icon_md": 20,
    "icon_lg": 24,
    "icon_xl": 32,
    "font_caption": 10,
    "font_sm": 12,
    "font_md": 14,
    "font_lg": 16,
    "font_xl": 20,
    "font_xxl": 24,
    "font_display": 28,
    "button_height_sm": 28,
    "button_height": 32,
    "button_height_lg": 40,
    "button_min_width": 80,
    "input_height_sm": 28,
    "input_height": 32,
    "input_height_lg": 40,
    "input_width": 120,
    "dropdown_width": 120,
    "dropdown_height": 32,
    "nav_width": 240,
    "nav_item_height": 40,
    "title_bar_height": 40,
    "divider_height": 1,
}

ANIMATION = {
    "duration_fast": 100,
    "duration_normal": 150,
    "duration_slow": 200,
    "duration_page": 300,
}

TYPOGRAPHY = {
    "font_family": "Segoe UI Variable, Segoe UI, system-ui, -apple-system, sans-serif",
    "font_family_mono": "Cascadia Code, Consolas, monospace",
    "weight_regular": 400,
    "weight_medium": 500,
    "weight_semibold": 600,
    "weight_bold": 700,
}


class UIConfig:
    """界面配置"""
    
    def __init__(
        self,
        theme_name: str = USER_DEFAULT_THEME,
        accent_name: str = USER_DEFAULT_ACCENT,
    ):
        self._theme_name = theme_name
        self._accent_name = accent_name
        self._sizes = SIZES.copy()
        self._animation = ANIMATION.copy()
        self._typography = TYPOGRAPHY.copy()
    
    @property
    def theme_name(self) -> str:
        return self._theme_name
    
    @property
    def accent_name(self) -> str:
        return self._accent_name
    
    @property
    def 当前主题颜色(self) -> Dict[str, str]:
        colors = THEMES.get(self._theme_name, THEMES["dark"]).copy()
        accent = ACCENT_COLORS.get(self._accent_name, ACCENT_COLORS["blue"])
        
        if self._theme_name == "dark":
            colors["accent"] = accent["dark"]
            colors["accent_hover"] = self._lighten_color(accent["dark"], 0.1)
            colors["accent_pressed"] = self._darken_color(accent["dark"], 0.1)
        else:
            colors["accent"] = accent["value"]
            colors["accent_hover"] = accent["light"]
            colors["accent_pressed"] = self._darken_color(accent["value"], 0.1)
        
        colors["bg_selected"] = colors["accent"]
        colors["border_focus"] = colors["accent"]
        colors["info"] = colors["accent"]
        
        return colors
    
    def _lighten_color(self, hex_color: str, amount: float) -> str:
        """使颜色变亮"""
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        
        r = min(255, int(r + (255 - r) * amount))
        g = min(255, int(g + (255 - g) * amount))
        b = min(255, int(b + (255 - b) * amount))
        
        return f"#{r:02X}{g:02X}{b:02X}"
    
    def _darken_color(self, hex_color: str, amount: float) -> str:
        """使颜色变暗"""
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        
        r = max(0, int(r * (1 - amount)))
        g = max(0, int(g * (1 - amount)))
        b = max(0, int(b * (1 - amount)))
        
        return f"#{r:02X}{g:02X}{b:02X}"
    
    def get_color(self, color_name: str) -> str:
        """获取颜色配置"""
        colors = self.当前主题颜色
        return colors.get(color_name, "#000000")
    
    def get_size(self, category: str, name: str) -> int:
        """获取尺寸配置"""
        return self._sizes.get(name, self._sizes.get(f"{category}_{name}", 0))
    
    def get_animation(self, name: str) -> int:
        """获取动画配置"""
        return self._animation.get(name, 150)
    
    def get_typography(self, name: str) -> Any:
        """获取字体配置"""
        return self._typography.get(name)
    
    def switch_theme(self, theme_name: str) -> None:
        """切换主题"""
        if theme_name in THEMES:
            self._theme_name = theme_name
    
    def switch_accent(self, accent_name: str) -> None:
        """切换强调色"""
        if accent_name in ACCENT_COLORS:
            self._accent_name = accent_name
    
    @staticmethod
    def get_available_themes() -> Dict[str, str]:
        """获取可用主题列表"""
        return {
            "light": "浅色",
            "dark": "深色",
        }
    
    @staticmethod
    def get_available_accents() -> Dict[str, Dict[str, str]]:
        """获取可用强调色列表"""
        return ACCENT_COLORS.copy()


# *** 标准测试格式: 仅调用被测模块,AI不得添加数据 ***
if __name__ == "__main__":
    config = UIConfig()
    print(f"主题: {config.theme_name}")
    print(f"强调色: {config.accent_name}")
    print(f"可用主题: {config.get_available_themes()}")
    print(f"可用强调色: {list(config.get_available_accents().keys())}")
    print(f"当前强调色: {config.get_color('accent')}")
