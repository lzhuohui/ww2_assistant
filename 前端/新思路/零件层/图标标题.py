# -*- coding: utf-8 -*-
"""
图标标题 - 零件层（新思路）

设计思路:
    独立功能模块，自带状态切换能力。
    符合"装配"模式，即插即用。

功能:
    1. 图标：上方居中
    2. 标题：下方居中
    3. 状态切换：内置切换逻辑，通过回调通知外部
    4. 外部控制：支持外部设置状态

数据来源:
    所有配置数据从配置目录获取。

使用场景:
    被组件层模块调用，也可独立使用。

可独立运行调试: python 图标标题.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft
from typing import Callable, Optional
from 配置.界面配置 import 界面配置


# *** 用户指定变量 - AI不得修改 ***
# (用户指定的变量放在这里，用户没有指定之前就空着)
# *********************************


class IconTitle:
    """图标标题 - 独立功能模块，自带状态切换"""
    
    @staticmethod
    def create(
        config: 界面配置,
        title: str,
        icon: str = None,
        enabled: bool = True,
        on_state_change: Callable[[bool], None] = None,
        on_click: Callable = None,
        **kwargs
    ) -> ft.Container:
        """
        创建图标标题组件
        
        参数:
            config: 界面配置对象
            title: 标题文字
            icon: 图标名称（字符串）
            enabled: 初始启用状态
            on_state_change: 状态变化回调函数，参数为新状态
            on_click: 点击回调函数（可选，用于扩展）
        
        返回:
            ft.Container: 包含图标标题的容器，具备状态切换能力
        """
        theme_colors = config.当前主题颜色
        
        weight_config = config.定义尺寸.get("字重", {})
        spacing_config = config.定义尺寸.get("间距", {})
        card_config = config.定义尺寸.get("卡片", {})
        
        default_icon_size = card_config.get("icon_size", 24)
        default_title_size = card_config.get("title_size", 14)
        
        icon_value = None
        if icon:
            if isinstance(icon, str):
                icon_name = icon.upper()
                icon_value = getattr(ft.Icons, icon_name, ft.Icons.SETTINGS)
            else:
                icon_value = icon
        
        # 创建图标控件
        icon_control = None
        if icon_value:
            icon_control = ft.Icon(
                icon_value,
                size=default_icon_size,
                color=theme_colors.get("accent"),
                opacity=1.0 if enabled else 0.4,
            )
        
        # 创建标题控件
        title_control = ft.Text(
            title,
            size=default_title_size,
            weight=weight_config.get("font_weight_medium", ft.FontWeight.W_500),
            color=theme_colors.get("text_primary"),
            opacity=1.0 if enabled else 0.4,
        )
        
        column_items = [icon_control, title_control] if icon_control else [title_control]
        
        content = ft.Column(
            column_items,
            spacing=spacing_config.get("spacing_xs", 4),
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        )
        
        # 内部状态
        current_enabled = enabled
        
        def set_state(new_enabled: bool, notify: bool = True):
            """设置状态"""
            nonlocal current_enabled
            current_enabled = new_enabled
            
            if icon_control:
                icon_control.opacity = 1.0 if current_enabled else 0.4
                icon_control.update()
            
            if title_control:
                title_control.opacity = 1.0 if current_enabled else 0.4
                title_control.update()
            
            if notify and on_state_change:
                on_state_change(current_enabled)
        
        def toggle_state(e=None):
            """切换状态"""
            set_state(not current_enabled)
        
        def handle_click(e):
            """处理点击事件"""
            toggle_state()
            if on_click:
                on_click(e)
        
        container = ft.Container(
            content=content,
            on_click=handle_click,
        )
        
        # 暴露控制接口
        container.set_state = set_state
        container.toggle_state = toggle_state
        container.get_state = lambda: current_enabled
        
        return container


# 兼容别名
图标标题 = IconTitle


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    # 1. 界面配置初始化
    配置 = 界面配置()
    
    # 2. 自动加载用户数据覆盖默认值（在界面配置.__init__中自动完成）
    
    # 3. 正常启动被测模块
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        page.add(IconTitle.create(配置, title="测试标题", icon="HOME", enabled=True))  # 只能更改此处**被测调用模块名称**
    
    ft.run(main)
