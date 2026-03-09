# -*- coding: utf-8 -*-
"""
界面配置 - 原子层

模块定位:
    本模块是原子层模块，定义主题颜色、尺寸和常量。

功能原理:
    1. 定义主题颜色（深色主题和浅色主题）
    2. 定义尺寸（字体、间距、圆角等）
    3. 定义常量（边距、高度等）

数据来源:
    无

使用场景:
    被所有层级的模块调用，提供统一的配置。

可独立运行调试: python 界面配置.py
"""

import flet as ft
from typing import Dict, Any


class 界面配置:
    """界面配置类 - 提供主题颜色、尺寸和常量"""
    
    # ==================== 主题颜色定义 ====================
    主题颜色 = {
        "深色": {
            # 背景色系
            "bg_primary": "#1C1C1C",          # 主背景色
            "bg_secondary": "#2D2D2D",        # 次背景色
            "bg_card": "#252525",             # 卡片背景色
            "bg_input": "#2D2D2D",            # 输入框背景色
            "bg_selected": "#0078D4",         # 选中背景色
            "bg_hover": "#3D3D3D",            # 悬停背景色
            
            # 文字色系
            "text_primary": "#F2F2F2",        # 主文本色
            "text_secondary": "#CCCCCC",      # 次文本色
            "text_hint": "#999999",           # 提示文本色
            "text_disabled": "#606060",       # 禁用文本色
            
            # 边框色系
            "border": "#404040",              # 边框色
            "border_light": "#383838",        # 浅边框色
            "divider": "#333333",             # 分隔线色
            
            # 强调色系
            "accent": "#0078D4",              # 强调色
            "accent_light": "#2B579A",        # 浅强调色
            
            # 开关色系
            "switch_thumb_on": "#FFFFFF",     # 开关按钮开启色
            "switch_thumb_off": "#AAAAAA",    # 开关按钮关闭色
            "switch_track_off": "#333333",    # 开关关闭轨道色
            "switch_border": "#555555",       # 开关边框色
            
            # 阴影
            "shadow": "#00000040",            # 阴影色
        },
        "浅色": {
            # 背景色系
            "bg_primary": "#F3F3F3",          # 主背景色
            "bg_secondary": "#FFFFFF",        # 次背景色
            "bg_card": "#FFFFFF",             # 卡片背景色
            "bg_input": "#FFFFFF",            # 输入框背景色
            "bg_selected": "#0078D4",         # 选中背景色
            "bg_hover": "#E5E5E5",            # 悬停背景色
            
            # 文字色系
            "text_primary": "#1A1A1A",        # 主文本色
            "text_secondary": "#666666",      # 次文本色
            "text_hint": "#999999",           # 提示文本色
            "text_disabled": "#CCCCCC",       # 禁用文本色
            
            # 边框色系
            "border": "#D1D1D1",              # 边框色
            "border_light": "#E5E5E5",        # 浅边框色
            "divider": "#E5E5E5",             # 分隔线色
            
            # 强调色系
            "accent": "#0078D4",              # 强调色
            "accent_light": "#CCE4F7",        # 浅强调色
            
            # 开关色系
            "switch_thumb_on": "#FFFFFF",     # 开关按钮开启色
            "switch_thumb_off": "#666666",    # 开关按钮关闭色
            "switch_track_off": "#CCCCCC",    # 开关关闭轨道色
            "switch_border": "#999999",       # 开关边框色
            
            # 阴影
            "shadow": "#00000020",            # 阴影色
        }
    }
    
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
            "peripheral_margin": 10,          # 外围边距
            "nav_width": 240,                 # 导航栏宽度
            "user_info_height": 80,           # 用户信息高度
            "card_padding": 16,               # 卡片内边距
            "item_padding": 12,               # 项目内边距
            "card_spacing": 5,                # 卡片间距（标准间距）
            "card_radius": 8,                 # 卡片圆角（Win11风格）
            "card_border_width": 1,           # 卡片边框宽度
        }
    }
    
    def __init__(self, 主题名称: str = "深色"):
        """初始化界面配置"""
        self._主题名称 = 主题名称
        self.当前主题颜色 = self.主题颜色.get(主题名称, self.主题颜色["深色"])
    
    def 切换主题(self, 主题名称: str):
        """切换主题"""
        if 主题名称 in self.主题颜色:
            self._主题名称 = 主题名称
            self.当前主题颜色 = self.主题颜色[主题名称]
            return True
        return False
    
    def 获取颜色(self, 颜色名称: str) -> str:
        """获取指定颜色的值"""
        return self.当前主题颜色.get(颜色名称, "#000000")
    
    def 获取尺寸(self, 分类: str, 名称: str) -> Any:
        """获取指定尺寸的值"""
        分类数据 = self.定义尺寸.get(分类, {})
        return 分类数据.get(名称)
    
    @property
    def 主题名称(self) -> str:
        """获取当前主题名称"""
        return self._主题名称


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    配置 = 界面配置()
    print(f"当前主题: {配置.主题名称}")
    print(f"主背景色: {配置.获取颜色('bg_primary')}")
    print(f"卡片背景色: {配置.获取颜色('bg_card')}")
    print(f"主文本色: {配置.获取颜色('text_primary')}")
    print(f"边框色: {配置.获取颜色('border')}")
    print(f"浅边框色: {配置.获取颜色('border_light')}")
    print(f"阴影色: {配置.获取颜色('shadow')}")
