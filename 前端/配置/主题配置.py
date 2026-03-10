# -*- coding: utf-8 -*-
"""
主题配置 - 配置层

模块定位:
    管理主题颜色配置，包括深色主题和浅色主题。

功能原理:
    1. 定义主题颜色（深色主题和浅色主题）
    2. 提供主题切换和颜色获取功能

数据来源:
    无

使用场景:
    被界面配置和其他需要主题颜色的模块调用。

可独立运行调试: python 主题配置.py
"""

import flet as ft
from typing import Dict, Any


class 主题配置:
    """主题配置类 - 提供主题颜色管理"""
    
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
    
    def __init__(self, 主题名称: str = "深色"):
        """初始化主题配置"""
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
    
    @property
    def 主题名称(self) -> str:
        """获取当前主题名称"""
        return self._主题名称


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    配置 = 主题配置()
    print(f"当前主题: {配置.主题名称}")
    print(f"主背景色: {配置.获取颜色('bg_primary')}")
    print(f"卡片背景色: {配置.获取颜色('bg_card')}")
    print(f"主文本色: {配置.获取颜色('text_primary')}")
    print(f"边框色: {配置.获取颜色('border')}")
    print(f"浅边框色: {配置.获取颜色('border_light')}")
    print(f"阴影色: {配置.获取颜色('shadow')}")
