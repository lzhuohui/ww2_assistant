# -*- coding: utf-8 -*-
"""模块名称：主题配置 | 设计思路：管理主题颜色配置，支持深色/浅色主题切换 | 模块隔离原则"""

import flet as ft
from typing import Dict, Any


class 主题配置:
    """主题配置类 - 提供主题颜色管理"""
    
    主题颜色 = {
        "深色": {
            "bg_primary": "#202020",
            "bg_secondary": "#252525",
            "bg_card": "#2D2D2D",
            "bg_input": "#2D2D2D",
            "bg_selected": "#4D4D4D",
            "bg_hover": "#3D3D3D",
            "bg_pressed": "#4A4A4A",
            "text_primary": "#FFFFFF",
            "text_secondary": "#C5C5C5",
            "text_hint": "#8A8A8A",
            "text_disabled": "#5C5C5C",
            "border": "#3D3D3D",
            "border_light": "#333333",
            "divider": "#333333",
            "accent": "#0078D4",
            "accent_hover": "#1A86D9",
            "accent_pressed": "#006CBD",
            "accent_light": "#2B579A",
            "success": "#6CCB5F",
            "warning": "#FCE100",
            "error": "#FF6B6B",
            "info": "#60CDFF",
            "switch_thumb_on": "#FFFFFF",
            "switch_thumb_off": "#FFFFFF",
            "switch_track_on": "#0078D4",
            "switch_track_off": "#4A4A4A",
            "switch_border_off": "#666666",
            "shadow": "rgba(0, 0, 0, 0.25)",
            "shadow_hover": "rgba(0, 0, 0, 0.35)",
        },
        "浅色": {
            "bg_primary": "#F3F3F3",
            "bg_secondary": "#FFFFFF",
            "bg_card": "#FFFFFF",
            "bg_input": "#FFFFFF",
            "bg_selected": "#0078D4",
            "bg_hover": "#E5E5E5",
            "bg_pressed": "#D0D0D0",
            "text_primary": "#1A1A1A",
            "text_secondary": "#666666",
            "text_hint": "#999999",
            "text_disabled": "#CCCCCC",
            "border": "#D0D0D0",
            "border_light": "#E0E0E0",
            "divider": "#E0E0E0",
            "accent": "#0078D4",
            "accent_hover": "#1A86D9",
            "accent_pressed": "#006CBD",
            "accent_light": "#CCE4F7",
            "success": "#6CCB5F",
            "warning": "#FCE100",
            "error": "#FF6B6B",
            "info": "#60CDFF",
            "switch_thumb_on": "#FFFFFF",
            "switch_thumb_off": "#666666",
            "switch_track_on": "#0078D4",
            "switch_track_off": "#CCCCCC",
            "switch_border_off": "#999999",
            "shadow": "rgba(0, 0, 0, 0.1)",
            "shadow_hover": "rgba(0, 0, 0, 0.15)",
        },
    }
    
    高对比度调色板 = {
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
    }
    
    def __init__(self, 主题名称: str="深色", 调色板名称: str=None):
        self._主题名称 = 主题名称
        self._调色板名称 = 调色板名称
        
        if 调色板名称 and 调色板名称 in self.高对比度调色板:
            self.当前主题颜色 = self.高对比度调色板[调色板名称]
        else:
            self.当前主题颜色 = self.主题颜色.get(主题名称, self.主题颜色["深色"])
    
    def 切换主题(self, 主题名称: str):
        if 主题名称 in self.主题颜色:
            self._主题名称 = 主题名称
            self._调色板名称 = None
            self.当前主题颜色 = self.主题颜色[主题名称]
            return True
        return False
    
    def 切换调色板(self, 调色板名称: str):
        if 调色板名称 in self.高对比度调色板:
            self._调色板名称 = 调色板名称
            self.当前主题颜色 = self.高对比度调色板[调色板名称]
            return True
        elif 调色板名称 is None or 调色板名称 == "":
            self._调色板名称 = None
            self.当前主题颜色 = self.主题颜色[self._主题名称]
            return True
        return False
    
    def 获取颜色(self, 颜色名称: str) -> str:
        return self.当前主题颜色.get(颜色名称, "#000000")
    
    @property
    def 主题名称(self) -> str:
        return self._主题名称
    
    @property
    def 调色板名称(self) -> str:
        return self._调色板名称


if __name__ == "__main__":
    配置 = 主题配置()
    print(f"当前主题: {配置.主题名称}")
    print(f"主背景色: {配置.获取颜色('bg_primary')}")
