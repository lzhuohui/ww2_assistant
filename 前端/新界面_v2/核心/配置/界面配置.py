# -*- coding: utf-8 -*-
"""
模块名称：界面配置
设计思路: 管理界面尺寸和布局配置
模块隔离: 纯配置模块，依赖主题配置
"""

from typing import Dict, Any
from .主题配置 import 主题配置, USER_DEFAULT_THEME


# *** 用户指定变量 - AI不得修改 ***
# （用户未指定变量）
# *********************************


class 界面配置:
    """界面配置类 - 提供界面尺寸和布局管理"""
    
    定义尺寸 = {
        "字体": {
            "font_family": "Segoe UI Variable, Segoe UI, system-ui, sans-serif",
            "font_size_body": 14,
            "font_size_title": 16,
        },
        "间距": {
            "spacing_xs": 4,
            "spacing_sm": 8,
            "spacing_md": 12,
            "spacing_lg": 16,
        },
        "圆角": {
            "radius_sm": 4,
            "radius_md": 8,
            "radius_lg": 12,
        },
        "组件": {
            "button_height": 32,
            "input_height": 35,
            "icon_size": 20,
        },
        "卡片": {
            "default_height": 70,
            "default_spacing": 10,
        },
        "动画": {
            "duration_fast": 167,
            "duration_normal": 250,
        },
    }
    
    def __init__(self, 主题名称: str=USER_DEFAULT_THEME):
        self._主题配置 = 主题配置(主题名称)
    
    def 切换主题(self, 主题名称: str) -> bool:
        return self._主题配置.切换主题(主题名称)
    
    def 获取颜色(self, 颜色名称: str) -> str:
        return self._主题配置.获取颜色(颜色名称)
    
    def 获取尺寸(self, 分类: str, 名称: str) -> Any:
        分类数据 = self.定义尺寸.get(分类, {})
        return 分类数据.get(名称)
    
    @property
    def 主题名称(self) -> str:
        return self._主题配置.主题名称
    
    @property
    def 当前主题颜色(self) -> Dict[str, str]:
        return self._主题配置.当前主题颜色


# *** 调试逻辑 ***
if __name__ == "__main__":
    config = 界面配置()
    print(f"当前主题: {config.主题名称}")
    print(f"字体: {config.获取尺寸('字体', 'font_family')}")
