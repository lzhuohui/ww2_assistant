# -*- coding: utf-8 -*-
"""
策略设置页面 - 页面层（新思路） - 配置驱动版本

设计思路:
    使用配置驱动方式创建卡片，与系统设置页面保持一致。

功能:
    1. 建筑速建卡片（配置驱动）
    2. 资源速产卡片（配置驱动）
    3. 策点保留卡片（配置驱动）

数据来源:
    所有配置数据从配置目录获取。

使用场景:
    被主界面调用。

可独立运行调试: python 策略设置页面.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft
from typing import Callable
from 配置.界面配置 import 界面配置
from 配置.配置管理器 import ConfigManager
from 新思路.组件层.通用卡片 import UniversalCard


class StrategySettingsPage:
    """策略设置页面 - 页面层（配置驱动版本）"""
    
    @staticmethod
    def create(config: 界面配置, page: ft.Page = None, on_refresh: Callable[[], None] = None) -> ft.Container:
        """
        创建策略设置页面
        
        参数:
            config: 界面配置对象
            page: 页面对象（可选，用于更新页面显示）
            on_refresh: 刷新回调（主题/调色板切换后调用）
        
        返回:
            ft.Container: 策略设置页面容器
        """
        theme_colors = config.当前主题颜色
        
        # 创建配置管理器
        config_manager = ConfigManager()
        
        # 创建值变化回调
        def on_value_change(config_key: str, value: any):
            """值变化回调"""
            print(f"配置变化: {config_key} = {value}")
        
        # 使用配置驱动创建三个卡片（与系统设置页面保持一致）
        building_speed_card = UniversalCard.create_from_config(
            config=config,
            card_name="建筑速建",
            config_manager=config_manager,
            on_value_change=on_value_change,
        )
        
        resource_speed_card = UniversalCard.create_from_config(
            config=config,
            card_name="资源速产",
            config_manager=config_manager,
            on_value_change=on_value_change,
        )
        
        points_keep_card = UniversalCard.create_from_config(
            config=config,
            card_name="策点保留",
            config_manager=config_manager,
            on_value_change=on_value_change,
        )
        
        # ========== 页面容器 ==========
        page_content = ft.Column(
            [
                # 页面标题
                ft.Text(
                    "策略设置",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=theme_colors.get("text_primary"),
                ),
                ft.Container(height=20),
                # 建筑速建卡片
                building_speed_card,
                ft.Container(height=15),
                # 资源速产卡片
                resource_speed_card,
                ft.Container(height=15),
                # 策点保留卡片
                points_keep_card,
            ],
            spacing=0,
            scroll=ft.ScrollMode.HIDDEN,
            expand=True,
        )
        
        # 页面容器
        page_container = ft.Container(
            content=page_content,
            padding=ft.Padding.all(0),
            expand=True,
        )
        
        return page_container


# 兼容别名
策略设置页面 = StrategySettingsPage


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    # 1. 界面配置初始化
    配置 = 界面配置()
    
    # 2. 自动加载用户数据覆盖默认值（在界面配置.__init__中自动完成）
    
    # 3. 正常启动被测模块
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        page.add(StrategySettingsPage.create(配置))
    
    ft.run(main)
