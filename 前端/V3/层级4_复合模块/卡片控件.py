# -*- coding: utf-8 -*-

"""
模块名称：卡片控件.py
模块功能：卡片控件区组件，管理卡片内的控件布局

职责：
- 创建控件（下拉框、输入框）
- 控件布局排列
- 从配置管理获取布局配置

不负责：
- 卡片标题和开关
- 数据存储
"""

import flet as ft
from typing import Callable, Dict, List

from 前端.V3.层级0_数据管理.配置管理 import ConfigManager
from 前端.V3.层级4_复合模块.标签下拉框 import LabeledDropdown
from 前端.V3.层级5_基础模块.输入框 import InputBox


class CardControls:
    """
    卡片控件 - V3版本
    
    职责：
    - 创建控件（下拉框、输入框）
    - 控件布局排列
    - 从配置管理获取布局配置
    
    不负责：
    - 卡片标题和开关
    - 数据存储
    """
    
    _config_manager: ConfigManager = None
    
    @classmethod
    def set_config_manager(cls, config_manager: ConfigManager):
        """设置配置管理实例"""
        cls._config_manager = config_manager
        LabeledDropdown.set_config_manager(config_manager)
        InputBox.set_config_manager(config_manager)
    
    @staticmethod
    def _check_config_manager():
        """检查配置管理是否已设置"""
        if CardControls._config_manager is None:
            raise RuntimeError(
                "CardControls模块未设置config_manager，"
                "请先调用 CardControls.set_config_manager(config_manager)"
            )
    
    @staticmethod
    def get_controls_per_row() -> int:
        """获取每行控件数（从用户偏好.yaml获取）"""
        CardControls._check_config_manager()
        value = CardControls._config_manager.get_ui_config("控件布局", "每行控件数")
        if value is None:
            value = 6
        return value
    
    @staticmethod
    def get_spacing() -> int:
        """获取控件间距（从用户偏好.yaml获取）"""
        CardControls._check_config_manager()
        value = CardControls._config_manager.get_ui_config("控件布局", "控件间距")
        if value is None:
            value = 6
        return value
    
    @staticmethod
    def get_right_margin() -> int:
        """获取控件区右边距（从用户偏好.yaml获取）"""
        CardControls._check_config_manager()
        value = CardControls._config_manager.get_ui_config("控件布局", "右边距")
        if value is None:
            value = 8
        return value
    
    def __init__(self, page: ft.Page, config_manager: ConfigManager = None):
        self._page = page
        self._config_manager = config_manager or CardControls._config_manager
        self._input_box = InputBox(page, self._config_manager)
        self._controls_cache: Dict[str, ft.Control] = {}
        self._controls_list: List[ft.Control] = []
        self._container: ft.Container = None
        self._enabled: bool = True
    
    @property
    def dropdown(self):
        """提供下拉框实例访问（用于销毁）"""
        return LabeledDropdown.get_dropdown()
    
    def create(
        self,
        interface: str,
        card: str,
        on_change: Callable[[str, str, str], None] = None,
        theme_colors: Dict[str, str] = None,
    ) -> ft.Control:
        """
        创建卡片控件区
        
        参数：
        - interface: 界面名称
        - card: 卡片名称
        - on_change: 值变更回调
        - theme_colors: 主题颜色
        
        返回：
        - ft.Control: 控件区内容
        """
        controls_config = self._get_controls_config(interface, card)
        enabled = self._get_enabled(interface, card)
        
        if not controls_config:
            return ft.Container()
        
        self._enabled = enabled
        
        controls_column = ft.Column(
            spacing=self.get_spacing(),
            alignment=ft.MainAxisAlignment.CENTER,
        )
        
        controls = self._create_controls(
            interface, card, controls_config, enabled, on_change, theme_colors
        )
        
        self._layout_controls(interface, card, controls_column, controls)
        
        self._container = ft.Container(
            content=controls_column,
        )
        
        return self._container
    
    def _get_controls_config(self, interface: str, card: str) -> List[Dict]:
        """获取控件配置"""
        if self._config_manager:
            return self._config_manager.get_controls(interface, card)
        return []
    
    def _get_enabled(self, interface: str, card: str) -> bool:
        """获取卡片开关状态"""
        if self._config_manager:
            return self._config_manager.get_enabled(interface, card)
        return True
    
    def _create_controls(
        self,
        interface: str,
        card: str,
        controls_config: List[Dict],
        enabled: bool,
        on_change: Callable,
        theme_colors: Dict,
    ) -> List[ft.Control]:
        """创建控件列表"""
        controls = []
        
        for config in controls_config:
            control_type = config.get("type", "dropdown")
            control_id = config.get("id", "")
            label = config.get("label", "")
            
            def make_callback(cid):
                def callback(intf, crd, ctrl_id, value):
                    if on_change:
                        on_change(intf, crd, cid, value)
                return callback
            
            if control_type == "dropdown":
                dropdown_width = self._config_manager.get_layout_value(
                    interface, card, "dropdown_width", control_id
                ) if self._config_manager else None
                
                control = LabeledDropdown.create(
                    interface=interface,
                    card=card,
                    control_id=control_id,
                    label=label,
                    enabled=enabled,
                    on_change=make_callback(control_id),
                    dropdown_width=dropdown_width,
                )
            
            elif control_type == "input":
                hint = config.get("hint", "")
                password = config.get("password", False)
                
                input_width = self._config_manager.get_layout_value(
                    interface, card, "input_width", control_id
                ) if self._config_manager else None
                
                control = self._input_box.create(
                    interface=interface,
                    card=card,
                    control_id=control_id,
                    enabled=enabled,
                    hint_text=hint,
                    password_mode=password,
                    width=input_width,
                    on_change=make_callback(control_id),
                )
            
            else:
                continue
            
            controls.append(control)
        
        self._controls_list = controls
        return controls
    
    def _layout_controls(
        self,
        interface: str,
        card: str,
        controls_column: ft.Column,
        controls: List[ft.Control],
    ):
        """布局控件"""
        per_row = self._config_manager.get_layout_value(
            interface, card, "controls_per_row"
        ) if self._config_manager else self.get_controls_per_row()
        
        if per_row is None:
            per_row = self.get_controls_per_row()
        
        spacing = self.get_spacing()
        
        for i in range(0, len(controls), per_row):
            row_controls = controls[i:i + per_row]
            row = ft.Row(
                controls=row_controls,
                spacing=spacing,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.END,
            )
            controls_column.controls.append(row)
    
    def set_enabled(self, enabled: bool):
        """设置所有控件的启用状态（opacity + disabled）"""
        if self._container:
            self._container.opacity = 1.0 if enabled else 0.5
            try:
                self._container.update()
            except:
                pass
        
        for control in self._controls_list:
            if hasattr(control, 'disabled'):
                control.disabled = not enabled
                try:
                    control.update()
                except:
                    pass
