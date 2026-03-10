# -*- coding: utf-8 -*-
"""
界面配置 - 配置层

模块定位:
    管理界面尺寸和布局配置。

功能原理:
    1. 定义尺寸（字体、间距、圆角等）
    2. 定义布局参数（边距、宽度、高度等）

数据来源:
    无

使用场景:
    被组件层和其他需要界面尺寸的模块调用。

可独立运行调试: python 界面配置.py
"""

import flet as ft
from typing import Dict, Any
from .主题配置 import 主题配置


class 界面配置:
    """界面配置类 - 提供界面尺寸和布局管理"""
    
    # ==================== 尺寸定义 ====================
    定义尺寸 = {
        "字体": {
            "font_size_xs": 11,
            "font_size_sm": 12,
            "font_size_md": 14,
            "font_size_lg": 16,
            "font_size_xl": 20,
        },
        "字重": {
            "font_weight_normal": ft.FontWeight.NORMAL,
            "font_weight_medium": ft.FontWeight.W_500,
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
            "button_height": 36,
            "icon_size_small": 16,
            "icon_size_medium": 20,
            "icon_size_large": 24,
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
            "content_padding_left": 40,
            "content_padding_right": 40,
            "content_padding_top": 32,
            "content_padding_bottom": 32,
            "divider_padding_left": 12,
            "divider_padding_right": 12,
            "nav_padding_left": 8,
            "nav_padding_right": 8,
            "nav_padding_top": 8,
            "nav_padding_bottom": 8,
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
        "多行卡片": {
            "divider_width": 2,
            "divider_height": 60,
            "divider_opacity": 0.7,
            "divider_blur": 6,
            "left_width": 60,
            "divider_left": 90,
            "content_left": 130,
        },
        "通用卡片": {
            "control_margin_left": 20,
            "control_margin_right": 16,
            "control_h_spacing": 20,
            "control_v_spacing": 10,
            "controls_per_row": 2,
            "vertical_center": True,
        },
        "阴影": {
            "blur_default": 4,
            "blur_hover": 8,
            "spread": 0,
            "offset_y": 2,
            "offset_y_hover": 3,
        },
    }
    
    def __init__(self, 主题名称: str = "深色"):
        """初始化界面配置"""
        self._主题配置 = 主题配置(主题名称)
    
    def 切换主题(self, 主题名称: str):
        """切换主题"""
        return self._主题配置.切换主题(主题名称)
    
    def 获取颜色(self, 颜色名称: str) -> str:
        """获取指定颜色的值"""
        return self._主题配置.获取颜色(颜色名称)
    
    def 获取尺寸(self, 分类: str, 名称: str) -> Any:
        """获取指定尺寸的值"""
        分类数据 = self.定义尺寸.get(分类, {})
        return 分类数据.get(名称)
    
    @property
    def 主题名称(self) -> str:
        """获取当前主题名称"""
        return self._主题配置.主题名称
    
    @property
    def 当前主题颜色(self) -> Dict[str, str]:
        """获取当前主题颜色"""
        return self._主题配置.当前主题颜色


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    配置 = 界面配置()
    print(f"当前主题: {配置.主题名称}")
    print(f"主背景色: {配置.获取颜色('bg_primary')}")
    print(f"字体大小: {配置.获取尺寸('字体', 'font_size_md')}")
    print(f"间距: {配置.获取尺寸('间距', 'spacing_md')}")
    print(f"卡片高度: {配置.获取尺寸('卡片', 'default_height')}")
