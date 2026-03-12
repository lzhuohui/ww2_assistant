# -*- coding: utf-8 -*-
"""
策略设置页面 - 页面层（新思路）

设计思路:
    调用卡片组件，构建策略设置页面。
    与系统设置页面保持一致的处理方式。

功能:
    1. 建筑速建卡片
    2. 资源速产卡片
    3. 策点保留卡片

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
from 新思路.组件层.建筑速建卡片 import BuildingSpeedCard
from 新思路.组件层.资源速产卡片 import ResourceSpeedCard
from 新思路.组件层.策点保留卡片 import PointsKeepCard


class StrategySettingsPage:
    """策略设置页面 - 页面层"""
    
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
        
        # ========== 建筑速建卡片 ==========
        building_speed_card = BuildingSpeedCard.create(
            config=config,
            enabled=True,
            level_value="08",
            type_value="城资建筑",
        )
        
        # ========== 资源速产卡片 ==========
        resource_speed_card = ResourceSpeedCard.create(
            config=config,
            enabled=True,
            level_value="07",
            type_value="平衡资源",
        )
        
        # ========== 策点保留卡片 ==========
        points_keep_card = PointsKeepCard.create(
            config=config,
            enabled=True,
            points_value="60",
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
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )
        
        # 页面容器
        page_container = ft.Container(
            content=page_content,
            padding=ft.Padding.all(20),
            expand=True,
        )
        
        # 暴露卡片引用
        page_container.building_speed_card = building_speed_card
        page_container.resource_speed_card = resource_speed_card
        page_container.points_keep_card = points_keep_card
        
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
