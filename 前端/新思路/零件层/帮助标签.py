# -*- coding: utf-8 -*-
"""
帮助标签 - 零件层（新思路）

设计思路:
    独立功能模块，自带状态切换能力。
    符合"装配"模式，即插即用。

功能:
    1. 图标：问号图标
    2. 提示：悬停/点击显示帮助内容
    3. 状态切换：内置切换逻辑，通过回调通知外部
    4. 外部控制：支持外部设置状态

数据来源:
    所有配置数据从配置目录获取。

使用场景:
    被组件层模块调用，也可独立使用。

可独立运行调试: python 帮助标签.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft
from typing import Callable, Optional
from 配置.界面配置 import 界面配置


class HelpTag:
    """帮助标签 - 独立功能模块，自带状态切换"""
    
    @staticmethod
    def create(
        config: 界面配置,
        help_text: str,
        enabled: bool = True,
        icon_size: int = 14,
        on_state_change: Callable[[bool], None] = None,
        on_click: Callable = None,
        **kwargs
    ) -> Optional[ft.Container]:
        """
        创建帮助标签组件
        
        参数:
            config: 界面配置对象
            help_text: 帮助提示文字
            enabled: 初始启用状态
            icon_size: 图标大小
            on_state_change: 状态变化回调函数，参数为新状态
            on_click: 点击回调函数（可选，用于扩展）
        
        返回:
            ft.Container: 包含帮助标签的容器，具备状态切换能力
            如果help_text为空，返回None
        """
        if not help_text:
            return None
        
        theme_colors = config.当前主题颜色
        
        # 计算外框尺寸，刚好包裹问号文字
        box_size = icon_size + 4
        
        # 创建图标控件
        icon_control = ft.Icon(
            ft.Icons.HELP_OUTLINE,
            size=icon_size,
            color=theme_colors.get("text_secondary"),
        )
        
        # 内部状态
        current_enabled = enabled
        
        def set_state(new_enabled: bool, notify: bool = True):
            """设置状态"""
            nonlocal current_enabled
            current_enabled = new_enabled
            
            container.opacity = 0.7 if current_enabled else 0.3
            container.update()
            
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
            content=icon_control,
            width=box_size,
            height=box_size,
            tooltip=help_text,
            opacity=0.7 if enabled else 0.3,
            on_click=handle_click,
        )
        
        # 暴露控制接口
        container.set_state = set_state
        container.toggle_state = toggle_state
        container.get_state = lambda: current_enabled
        
        return container


# 兼容别名
帮助标签 = HelpTag


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    config = 界面配置()
    
    def main(page: ft.Page):
        page.padding = 20
        page.bgcolor = config.获取颜色("bg_primary")
        
        page.add(ft.Text("帮助标签测试（独立功能模块）:", color=config.获取颜色("text_secondary")))
        page.add(ft.Divider(height=20, color="transparent"))
        
        def on_state_change(enabled):
            print(f"状态变化: {'启用' if enabled else '禁用'}")
        
        help_tag = HelpTag.create(
            config=config,
            help_text="这是帮助提示内容",
            enabled=True,
            on_state_change=on_state_change,
        )
        
        page.add(ft.Container(
            content=help_tag,
            padding=20,
            bgcolor=config.获取颜色("bg_card"),
            border_radius=8,
        ))
        
        page.add(ft.Divider(height=20, color="transparent"))
        
        # 测试外部控制
        def external_toggle(e):
            help_tag.toggle_state()
        
        page.add(ft.ElevatedButton("外部切换状态", on_click=external_toggle))
    
    ft.run(main)
