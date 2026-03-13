# -*- coding: utf-8 -*-
"""
自定义下拉框 - 零件层（新思路）

设计思路:
    独立功能模块，轻量级设计。
    PopupMenuButton实现下拉选择。

功能:
    1. 下拉选择
    2. 自定义选项列表
    3. 选中值回调
    4. 外部控制接口

数据来源:
    所有配置数据从配置目录获取。

使用场景:
    被组件层模块调用，也可独立使用。

可独立运行调试: python 自定义下拉框.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft
from typing import Callable, List, Optional
from 配置.界面配置 import 界面配置


# *** 用户指定变量 - AI不得修改 ***
# 默认宽度（像素）
DEFAULT_WIDTH = 100
# 默认高度（像素）
DEFAULT_HEIGHT = 32
# *********************************


class CustomDropDown:
    """自定义下拉框 - 独立功能模块"""
    
    @staticmethod
    def create(
        config: 界面配置,
        options: List[str] = None,
        value: str = None,
        width: int = None,
        height: int = None,
        on_change: Callable[[str], None] = None,
        enabled: bool = True,
        **kwargs
    ) -> ft.PopupMenuButton:
        """
        创建下拉框组件
        
        参数:
            config: 界面配置对象
            options: 选项列表
            value: 初始值
            width: 宽度（可选，默认使用用户指定变量DEFAULT_WIDTH）
            height: 高度（可选，默认使用用户指定变量DEFAULT_HEIGHT）
            on_change: 值变化回调
            enabled: 启用状态（默认True）
        
        返回:
            ft.PopupMenuButton: 下拉框控件
        """
        theme_colors = config.当前主题颜色
        
        # 使用用户指定的默认值
        current_width = width if width is not None else DEFAULT_WIDTH
        current_height = height if height is not None else DEFAULT_HEIGHT
        
        # 默认选项
        current_options = options or ["选项A", "选项B", "选项C"]
        current_value = value if value else (current_options[0] if current_options else "")
        
        # 创建选中文字
        selected_text = ft.Text(
            current_value,
            size=14,
            color=theme_colors.get("text_primary"),
            overflow=ft.TextOverflow.ELLIPSIS,
        )
        
        # 创建下拉图标
        dropdown_icon = ft.Icon(
            ft.Icons.KEYBOARD_ARROW_DOWN,
            size=18,
            color=theme_colors.get("text_primary"),
        )
        
        # 创建按钮容器
        button_container = ft.Container(
            content=ft.Row(
                [selected_text, dropdown_icon],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=current_width,
            height=current_height,
            border_radius=6,
            bgcolor=theme_colors.get("bg_secondary"),
            border=ft.Border.all(1, theme_colors.get("border")),
            padding=ft.Padding(left=12, right=8, top=0, bottom=0),
            alignment=ft.Alignment(-1.0, 0.0),
            ink=True,
        )
        
        # 内部状态
        current_value_state = current_value
        current_enabled_state = enabled
        
        def select_option(option_value: str):
            """选择选项"""
            nonlocal current_value_state
            current_value_state = option_value
            selected_text.value = option_value
            selected_text.update()
            if on_change:
                on_change(option_value)
        
        def set_enabled(new_enabled: bool):
            """设置启用状态"""
            nonlocal current_enabled_state
            current_enabled_state = new_enabled
            button_container.opacity = 1.0 if new_enabled else 0.5
            button_container.update()
            # 设置PopupMenuButton的disabled属性
            control.disabled = not new_enabled
            if control.page:
                control.update()
        
        def get_enabled() -> bool:
            """获取启用状态"""
            return current_enabled_state
        
        # 创建菜单项
        menu_items = []
        for option in current_options:
            item = ft.PopupMenuItem(
                content=ft.Text(option, size=14, color=theme_colors.get("text_primary")),
                on_click=lambda e, o=option: select_option(o),
            )
            menu_items.append(item)
        
        # 创建PopupMenuButton
        control = ft.PopupMenuButton(
            content=button_container,
            items=menu_items,
            bgcolor=theme_colors.get("bg_card"),
            elevation=4,
            tooltip="",
            menu_padding=0,
            menu_position=ft.PopupMenuPosition.UNDER,
            size_constraints=ft.BoxConstraints(
                min_width=current_width,
                max_width=current_width,
            ),
            height=current_height,  # 设置高度属性
        )
        
        # 暴露控制接口
        control.get_value = lambda: current_value_state
        control.set_value = lambda v: select_option(v)
        control.set_enabled = set_enabled
        control.get_enabled = get_enabled
        control.set_state = set_enabled  # 兼容别名
        control.enabled = property(get_enabled, set_enabled)  # 兼容属性
        
        return control


# 兼容别名
自定义下拉框 = CustomDropDown


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    # 1. 界面配置初始化
    配置 = 界面配置()
    
    # 2. 自动加载用户数据覆盖默认值（在界面配置.__init__中自动完成）
    
    # 3. 正常启动被测模块
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        page.add(CustomDropDown.create(配置, options=["选项A", "选项B", "选项C"], value="选项A"))  # 只能更改此处**被测调用模块名称**
    
    ft.run(main)
