# -*- coding: utf-8 -*-
"""
模块名称：折叠卡片 | 设计思路：可展开/收起的卡片组件，默认折叠状态，点击展开显示控件 | 模块隔离原则：不直接创建被调用模块的内容，不覆盖被调用模块的计算结果，用户指定变量除外
"""

import flet as ft
from typing import Callable, Dict, Any, List

from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider
from 前端.用户设置界面.单元模块.卡片容器 import CardContainer, USER_WIDTH, USER_PADDING
from 前端.用户设置界面.单元模块.下拉框 import Dropdown, USER_WIDTH as DROPDOWN_WIDTH, USER_HEIGHT as DROPDOWN_HEIGHT


# *** 用户指定变量 - AI不得修改, 变量值必须生效 ***
USER_HEADER_HEIGHT = 48
USER_COLLAPSED_HEIGHT = USER_HEADER_HEIGHT + USER_PADDING * 2
USER_ANIMATION_DURATION = 200
# *********************************


class CollapsibleCard:
    """折叠卡片 - 可展开/收起的卡片组件"""
    
    @staticmethod
    def create(
        title: str="卡片标题",
        icon: str="HOME",
        subtitle: str="",
        enabled: bool=True,
        expanded: bool=False,
        controls_config: List[Dict[str, Any]]=None,
        controls_per_row: int=6,
        width: int=USER_WIDTH,
        on_value_change: Callable[[str, Any], None]=None,
        on_state_change: Callable[[bool], None]=None,
    ) -> ft.Container:
        is_expanded = [expanded]
        is_enabled = [enabled]
        dropdown_controls = {}
        
        theme_colors = {
            "text_primary": ThemeProvider.get_color("text_primary"),
            "text_secondary": ThemeProvider.get_color("text_secondary"),
            "bg_card": ThemeProvider.get_color("bg_card"),
            "bg_secondary": ThemeProvider.get_color("bg_secondary"),
            "border": ThemeProvider.get_color("border"),
        }
        
        expand_icon = ft.Icon(
            ft.Icons.EXPAND_LESS if expanded else ft.Icons.EXPAND_MORE,
            size=20,
            color=theme_colors["text_secondary"],
        )
        
        title_text = ft.Text(
            title,
            size=16,
            weight=ft.FontWeight.BOLD,
            color=theme_colors["text_primary"],
        )
        
        subtitle_text = ft.Text(
            subtitle,
            size=12,
            color=theme_colors["text_secondary"],
        )
        
        icon_control = ft.Icon(
            getattr(ft.Icons, icon, ft.Icons.HOME),
            size=24,
            color=theme_colors["text_primary"],
        )
        
        header_row = ft.Row([
            icon_control,
            ft.Column([title_text, subtitle_text], spacing=2, expand=True),
            ft.Container(expand=True),
            expand_icon,
        ], spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER)
        
        header_container = ft.Container(
            content=header_row,
            height=USER_HEADER_HEIGHT,
            padding=ft.Padding(left=16, right=16, top=8, bottom=8),
            on_click=lambda e: toggle_expand(),
        )
        
        content_column = ft.Column([], spacing=8)
        controls_created = [False]
        
        content_container = ft.Container(
            content=content_column,
            padding=ft.Padding(left=16, right=16, top=0, bottom=16),
            visible=expanded,
            animate=ft.Animation(USER_ANIMATION_DURATION, ft.AnimationCurve.EASE_OUT),
        )
        
        main_column = ft.Column([
            header_container,
            content_container,
        ], spacing=0)
        
        def create_controls_if_needed():
            if controls_created[0] or not controls_config:
                return
            
            rows = []
            num_controls = len(controls_config)
            num_rows = (num_controls + controls_per_row - 1) // controls_per_row
            
            for row_idx in range(num_rows):
                start_idx = row_idx * controls_per_row
                end_idx = min(start_idx + controls_per_row, num_controls)
                row_configs = controls_config[start_idx:end_idx]
                
                row_controls = []
                for ctrl_config in row_configs:
                    if ctrl_config.get("type") == "dropdown":
                        label = ctrl_config.get("label", "")
                        config_key = ctrl_config.get("config_key", "")
                        options = ctrl_config.get("options", [])
                        value = ctrl_config.get("value", options[0] if options else "")
                        ctrl_width = ctrl_config.get("width", DROPDOWN_WIDTH)
                        
                        label_text = ft.Text(
                            label,
                            size=14,
                            color=theme_colors["text_secondary"],
                        )
                        
                        dropdown = Dropdown.create(
                            options=options,
                            value=value,
                            width=ctrl_width,
                            enabled=is_enabled[0],
                            on_change=lambda v, k=config_key: handle_value_change(k, v),
                        )
                        dropdown_controls[config_key] = dropdown
                        
                        row_controls.append(ft.Row([
                            label_text,
                            dropdown,
                        ], spacing=4, vertical_alignment=ft.CrossAxisAlignment.CENTER))
                
                row = ft.Row(
                    row_controls,
                    spacing=16,
                    alignment=ft.MainAxisAlignment.START,
                )
                rows.append(row)
            
            content_column.controls = rows
            controls_created[0] = True
        
        def toggle_expand():
            is_expanded[0] = not is_expanded[0]
            if is_expanded[0] and not controls_created[0]:
                create_controls_if_needed()
            content_container.visible = is_expanded[0]
            expand_icon.name = ft.Icons.EXPAND_LESS if is_expanded[0] else ft.Icons.EXPAND_MORE
            try:
                if header_container.page:
                    header_container.page.update()
            except:
                pass
        
        def handle_value_change(config_key: str, value: Any):
            if on_value_change:
                on_value_change(config_key, value)
        
        def set_state(new_enabled: bool):
            is_enabled[0] = new_enabled
            title_text.opacity = 1.0 if new_enabled else 0.4
            subtitle_text.opacity = 1.0 if new_enabled else 0.4
            icon_control.opacity = 1.0 if new_enabled else 0.4
            for ctrl in dropdown_controls.values():
                if hasattr(ctrl, 'set_state'):
                    ctrl.set_state(new_enabled)
            try:
                if header_container.page:
                    header_container.page.update()
            except:
                pass
            if on_state_change:
                on_state_change(new_enabled)
        
        def get_state() -> bool:
            return is_enabled[0]
        
        def get_values() -> Dict[str, str]:
            values = {}
            for key, ctrl in dropdown_controls.items():
                if hasattr(ctrl, 'get_value'):
                    values[key] = ctrl.get_value()
            return values
        
        def set_values(values: Dict[str, str]):
            for key, value in values.items():
                if key in dropdown_controls:
                    ctrl = dropdown_controls[key]
                    if hasattr(ctrl, 'set_value'):
                        ctrl.set_value(value)
        
        def expand():
            if not is_expanded[0]:
                toggle_expand()
        
        def collapse():
            if is_expanded[0]:
                toggle_expand()
        
        container = CardContainer.create(
            content=main_column,
            height=None,
            width=width,
            padding=0,
            on_hover_enabled=True,
        )
        
        container.set_state = set_state
        container.get_state = get_state
        container.get_values = get_values
        container.set_values = set_values
        container.expand_card = expand
        container.collapse_card = collapse
        container.is_expanded = lambda: is_expanded[0]
        
        if not enabled:
            set_state(False)
        
        return container


# *** 调试逻辑 ***
if __name__ == "__main__":
    from 前端.用户设置界面.配置.界面配置 import 界面配置
    from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider
    
    配置 = 界面配置()
    ThemeProvider.initialize(配置)
    
    test_controls = [
        {"type": "dropdown", "config_key": "test_1", "label": "城市", "value": "17"},
        {"type": "dropdown", "config_key": "test_2", "label": "兵工", "value": "10"},
        {"type": "dropdown", "config_key": "test_3", "label": "陆军", "value": "14"},
    ]
    
    ft.run(lambda page: page.add(CollapsibleCard.create(
        title="测试卡片",
        icon="HOME",
        subtitle="这是一个测试卡片",
        controls_config=test_controls,
        controls_per_row=3,
    )))
