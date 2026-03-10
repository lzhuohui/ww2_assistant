# -*- coding: utf-8 -*-
"""
帮助标签 - 原子层（新思路）

设计思路:
    最小模块化的帮助标签组件，点击显示提示内容。

功能:
    1. 图标：问号图标
    2. 提示：悬停/点击显示帮助内容
    3. 状态切换：启用/禁用透明度变化

数据来源:
    所有配置数据从配置目录获取。

使用场景:
    被组件层模块调用。

可独立运行调试: python 帮助标签.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft
from typing import Optional
from 配置.界面配置 import 界面配置


class HelpTag:
    """帮助标签 - 问号图标+提示内容"""
    
    @staticmethod
    def create(
        config: 界面配置,
        help_text: str,
        enabled: bool = True,
        **kwargs
    ) -> Optional[ft.IconButton]:
        if not help_text:
            return None
        
        theme_colors = config.当前主题颜色
        
        return ft.IconButton(
            icon=ft.Icons.HELP_OUTLINE,
            icon_size=14,
            icon_color=theme_colors.get("text_secondary"),
            tooltip=help_text,
            opacity=0.7 if enabled else 0.3,
            style=ft.ButtonStyle(padding=0),
        )


# 兼容别名
帮助标签 = HelpTag


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    config = 界面配置()
    
    def main(page: ft.Page):
        page.padding = 20
        page.bgcolor = config.获取颜色("bg_primary")
        
        page.add(ft.Text("帮助标签测试:", color=config.获取颜色("text_secondary")))
        page.add(ft.Divider(height=20, color="transparent"))
        
        help_tag = HelpTag.create(
            config=config,
            help_text="这是帮助提示内容",
            enabled=True,
        )
        
        page.add(ft.Container(
            content=help_tag,
            padding=20,
            bgcolor=config.获取颜色("bg_card"),
            border_radius=8,
        ))
    
    ft.run(main)
