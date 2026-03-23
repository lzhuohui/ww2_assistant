# -*- coding: utf-8 -*-
"""
模块名称：折叠卡片V2 | 设计思路：卡片高度固定，右侧内容切换（副标题↔控件），带动画效果 | 模块隔离原则：不直接创建被调用模块的内容，不覆盖被调用模块的计算结果，用户指定变量除外
"""

import flet as ft
from typing import Callable, Dict, Any, List, Optional
import threading

from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider
from 前端.用户设置界面.单元模块.卡片容器 import CardContainer, USER_WIDTH, USER_PADDING, USER_HEIGHT
from 前端.用户设置界面.组件模块.图标标题 import IconTitle
from 前端.用户设置界面.单元模块.下拉框 import Dropdown, USER_WIDTH as DROPDOWN_WIDTH
from 前端.用户设置界面.配置.界面配置 import 界面配置


# *** 用户指定变量 - AI不得修改, 变量值必须生效 ***
USER_ANIMATION_DURATION = 200
USER_DESTROY_DELAY_SECONDS = 30
USER_DIVIDER_LEFT = 70
# *********************************


class CollapsibleCardV2:
    """折叠卡片V2 - 卡片高度固定，右侧内容切换，带动画效果"""
    
    @staticmethod
    def create(
        title: str="卡片标题",
        icon: str="HOME",
        subtitle: str="",
        enabled: bool=True,
        controls_config: List[Dict[str, Any]]=None,
        controls_per_row: int=6,
        width: int=USER_WIDTH,
        on_value_change: Callable[[str, Any], None]=None,
        on_state_change: Callable[[bool], None]=None,
        on_save: Callable[[str, str], None]=None,
    ) -> ft.Container:
        配置 = 界面配置()
        theme_colors = 配置.当前主题颜色
        spacing_config = 配置.定义尺寸.get("间距", {})
        control_h_spacing = spacing_config.get("spacing_md", 16)
        control_v_spacing = spacing_config.get("spacing_sm", 8)
        control_margin_right = spacing_config.get("spacing_lg", 20)
        
        card_height = USER_HEIGHT
        card_padding = USER_PADDING
        
        is_loaded = [False]
        is_enabled = [enabled]
        dropdown_controls: Dict[str, ft.Control] = {}
        destroy_timer: Optional[threading.Timer] = None
        current_values: Dict[str, str] = {}
        
        load_icon = ft.Icon(
            ft.Icons.PLAY_ARROW,
            size=18,
            color=theme_colors.get("text_secondary"),
        )
        
        subtitle_text = ft.Text(
            subtitle,
            size=14,
            color=theme_colors.get("text_secondary"),
        )
        
        subtitle_container = ft.Container(
            content=ft.Row([
                subtitle_text,
                ft.Container(width=8),
                load_icon,
            ], alignment=ft.MainAxisAlignment.END, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            opacity=1.0,
            animate=ft.Animation(USER_ANIMATION_DURATION, ft.AnimationCurve.EASE_OUT),
        )
        
        controls_column = ft.Column([], spacing=control_v_spacing)
        
        controls_container = ft.Container(
            content=controls_column,
            opacity=0.0,
            animate=ft.Animation(USER_ANIMATION_DURATION, ft.AnimationCurve.EASE_OUT),
        )
        
        right_stack = ft.Stack([
            subtitle_container,
            controls_container,
        ], height=card_height - card_padding * 2)
        
        right_container = ft.Container(
            content=right_stack,
            right=control_margin_right,
            top=card_padding,
            bottom=card_padding,
            alignment=ft.Alignment(1, 0),
            on_click=lambda e: load_controls(),
        )
        
        icon_title = IconTitle.create(
            title=title,
            icon=icon,
            enabled=enabled,
            on_state_change=lambda new_enabled: handle_state_change(new_enabled),
            subtitle="",
            divider_height=card_height - card_padding,
            divider_left=USER_DIVIDER_LEFT,
            divider_top=-int(card_padding / 2),
        )
        
        left_container = ft.Container(content=icon_title)
        
        main_stack = ft.Stack([
            left_container,
            right_container,
        ], height=card_height, width=width)
        
        def create_controls():
            """创建控件"""
            if is_loaded[0] or not controls_config:
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
                        
                        current_values[config_key] = value
                        
                        label_text = ft.Text(
                            label,
                            size=14,
                            color=theme_colors.get("text_secondary"),
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
                    spacing=control_h_spacing,
                    alignment=ft.MainAxisAlignment.END,
                )
                rows.append(row)
            
            controls_column.controls = rows
            is_loaded[0] = True
        
        def destroy_controls():
            """销毁控件"""
            nonlocal destroy_timer
            if not is_loaded[0]:
                return
            
            controls_column.controls = []
            dropdown_controls.clear()
            is_loaded[0] = False
            
            if destroy_timer:
                destroy_timer.cancel()
                destroy_timer = None
        
        def start_destroy_timer():
            """启动延迟销毁定时器"""
            nonlocal destroy_timer
            if destroy_timer:
                destroy_timer.cancel()
            
            destroy_timer = threading.Timer(
                USER_DESTROY_DELAY_SECONDS,
                lambda: safe_destroy()
            )
            destroy_timer.daemon = True
            destroy_timer.start()
        
        def safe_destroy():
            """安全销毁"""
            try:
                if main_stack.page:
                    main_stack.page.run_thread(lambda: destroy_controls())
            except:
                pass
        
        def cancel_destroy_timer():
            """取消销毁定时器"""
            nonlocal destroy_timer
            if destroy_timer:
                destroy_timer.cancel()
                destroy_timer = None
        
        def load_controls():
            """加载控件（右侧内容切换）"""
            if is_loaded[0]:
                return
            
            cancel_destroy_timer()
            create_controls()
            
            subtitle_container.opacity = 0.0
            controls_container.opacity = 1.0
            
            try:
                if main_stack.page:
                    main_stack.page.update()
            except:
                pass
        
        def unload_controls():
            """卸载控件（恢复副标题）"""
            subtitle_container.opacity = 1.0
            controls_container.opacity = 0.0
            
            start_destroy_timer()
            
            try:
                if main_stack.page:
                    main_stack.page.update()
            except:
                pass
        
        def handle_value_change(config_key: str, value: Any):
            """处理值变化"""
            current_values[config_key] = value
            
            if on_value_change:
                on_value_change(config_key, value)
            
            if on_save:
                on_save(config_key, value)
        
        def handle_state_change(new_enabled: bool):
            """处理状态变化"""
            is_enabled[0] = new_enabled
            load_icon.opacity = 1.0 if new_enabled else 0.4
            subtitle_text.opacity = 1.0 if new_enabled else 0.4
            
            for ctrl in dropdown_controls.values():
                if hasattr(ctrl, 'set_state'):
                    ctrl.set_state(new_enabled)
            
            try:
                if main_stack.page:
                    main_stack.page.update()
            except:
                pass
            
            if on_state_change:
                on_state_change(new_enabled)
        
        def set_state(new_enabled: bool):
            """设置启用状态"""
            icon_title.set_state(new_enabled, notify=True)
        
        def get_state() -> bool:
            """获取启用状态"""
            return is_enabled[0]
        
        def get_values() -> Dict[str, str]:
            """获取所有值"""
            for key, ctrl in dropdown_controls.items():
                if hasattr(ctrl, 'get_value'):
                    current_values[key] = ctrl.get_value()
            return current_values.copy()
        
        def set_values(values: Dict[str, str]):
            """设置值"""
            for key, value in values.items():
                if key in dropdown_controls:
                    ctrl = dropdown_controls[key]
                    if hasattr(ctrl, 'set_value'):
                        ctrl.set_value(value)
                    current_values[key] = value
        
        def is_controls_loaded() -> bool:
            """检查控件是否已加载"""
            return is_loaded[0]
        
        def dispose():
            """释放资源"""
            cancel_destroy_timer()
            destroy_controls()
        
        container = CardContainer.create(
            config=配置,
            content=main_stack,
            height=card_height,
            width=width,
            padding=card_padding,
        )
        
        container.set_state = set_state
        container.get_state = get_state
        container.get_values = get_values
        container.set_values = set_values
        container.load_controls = load_controls
        container.unload_controls = unload_controls
        container.is_loaded = is_controls_loaded
        container.dispose = dispose
        
        if not enabled:
            load_icon.opacity = 0.4
            subtitle_text.opacity = 0.4
        
        return container


# *** 调试逻辑 ***
if __name__ == "__main__":
    from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider
    
    配置 = 界面配置()
    ThemeProvider.initialize(配置)
    
    test_controls = [
        {"type": "dropdown", "config_key": "test_1", "label": "城市", "value": "17", "options": [f"{i:02d}级" for i in range(1, 21)]},
        {"type": "dropdown", "config_key": "test_2", "label": "兵工", "value": "10", "options": [f"{i:02d}级" for i in range(1, 21)]},
        {"type": "dropdown", "config_key": "test_3", "label": "陆军", "value": "14", "options": [f"{i:02d}级" for i in range(1, 21)]},
    ]
    
    saved_values = {}
    
    def on_save(key, value):
        saved_values[key] = value
        print(f"即时保存: {key} = {value}")
    
    ft.run(lambda page: page.add(
        CollapsibleCardV2.create(
            title="主帅主城",
            icon="HOME",
            subtitle="设置主帅主城建筑等级",
            controls_config=test_controls,
            controls_per_row=3,
            on_save=on_save,
        )
    ))
