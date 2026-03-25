# -*- coding: utf-8 -*-
"""
模块名称：CollapsibleCard
设计思路: 卡片高度固定，支持配置模式和只读模式
模块隔离: 复合组件，依赖基础组件
"""

import flet as ft
from typing import Callable, Dict, Any, List, Optional

from 前端.新界面_v2.核心.配置.界面配置 import UIConfig
from 前端.新界面_v2.表示层.组件.基础.卡片容器 import CardContainer, USER_WIDTH, USER_PADDING, USER_HEIGHT
from 前端.新界面_v2.表示层.组件.基础.下拉框 import Dropdown, USER_WIDTH as DROPDOWN_WIDTH


# *** 用户指定变量: 变量值必须生效,AI不得更改数据 ***
USER_ANIMATION_DURATION = 150   # 动画时长(毫秒)
USER_DIVIDER_LEFT = 70          # 分割线到卡片左侧距离
USER_ICON_SIZE = 22             # 图标大小
USER_TITLE_SIZE = 14            # 标题大小
USER_SUBTITLE_SIZE = 10         # 副标题大小
# *********************************


class CollapsibleCard:
    """折叠卡片 - 支持配置模式和只读模式"""
    
    @staticmethod
    def create(
        title: str = "卡片标题",
        icon: str = "HOME",
        subtitle: str = "",
        enabled: bool = True,
        read_only: bool = False,
        controls: List[ft.Control] = None,
        controls_config: List[Dict[str, Any]] = None,
        controls_per_row: int = 6,
        width: int = None,
        on_value_change: Callable[[str, Any], None] = None,
        on_save: Callable[[str, str], None] = None,
        on_expand: Callable[[], None] = None,
        on_collapse: Callable[[], None] = None,
        config: UIConfig = None,
    ) -> ft.Container:
        if config is None:
            config = UIConfig()
        
        theme_colors = config.当前主题颜色
        control_h_spacing = config.get_size("spacing", "spacing_md") or 12
        control_v_spacing = config.get_size("spacing", "spacing_sm") or 8
        control_right_margin = config.get_size("spacing", "spacing_lg") or 16
        
        card_height = USER_HEIGHT
        card_padding = USER_PADDING
        
        loaded = [False]
        is_enabled = [enabled]
        switch_state = [enabled]
        control_dict: Dict[str, ft.Control] = {}
        current_values: Dict[str, str] = {}
        initial_values: Dict[str, str] = {}
        
        icon_control = ft.Icon(
            getattr(ft.Icons, icon.upper(), ft.Icons.HOME),
            size=USER_ICON_SIZE,
            color=theme_colors.get("accent"),
            opacity=1.0 if enabled else 0.4,
        )
        
        title_text = ft.Text(
            title,
            size=USER_TITLE_SIZE,
            weight=ft.FontWeight.BOLD,
            color=theme_colors.get("text_primary"),
            opacity=1.0 if enabled else 0.4,
        )
        
        original_subtitle = subtitle
        subtitle_text = ft.Text(
            subtitle + " >>" if not read_only else subtitle,
            size=USER_SUBTITLE_SIZE,
            color=theme_colors.get("text_secondary"),
        )
        
        controls_column = ft.Column([], spacing=control_v_spacing, alignment=ft.MainAxisAlignment.CENTER)
        
        controls_container = ft.Container(
            content=controls_column,
            opacity=0.0 if not read_only else 1.0,
            animate=ft.Animation(USER_ANIMATION_DURATION, ft.AnimationCurve.EASE_OUT) if not read_only else None,
            right=control_right_margin,
            top=0,
            bottom=0,
            alignment=ft.alignment.Alignment(1.0, 0.5),
            clip_behavior=ft.ClipBehavior.NONE,
        )
        
        subtitle_container = ft.Container(
            content=subtitle_text,
            left=0,
            top=0,
            bottom=0,
            right=0,
            opacity=1.0 if not read_only else 0.0,
            animate=ft.Animation(USER_ANIMATION_DURATION, ft.AnimationCurve.EASE_OUT) if not read_only else None,
            alignment=ft.Alignment(-1.0, 0.0),
        )
        
        right_stack = ft.Stack([
            subtitle_container,
            controls_container,
        ], clip_behavior=ft.ClipBehavior.NONE)
        
        right_container = ft.Container(
            content=right_stack,
            expand=True,
            clip_behavior=ft.ClipBehavior.NONE,
        )
        
        left_content = ft.Column([
            icon_control,
            ft.Container(height=4),
            title_text,
        ], spacing=0, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        left_container = ft.Container(
            content=left_content,
            padding=ft.Padding(left=card_padding, top=0, right=card_padding, bottom=0),
            expand=False,
        )
        
        # 计算左侧内容容器的宽度，确保分割线位置固定
        left_width = USER_DIVIDER_LEFT - 2  # 减去分割线宽度
        
        divider = ft.Container(
            width=2,
            bgcolor=theme_colors.get("accent", "#0078d4"),
            height=card_height - card_padding,
            margin=ft.Margin(0, card_padding / 2, 0, card_padding / 2)
        )
        
        # 创建左侧内容容器
        left_container = ft.Container(
            content=left_content,
            padding=ft.Padding(left=card_padding, top=0, right=card_padding, bottom=0),
            width=left_width,
            expand=False,
            alignment=ft.Alignment(0, 0.5),
        )
        
        main_row = ft.Row([
            left_container,
            divider,
            right_container,
        ], height=card_height, spacing=0, vertical_alignment=ft.CrossAxisAlignment.CENTER, expand=True if width is None else False)
        
        container = CardContainer.create(
            config=config,
            content=main_row,
            height=card_height,
            width=width,
            padding=card_padding,
        )
        container.clip_behavior = ft.ClipBehavior.NONE
        
        def handle_switch_toggle():
            if read_only:
                return
            new_state = not switch_state[0]
            switch_state[0] = new_state
            is_enabled[0] = new_state
            
            if on_save:
                on_save("enabled", new_state)
            
            update_card_state()
        
        def update_card_state():
            if read_only:
                container.opacity = 1.0
                icon_control.opacity = 1.0
                title_text.opacity = 1.0
                return
            
            if switch_state[0]:
                container.opacity = 1.0
                if not loaded[0]:
                    right_container.on_click = lambda e: load_controls()
                else:
                    right_container.on_click = None
                subtitle_text.color = theme_colors.get("text_secondary")
                icon_control.opacity = 1.0
                title_text.opacity = 1.0
                
                if loaded[0]:
                    for control_instance in control_dict.values():
                        if hasattr(control_instance, 'set_enabled'):
                            control_instance.set_enabled(True)
            else:
                container.opacity = 0.5
                right_container.on_click = None
                subtitle_text.color = theme_colors.get("text_disabled", "#888888")
                icon_control.opacity = 0.4
                title_text.opacity = 0.4
                
                if loaded[0]:
                    for control_instance in control_dict.values():
                        if hasattr(control_instance, 'set_enabled'):
                            control_instance.set_enabled(False)
            
            try:
                if container.page:
                    container.page.update()
            except:
                pass
        
        if not read_only:
            left_container.on_click = lambda e: handle_switch_toggle()
        
        def create_controls_from_config() -> List[ft.Control]:
            created_controls = []
            
            for control_config_item in controls_config:
                if control_config_item.get("type") == "dropdown":
                    config_key = control_config_item.get("config_key", "")
                    label = control_config_item.get("label", "")
                    options = control_config_item.get("options", [])
                    value = control_config_item.get("value", options[0] if options else "")
                    control_width = control_config_item.get("width", DROPDOWN_WIDTH)
                    
                    current_values[config_key] = value
                    initial_values[config_key] = value
                    
                    label_text = ft.Text(
                        label,
                        size=14,
                        color=theme_colors.get("text_secondary"),
                    )
                    
                    dropdown_instance = Dropdown.create(
                        options=options,
                        current_value=value,
                        width=control_width,
                        enabled=is_enabled[0] if not read_only else True,
                        on_change=lambda v, k=config_key: handle_value_change(k, v),
                        config=config,
                    )
                    control_dict[config_key] = dropdown_instance
                    
                    single_control = ft.Row([
                        label_text,
                        dropdown_instance,
                    ], spacing=4, vertical_alignment=ft.CrossAxisAlignment.CENTER)
                    
                    created_controls.append(single_control)
            
            return created_controls
        
        def layout_controls(control_list: List[ft.Control]):
            row_list = []
            current_row_controls = []
            current_row_count = 0
            
            for single_control in control_list:
                if current_row_count >= controls_per_row and current_row_controls:
                    row_list.append(ft.Row(
                        current_row_controls,
                        spacing=control_h_spacing,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.END,
                    ))
                    current_row_controls = []
                    current_row_count = 0
                
                current_row_controls.append(single_control)
                current_row_count += 1
            
            if current_row_controls:
                row_list.append(ft.Row(
                    current_row_controls,
                    spacing=control_h_spacing,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.END,
                ))
            
            controls_column.controls = row_list
            loaded[0] = True
        
        def handle_value_change(config_key: str, value: Any):
            current_values[config_key] = value
            
            if initial_values.get(config_key) != value:
                if on_value_change:
                    on_value_change(config_key, value)
                
                if on_save:
                    on_save(config_key, value)
        
        def load_controls():
            if loaded[0] or (not switch_state[0] and not read_only):
                return
            
            if on_expand:
                on_expand()
            
            final_control_list = []
            
            if controls is not None:
                final_control_list = controls
            elif controls_config is not None:
                final_control_list = create_controls_from_config()
            
            if final_control_list:
                layout_controls(final_control_list)
            
            # 设置加载标识
            loaded[0] = True
            
            # 展开后移除点击事件，让子控件可以正常响应
            right_container.on_click = None
            
            # 展开时不显示 >>
            subtitle_text.value = original_subtitle
            subtitle_container.top = 0
            subtitle_container.bottom = 0
            subtitle_container.left = 0
            subtitle_container.right = 0
            subtitle_container.alignment = ft.Alignment(-1.0, 1.0)
            subtitle_container.opacity = 1.0
            controls_container.opacity = 1.0
            
            try:
                if container.page:
                    container.page.update()
            except:
                pass
        
        def get_values() -> Dict[str, str]:
            for key, control_instance in control_dict.items():
                if hasattr(control_instance, 'get_value'):
                    current_values[key] = control_instance.get_value()
            return current_values.copy()
        
        def set_values(value_dict: Dict[str, str]):
            for key, value in value_dict.items():
                if key in control_dict:
                    control_instance = control_dict[key]
                    if hasattr(control_instance, 'set_value'):
                        control_instance.set_value(value)
                    current_values[key] = value
                    initial_values[key] = value
        
        def get_switch_state() -> bool:
            return switch_state[0]
        
        def set_switch_state(state: bool):
            if read_only:
                return
            switch_state[0] = state
            is_enabled[0] = state
            update_card_state()
        
        def destroy_controls():
            if not loaded[0]:
                return
            controls_column.controls = []
            control_dict.clear()
            loaded[0] = False
        
        def unload_options_only():
            if not loaded[0]:
                return
            for control_instance in control_dict.values():
                if hasattr(control_instance, 'unload_options'):
                    control_instance.unload_options()
        
        def collapse():
            if read_only:
                return
            destroy_controls()
            # 折叠时显示 >>
            subtitle_text.value = original_subtitle + " >>"
            subtitle_container.top = 0
            subtitle_container.bottom = 0
            subtitle_container.left = 0
            subtitle_container.right = 0
            subtitle_container.alignment = ft.Alignment(-1.0, 0.0)
            subtitle_container.opacity = 1.0
            controls_container.opacity = 0.0
            if on_collapse:
                on_collapse()
            try:
                if container.page:
                    container.page.update()
            except:
                pass
        
        container.get_values = get_values
        container.set_values = set_values
        container.load_controls = load_controls
        container.is_loaded = lambda: loaded[0]
        container.get_switch_state = get_switch_state
        container.set_switch_state = set_switch_state
        container.destroy_controls = destroy_controls
        container.unload_options_only = unload_options_only
        container.collapse = collapse
        
        def set_subtitle(new_subtitle: str, is_expanded: bool = None):
            nonlocal original_subtitle
            original_subtitle = new_subtitle
            if is_expanded is None:
                is_expanded = loaded[0]
            # 根据展开状态决定是否添加 " >>"
            subtitle_text.value = new_subtitle if is_expanded else new_subtitle + " >>"
            try:
                if container.page:
                    container.page.update()
            except:
                pass
        
        container.set_subtitle = set_subtitle
        
        if read_only and (controls is not None or controls_config is not None):
            load_controls()
        
        update_card_state()
        
        return container


# *** 标准测试格式: 仅调用被测模块,AI不得添加数据 ***
if __name__ == "__main__":
    def main(page: ft.Page):
        page.add(CollapsibleCard.create())
    
    ft.app(target=main)
