# -*- coding: utf-8 -*-
"""
标签下拉框 - 组件层

设计思路:
    本模块是组件层模块，组合标签文本和自定义下拉框控件。

功能:
    1. 结构：标签文本 + 自定义下拉框（水平排列）
    2. 布局：标签在左，下拉框在右
    3. 交互：下拉框选择后触发回调

数据来源:
    主题颜色从界面配置动态获取。

使用场景:
    被多行卡片、建筑卡片等模块调用。

可独立运行调试: python 标签下拉框.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import flet as ft
from typing import List, Callable, Optional
from 原子层.界面配置 import 界面配置
from 组件层.自定义下拉框 import CustomDropDown


# ==================== 用户指定变量区 ====================
DEFAULT_DROPDOWN_WIDTH = 70    # 下拉框宽度
DEFAULT_DROPDOWN_HEIGHT = 32   # 下拉框高度
# ========================================================


class LabelDropdown:  # 标签下拉框组件
    """标签下拉框组件 - 标签文本 + 自定义下拉框组合"""
    
    @staticmethod
    def create(
        config: 界面配置,
        label: str,
        options: List[str] = None,
        value: str = None,
        on_change: Callable[[str], None] = None,
        width: int = DEFAULT_DROPDOWN_WIDTH,
        **kwargs
    ) -> ft.Row:
        theme_colors = config.当前主题颜色
        font_config = config.定义尺寸.get("字体", {})
        spacing_config = config.定义尺寸.get("间距", {})
        component_config = config.定义尺寸.get("组件", {})
        
        font_size = font_config.get("font_size_sm", 12)
        dropdown_height = component_config.get("dropdown_height", DEFAULT_DROPDOWN_HEIGHT)
        
        label_control = ft.Text(
            label,
            size=font_size,
            color=theme_colors.get("text_secondary"),
        )
        
        label_container = ft.Container(
            content=label_control,
            height=dropdown_height,
            alignment=ft.Alignment(-1, 0),
        )
        
        dropdown_control = CustomDropDown(
            config=config,
            options=options or [],
            value=value or (options[0] if options else ""),
            width=width,
            height=dropdown_height,
            on_change=on_change,
        )
        
        return ft.Row(
            [
                label_container,
                dropdown_control.create(),
            ],
            spacing=spacing_config.get("spacing_xs", 4),
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )


# 兼容别名
标签下拉框 = LabelDropdown


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    config = 界面配置()
    
    def main(page: ft.Page):
        page.padding = 20
        page.bgcolor = config.获取颜色("bg_primary")
        
        level_options = [f"{i:02d}" for i in range(1, 21)]
        
        page.add(LabelDropdown.create(
            config=config,
            label="城市",
            options=level_options,
            value="17",
        ))
    
    ft.run(main)
