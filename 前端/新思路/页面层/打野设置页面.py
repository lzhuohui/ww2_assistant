# -*- coding: utf-8 -*-
"""
打野设置页面 - 页面层（新思路）

设计思路:
    组装组件，构建打野设置页面。

功能:
    1. 自动打野卡片（待开发）

数据来源:
    所有配置数据从配置目录获取。

使用场景:
    被主界面调用。

可独立运行调试: python 打野设置页面.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft
from typing import Callable
from 配置.界面配置 import 界面配置


class WildSettingsPage:
    """打野设置页面 - 页面层"""
    
    @staticmethod
    def create(config: 界面配置, page: ft.Page = None, on_refresh: Callable[[], None] = None) -> ft.Column:
        """
        创建打野设置页面
        
        参数:
            config: 界面配置对象
            page: 页面对象（可选，用于更新页面显示）
            on_refresh: 刷新回调（主题/调色板切换后调用）
        
        返回:
            ft.Column: 打野设置页面容器
        """
        theme_colors = config.当前主题颜色
        
        # ========== 页面容器 ==========
        page_content = ft.Column(
            [
                # 页面标题
                ft.Text(
                    "打野设置",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=theme_colors.get("text_primary"),
                ),
                ft.Container(height=20),
                # 占位提示
                ft.Text(
                    "自动打野卡片开发中...",
                    size=14,
                    color=theme_colors.get("text_secondary"),
                ),
            ],
            spacing=0,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )
        
        # 页面容器
        page_container = ft.Container(
            content=page_content,
            padding=ft.Padding.all(20),
            expand=True,
        )
        
        return page_container


# 兼容别名
打野设置页面 = WildSettingsPage


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    # 1. 界面配置初始化
    配置 = 界面配置()
    
    # 2. 自动加载用户数据覆盖默认值（在界面配置.__init__中自动完成）
    
    # 3. 正常启动被测模块
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        page.add(WildSettingsPage.create(配置))
    
    ft.run(main)
