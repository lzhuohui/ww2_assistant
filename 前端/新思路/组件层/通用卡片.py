# -*- coding: utf-8 -*-
"""
通用卡片 - 组件层（新思路）

设计思路:
    装配模式：组合零件模块，协调交互。
    - 不直接操作零件内部控件
    - 通过零件暴露的接口进行控制
    - 负责布局和协调

功能:
    1. 组合零件模块
    2. 协调状态切换
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
from typing import Callable, Optional, List
from 配置.界面配置 import 界面配置
from 新思路.零件层.卡片容器 import CardContainer
from 新思路.零件层.图标标题 import IconTitle
from 新思路.零件层.帮助标签 import HelpTag
from 新思路.零件层.分割线 import Divider


class UniversalCard:
    """通用卡片 - 装配模式，组合零件模块"""
    
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
        """
        创建通用卡片
        
        参数:
            config: 界面配置对象
            title: 标题文字
            icon: 图标名称
            enabled: 初始启用状态
            on_state_change: 状态变化回调
            help_text: 帮助提示文字
            height: 卡片高度
            width: 卡片宽度
        
        返回:
            ft.Container: 完整的卡片容器
        """
        theme_colors = config.当前主题颜色
        
        ui_config = config.定义尺寸.get("界面", {})
        card_config = config.定义尺寸.get("卡片", {})
        multirow_config = config.定义尺寸.get("多行卡片", {})
        
        card_padding = ui_config.get("card_padding", 16)
        
        card_height = height or card_config.get("default_height", 70)
        card_width = width or 800
        
        # 内部状态
        current_enabled = enabled
        
        # 零件列表，用于协调状态
        parts: List = []
        
        # 创建图标标题零件
        def on_icon_title_state_change(new_enabled: bool):
            """图标标题状态变化时，同步其他零件"""
            nonlocal current_enabled
            current_enabled = new_enabled
            sync_parts_state(new_enabled)
            if on_state_change:
                on_state_change(new_enabled)
        
        icon_title = IconTitle.create(
            config=config,
            title=title,
            icon=icon,
            enabled=current_enabled,
            on_state_change=on_icon_title_state_change,
        )
        parts.append(icon_title)
        
        # 创建帮助标签零件
        help_tag = None
        if help_text:
            help_tag = HelpTag.create(
                config=config,
                help_text=help_text,
                enabled=current_enabled,
            )
            if help_tag:
                parts.append(help_tag)
        
        # 创建分割线零件
        divider = Divider.create(
            config=config,
            height=multirow_config.get("divider_height", 60),
            enabled=current_enabled,
        )
        
        def sync_parts_state(new_enabled: bool):
            """同步所有零件状态"""
            for part in parts:
                if hasattr(part, 'set_state'):
                    part.set_state(new_enabled, notify=False)
            
            # 更新分割线
            if divider:
                divider.opacity = multirow_config.get("divider_opacity", 0.7) if new_enabled else 0.2
                divider.update()
        
        # 创建布局
        icon_title_container = ft.Container(
            content=icon_title,
            left=card_padding,
            top=0,
            bottom=0,
            alignment=ft.Alignment(-1, 0),
        )
        
        stack_children = [icon_title_container]
        
        # 计算帮助标签位置
        if help_tag:
            help_left = card_padding + 60 + 4
            help_tag.left = help_left
            help_tag.top = 0
            stack_children.append(help_tag)
        
        # 计算分割线位置
        if help_tag:
            divider_left = help_left + 18 + 4
        else:
            divider_left = card_padding + 60 + 4
        
        divider_container = ft.Container(
            content=divider,
            left=divider_left,
            top=0,
            bottom=0,
            alignment=ft.Alignment(-1, 0),
        )
        stack_children.append(divider_container)
        
        # 创建主布局
        main_stack = ft.Stack(
            stack_children,
            height=card_height,
            width=card_width,
            clip_behavior=ft.ClipBehavior.NONE,
        )
        
        # 创建卡片容器
        container = CardContainer.create(
            config=config,
            content=main_stack,
            height=card_height,
            width=card_width,
        )
        
        # 暴露控制接口
        def set_state(new_enabled: bool):
            """设置卡片状态"""
            nonlocal current_enabled
            current_enabled = new_enabled
            icon_title.set_state(new_enabled, notify=False)
            sync_parts_state(new_enabled)
            if on_state_change:
                on_state_change(new_enabled)
        
        def toggle_state():
            """切换卡片状态"""
            set_state(not current_enabled)
        
        def get_state() -> bool:
            """获取当前状态"""
            return current_enabled
        
        container.set_state = set_state
        container.toggle_state = toggle_state
        container.get_state = get_state
        
        return container


# 兼容别名
通用卡片 = UniversalCard


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    # 1. 界面配置初始化
    配置 = 界面配置()
    
    # 2. 自动加载用户数据覆盖默认值（在界面配置.__init__中自动完成）
    
    # 3. 正常启动被测模块
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        page.add(UniversalCard.create(配置, title="主界面", icon="HOME", enabled=True, help_text="点击切换状态"))  # 只能更改此处**被测调用模块名称**
    
    ft.run(main)
