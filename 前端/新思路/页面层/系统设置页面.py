# -*- coding: utf-8 -*-
"""
系统设置页面 - 页面层（新思路） - 配置驱动版本

设计思路:
    使用配置驱动方式创建卡片，简化代码，提高可维护性。

功能:
    1. 基础设置卡片（配置驱动）

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
from 配置.配置管理器 import ConfigManager
from 新思路.组件层.通用卡片 import UniversalCard


class SystemSettingsPage:
    """系统设置页面 - 页面层（配置驱动版本）"""
    
    @staticmethod
    def create(config: 界面配置, page: ft.Page = None, on_refresh: Callable[[], None] = None) -> ft.Container:
        """
        创建系统设置页面
        
        参数:
            config: 界面配置对象
            page: 页面对象（可选，用于更新页面显示）
            on_refresh: 刷新回调
        
        返回:
            ft.Container: 系统设置页面容器
        """
        theme_colors = config.当前主题颜色
        
        config_manager = ConfigManager()
        
        def on_value_change(config_key: str, value: any):
            """值变化回调"""
            print(f"配置变化: {config_key} = {value}")
        
        auto_mode_card = UniversalCard.create_from_config(
            config=config,
            card_name="挂机模式",
            config_manager=config_manager,
            on_value_change=on_value_change,
        )
        
        speed_card = UniversalCard.create_from_config(
            config=config,
            card_name="指令速度",
            config_manager=config_manager,
            on_value_change=on_value_change,
        )
        
        retry_card = UniversalCard.create_from_config(
            config=config,
            card_name="尝试次数",
            config_manager=config_manager,
            on_value_change=on_value_change,
        )
        
        cache_card = UniversalCard.create_from_config(
            config=config,
            card_name="清缓限量",
            config_manager=config_manager,
            on_value_change=on_value_change,
        )
        
        page_content = ft.Column(
            [
                ft.Text(
                    "系统设置",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=theme_colors.get("text_primary"),
                ),
                ft.Container(height=20),
                auto_mode_card,
                ft.Container(height=15),
                speed_card,
                ft.Container(height=15),
                retry_card,
                ft.Container(height=15),
                cache_card,
            ],
            spacing=0,
            scroll=ft.ScrollMode.HIDDEN,
            expand=True,
        )
        
        page_container = ft.Container(
            content=page_content,
            padding=ft.Padding.all(20),
            expand=True,
        )
        
        return page_container


系统设置页面 = SystemSettingsPage


if __name__ == "__main__":
    配置 = 界面配置()
    
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        page.add(SystemSettingsPage.create(配置))
    
    ft.run(main)
