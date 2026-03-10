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
    # 基础主题（深色/浅色）
    主题颜色 = {
        "深色": {
            # 背景色系（Win11规范）
            "bg_primary": "#202020",          # 主背景色
            "bg_secondary": "#252525",        # 次背景色（导航栏）
            "bg_card": "#2D2D2D",             # 卡片背景色
            "bg_input": "#2D2D2D",            # 输入框背景色
            "bg_selected": "#4D4D4D",         # 选中背景色
            "bg_hover": "#3D3D3D",            # 悬停背景色
            "bg_pressed": "#4A4A4A",          # 按下背景色
            
            # 文字色系（Win11规范）
            "text_primary": "#FFFFFF",        # 主文本色
            "text_secondary": "#C5C5C5",      # 次文本色
            "text_hint": "#8A8A8A",           # 提示文本色
            "text_disabled": "#5C5C5C",       # 禁用文本色
            
            # 边框色系（Win11规范）
            "border": "#3D3D3D",              # 边框色
            "border_light": "#333333",        # 浅边框色
            "divider": "#333333",             # 分隔线色
            
            # 强调色系（Win11规范）
            "accent": "#0078D4",              # 强调色
            "accent_hover": "#1A86D9",        # 悬停强调色
            "accent_pressed": "#006CBD",      # 按下强调色
            "accent_light": "#2B579A",        # 浅强调色
            
            # 状态色系（Win11规范）
            "success": "#6CCB5F",             # 成功色
            "warning": "#FCE100",             # 警告色
            "error": "#FF6B6B",               # 错误色
            "info": "#60CDFF",                # 信息色
            
            # 开关色系（Win11规范）
            "switch_thumb_on": "#FFFFFF",     # 开关按钮开启色
            "switch_thumb_off": "#FFFFFF",    # 开关按钮关闭色
            "switch_track_on": "#0078D4",     # 开关开启轨道色
            "switch_track_off": "#4A4A4A",    # 开关关闭轨道色
            "switch_border_off": "#666666",   # 开关关闭边框色
            
            # 阴影色系（Win11规范）
            "shadow": "rgba(0, 0, 0, 0.25)",  # 阴影色
            "shadow_hover": "rgba(0, 0, 0, 0.35)", # 悬停阴影色
        },
        "浅色": {
            # 背景色系（Win11规范）
            "bg_primary": "#F3F3F3",          # 主背景色
            "bg_secondary": "#FFFFFF",        # 次背景色（导航栏）
            "bg_card": "#FFFFFF",             # 卡片背景色
            "bg_input": "#FFFFFF",            # 输入框背景色
            "bg_selected": "#0078D4",         # 选中背景色
            "bg_hover": "#E5E5E5",            # 悬停背景色
            "bg_pressed": "#D0D0D0",          # 按下背景色
            
            # 文字色系（Win11规范）
            "text_primary": "#1A1A1A",        # 主文本色
            "text_secondary": "#666666",      # 次文本色
            "text_hint": "#999999",           # 提示文本色
            "text_disabled": "#CCCCCC",       # 禁用文本色
            
            # 边框色系（Win11规范）
            "border": "#D0D0D0",              # 边框色
            "border_light": "#E0E0E0",        # 浅边框色
            "divider": "#E0E0E0",             # 分隔线色
            
            # 强调色系（Win11规范）
            "accent": "#0078D4",              # 强调色
            "accent_hover": "#1A86D9",        # 悬停强调色
            "accent_pressed": "#006CBD",      # 按下强调色
            "accent_light": "#CCE4F7",        # 浅强调色
            
            # 状态色系（Win11规范）
            "success": "#6CCB5F",             # 成功色
            "warning": "#FCE100",             # 警告色
            "error": "#FF6B6B",               # 错误色
            "info": "#60CDFF",                # 信息色
            
            # 开关色系（Win11规范）
            "switch_thumb_on": "#FFFFFF",     # 开关按钮开启色
            "switch_thumb_off": "#666666",    # 开关按钮关闭色
            "switch_track_on": "#0078D4",     # 开关开启轨道色
            "switch_track_off": "#CCCCCC",    # 开关关闭轨道色
            "switch_border_off": "#999999",   # 开关关闭边框色
            
            # 阴影色系（Win11规范）
            "shadow": "rgba(0, 0, 0, 0.1)",   # 阴影色
            "shadow_hover": "rgba(0, 0, 0, 0.15)", # 悬停阴影色
        },
    }
    
    # ==================== 高对比度调色板定义 ====================
    高对比度调色板 = {
        # 高对比度调色板 - Aquatic（水生）
        "水生": {
            "bg_primary": "#000000",
            "bg_secondary": "#000000",
            "bg_card": "#000000",
            "bg_input": "#000000",
            "bg_selected": "#1A1A1A",
            "bg_hover": "#1A1A1A",
            "bg_pressed": "#2A2A2A",
            "text_primary": "#FFFFFF",
            "text_secondary": "#B4E7FF",
            "text_hint": "#7AC4FF",
            "text_disabled": "#5C5C5C",
            "border": "#00BCFF",
            "border_light": "#00BCFF",
            "divider": "#00BCFF",
            "accent": "#00BCFF",
            "accent_hover": "#33C9FF",
            "accent_pressed": "#00A3D9",
            "accent_light": "#004B6E",
            "success": "#00FF00",
            "warning": "#FFFF00",
            "error": "#FF0000",
            "info": "#00BCFF",
            "switch_thumb_on": "#FFFFFF",
            "switch_thumb_off": "#FFFFFF",
            "switch_track_on": "#00BCFF",
            "switch_track_off": "#333333",
            "switch_border_off": "#00BCFF",
            "shadow": "rgba(0, 0, 0, 0.5)",
            "shadow_hover": "rgba(0, 0, 0, 0.7)",
        },
        # 高对比度调色板 - Desert（沙漠）
        "沙漠": {
            "bg_primary": "#000000",
            "bg_secondary": "#000000",
            "bg_card": "#000000",
            "bg_input": "#000000",
            "bg_selected": "#1A1A1A",
            "bg_hover": "#1A1A1A",
            "bg_pressed": "#2A2A2A",
            "text_primary": "#FFFFFF",
            "text_secondary": "#FFD699",
            "text_hint": "#FFB84D",
            "text_disabled": "#5C5C5C",
            "border": "#FFB900",
            "border_light": "#FFB900",
            "divider": "#FFB900",
            "accent": "#FFB900",
            "accent_hover": "#FFC733",
            "accent_pressed": "#CC9400",
            "accent_light": "#4D3700",
            "success": "#00FF00",
            "warning": "#FFFF00",
            "error": "#FF0000",
            "info": "#FFB900",
            "switch_thumb_on": "#FFFFFF",
            "switch_thumb_off": "#FFFFFF",
            "switch_track_on": "#FFB900",
            "switch_track_off": "#333333",
            "switch_border_off": "#FFB900",
            "shadow": "rgba(0, 0, 0, 0.5)",
            "shadow_hover": "rgba(0, 0, 0, 0.7)",
        },
        # 高对比度调色板 - Dusk（黄昏）
        "黄昏": {
            "bg_primary": "#000000",
            "bg_secondary": "#000000",
            "bg_card": "#000000",
            "bg_input": "#000000",
            "bg_selected": "#1A1A1A",
            "bg_hover": "#1A1A1A",
            "bg_pressed": "#2A2A2A",
            "text_primary": "#FFFFFF",
            "text_secondary": "#FFB3D9",
            "text_hint": "#FF80BF",
            "text_disabled": "#5C5C5C",
            "border": "#FF00FF",
            "border_light": "#FF00FF",
            "divider": "#FF00FF",
            "accent": "#FF00FF",
            "accent_hover": "#FF33FF",
            "accent_pressed": "#CC00CC",
            "accent_light": "#4D004D",
            "success": "#00FF00",
            "warning": "#FFFF00",
            "error": "#FF0000",
            "info": "#FF00FF",
            "switch_thumb_on": "#FFFFFF",
            "switch_thumb_off": "#FFFFFF",
            "switch_track_on": "#FF00FF",
            "switch_track_off": "#333333",
            "switch_border_off": "#FF00FF",
            "shadow": "rgba(0, 0, 0, 0.5)",
            "shadow_hover": "rgba(0, 0, 0, 0.7)",
        },
        # 高对比度调色板 - Night sky（夜空）
        "夜空": {
            "bg_primary": "#000000",
            "bg_secondary": "#000000",
            "bg_card": "#000000",
            "bg_input": "#000000",
            "bg_selected": "#1A1A1A",
            "bg_hover": "#1A1A1A",
            "bg_pressed": "#2A2A2A",
            "text_primary": "#FFFFFF",
            "text_secondary": "#B3D9FF",
            "text_hint": "#66B3FF",
            "text_disabled": "#5C5C5C",
            "border": "#0066FF",
            "border_light": "#0066FF",
            "divider": "#0066FF",
            "accent": "#0066FF",
            "accent_hover": "#3385FF",
            "accent_pressed": "#0052CC",
            "accent_light": "#00265C",
            "success": "#00FF00",
            "warning": "#FFFF00",
            "error": "#FF0000",
            "info": "#0066FF",
            "switch_thumb_on": "#FFFFFF",
            "switch_thumb_off": "#FFFFFF",
            "switch_track_on": "#0066FF",
            "switch_track_off": "#333333",
            "switch_border_off": "#0066FF",
            "shadow": "rgba(0, 0, 0, 0.5)",
            "shadow_hover": "rgba(0, 0, 0, 0.7)",
        },
    }
    
    def __init__(self, 主题名称: str = "深色", 调色板名称: str = None):
        """初始化主题配置"""
        self._主题名称 = 主题名称
        self._调色板名称 = 调色板名称
        
        # 优先使用调色板，如果没有则使用主题
        if 调色板名称 and 调色板名称 in self.高对比度调色板:
            self.当前主题颜色 = self.高对比度调色板[调色板名称]
        else:
            self.当前主题颜色 = self.主题颜色.get(主题名称, self.主题颜色["深色"])
    
    def 切换主题(self, 主题名称: str):
        """切换主题"""
        if 主题名称 in self.主题颜色:
            self._主题名称 = 主题名称
            self._调色板名称 = None
            self.当前主题颜色 = self.主题颜色[主题名称]
            return True
        return False
    
    def 切换调色板(self, 调色板名称: str):
        """切换高对比度调色板"""
        if 调色板名称 in self.高对比度调色板:
            self._调色板名称 = 调色板名称
            self.当前主题颜色 = self.高对比度调色板[调色板名称]
            return True
        return False
    
    def 获取颜色(self, 颜色名称: str) -> str:
        """获取指定颜色的值"""
        return self.当前主题颜色.get(颜色名称, "#000000")
    
    @property
    def 主题名称(self) -> str:
        """获取当前主题名称"""
        return self._主题名称
    
    @property
    def 调色板名称(self) -> str:
        """获取当前调色板名称"""
        return self._调色板名称
    
    def 获取所有主题(self) -> list:
        """获取所有主题名称"""
        return list(self.主题颜色.keys())
    
    def 获取所有调色板(self) -> list:
        """获取所有调色板名称"""
        return list(self.高对比度调色板.keys())


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
