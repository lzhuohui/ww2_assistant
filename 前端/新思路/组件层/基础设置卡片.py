# -*- coding: utf-8 -*-
"""
基础设置卡片 - 组件层（新思路）

设计思路:
    组装零件，构建基础设置卡片。
    采用装配模式，协调各零件交互。
    使用通用卡片组件，保持统一风格。

功能:
    1. 调用通用卡片组件
    2. 在右侧放置标签下拉框/标签输入框
    3. 支持动态添加设置项

数据来源:
    所有配置数据从配置目录获取。

使用场景:
    被页面层模块调用。

可独立运行调试: python 基础设置卡片.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft
from typing import Callable, List, Dict, Any
from 配置.界面配置 import 界面配置
from 新思路.组件层.通用卡片 import UniversalCard
from 新思路.零件层.标签下拉框 import LabelDropdown
from 新思路.零件层.标签输入框 import LabelInput


class BasicSettingsCard:
    """基础设置卡片 - 组件层"""
    
    @staticmethod
    def create(
        config: 界面配置,
        title: str = "基础设置",
        icon: str = "SETTINGS",
        enabled: bool = True,
        on_state_change: Callable[[bool], None] = None,
        help_text: str = None,
        settings: List[Dict[str, Any]] = None,
        **kwargs
    ) -> ft.Container:
        """
        创建基础设置卡片
        
        参数:
            config: 界面配置对象
            title: 卡片标题
            icon: 图标名称
            enabled: 初始启用状态
            on_state_change: 状态变化回调
            help_text: 帮助提示文字
            settings: 设置项列表
                [
                    {"type": "dropdown", "label": "挂机模式", "options": [...], "value": "...", "on_change": ...},
                    {"type": "input", "label": "尝试次数", "value": "3", "on_change": ...},
                ]
        
        返回:
            ft.Container: 基础设置卡片容器
        """
        # 默认设置项
        default_settings = []
        current_settings = settings if settings else default_settings
        
        # 创建设置项列表
        controls = []
        settings_refs = {}  # 存储控件引用，便于后续访问
        
        for i, setting in enumerate(current_settings):
            setting_type = setting.get("type", "input")
            label = setting.get("label", f"设置项{i+1}")
            value = setting.get("value", "")
            width = setting.get("width", 150)
            on_change = setting.get("on_change", None)
            
            if setting_type == "dropdown":
                options = setting.get("options", [])
                control = LabelDropdown.create(
                    config=config,
                    label=label,
                    options=options,
                    value=value or (options[0] if options else ""),
                    width=width,
                    on_change=on_change,
                )
            else:  # input
                control = LabelInput.create(
                    config=config,
                    label=label,
                    value=value,
                    width=width,
                    on_change=on_change,
                )
            
            controls.append(control)
            settings_refs[label] = control
        
        # 调用通用卡片组件（高度自动计算）
        card = UniversalCard.create(
            config=config,
            title=title,
            icon=icon,
            enabled=enabled,
            on_state_change=on_state_change,
            help_text=help_text,
            controls=controls,
        )
        
        # 暴露控制接口
        def get_value(label: str) -> str:
            """获取指定设置项的值"""
            if label in settings_refs:
                return settings_refs[label].get_value()
            return None
        
        def set_value(label: str, value: str):
            """设置指定设置项的值"""
            if label in settings_refs:
                settings_refs[label].set_value(value)
        
        def get_all_values() -> Dict[str, str]:
            """获取所有设置项的值"""
            return {label: control.get_value() for label, control in settings_refs.items()}
        
        card.get_value = get_value
        card.set_value = set_value
        card.get_all_values = get_all_values
        
        return card


# 兼容别名
基础设置卡片 = BasicSettingsCard


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    # 1. 界面配置初始化
    配置 = 界面配置()
    
    # 2. 自动加载用户数据覆盖默认值（在界面配置.__init__中自动完成）
    
    # 3. 正常启动被测模块
    def main(page: ft.Page):
        page.padding = 20
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        
        # 创建基础设置卡片
        settings = [
            {"type": "dropdown", "label": "挂机模式", "options": ["自动挂机", "手动挂机", "半自动挂机"], "value": "自动挂机"},
            {"type": "dropdown", "label": "指令速度", "options": ["快速", "正常", "慢速"], "value": "正常"},
            {"type": "input", "label": "尝试次数", "value": "3"},
            {"type": "input", "label": "清换限量", "value": "100"},
        ]
        page.add(BasicSettingsCard.create(配置, title="基础设置", settings=settings))  # 只能更改此处**被测调用模块名称**
    
    ft.run(main)
