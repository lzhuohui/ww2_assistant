# -*- coding: utf-8 -*-
"""
建筑卡片 - 组件层

设计思路:
    本模块是组件层模块，组合多行卡片和标签下拉框。

功能:
    1. 使用多行卡片作为容器
    2. 使用标签下拉框作为配置项
    3. 专门用于建筑等级配置

数据来源:
    主题颜色从界面配置获取。

使用场景:
    被建筑设置界面调用。

可独立运行调试: python 建筑卡片.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import flet as ft
from typing import List, Dict, Any, Callable
from 原子层.界面配置 import 界面配置
from 组件层.多行卡片 import MultiRowCard
from 组件层.标签下拉框 import LabelDropdown


# ==================== 用户指定变量区 ====================
# （暂无用户指定的默认值）
# ========================================================


class BuildingCard:  # 建筑卡片组件
    """建筑卡片 - 多行卡片 + 标签下拉框"""
    
    @staticmethod
    def create(
        config: 界面配置,
        title: str,
        icon: str = None,
        items: List[Dict[str, Any]] = None,
        enabled: bool = True,
        on_state_change: Callable[[bool], None] = None,
        **kwargs
    ) -> ft.Container:
        controls = []
        if items:
            for item in items:
                label = item.get("label", "")
                options = item.get("options", [])
                value = item.get("value", options[0] if options else "")
                callback = item.get("on_change")
                
                controls.append(LabelDropdown.create(
                    config=config,
                    label=label,
                    options=options,
                    value=value,
                    on_change=callback,
                ))
        
        return MultiRowCard.create(
            config=config,
            title=title,
            icon=icon,
            controls=controls,
            enabled=enabled,
            on_state_change=on_state_change,
        )


# 兼容别名
建筑卡片 = BuildingCard


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    config = 界面配置()
    
    def main(page: ft.Page):
        page.padding = 20
        page.bgcolor = config.获取颜色("bg_primary")
        
        level_options = [f"{i:02d}" for i in range(1, 21)]
        
        page.add(BuildingCard.create(
            config=config,
            title="主帅主城",
            icon="HOME",
            items=[
                {"label": "城市", "options": level_options, "value": "17"},
                {"label": "兵工", "options": level_options, "value": "17"},
                {"label": "陆军", "options": level_options, "value": "14"},
                {"label": "空军", "options": level_options, "value": "03"},
                {"label": "商业", "options": level_options, "value": "04"},
                {"label": "补给", "options": level_options, "value": "03"},
                {"label": "内塔", "options": level_options, "value": "04"},
                {"label": "村庄", "options": level_options, "value": "03"},
                {"label": "资源", "options": level_options, "value": "03"},
                {"label": "军工", "options": level_options, "value": "03"},
                {"label": "港口", "options": level_options, "value": "03"},
                {"label": "外塔", "options": level_options, "value": "03"},
            ],
        ))
    
    ft.run(main)
