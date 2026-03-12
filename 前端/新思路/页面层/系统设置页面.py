# -*- coding: utf-8 -*-
"""
系统设置页面 - 页面层（新思路） - 配置驱动版本

设计思路:
    使用配置驱动方式创建卡片，简化代码，提高可维护性。

功能:
    1. 基础设置卡片（配置驱动）
    2. 主题设置卡片（配置驱动）
    3. 调色板设置卡片（配置驱动）

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
from 新思路.组件层.通用卡片配置驱动扩展 import UniversalCard


class SystemSettingsPage:
    """系统设置页面 - 页面层（配置驱动版本）"""
    
    @staticmethod
    def create(config: 界面配置, page: ft.Page = None, on_refresh: Callable[[], None] = None) -> ft.Container:
        """
        创建系统设置页面
        
        参数:
            config: 界面配置对象
            page: 页面对象（可选，用于更新页面显示）
            on_refresh: 刷新回调（主题/调色板切换后调用）
        
        返回:
            ft.Container: 系统设置页面容器
        """
        theme_colors = config.当前主题颜色
        
        # 创建配置管理器
        config_manager = ConfigManager()
        
        # 创建值变化回调
        def on_value_change(config_key: str, value: any):
            """值变化回调"""
            print(f"配置变化: {config_key} = {value}")
            
            # 处理主题切换
            if config_key == "主题模式" and value:
                config.切换主题(value)
                if on_refresh:
                    on_refresh()
            
            # 处理调色板切换
            elif config_key == "调色板模式":
                if value:
                    # 切换到指定调色板
                    config.切换调色板(value)
                else:
                    # 取消调色板效果
                    config.切换调色板(None)
                if on_refresh:
                    on_refresh()
        
        # 使用配置驱动创建三个卡片
        basic_card = UniversalCard.create_from_config(
            config=config,
            card_name="基础设置",
            config_manager=config_manager,
            on_value_change=on_value_change,
        )
        
        theme_card = UniversalCard.create_from_config(
            config=config,
            card_name="主题设置",
            config_manager=config_manager,
            on_value_change=on_value_change,
        )
        
        palette_card = UniversalCard.create_from_config(
            config=config,
            card_name="调色板设置",
            config_manager=config_manager,
            on_value_change=on_value_change,
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
        page.add(SystemSettingsPage.create(配置))
    
    ft.run(main)
