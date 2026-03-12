# -*- coding: utf-8 -*-
"""
策略设置页面 - 页面层（新思路）

设计思路:
    使用开关下拉卡片组件，构建策略设置页面。
    按旧版分组，保持功能完整。

功能:
    1. 建筑速建组
    2. 资源速产组
    3. 策点保留组

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
from 新思路.组件层.开关下拉卡片 import SwitchDropdownCard
from 新思路.组件层.通用卡片 import UniversalCard
from 新思路.零件层.标签下拉框 import LabelDropdown


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
        
        # ========== 建筑速建组 ==========
        speed_build_card = SwitchDropdownCard.create(
            config=config,
            title="建筑速建",
            icon="ROCKET_LAUNCH",
            subtitle="速建限级",
            dropdown_options=["05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15"],
            dropdown_value="08",
            enabled=True,
        )
        
        # 建筑类型卡片
        build_type_control = LabelDropdown.create(
            config=config,
            label="建筑类型:",
            options=["城资建筑", "城市建筑", "资源建筑"],
            value="城资建筑",
        )
        
        build_type_card = UniversalCard.create(
            config=config,
            title="建筑类型",
            icon="APARTMENT",
            subtitle="设置加速建筑类型",
            controls=[build_type_control],
            enabled=True,
        )
        
        # ========== 资源速产组 ==========
        speed_prod_card = SwitchDropdownCard.create(
            config=config,
            title="资源速产",
            icon="BOLT",
            subtitle="速产限级",
            dropdown_options=["05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15"],
            dropdown_value="07",
            enabled=True,
        )
        
        # 策略类型卡片
        strategy_type_control = LabelDropdown.create(
            config=config,
            label="策略类型:",
            options=["平衡资源", "战时经济", "钢铁熔炉", "橡胶采集", "石油开采"],
            value="平衡资源",
        )
        
        strategy_type_card = UniversalCard.create(
            config=config,
            title="策略类型",
            icon="FACTORY",
            subtitle="设置加速策略类型",
            controls=[strategy_type_control],
            enabled=True,
        )
        
        # ========== 策点保留组 ==========
        keep_points_card = SwitchDropdownCard.create(
            config=config,
            title="策点保留",
            icon="SAVINGS",
            subtitle="保留点数",
            dropdown_options=["30", "60", "90", "120", "150", "180", "210", "240"],
            dropdown_value="60",
            enabled=True,
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
                # 建筑速建组
                ft.Text(
                    "建筑速建",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=theme_colors.get("text_primary"),
                ),
                ft.Container(height=10),
                speed_build_card,
                ft.Container(height=10),
                build_type_card,
                ft.Container(height=20),
                # 资源速产组
                ft.Text(
                    "资源速产",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=theme_colors.get("text_primary"),
                ),
                ft.Container(height=10),
                speed_prod_card,
                ft.Container(height=10),
                strategy_type_card,
                ft.Container(height=20),
                # 策点保留组
                ft.Text(
                    "策点保留",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=theme_colors.get("text_primary"),
                ),
                ft.Container(height=10),
                keep_points_card,
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
        page_container.speed_build_card = speed_build_card
        page_container.build_type_card = build_type_card
        page_container.speed_prod_card = speed_prod_card
        page_container.strategy_type_card = strategy_type_card
        page_container.keep_points_card = keep_points_card
        
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
