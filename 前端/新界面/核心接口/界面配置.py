# -*- coding: utf-8 -*-
"""模块名称：界面配置 | 设计思路：管理界面尺寸和布局配置 | 模块隔离原则"""

import flet as ft
from typing import Dict, Any
from .主题配置 import 主题配置


class 界面配置:
    """界面配置类 - 提供界面尺寸和布局管理"""
    
    定义尺寸 = {
        "字体": {
            "font_family": "Segoe UI Variable, Segoe UI, system-ui, -apple-system, sans-serif",
            "font_family_mono": "Cascadia Code, Consolas, monospace",
            "font_size_caption": 12,
            "font_size_body": 14,
            "font_size_body_large": 18,
            "font_size_subtitle": 20,
            "font_size_title": 28,
            "font_size_title_large": 40,
            "font_size_display": 68,
        },
        "字重": {
            "font_weight_normal": ft.FontWeight.NORMAL,
            "font_weight_semibold": ft.FontWeight.W_500,
            "font_weight_bold": ft.FontWeight.BOLD,
        },
        "间距": {
            "spacing_xs": 4,
            "spacing_sm": 8,
            "spacing_md": 12,
            "spacing_lg": 16,
            "spacing_xl": 20,
        },
        "圆角": {
            "radius_xs": 4,
            "radius_sm": 8,
            "radius_md": 12,
            "radius_lg": 16,
        },
        "组件": {
            "button_height": 32,
            "button_height_large": 40,
            "icon_size_small": 16,
            "icon_size_medium": 20,
            "icon_size_large": 24,
            "input_height": 35,
            "dropdown_height": 35,
            "switch_width": 44,
            "switch_height": 22,
        },
        "界面": {
            "peripheral_margin": 10,
            "nav_width": 240,
            "user_info_height": 80,
            "card_padding": 16,
            "item_padding": 12,
            "card_spacing": 5,
            "card_radius": 8,
            "card_border_width": 1,
            "window_width": 1200,
            "window_height": 540,
            "left_panel_width": 280,
            "content_padding_left": 20,
            "content_padding_right": 10,
            "content_padding_top": 10,
            "content_padding_bottom": 10,
        },
        "卡片": {
            "default_height": 70,
            "default_spacing": 10,
            "items_per_row": 6,
            "row_height": 32,
            "icon_size": 24,
            "title_size": 14,
            "desc_size": 12,
        },
        "阴影": {
            "blur_default": 4,
            "blur_hover": 12,
            "spread": 1,
            "spread_hover": 2,
            "offset_y": 2,
            "offset_y_hover": 4,
        },
        "风格": {
            "current_style": "3D立体",
            "styles": {
                "普通平铺": {
                    "border_radius": 0,
                    "shadow_blur": 0,
                    "shadow_spread": 0,
                    "shadow_offset_y": 0,
                    "border_width": 0,
                },
                "3D立体": {
                    "border_radius": 8,
                    "shadow_blur": 8,
                    "shadow_spread": 1,
                    "shadow_offset_y": 2,
                    "border_width": 1,
                },
            },
        },
        "动画": {
            "duration_instant": 83,
            "duration_fast": 167,
            "duration_normal": 250,
            "duration_slow": 333,
            "curve_direct_out": "EASE_OUT",
        },
    }
    
    def __init__(self, 主题名称: str="深色", 调色板名称: str=None):
        self._主题配置 = 主题配置(主题名称, 调色板名称)
    
    def 切换主题(self, 主题名称: str):
        return self._主题配置.切换主题(主题名称)
    
    def 切换调色板(self, 调色板名称: str):
        return self._主题配置.切换调色板(调色板名称)
    
    def 获取颜色(self, 颜色名称: str) -> str:
        return self._主题配置.获取颜色(颜色名称)
    
    def 获取尺寸(self, 分类: str, 名称: str) -> Any:
        分类数据 = self.定义尺寸.get(分类, {})
        return 分类数据.get(名称)
    
    @property
    def 主题名称(self):
        return self._主题配置.主题名称
    
    @property
    def 调色板名称(self):
        return self._主题配置.调色板名称
    
    @property
    def 当前主题颜色(self):
        return self._主题配置.当前主题颜色
    
    def 获取风格配置(self) -> dict:
        风格名称 = self.定义尺寸.get("风格", {}).get("current_style", "3D立体")
        return self.定义尺寸.get("风格", {}).get("styles", {}).get(风格名称, {})


if __name__ == "__main__":
    配置 = 界面配置()
    print(f"当前主题: {配置.主题名称}")
    print(f"主背景色: {配置.获取颜色('bg_primary')}")
