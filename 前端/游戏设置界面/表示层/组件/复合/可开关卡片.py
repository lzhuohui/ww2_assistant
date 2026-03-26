# -*- coding: utf-8 -*-
"""
模块名称:SwitchableCard
模块功能:可开关卡片组件,保留开关功能,移除折叠功能,控件始终显示

控制流程:
1. 启动时加载所有卡片的控件默认值
2. 启动时只加载第一个卡片的选项列表
3. 点击卡片时检查加载标识
4. 未加载:通知管理器加载选项列表
5. 已加载:不做任何操作(避免重复加载)

实现步骤:
- 创建卡片布局(左侧图标+标题,右侧控件)
- 支持开关状态切换(启用/禁用)
- 控件始终显示(无需展开)
- 支持控件选项列表按需加载
"""

import flet as ft
from typing import Callable, Dict, Any, List, Optional

from 前端.游戏设置界面.核心层.配置.界面配置 import UIConfig
from 前端.游戏设置界面.表示层.组件.基础.卡片容器 import CardContainer, USER_HEIGHT, USER_PADDING


# *** 用户指定变量: 变量值必须生效,AI不得更改数据 ***
USER_DIVIDER_LEFT = 76  # 左侧分隔线位置
USER_ICON_SIZE = 22  # 图标大小
USER_TITLE_SIZE = 14  # 标题字体大小
USER_SUBTITLE_SIZE = 11  # 副标题字体大小
# *********************************


