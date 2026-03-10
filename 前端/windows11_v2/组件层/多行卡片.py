# -*- coding: utf-8 -*-
"""
多行卡片 - 组件层（兼容别名）

设计思路:
    本模块是通用卡片的兼容别名，保持向后兼容。

功能:
    多行卡片，左侧图标+标题，中间分割线，右侧多行控件。

使用场景:
    被需要多行布局的模块调用。

可独立运行调试: python 多行卡片.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from 组件层.通用卡片 import UniversalCard

# 兼容别名
MultiRowCard = UniversalCard
多行卡片 = UniversalCard

# 保留原有的用户指定变量（向后兼容）
ITEMS_PER_ROW = 6
DIVIDER_WIDTH = 2
DIVIDER_HEIGHT = 60
DIVIDER_OPACITY = 0.7
DIVIDER_BLUR = 6
LEFT_WIDTH = 60
DIVIDER_LEFT = 90
CONTENT_LEFT = 130


if __name__ == "__main__":
    import flet as ft
    from 原子层.界面配置 import 界面配置
    from 组件层.自定义下拉框 import CustomDropDown
    
    config = 界面配置()
    
    def main(page: ft.Page):
        page.padding = 20
        page.bgcolor = config.获取颜色("bg_primary")
        
        level_options = [f"{i:02d}" for i in range(1, 13)]
        controls = [
            CustomDropDown(config=config, width=70, options=level_options, value="01").create(),
            CustomDropDown(config=config, width=70, options=level_options, value="02").create(),
            CustomDropDown(config=config, width=70, options=level_options, value="03").create(),
            CustomDropDown(config=config, width=70, options=level_options, value="04").create(),
            CustomDropDown(config=config, width=70, options=level_options, value="05").create(),
            CustomDropDown(config=config, width=70, options=level_options, value="06").create(),
        ]
        
        def on_state_change(enabled):
            print(f"状态变化: {'启用' if enabled else '禁用'}")
        
        page.add(MultiRowCard.create(
            config=config,
            title="测试卡片",
            icon="HOME",
            controls=controls,
            enabled=True,
            on_state_change=on_state_change,
        ))
    
    ft.run(main)
