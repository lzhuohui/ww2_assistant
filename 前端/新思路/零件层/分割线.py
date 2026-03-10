# -*- coding: utf-8 -*-
"""
分割线 - 零件层（新思路）

设计思路:
    最小模块化的垂直分割线组件，用于分隔左右区域。

功能:
    1. 垂直线：固定宽度
    2. 阴影：发光效果
    3. 状态切换：启用/禁用透明度变化

数据来源:
    所有配置数据从配置目录获取。

使用场景:
    被组件层模块调用。

可独立运行调试: python 分割线.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft
from typing import Optional
from 配置.界面配置 import 界面配置


class Divider:
    """分割线 - 垂直分割线+发光效果"""
    
    @staticmethod
    def create(
        config: 界面配置,
        height: int = None,
        enabled: bool = True,
        **kwargs
    ) -> ft.Container:
        theme_colors = config.当前主题颜色
        
        multirow_config = config.定义尺寸.get("多行卡片", {})
        
        divider_width = multirow_config.get("divider_width", 2)
        divider_height = height or multirow_config.get("divider_height", 60)
        divider_opacity = multirow_config.get("divider_opacity", 0.7)
        divider_blur = multirow_config.get("divider_blur", 6)
        
        return ft.Container(
            width=divider_width,
            height=divider_height,
            bgcolor=theme_colors.get("accent"),
            opacity=divider_opacity if enabled else 0.2,
            shadow=ft.BoxShadow(
                blur_radius=divider_blur,
                color=theme_colors.get("accent"),
                spread_radius=0,
            ) if enabled else None,
        )


# 兼容别名
分割线 = Divider


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    # 1. 界面配置初始化
    配置 = 界面配置()
    
    # 2. 自动加载用户数据覆盖默认值（在界面配置.__init__中自动完成）
    
    # 3. 正常启动被测模块
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        page.add(Divider.create(配置, height=60, enabled=True))  # 只能更改此处**被测调用模块名称**
    
    ft.run(main)