class SwitchableCard:
    """可开关卡片组件 - 保留开关功能,控件始终显示"""
    
    @staticmethod
    def create(
        title: str = "卡片标题",
        icon: str = "HOME",
        subtitle: str = "",
        enabled: bool = True,
        controls: List[ft.Control] = None,
        controls_config: List[Dict[str, Any]] = None,
        controls_per_row: int = 6,
        width: int = None,
        on_value_change: Callable[[str, Any], None] = None,
        on_save: Callable[[str, str], None] = None,
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
        
        # 卡片状态
        is_enabled = [enabled]
        switch_state = [enabled]
        control_dict: Dict[str, ft.Control] = {}
        options_dict: Dict[str, List[str]] = {}
        current_values: Dict[str, str] = {}
        initial_values: Dict[str, str] = {}
        
        # 左侧图标
        icon_control = ft.Icon(
            getattr(ft.Icons, icon.upper(), ft.Icons.HOME),
            size=USER_ICON_SIZE,
            color=theme_colors.get("accent"),
            opacity=1.0 if enabled else 0.4,
        )
        
        # 左侧标题
        title_text = ft.Text(
            title,
            size=USER_TITLE_SIZE,
            weight=ft.FontWeight.BOLD,
            color=theme_colors.get("text_primary"),
            opacity=1.0 if enabled else 0.4,
            no_wrap=True,
            overflow=ft.TextOverflow.ELLIPSIS,
        )
        
        # 副标题(始终显示)
        subtitle_text = ft.Text(
            subtitle,
            size=USER_SUBTITLE_SIZE,
            color=theme_colors.get("text_secondary"),
        )
        
        # 控件容器(始终显示)
        controls_column = ft.Column([], spacing=control_v_spacing, alignment=ft.MainAxisAlignment.CENTER)
        
        controls_container = ft.Container(
            content=controls_column,
            opacity=1.0,  # 始终显示,无需动画
            right=control_right_margin,
            top=0,
            bottom=0,
            alignment=ft.alignment.Alignment(1.0, 0.5),
            clip_behavior=ft.ClipBehavior.NONE,
        )
        
        # 副标题容器(始终显示,底部对齐)
        subtitle_container = ft.Container(
            content=subtitle_text,
            left=8,
            top=0,
            bottom=0,
            right=0,
            opacity=1.0,  # 显示副标题
            alignment=ft.Alignment(-1.0, 1.0),  # 左下对齐
        )
        
        # 右侧区域Stack
        right_stack = ft.Stack([
            subtitle_container,
            controls_container,
        ], clip_behavior=ft.ClipBehavior.NONE)
        
        # 右侧容器
        right_container = ft.Container(
            content=right_stack,
            expand=True,
            clip_behavior=ft.ClipBehavior.NONE,
        )
        
        # 左侧内容
        left_width = USER_DIVIDER_LEFT - 2
        
        left_content = ft.Column([
            icon_control,
            ft.Container(height=4),
            title_text,
        ], spacing=0, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        # 分隔线
        divider = ft.Container(
            width=2,
            bgcolor=theme_colors.get("accent", "#0078d4"),
            height=card_height - card_padding,
            margin=ft.Margin(0, card_padding / 2, 0, card_padding / 2)
        )
        
        # 左侧容器
        left_container = ft.Container(
            content=left_content,
            padding=ft.Padding(left=card_padding, top=0, right=card_padding, bottom=0),
            width=left_width,
            expand=False,
            alignment=ft.Alignment(0, 0.5),
        )
        
        # 主行布局
        main_row = ft.Row([
            left_container,
            divider,
            right_container,
        ], height=card_height, spacing=0, vertical_alignment=ft.CrossAxisAlignment.CENTER, expand=True if width is None else False)
        
        # 卡片容器
        container = CardContainer.create(
            config=config,
            content=main_row,
            height=card_height,
            width=width,
            padding=card_padding,
        )
        container.clip_behavior = ft.ClipBehavior.NONE
        
        def handle_switch_toggle():
            """处理开关切换"""
            new_state = not switch_state[0]
            switch_state[0] = new_state
            is_enabled[0] = new_state
            
            if on_save:
                on_save("enabled", new_state)
            
            update_card_state()
        
        def update_card_state():
            """更新卡片状态"""
            if switch_state[0]:
                container.opacity = 1.0
                subtitle_text.color = theme_colors.get("text_secondary")
                icon_control.opacity = 1.0
                title_text.opacity = 1.0
                
                # 启用所有控件
                for control_instance in control_dict.values():
                    if hasattr(control_instance, 'set_enabled'):
                        control_instance.set_enabled(True)
            else:
                container.opacity = 0.5
                subtitle_text.color = theme_colors.get("text_disabled", "#888888")
                icon_control.opacity = 0.4
                title_text.opacity = 0.4
                
                # 禁用所有控件
                for control_instance in control_dict.values():
                    if hasattr(control_instance, 'set_enabled'):
                        control_instance.set_enabled(False)
            
            try:
                if container.page:
                    container.page.update()
            except:
                pass
        
        # 左侧点击切换开关状态
        left_container.on_click = lambda e: handle_switch_toggle()
        
        def load_controls():
            """加载控件选项列表"""
            # 加载所有控件的选项列表
            for config_key, control_instance in control_dict.items():
                if hasattr(control_instance, 'set_options') and config_key in options_dict:
                    control_instance.set_options(options_dict[config_key])
            
            try:
                if container.page:
                    container.page.update()
            except:
                pass
        
        def create_controls_from_config() -> List[ft.Control]:
            """根据配置创建控件"""
            from 前端.游戏设置界面.表示层.组件.基础.下拉框 import Dropdown, USER_WIDTH as DROPDOWN_WIDTH
            from 前端.游戏设置界面.表示层.组件.基础.输入框 import InputBox, USER_WIDTH as INPUT_WIDTH
            
            created_controls = []
            
            for control_config_item in (controls_config or []):
                if control_config_item.get("type") == "dropdown":
                    config_key = control_config_item.get("config_key", "")
                    label = control_config_item.get("label", "")
                    options = control_config_item.get("options", [])
                    value = control_config_item.get("value", options[0] if options else "")
                    control_width = control_config_item.get("width", DROPDOWN_WIDTH)
                    
                    current_values[config_key] = value
                    initial_values[config_key] = value
                    options_dict[config_key] = options
                    
                    label_text = ft.Text(
                        label,
                        size=14,
                        color=theme_colors.get("text_secondary"),
                    )
                    
                    # 创建下拉框,直接传入完整选项列表
                    dropdown_instance = Dropdown.create(
                        options=options,
                        current_value=value,
                        width=control_width,
                        enabled=is_enabled[0],
                        on_change=lambda v, k=config_key: handle_value_change(k, v),
                        config=config,
                    )
                    control_dict[config_key] = dropdown_instance
                    
                    single_control = ft.Row([
                        label_text,
                        dropdown_instance,
                    ], spacing=4, vertical_alignment=ft.CrossAxisAlignment.CENTER)
                    
                    created_controls.append(single_control)
                
                elif control_config_item.get("type") == "input":
                    config_key = control_config_item.get("config_key", "")
                    label = control_config_item.get("label", "")
                    value = control_config_item.get("value", "")
                    hint = control_config_item.get("hint", "")
                    control_width = control_config_item.get("width", INPUT_WIDTH)
                    
                    current_values[config_key] = value
                    initial_values[config_key] = value
                    
                    label_text = ft.Text(
                        label,
                        size=14,
                        color=theme_colors.get("text_secondary"),
                    )
                    
                    input_instance = InputBox.create(
                        config=config,
                        hint_text=hint,
                        value=value,
                        width=control_width,
                        enabled=is_enabled[0],
                        on_change=lambda v, k=config_key: handle_value_change(k, v),
                    )
                    control_dict[config_key] = input_instance
                    
                    single_control = ft.Row([
                        label_text,
                        input_instance,
                    ], spacing=4, vertical_alignment=ft.CrossAxisAlignment.CENTER)
                    
                    created_controls.append(single_control)
            
            return created_controls
        
        def layout_controls(control_list: List[ft.Control]):
            """布局控件"""
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
        
        def handle_value_change(config_key: str, value: Any):
            """处理值变更"""
            current_values[config_key] = value
            
            if initial_values.get(config_key) != value:
                if on_value_change:
                    on_value_change(config_key, value)
                
                if on_save:
                    on_save(config_key, value)
        
        def unload_options():
            """卸载控件选项列表"""
            for control_instance in control_dict.values():
                if hasattr(control_instance, 'unload_options'):
                    control_instance.unload_options()
        
        def get_values() -> Dict[str, str]:
            """获取所有控件的值"""
            for key, control_instance in control_dict.items():
                if hasattr(control_instance, 'get_value'):
                    current_values[key] = control_instance.get_value()
            return current_values.copy()
        
        def set_values(value_dict: Dict[str, str]):
            """设置控件的值"""
            for key, value in value_dict.items():
                if key in control_dict:
                    control_instance = control_dict[key]
                    if hasattr(control_instance, 'set_value'):
                        control_instance.set_value(value)
                    current_values[key] = value
                    initial_values[key] = value
        
        def get_switch_state() -> bool:
            """获取开关状态"""
            return switch_state[0]
        
        def set_switch_state(state: bool):
            """设置开关状态"""
            switch_state[0] = state
            is_enabled[0] = state
            update_card_state()
        
        def is_loaded() -> bool:
            """检查控件是否有选项列表"""
            return any(hasattr(c, 'unload_options') for c in control_dict.values())
        
        def destroy_controls():
            """销毁控件"""
            unload_options()
        
        # 添加方法到容器
        container.get_values = get_values
        container.set_values = set_values
        container.load_controls = load_controls
        container.is_loaded = is_loaded
        container.get_switch_state = get_switch_state
        container.set_switch_state = set_switch_state
        container.destroy_controls = destroy_controls
        container.unload_options_only = unload_options
        
        def set_subtitle(new_subtitle: str):
            """设置副标题"""
            subtitle_text.value = new_subtitle
            try:
                if container.page:
                    container.page.update()
            except:
                pass
        
        container.set_subtitle = set_subtitle
        
        # 创建控件
        if controls is not None:
            # 直接使用传入的控件
            layout_controls(controls)
        elif controls_config is not None:
            # 从配置创建控件
            final_control_list = create_controls_from_config()
            if final_control_list:
                layout_controls(final_control_list)
        
        update_card_state()
        
        return container


# *** 标准测试格式: 仅调用被测模块,AI不得添加数据 ***
if __name__ == "__main__":
    def main(page: ft.Page):
        config = UIConfig()
        card = SwitchableCard.create(
            title="测试卡片",
            icon="SETTINGS",
            subtitle="这是测试卡片",
            config=config,
        )
        page.add(card)
    
    ft.app(target=main)
