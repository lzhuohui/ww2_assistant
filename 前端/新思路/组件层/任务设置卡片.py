# -*- coding: utf-8 -*-
"""
任务设置卡片 - 组件层（新思路）

设计思路:
    组装零件，构建任务设置卡片。
    采用装配模式，协调各零件交互。
    三级控制：左侧总开关 + 右侧主线/支线独立开关

功能:
    1. 左侧：图标+标题+总开关
    2. 右侧单行：圆形开关 + 主线限级下拉框 + 圆形开关 + 支线限级下拉框

数据来源:
    所有配置数据从配置目录获取。

使用场景:
    被页面层模块调用。

可独立运行调试: python 任务设置卡片.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft
from typing import Callable, Dict, Any
from 配置.界面配置 import 界面配置
from 新思路.组件层.通用卡片 import UniversalCard
from 新思路.零件层.圆形开关 import CircleSwitch
from 新思路.零件层.标签下拉框 import LabelDropdown


class TaskSettingsCard:
    """任务设置卡片 - 组件层"""
    
    # 默认值定义
    默认值 = {
        "开启主线": True,
        "主城等级": "05",
        "开启支线": True,
        "支线主城等级": "10",
    }
    
    @staticmethod
    def create(
        config: 界面配置,
        title: str = "任务设置",
        icon: str = "TASK",
        enabled: bool = True,
        on_state_change: Callable[[bool], None] = None,
        help_text: str = None,
        main_task_enabled: bool = True,
        main_city_level: str = "05",
        side_task_enabled: bool = True,
        side_city_level: str = "10",
        **kwargs
    ) -> ft.Container:
        """
        创建任务设置卡片
        
        参数:
            config: 界面配置对象
            title: 卡片标题
            icon: 图标名称
            enabled: 初始启用状态（左侧总开关）
            on_state_change: 状态变化回调
            help_text: 帮助提示文字
            main_task_enabled: 主线任务开关状态
            main_city_level: 主城等级值
            side_task_enabled: 支线任务开关状态
            side_city_level: 支线主城等级值
        
        返回:
            ft.Container: 任务设置卡片容器
        """
        theme_colors = config.当前主题颜色
        
        # 内部状态
        current_enabled = enabled
        current_main_enabled = main_task_enabled
        current_side_enabled = side_task_enabled
        
        # 主城等级选项 (01-15)
        main_level_options = [f"{i:02d}" for i in range(1, 16)]
        # 支线主城等级选项 (05-15)
        side_level_options = [f"{i:02d}" for i in range(5, 16)]
        
        # 创建主线圆形开关
        main_switch = CircleSwitch.create(
            config=config,
            value=main_task_enabled,
            on_change=lambda v: handle_main_switch_change(v),
        )
        
        # 创建主线限级下拉框
        main_dropdown = LabelDropdown.create(
            config=config,
            label="主线限级",
            options=main_level_options,
            value=main_city_level,
            width=140,
            enabled=current_enabled and current_main_enabled,
        )
        
        # 创建支线圆形开关
        side_switch = CircleSwitch.create(
            config=config,
            value=side_task_enabled,
            on_change=lambda v: handle_side_switch_change(v),
        )
        
        # 创建支线限级下拉框
        side_dropdown = LabelDropdown.create(
            config=config,
            label="支线限级",
            options=side_level_options,
            value=side_city_level,
            width=140,
            enabled=current_enabled and current_side_enabled,
        )
        
        # 创建右侧单行布局
        right_row = ft.Row(
            [
                main_switch,
                main_dropdown,
                ft.Container(width=20),
                side_switch,
                side_dropdown,
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        
        # 处理主线开关变化
        def handle_main_switch_change(new_value: bool):
            nonlocal current_main_enabled
            current_main_enabled = new_value
            update_dropdown_state(main_dropdown, current_enabled and current_main_enabled)
            if on_state_change:
                on_state_change(current_enabled)
        
        # 处理支线开关变化
        def handle_side_switch_change(new_value: bool):
            nonlocal current_side_enabled
            current_side_enabled = new_value
            update_dropdown_state(side_dropdown, current_enabled and current_side_enabled)
            if on_state_change:
                on_state_change(current_enabled)
        
        # 更新下拉框状态
        def update_dropdown_state(dropdown, enabled: bool):
            dropdown.disabled = not enabled
            dropdown.opacity = 1.0 if enabled else 0.4
            dropdown.update()
        
        # 更新所有子控件状态
        def update_children_state(new_enabled: bool):
            main_switch.set_enabled(new_enabled)
            side_switch.set_enabled(new_enabled)
            update_dropdown_state(main_dropdown, new_enabled and current_main_enabled)
            update_dropdown_state(side_dropdown, new_enabled and current_side_enabled)
        
        # 处理总开关状态变化
        def handle_total_state_change(new_enabled: bool):
            nonlocal current_enabled
            current_enabled = new_enabled
            update_children_state(new_enabled)
            if on_state_change:
                on_state_change(new_enabled)
        
        # 调用通用卡片组件
        card = UniversalCard.create(
            config=config,
            title=title,
            icon=icon,
            enabled=enabled,
            on_state_change=handle_total_state_change,
            help_text=help_text,
            controls=[right_row],
        )
        
        # 暴露控制接口
        def get_main_task_enabled() -> bool:
            return current_main_enabled
        
        def get_side_task_enabled() -> bool:
            return current_side_enabled
        
        def get_main_city_level() -> str:
            return main_dropdown.get_value()
        
        def get_side_city_level() -> str:
            return side_dropdown.get_value()
        
        def get_all_values() -> Dict[str, Any]:
            return {
                "开启主线": current_main_enabled,
                "主城等级": main_dropdown.get_value(),
                "开启支线": current_side_enabled,
                "支线主城等级": side_dropdown.get_value(),
            }
        
        def get_effective_values() -> Dict[str, Any]:
            """获取有效值（总开关开启时返回当前值，关闭时返回默认值）"""
            if card.get_state():
                return get_all_values()
            else:
                return TaskSettingsCard.默认值.copy()
        
        card.get_main_task_enabled = get_main_task_enabled
        card.get_side_task_enabled = get_side_task_enabled
        card.get_main_city_level = get_main_city_level
        card.get_side_city_level = get_side_city_level
        card.get_all_values = get_all_values
        card.get_effective_values = get_effective_values
        
        return card


# 兼容别名
任务设置卡片 = TaskSettingsCard


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    # 1. 界面配置初始化
    配置 = 界面配置()
    
    # 2. 自动加载用户数据覆盖默认值（在界面配置.__init__中自动完成）
    
    # 3. 正常启动被测模块
    def main(page: ft.Page):
        page.padding = 20
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        
        page.add(TaskSettingsCard.create(
            配置,
            title="任务设置",
            icon="TASK",
            enabled=True,
            main_task_enabled=True,
            main_city_level="05",
            side_task_enabled=True,
            side_city_level="10",
        ))
    
    ft.run(main)
