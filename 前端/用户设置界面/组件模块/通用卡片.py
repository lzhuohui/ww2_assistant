# -*- coding: utf-8 -*-
"""
模块名称：通用卡片 | 层级：组件模块层
设计思路：
    装配模式：组合零件模块，协调交互。
    - 不直接操作零件内部控件
    - 通过零件暴露的接口进行控制
    - 负责布局和协调
    - 支持多行控件布局

功能：
    1. 组合零件模块
    2. 协调状态切换
    3. 布局排列
    4. 支持多行控件
    5. 支持副标题

对外接口：
    - create(): 创建通用卡片
    - set_state(): 设置启用状态
    - toggle_state(): 切换状态
    - get_state(): 获取状态
"""

import flet as ft
from typing import Callable, Optional, List
from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider
from 前端.用户设置界面.单元模块.卡片容器 import CardContainer
from 前端.用户设置界面.组件模块.图标标题 import IconTitle
from 前端.配置.界面配置 import 界面配置

# *** 用户指定变量 - AI不得修改 ***
DEFAULT_CARD_WIDTH = 800
# *********************************


class UniversalCard:
    """通用卡片 - 装配模式，组合零件模块，支持多行控件"""
    
    @staticmethod
    def create(
        title: str,
        icon: str = None,
        enabled: bool = True,
        on_state_change: Callable[[bool], None] = None,
        help_text: str = None,
        height: int = None,
        width: int = None,
        controls: List[ft.Control] = None,
        subtitle: str = None,
        controls_per_row: int = None,
        **kwargs
    ) -> ft.Container:
        """
        创建通用卡片
        
        参数：
            title: 标题文字
            icon: 图标名称
            enabled: 初始启用状态
            on_state_change: 状态变化回调
            help_text: 帮助提示文字
            height: 卡片高度
            width: 卡片宽度
            controls: 右侧控件列表（支持多行）
            subtitle: 副标题
            controls_per_row: 每行控件数量
        
        返回：
            ft.Container: 完整的卡片容器
        """
        配置 = 界面配置()
        
        ui_config = 配置.定义尺寸.get("界面", {})
        card_padding = ui_config.get("card_padding", 16)
        spacing_config = 配置.定义尺寸.get("间距", {})
        control_h_spacing = spacing_config.get("spacing_md", 16)
        control_v_spacing = spacing_config.get("spacing_sm", 8)
        control_margin_right = spacing_config.get("spacing_lg", 20)
        
        current_enabled = enabled
        current_controls_per_row = controls_per_row if controls_per_row is not None else 1
        
        min_control_height = 35
        min_card_height = min_control_height + card_padding * 2
        card_height = min_card_height
        
        if controls:
            num_controls = len(controls)
            num_rows = (num_controls + current_controls_per_row - 1) // current_controls_per_row
            
            total_controls_height = 0
            for i, control in enumerate(controls):
                control_height = getattr(control, 'height', 35) or 35
                if i % current_controls_per_row == 0:
                    total_controls_height += control_height
            
            calculated_height = total_controls_height + card_padding * (num_rows + 1)
            card_height = max(calculated_height, min_card_height)
        
        def on_icon_title_state_change(new_enabled: bool):
            nonlocal current_enabled
            current_enabled = new_enabled
            sync_controls_state(new_enabled)
            if on_state_change:
                on_state_change(new_enabled)
        
        # 计算分割线高度，确保分割线上部离卡片上部半个边距，分割线下部离卡片下部半个边距
        divider_height = card_height - card_padding
        
        icon_title = IconTitle.create(
            title=title,
            icon=icon,
            enabled=current_enabled,
            on_state_change=on_icon_title_state_change,
            subtitle=subtitle,
            divider_height=divider_height,
        )
        
        def sync_controls_state(new_enabled: bool):
            if controls:
                for control in controls:
                    control.opacity = 1.0 if new_enabled else 0.4
                    if hasattr(control, 'set_state'):
                        control.set_state(new_enabled)
                    if control.page:
                        control.update()
        
        if controls and not current_enabled:
            for control in controls:
                control.opacity = 0.4
                if hasattr(control, 'set_state'):
                    control.set_state(current_enabled)
        
        # 计算图标标题和分割线的位置，确保分割线上部离卡片上部半个边距，分割线下部离卡片下部半个边距
        left_container = ft.Container(
            content=icon_title,
            top=card_padding / 2,
        )
        
        stack_children = [left_container]
        
        if controls:
            rows = []
            
            for row_idx in range(num_rows):
                start_idx = row_idx * current_controls_per_row
                end_idx = min(start_idx + current_controls_per_row, len(controls))
                row_controls = controls[start_idx:end_idx]
                
                row = ft.Row(
                    row_controls,
                    spacing=control_h_spacing,
                    alignment=ft.MainAxisAlignment.END,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                )
                rows.append(row)
            
            content_column = ft.Column(
                rows,
                spacing=control_v_spacing,
                scroll=ft.ScrollMode.AUTO,
            )
            
            content_container = ft.Container(
                content=content_column,
                right=control_margin_right,
                top=0,
                bottom=0,
                alignment=ft.Alignment(1, 0),
            )
            stack_children.append(content_container)
        
        main_stack = ft.Stack(
            stack_children,
            height=card_height,
            width=float('inf'),
            clip_behavior=ft.ClipBehavior.NONE,
        )
        
        container = CardContainer.create(
            config=配置,
            content=main_stack,
            height=card_height,
            width=float('inf'),
            padding=card_padding,
        )
        
        def set_state(new_enabled: bool):
            nonlocal current_enabled
            current_enabled = new_enabled
            icon_title.set_state(new_enabled, notify=False)
            sync_controls_state(new_enabled)
            if on_state_change:
                on_state_change(new_enabled)
        
        def toggle_state(e=None):
            set_state(not current_enabled)
        
        def get_state() -> bool:
            return current_enabled
        
        def set_subtitle(new_text: str):
            if hasattr(icon_title, 'set_subtitle'):
                icon_title.set_subtitle(new_text)
        
        container.set_state = set_state
        container.toggle_state = toggle_state
        container.get_state = get_state
        container.set_subtitle = set_subtitle
        
        return container


# *** 调试逻辑 ***
if __name__ == "__main__":
    配置 = 界面配置()
    from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider
    ThemeProvider.initialize(配置)
    def main(page: ft.Page):
        page.add(UniversalCard.create(title="测试卡片", icon="SETTINGS", subtitle="这是副标题"))
    ft.run(main)
