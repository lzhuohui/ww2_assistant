# -*- coding: utf-8 -*-
"""
策点保留卡片 - 组件层（新思路）

设计思路:
    组装零件，构建策点保留卡片。
    一个卡片包含左侧开关和右侧下拉框。

功能:
    1. 左侧开关
    2. 右侧下拉框（保留点数）

数据来源:
    所有配置数据从配置目录获取。

使用场景:
    被策略设置页面调用。

可独立运行调试: python 策点保留卡片.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft
from typing import Callable
from 配置.界面配置 import 界面配置
from 新思路.组件层.开关下拉卡片 import SwitchDropdownCard


class PointsKeepCard:
    """策点保留卡片 - 组件层"""
    
    @staticmethod
    def create(
        config: 界面配置,
        enabled: bool = True,
        on_state_change: Callable[[bool], None] = None,
        points_value: str = "60",
    ) -> ft.Container:
        """
        创建策点保留卡片
        
        参数:
            config: 界面配置对象
            enabled: 初始启用状态
            on_state_change: 状态变化回调
            points_value: 保留点数默认值
        
        返回:
            ft.Container: 策点保留卡片容器
        """
        # ========== 开关下拉卡片 ==========
        # 使用settings参数传递下拉框
        settings = [
            {
                "type": "dropdown",
                "label": "保留点数:",
                "options": ["30", "60", "90", "120", "150", "180", "210", "240"],
                "value": points_value,
            },
        ]
        
        card = SwitchDropdownCard.create(
            config=config,
            title="策点保留",
            icon="SAVINGS",
            enabled=enabled,
            on_state_change=on_state_change,
            settings=settings,
        )
        
        return card


# 兼容别名
策点保留卡片 = PointsKeepCard


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    # 1. 界面配置初始化
    配置 = 界面配置()
    
    # 2. 自动加载用户数据覆盖默认值（在界面配置.__init__中自动完成）
    
    # 3. 正常启动被测模块
    def main(page: ft.Page):
        page.padding = 20
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        page.add(PointsKeepCard.create(配置))
    
    ft.run(main)
