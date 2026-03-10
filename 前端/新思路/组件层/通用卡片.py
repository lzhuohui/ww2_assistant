# -*- coding: utf-8 -*-
"""
通用卡片 - 组件层（新思路）

设计思路:
    调用零件模块组合成卡片组件。
    - 容器：卡片容器.py
    - 左侧：图标标题.py + 帮助标签.py
    - 分割线：分割线.py
    - 右侧：空着，由扩展卡片模块填充

功能:
    1. 组合零件模块
    2. 状态切换逻辑
    3. 布局排列

数据来源:
    所有配置数据从配置目录获取。

使用场景:
    被扩展卡片模块调用，不直接使用。

可独立运行调试: python 通用卡片.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft
from typing import Callable, Optional, Tuple
from 配置.界面配置 import 界面配置
from 新思路.零件层.卡片容器 import CardContainer
from 新思路.零件层.图标标题 import IconTitle
from 新思路.零件层.帮助标签 import HelpTag
from 新思路.零件层.分割线 import Divider


class UniversalCard:
    """通用卡片 - 调用原子模块组合"""
    
    @staticmethod
    def create(
        config: 界面配置,
        title: str,
        icon: str = None,
        enabled: bool = True,
        on_state_change: Callable[[bool], None] = None,
        help_text: str = None,
        height: int = None,
        width: int = None,
        **kwargs
    ) -> ft.Container:
        theme_colors = config.当前主题颜色
        
        spacing_config = config.定义尺寸.get("间距", {})
        ui_config = config.定义尺寸.get("界面", {})
        card_config = config.定义尺寸.get("卡片", {})
        multirow_config = config.定义尺寸.get("多行卡片", {})
        
        card_padding = ui_config.get("card_padding", 16)
        left_width = multirow_config.get("left_width", 60)
        divider_left = multirow_config.get("divider_left", 90)
        
        card_height = height or card_config.get("default_height", 70)
        card_width = width or 800
        
        current_enabled = enabled
        
        icon_title_content, icon_control, title_control = IconTitle.create(
            config=config,
            title=title,
            icon=icon,
            enabled=current_enabled,
        )
        
        help_icon = HelpTag.create(
            config=config,
            help_text=help_text,
            enabled=current_enabled,
        )
        
        left_row_items = [icon_title_content]
        if help_icon:
            left_row_items.append(help_icon)
        
        left_content = ft.Row(
            left_row_items,
            spacing=spacing_config.get("spacing_xs", 4),
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        
        left_container = ft.Container(
            content=left_content,
            left=card_padding,
            top=0,
            bottom=0,
            width=left_width,
            alignment=ft.Alignment(0, 0),
            on_click=lambda e: toggle_state(e),
        )
        
        divider = Divider.create(
            config=config,
            height=multirow_config.get("divider_height", 60),
            enabled=current_enabled,
        )
        divider.left = divider_left
        divider.top = 0
        divider.bottom = 0
        
        stack_children = [
            left_container,
            divider,
        ]
        
        main_stack = ft.Stack(
            stack_children,
            height=card_height,
            width=card_width,
            clip_behavior=ft.ClipBehavior.NONE,
        )
        
        container = CardContainer.create(
            config=config,
            content=main_stack,
            height=card_height,
            width=card_width,
            enabled=current_enabled,
        )
        
        def toggle_state(e):
            nonlocal current_enabled
            current_enabled = not current_enabled
            
            if icon_control:
                icon_control.opacity = 1.0 if current_enabled else 0.4
                icon_control.update()
            if title_control:
                title_control.opacity = 1.0 if current_enabled else 0.4
                title_control.update()
            
            if help_icon:
                help_icon.opacity = 0.7 if current_enabled else 0.3
                help_icon.update()
            
            if divider:
                divider.opacity = multirow_config.get("divider_opacity", 0.7) if current_enabled else 0.2
                divider.update()
            
            if on_state_change:
                on_state_change(current_enabled)
        
        return container


# 兼容别名
通用卡片 = UniversalCard


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    config = 界面配置()
    
    def main(page: ft.Page):
        page.padding = 20
        page.bgcolor = config.获取颜色("bg_primary")
        
        page.add(ft.Text("通用卡片测试（原子模块组合）:", color=config.获取颜色("text_secondary")))
        page.add(ft.Divider(height=20, color="transparent"))
        
        def on_state_change(enabled):
            print(f"状态变化: {'启用' if enabled else '禁用'}")
        
        page.add(UniversalCard.create(
            config=config,
            title="测试卡片",
            icon="HOME",
            enabled=True,
            on_state_change=on_state_change,
            help_text="点击切换启用/禁用状态",
        ))
        
        page.add(ft.Divider(height=20, color="transparent"))
        
        page.add(UniversalCard.create(
            config=config,
            title="设置卡片",
            icon="SETTINGS",
            enabled=True,
            help_text="这是设置卡片的帮助提示",
        ))
    
    ft.run(main)
