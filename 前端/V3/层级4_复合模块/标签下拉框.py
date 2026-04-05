# -*- coding: utf-8 -*-

"""
模块名称：标签下拉框.py
模块功能：标签+下拉框组合组件

职责：
- 标签 + 下拉框 的组合
- 提供统一的接口

不负责：
- 数据获取（由下拉框模块自己获取）
- 销毁（由下拉框模块负责）
"""

import flet as ft
from typing import Callable, Dict

from 前端.V3.层级0_数据管理.配置管理 import ConfigManager
from 前端.V3.层级5_基础模块.标签 import Label
from 前端.V3.层级5_基础模块.下拉框 import Dropdown


class LabeledDropdown:
    _config_manager: ConfigManager = None
    _dropdown_instance: Dropdown = None
    
    @classmethod
    def set_config_manager(cls, config_manager: ConfigManager):
        cls._config_manager = config_manager
        Label.set_config_manager(config_manager)
        Dropdown.set_config_manager(config_manager)
    
    @staticmethod
    def get_dropdown() -> Dropdown:
        LabeledDropdown._check_config_manager()
        if LabeledDropdown._dropdown_instance is None:
            LabeledDropdown._dropdown_instance = Dropdown(None, LabeledDropdown._config_manager)
        return LabeledDropdown._dropdown_instance
    
    @staticmethod
    def _check_config_manager():
        if LabeledDropdown._config_manager is None:
            raise RuntimeError(
                "LabeledDropdown模块未设置config_manager，"
                "请先调用 LabeledDropdown.set_config_manager(config_manager)"
            )
    
    @staticmethod
    def get_spacing() -> int:
        """获取标签与下拉框间距"""
        LabeledDropdown._check_config_manager()
        spacing = LabeledDropdown._config_manager.get_ui_size("边距", "标签控件间距")
        if spacing is None:
            spacing = 6
        return spacing
    
    @staticmethod
    def create(
        interface: str = "",
        card: str = "",
        control_id: str = "",
        label: str = "",
        enabled: bool = True,
        on_change: Callable[[str, str, str, Dict[str, str]], None] = None,
        label_size: int = None,
        dropdown_width: int = None,
        use_defaults: bool = False,
    ) -> ft.Row:
        """
        创建标签下拉框
        
        参数：
        - interface: 界面名称
        - card: 卡片名称
        - control_id: 控件ID
        - label: 标签文本
        - enabled: 是否启用
        - on_change: 值变更回调
        - label_size: 标签字体大小
        - dropdown_width: 下拉框宽度
        - use_defaults: 是否使用默认值（True时忽略方案值）
        
        返回：
        - ft.Row: 标签+下拉框组合
        """
        LabeledDropdown._check_config_manager()
        
        if LabeledDropdown._dropdown_instance is None:
            LabeledDropdown._dropdown_instance = Dropdown(None, LabeledDropdown._config_manager)
        
        if label_size is None:
            label_size = LabeledDropdown._config_manager.get_ui_size("字体", "正文字体")
        
        label_text = Label.create(
            text=label,
            size=label_size,
            color_type="secondary",
        )
        
        dropdown_container = LabeledDropdown._dropdown_instance.create(
            interface=interface,
            card=card,
            control_id=control_id,
            enabled=enabled,
            on_change=on_change,
            width=dropdown_width,
            use_defaults=use_defaults,
        )
        
        row = ft.Row(
            [label_text, dropdown_container],
            spacing=LabeledDropdown.get_spacing(),
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        
        def set_enabled(is_enabled: bool):
            dropdown_container.set_enabled(is_enabled)
        
        row.set_enabled = set_enabled
        
        return row
