# -*- coding: utf-8 -*-
"""
基础设置卡片 - 组件层（新思路）

设计思路:
    组装零件，构建基础设置卡片。
    采用装配模式，协调各零件交互。
    使用通用卡片组件，保持统一风格。

功能:
    1. 调用通用卡片组件
    2. 在右侧放置标签下拉框
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
from 新思路.组件层.通用卡片 import UniversalCard, DEFAULT_CONTROLS_PER_ROW
from 新思路.零件层.标签下拉框 import LabelDropdown


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
        subtitle: str = None,
        controls_per_row: int = 2,
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
                ]
            subtitle: 副标题（显示在分割线右侧下方）
            controls_per_row: 每行控件数量
        
        返回:
            ft.Container: 基础设置卡片容器
        """
        # 默认设置项（从按键精灵脚本转换）
        default_settings = [
            {"type": "dropdown", "label": "卦机模式:", "options": ["自动", "手动"], "value": "自动"},
            {"type": "dropdown", "label": "指令限速:", "options": ["100", "150", "200", "250", "300", "350", "400", "450", "500"], "value": "100"},
            {"type": "dropdown", "label": "尝试次数:", "options": ["10", "15", "20", "25", "30"], "value": "15"},
            {"type": "dropdown", "label": "清缓限量:", "options": ["1.0", "1.5", "2.0", "2.5", "3.0", "3.5", "4.0", "4.5", "5.0"], "value": "1.0"},
            {"type": "dropdown", "label": "备用平台:", "options": ["Tap", "九游", "Fan", "小7", "Vivo", "Opop"], "value": "Tap"},
        ]
        current_settings = settings if settings else default_settings
        
        # 创建控件列表
        controls = []
        for setting in current_settings:
            setting_type = setting.get("type", "dropdown")
            label = setting.get("label", "")
            value = setting.get("value", "")
            options = setting.get("options", [])
            on_change = setting.get("on_change", None)
            
            if setting_type == "dropdown" and label:
                control = LabelDropdown.create(
                    config=config,
                    label=label,
                    options=options,
                    value=value or (options[0] if options else ""),
                    on_change=on_change,
                    enabled=enabled,
                )
                controls.append(control)
        
        # 调用通用卡片组件（只传递数据，不覆盖布局参数）
        card = UniversalCard.create(
            config=config,
            title=title,
            icon=icon,
            enabled=enabled,
            on_state_change=on_state_change,
            help_text=help_text,
            controls=controls,
            subtitle=subtitle if subtitle else "通用配置描述",
            controls_per_row=controls_per_row,
        )
        
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
        page.padding = 0
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        page.add(BasicSettingsCard.create(配置))  # 只能更改此处**被测调用模块名称**
    
    ft.run(main)
