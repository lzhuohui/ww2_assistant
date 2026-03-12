# -*- coding: utf-8 -*-
"""
资源速产卡片 - 组件层（新思路）

设计思路:
    组装零件，构建资源速产卡片。
    一个卡片包含左侧开关和右侧多个下拉框。

功能:
    1. 左侧开关
    2. 右侧下拉框（速产限级、策略类型）

数据来源:
    所有配置数据从配置目录获取。

使用场景:
    被策略设置页面调用。

可独立运行调试: python 资源速产卡片.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft
from typing import Callable
from 配置.界面配置 import 界面配置
from 新思路.组件层.开关下拉卡片 import SwitchDropdownCard


class ResourceSpeedCard:
    """资源速产卡片 - 组件层"""
    
    @staticmethod
    def create(
        config: 界面配置,
        enabled: bool = True,
        on_state_change: Callable[[bool], None] = None,
        level_value: str = "07",
        type_value: str = "平衡资源",
    ) -> ft.Container:
        """
        创建资源速产卡片
        
        参数:
            config: 界面配置对象
            enabled: 初始启用状态
            on_state_change: 状态变化回调
            level_value: 速产限级默认值
            type_value: 策略类型默认值
        
        返回:
            ft.Container: 资源速产卡片容器
        """
        # ========== 开关下拉卡片 ==========
        # 使用settings参数传递多个下拉框
        settings = [
            {
                "type": "dropdown",
                "label": "速产限级:",
                "options": ["05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15"],
                "value": level_value,
            },
            {
                "type": "dropdown",
                "label": "策略类型:",
                "options": ["平衡资源", "战时经济", "钢铁熔炉", "橡胶采集", "石油开采"],
                "value": type_value,
            },
        ]
        
        card = SwitchDropdownCard.create(
            config=config,
            title="资源速产",
            icon="BOLT",
            enabled=enabled,
            on_state_change=on_state_change,
            settings=settings,
        )
        
        return card


# 兼容别名
资源速产卡片 = ResourceSpeedCard


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    # 1. 界面配置初始化
    配置 = 界面配置()
    
    # 2. 自动加载用户数据覆盖默认值（在界面配置.__init__中自动完成）
    
    # 3. 正常启动被测模块
    def main(page: ft.Page):
        page.padding = 20
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        page.add(ResourceSpeedCard.create(配置))
    
    ft.run(main)
