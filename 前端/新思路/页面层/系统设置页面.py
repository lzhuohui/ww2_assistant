# -*- coding: utf-8 -*-
"""
系统设置页面 - 页面层（新思路）

设计思路:
    组装组件，构建系统设置页面。
    采用装配模式，协调各组件交互。

功能:
    1. 基础设置卡片（脚本使用）
    2. 个性化卡片（界面使用）
    3. 预留扩展接口

数据来源:
    所有配置数据从配置目录获取。

使用场景:
    被主界面调用。

可独立运行调试: python 系统设置页面.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft
from typing import Callable
from 配置.界面配置 import 界面配置
from 新思路.组件层.基础设置卡片 import BasicSettingsCard
from 新思路.组件层.主题设置卡片 import ThemeSettingsCard
from 新思路.组件层.调色板设置卡片 import PaletteSettingsCard


class SystemSettingsPage:
    """系统设置页面 - 页面层"""
    
    @staticmethod
    def create(config: 界面配置, page: ft.Page = None, on_refresh: Callable[[], None] = None) -> ft.Column:
        """
        创建系统设置页面
        
        参数:
            config: 界面配置对象
            page: 页面对象（可选，用于更新页面显示）
            on_refresh: 刷新回调（主题/调色板切换后调用）
        
        返回:
            ft.Column: 系统设置页面容器
        """
        theme_colors = config.当前主题颜色
        
        # ========== 基础设置卡片 ==========
        settings = [
            {"type": "dropdown", "label": "挂机模式", "options": ["自动挂机", "手动挂机", "半自动挂机"], "value": "自动挂机"},
            {"type": "dropdown", "label": "指令速度", "options": ["快速", "正常", "慢速"], "value": "正常"},
            {"type": "dropdown", "label": "尝试次数", "options": ["10", "15", "20", "25", "30"], "value": "15"},
            {"type": "dropdown", "label": "清换限量", "options": ["1.0", "1.5", "2.0", "2.5", "3.0", "3.5", "4.0", "4.5", "5.0"], "value": "1.0"},
        ]
        
        basic_card = BasicSettingsCard.create(
            config=config,
            title="基础设置",
            settings=settings,
        )
        
        # ========== 个性化卡片 ==========
        # 主题设置卡片（已集成切换功能）
        theme_card = ThemeSettingsCard.create(
            config=config,
            page=page,
            on_refresh=on_refresh,
            title="主题设置",
        )
        
        # 调色板设置卡片（已集成切换功能）
        palette_card = PaletteSettingsCard.create(
            config=config,
            page=page,
            on_refresh=on_refresh,
            title="高对比度调色板",
        )
        
        # ========== 页面容器 ==========
        page_content = ft.Column(
            [
                # 页面标题
                ft.Text(
                    "系统设置",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=theme_colors.get("text_primary"),
                ),
                ft.Container(height=20),
                # 基础设置卡片
                basic_card,
                ft.Container(height=15),
                # 主题设置卡片
                theme_card,
                ft.Container(height=15),
                # 调色板设置卡片
                palette_card,
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
系统设置页面 = SystemSettingsPage


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    # 1. 界面配置初始化
    配置 = 界面配置()
    
    # 2. 自动加载用户数据覆盖默认值（在界面配置.__init__中自动完成）
    
    # 3. 正常启动被测模块
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        page.add(SystemSettingsPage.create(配置))  # 只能更改此处**被测调用模块名称**
    
    ft.run(main)
