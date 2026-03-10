# -*- coding: utf-8 -*-
"""
通用卡片 - 组件层（新思路）

设计思路:
    装配模式：组合零件模块，协调交互。
    - 不直接操作零件内部控件
    - 通过零件暴露的接口进行控制
    - 负责布局和协调
    - 支持多行控件布局

功能:
    1. 组合零件模块
    2. 协调状态切换
    3. 布局排列
    4. 支持多行控件

数据来源:
    所有配置数据从配置目录获取。

使用场景:
    被扩展卡片模块调用，也可直接使用。

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
    """通用卡片 - 装配模式，组合零件模块，支持多行控件"""
    
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
        controls: List[ft.Control] = None,
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
            controls: 右侧控件列表（支持多行）
        
        返回:
            ft.Container: 完整的卡片容器
        """
        theme_colors = config.当前主题颜色
        
        ui_config = config.定义尺寸.get("界面", {})
        card_config = config.定义尺寸.get("卡片", {})
        multirow_config = config.定义尺寸.get("多行卡片", {})
        
        card_padding = ui_config.get("card_padding", 16)
        left_width = multirow_config.get("left_width", 60)
        divider_left = multirow_config.get("divider_left", 90)
        content_left = multirow_config.get("content_left", 130)
        
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
        
        # ========== 左侧布局 ==========
        # 使用Stack布局，将帮助标签放置在图标标题的右上角
        left_stack_children = [icon_title]
        
        if help_tag:
            # 帮助标签放置在图标标题的右上角
            left_stack_children.append(
                ft.Container(
                    content=help_tag,
                    left=50,  # 图标标题右侧
                    top=-5,   # 右上角
                )
            )
        
        left_content = ft.Stack(
            left_stack_children,
            width=left_width,
            height=60,
            clip_behavior=ft.ClipBehavior.NONE,
        )
        
        left_container = ft.Container(
            content=left_content,
            left=card_padding,
            top=0,
            bottom=0,
            width=left_width,
            alignment=ft.Alignment(0, 0),
        )
        
        # ========== 分割线布局 ==========
        divider_container = ft.Container(
            content=divider,
            left=divider_left,
            top=0,
            bottom=0,
            alignment=ft.Alignment(-1, 0),
        )
        
        # ========== 右侧内容布局 ==========
        stack_children = [left_container, divider_container]
        
        if controls:
            # 获取通用卡片配置
            card_params = config.定义尺寸.get("通用卡片", {})
            control_margin_left = card_params.get("control_margin_left", 20)
            control_margin_right = card_params.get("control_margin_right", 16)
            control_h_spacing = card_params.get("control_h_spacing", 20)
            control_v_spacing = card_params.get("control_v_spacing", 10)
            controls_per_row = card_params.get("controls_per_row", 2)
            vertical_center = card_params.get("vertical_center", True)
            
            # 计算行数
            num_controls = len(controls)
            num_rows = (num_controls + controls_per_row - 1) // controls_per_row
            
            # 创建每行的控件
            rows = []
            for row_idx in range(num_rows):
                start_idx = row_idx * controls_per_row
                end_idx = min(start_idx + controls_per_row, num_controls)
                row_controls = controls[start_idx:end_idx]
                
                # 创建一行控件
                row = ft.Row(
                    row_controls,
                    spacing=control_h_spacing,
                    alignment=ft.MainAxisAlignment.START,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                )
                rows.append(row)
            
            # 创建右侧内容容器
            content_column = ft.Column(
                rows,
                spacing=control_v_spacing,
                scroll=ft.ScrollMode.AUTO,
            )
            
            # 计算卡片高度
            control_height = 40  # 每个控件的高度
            total_controls_height = num_rows * control_height + (num_rows - 1) * control_v_spacing
            min_card_height = max(card_height, total_controls_height + 40)  # 40是上下边距
            
            content_container = ft.Container(
                content=content_column,
                left=content_left,
                top=0,
                bottom=0,
                right=control_margin_right,
                alignment=ft.Alignment(-1, 0) if vertical_center else ft.Alignment(-1, -1),
            )
            stack_children.append(content_container)
            
            # 更新卡片高度
            card_height = min_card_height
        
        # ========== 创建主布局 ==========
        main_stack = ft.Stack(
            stack_children,
            height=card_height,
            width=card_width,
            clip_behavior=ft.ClipBehavior.NONE,
        )
        
        # ========== 创建卡片容器 ==========
        container = CardContainer.create(
            config=config,
            content=main_stack,
            height=card_height,
            width=card_width,
        )
        
        # ========== 暴露控制接口 ==========
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
MultiRowCard = UniversalCard
多行卡片 = UniversalCard


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    # 1. 界面配置初始化
    配置 = 界面配置()
    
    # 2. 自动加载用户数据覆盖默认值（在界面配置.__init__中自动完成）
    
    # 3. 正常启动被测模块
    def main(page: ft.Page):
        page.padding = 20
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        
        # 创建多个控件
        controls = [
            ft.Dropdown(
                options=[ft.dropdown.Option(f"选项{i}") for i in range(1, 4)],
                value="选项1",
                width=120,
            ),
            ft.Dropdown(
                options=[ft.dropdown.Option(f"选项{i}") for i in range(1, 4)],
                value="选项2",
                width=120,
            ),
            ft.TextField(value="输入框", width=120),
        ]
        
        page.add(UniversalCard.create(
            配置,
            title="多行卡片测试",
            icon="HOME",
            enabled=True,
            help_text="点击切换状态",
            controls=controls,
            height=150,
        ))  # 只能更改此处**被测调用模块名称**
    
    ft.run(main)
