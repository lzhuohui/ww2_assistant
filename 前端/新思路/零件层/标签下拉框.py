# -*- coding: utf-8 -*-
"""
标签下拉框 - 零件层（新思路）

设计思路:
    独立功能模块，轻量级设计。
    标签文本 + 自定义下拉框组合。

功能:
    1. 标签文本显示
    2. 自定义下拉框
    3. 水平排列布局
    4. 选中值回调

数据来源:
    所有配置数据从配置目录获取。

使用场景:
    被组件层模块调用，也可独立使用。

可独立运行调试: python 标签下拉框.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft
from typing import Callable, List, Optional
from 配置.界面配置 import 界面配置
from 新思路.零件层.自定义下拉框v2 import LazyDropDown as CustomDropDown


# *** 用户指定变量 - AI不得修改 ***
# (用户指定的变量放在这里，用户没有指定之前就空着)
# *********************************


class LabelDropdown:
    """标签下拉框 - 独立功能模块"""
    
    @staticmethod
    def create(
        config: 界面配置,
        label: str,
        options: List[str] = None,
        value: str = None,
        width: int = None,
        on_change: Callable[[str], None] = None,
        enabled: bool = True,
        **kwargs
    ) -> ft.Row:
        """
        创建标签下拉框
        
        参数:
            config: 界面配置对象
            label: 标签文本
            options: 选项列表
            value: 初始值
            width: 下拉框宽度（可选，默认从配置中获取）
            on_change: 值变化回调
            enabled: 启用状态（默认True）
        
        返回:
            ft.Row: 标签下拉框容器
        """
        theme_colors = config.当前主题颜色
        
        # 创建标签文本（自适应宽度）
        label_control = ft.Text(
            label,
            size=14,
            color=theme_colors.get("text_primary"),
            no_wrap=True,
        )
        
        # 创建下拉框（宽度由调用者决定，或使用自定义下拉框的默认值）
        dropdown_control = CustomDropDown.create(
            config=config,
            options=options or [],
            value=value if value is not None else (options[0] if options else ""),
            width=width,
            on_change=on_change,
            enabled=enabled,
        )
        
        # 获取下拉框高度
        dropdown_height = getattr(dropdown_control, 'height', 32) or 32
        
        # 创建行容器（标签紧靠下拉框）
        row = ft.Row(
            [
                label_control,
                dropdown_control,
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=4,
            height=dropdown_height,  # 设置行高度等于下拉框高度
        )
        
        # 暴露控制接口
        row.get_value = dropdown_control.get_value
        row.set_value = dropdown_control.set_value
        row.set_enabled = dropdown_control.set_enabled
        row.get_enabled = dropdown_control.get_enabled
        row.set_state = dropdown_control.set_state  # 兼容别名
        
        return row


# 兼容别名
标签下拉框 = LabelDropdown


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    # 1. 界面配置初始化
    配置 = 界面配置()
    
    # 2. 自动加载用户数据覆盖默认值（在界面配置.__init__中自动完成）
    
    # 3. 正常启动被测模块
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        page.add(LabelDropdown.create(配置, label="挂机模式", options=["自动挂机", "手动挂机", "半自动挂机"], value="自动挂机"))  # 只能更改此处**被测调用模块名称**
    
    ft.run(main)
