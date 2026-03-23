# -*- coding: utf-8 -*-
"""
模块名称：主题配置
设计思路: 管理主题颜色配置，支持深色/浅色主题切换
模块隔离: 纯配置模块，无外部依赖
"""

from typing import Dict, Any


# *** 用户指定变量 - AI不得修改 ***
USER_DEFAULT_THEME = "深色"
# *********************************


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
        "浅色": {
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
    
    def __init__(self, 主题名称: str=USER_DEFAULT_THEME):
        self._主题名称 = 主题名称
        self.当前主题颜色 = self.主题颜色.get(主题名称, self.主题颜色["深色"])
    
    def 切换主题(self, 主题名称: str) -> bool:
        if 主题名称 in self.主题颜色:
            self._主题名称 = 主题名称
            self.当前主题颜色 = self.主题颜色[主题名称]
            return True
        return False
    
    def 获取颜色(self, 颜色名称: str) -> str:
        return self.当前主题颜色.get(颜色名称, "#000000")
    
    @property
    def 主题名称(self) -> str:
        return self._主题名称


# *** 调试逻辑 ***
if __name__ == "__main__":
    config = 主题配置()
    print(f"当前主题: {config.主题名称}")
    print(f"主背景色: {config.获取颜色('bg_primary')}")
