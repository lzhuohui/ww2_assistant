# -*- coding: utf-8 -*-
"""
模块名称：通用卡片
设计思路及联动逻辑:
    1. 分割线定位: 上部到卡片外缘=0.5*边距, 高度=卡片高度-1*边距
    2. 通过divider_height/divider_top参数传递给图标标题模块实现联动
    3. 卡片高度根据控件数量自动计算
模块隔离原则:
    1. 不直接创建被调用模块的内容
    2. 不覆盖被调用模块的计算结果
    3. 用户指定变量除外
"""

from flet.controls.control import Control


import flet as ft
from typing import Callable, List

from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider
from 前端.用户设置界面.单元模块.卡片容器 import CardContainer, USER_WIDTH, USER_HEIGHT, USER_PADDING
from 前端.用户设置界面.组件模块.图标标题 import IconTitle
from 前端.用户设置界面.配置.界面配置 import 界面配置


# *** 用户指定变量 - AI不得修改, 变量值必须生效 ***
USER_DIVIDER_LEFT = 70  # 分割线到卡片左侧的距离
# *********************************


class UniversalCard:
    """通用卡片 - 组合零件模块，支持多行控件"""
    
    @staticmethod
    def create(
        title: str="测试标题",
        icon: str="HOME",
        enabled: bool=True,
        on_state_change: Callable[[bool], None]=None,
        width: int=USER_WIDTH,
        controls: List[ft.Control]=None,
        subtitle: str="这是副标题",
        controls_per_row: int=1
    ) -> ft.Container:
        配置 = 界面配置()
        
        card_padding = USER_PADDING
        spacing_config = 配置.定义尺寸.get("间距", {})
        control_h_spacing = spacing_config.get("spacing_md", 16)
        control_v_spacing = spacing_config.get("spacing_sm", 8)
        control_margin_right = spacing_config.get("spacing_lg", 20)
        
        current_enabled = enabled
        current_controls_per_row = controls_per_row
        
        min_control_height = 50
        min_card_height = min_control_height + card_padding * 2
        card_height = min_card_height
        
        if controls:
            num_controls = len(controls)
            num_rows = (num_controls + current_controls_per_row - 1) // current_controls_per_row
            
            total_controls_height = 0
            for i, control in enumerate[Control](controls):
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
        
        divider_height = card_height - card_padding
        divider_top = -int(card_padding / 2)
        
        icon_title = IconTitle.create(
            title=title,
            icon=icon,
            enabled=current_enabled,
            on_state_change=on_icon_title_state_change,
            subtitle=subtitle,
            divider_height=divider_height,
            divider_left=USER_DIVIDER_LEFT,
            divider_top=divider_top,
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
        
        left_container = ft.Container(
            content=icon_title,
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
            width=width,
            clip_behavior=ft.ClipBehavior.NONE,
        )
        
        container = CardContainer.create(
            config=配置,
            content=main_stack,
            height=card_height,
            width=width,
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
    ft.run(lambda page: page.add(UniversalCard.create()))
