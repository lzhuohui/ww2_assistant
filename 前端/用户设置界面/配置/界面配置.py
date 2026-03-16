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
            "font_size_xs": 10,      # 微小文本（辅助信息、标签）
            "font_size_sm": 12,      # 小号（次要文字、描述）
            "font_size_md": 14,      # 中号（正文、按钮）
            "font_size_lg": 16,      # 大号（小标题）
            "font_size_xl": 20,      # 超大号（标题）
            "font_size_xxl": 24,     # 特大号（页面标题）
            "font_size_title": 28,   # 标题号（大标题）
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
            "button_height": 32,
            "button_height_large": 40,
            "icon_size_small": 16,
            "icon_size_medium": 20,
            "icon_size_large": 24,
            "input_height": 35,
            "dropdown_height": 35,
            "switch_width": 44,
            "switch_height": 22,
            "switch_width_small": 40,
            "switch_height_small": 20,
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
            "controls_per_row": 3,
            "vertical_center": True,
        },
        "阴影": {
            "blur_default": 4,
            "blur_hover": 12,
            "spread": 1,
            "spread_hover": 2,
            "offset_y": 2,
            "offset_y_hover": 4,
            "inset": 16,
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
            "duration_fast": 150,
            "duration_normal": 300,
            "duration_slow": 500,
            "curve": "EASE_OUT",
        },
    }
    
    def __init__(self, 主题名称: str = "深色", 调色板名称: str = None):
        """初始化界面配置"""
        self._主题配置 = 主题配置(主题名称, 调色板名称)
    
    def 切换主题(self, 主题名称: str):
        """切换主题"""
        return self._主题配置.切换主题(主题名称)
    
    def 切换调色板(self, 调色板名称: str):
        """切换调色板"""
        return self._主题配置.切换调色板(调色板名称)
    
    def 获取颜色(self, 颜色名称: str) -> str:
        """获取指定颜色的值"""
        return self._主题配置.获取颜色(颜色名称)
    
    def 获取尺寸(self, 分类: str, 名称: str) -> Any:
        """获取指定尺寸的值"""
        分类数据 = self.定义尺寸.get(分类, {})
        return 分类数据.get(名称)
    
    @property
    def 主题名称(self):
        """获取当前主题名称"""
        return self._主题配置.主题名称
    
    @property
    def 调色板名称(self):
        """获取当前调色板名称"""
        return self._主题配置.调色板名称
    
    @property
    def 当前主题颜色(self):
        """获取当前主题颜色"""
        return self._主题配置.当前主题颜色
    
    def 获取风格配置(self) -> dict:
        """获取当前风格配置"""
        风格名称 = self.定义尺寸.get("风格", {}).get("current_style", "3D立体")
        风格配置 = self.定义尺寸.get("风格", {}).get("styles", {}).get(风格名称, {})
        return 风格配置
    
    def 切换风格(self, 风格名称: str):
        """切换风格"""
        if 风格名称 in self.定义尺寸.get("风格", {}).get("styles", {}):
            self.定义尺寸["风格"]["current_style"] = 风格名称
            return True
        return False
    
    @property
    def 当前风格名称(self):
        """获取当前风格名称"""
        return self.定义尺寸.get("风格", {}).get("current_style", "3D立体")


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    配置 = 界面配置()
    print(f"当前主题: {配置.主题名称}")
    print(f"主背景色: {配置.获取颜色('bg_primary')}")
    print(f"字体大小: {配置.获取尺寸('字体', 'font_size_md')}")
    print(f"间距: {配置.获取尺寸('间距', 'spacing_md')}")
    print(f"卡片高度: {配置.获取尺寸('卡片', 'default_height')}")
