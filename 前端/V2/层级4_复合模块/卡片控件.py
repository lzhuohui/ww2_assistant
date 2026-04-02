# -*- coding: utf-8 -*-

"""
模块名称：卡片控件.py
模块功能：卡片控件组件，创建和管理控件

实现步骤：
- 创建标签下拉框实例
- 创建输入框实例
- 创建控件
- 布局控件
- 提供dropdown属性

职责：
- 创建标签下拉框
- 创建输入框
- 控件排列逻辑
- 控件高度和间距
- 提供dropdown属性
- 从配置服务获取UI配置、控件列表

不负责：
- 开关逻辑
- 卡片布局
- 卡片容器

设计原则（符合V2版本模块化设计补充共识）：
- 不调用卡片容器，只返回右侧控件区内容
- 尺寸配置直接从用户偏好.json获取
- 控件高度和间距由本模块管理
"""

import flet as ft
from typing import Callable, Dict, List, Optional, Any

from 前端.V2.层级5_基础模块.标签下拉框 import LabeledDropdown
from 前端.V2.层级5_基础模块.输入框 import InputBox

# ============================================
# 数据和文件接口（前置，方便查看和修改）
# ============================================

# ============================================
# 公开接口
# ============================================

class CardControls:
    """
    卡片控件（层级4：复合模块）
    
    职责：
    - 创建标签下拉框
    - 创建输入框
    - 控件排列逻辑
    - 控件高度和间距
    - 提供dropdown属性
    - 从配置服务获取UI配置、控件列表
    
    不负责：
    - 开关逻辑
    - 卡片布局
    - 卡片容器
    """
    
    _config_service = None
    
    @classmethod
    def set_config_service(cls, config_service):
        """设置配置服务实例"""
        cls._config_service = config_service
        LabeledDropdown.set_config_service(config_service)
        InputBox.set_config_service(config_service)
    
    @staticmethod
    def _check_config_service():
        """检查配置服务是否已设置"""
        if CardControls._config_service is None:
            raise RuntimeError(
                "CardControls模块未设置config_service，"
                "请先调用 CardControls.set_config_service(config_service)"
            )
    
    @staticmethod
    def get_controls_per_row() -> int:
        """获取每行控件数（从用户偏好.json获取）"""
        CardControls._check_config_service()
        value = CardControls._config_service.get_ui_config("控件布局", "每行控件数")
        if value is None:
            raise RuntimeError("用户偏好.json缺少配置: 控件布局.每行控件数")
        return value
    
    @staticmethod
    def get_h_spacing() -> int:
        """获取控件水平间距（从用户偏好.json获取）"""
        CardControls._check_config_service()
        value = CardControls._config_service.get_ui_config("控件布局", "水平间距")
        if value is None:
            raise RuntimeError("用户偏好.json缺少配置: 控件布局.水平间距")
        return value
    
    @staticmethod
    def get_v_spacing() -> int:
        """获取控件垂直间距（从用户偏好.json获取）"""
        CardControls._check_config_service()
        value = CardControls._config_service.get_ui_config("控件布局", "垂直间距")
        if value is None:
            raise RuntimeError("用户偏好.json缺少配置: 控件布局.垂直间距")
        return value
    
    @staticmethod
    def get_right_margin() -> int:
        """获取控件区右边距（从用户偏好.json获取）"""
        CardControls._check_config_service()
        value = CardControls._config_service.get_ui_config("控件布局", "右边距")
        if value is None:
            raise RuntimeError("用户偏好.json缺少配置: 控件布局.右边距")
        return value
    
    
    def __init__(self, page: ft.Page, config_service=None):
        self._page = page
        self._config_service = config_service or CardControls._config_service
        self._input_box = InputBox(page, self._config_service)
        self._controls_cache: Dict[str, ft.Control] = {}
    
    @property
    def dropdown(self):
        """提供下拉框实例访问（用于销毁）- 通过公开接口"""
        return LabeledDropdown.get_dropdown()
    
    def create(
        self,
        section: str,
        on_change: Callable[[str, str, Any], None] = None,
        theme_colors: Dict[str, str] = None,
    ) -> ft.Control:
        """
        创建控件区（不包装容器）
        
        参数：
        - section: 配置节
        - on_change: 值变更回调
        - theme_colors: 主题颜色（可选，不传则从配置服务获取）
        
        返回：
        - ft.Control: 右侧控件区内容（Column）
        
        注意：
        - enabled状态、控件列表由模块自己从config_service获取
        - 布局值（下拉框宽度、每行控件数）按优先级从配置获取：
          控件列表 > 卡片信息 > 界面布局 > 默认值
        """
        if self._config_service is None:
            raise RuntimeError("CardControls模块未设置config_service，请先调用CardControls.set_config_service()")
        
        enabled = self._get_enabled(section)
        controls_config = self._get_controls(section)
        
        controls = self._create_controls(section, controls_config, enabled, on_change)
        
        v_spacing = self.get_v_spacing()
        controls_column = ft.Column([], spacing=v_spacing, alignment=ft.MainAxisAlignment.CENTER)
        self._layout_controls(section, controls_column, controls)
        
        self._controls_cache[section] = controls_column
        
        container = ft.Container(
            content=controls_column,
            alignment=ft.alignment.Alignment(0, 0),
            opacity=1.0 if enabled else 0.5,
        )
        
        def set_opacity(opacity: float):
            container.opacity = opacity
        
        def set_enabled(state: bool):
            container.opacity = 1.0 if state else 0.5
            for row in controls_column.controls:
                if hasattr(row, 'controls'):
                    for ctrl in row.controls:
                        if hasattr(ctrl, 'set_enabled'):
                            ctrl.set_enabled(state)
        
        container.set_opacity = set_opacity
        container.set_enabled = set_enabled
        
        return container
    
    def _create_controls(
        self,
        section: str,
        controls_config: List[Dict[str, Any]],
        enabled: bool,
        on_change: Callable,
    ) -> List[ft.Control]:
        """创建控件列表"""
        created_controls = []
        
        for config in controls_config:
            control_type = config.get("type", "dropdown")
            control_id = config.get("id", "")
            label = config.get("label", "")
            
            if control_type == "dropdown":
                width = self._config_service.get_layout_value(section, "下拉框宽度", control_id)
                control = LabeledDropdown.create(
                    section=section,
                    control_id=control_id,
                    label=label,
                    enabled=enabled,
                    on_change=on_change,
                    dropdown_width=width,
                )
            elif control_type == "input":
                control = self._create_input_control(section, control_id, config, enabled, on_change)
            else:
                continue
            
            created_controls.append(control)
        
        return created_controls
    
    def _create_input_control(
        self,
        section: str,
        control_id: str,
        config: Dict[str, Any],
        enabled: bool,
        on_change: Callable,
    ) -> ft.Control:
        """创建输入框控件（无标签）"""
        hint = config.get("hint", "")
        password_mode = config.get("password", False)
        max_length = config.get("max_length", None)
        
        return self._input_box.create(
            section=section,
            control_id=control_id,
            hint_text=hint,
            enabled=enabled,
            password_mode=password_mode,
            max_length=max_length,
            on_change=on_change,
        )
    
    def _layout_controls(self, section: str, controls_column: ft.Column, controls: List[ft.Control]):
        """布局控件"""
        per_row = self._config_service.get_layout_value(section, "每行控件数")
        h_spacing = self.get_h_spacing()
        
        row_list = []
        current_row_controls = []
        current_row_count = 0
        
        for i, control in enumerate(controls):
            need_break = False
            if i < len(controls) and hasattr(control, 'data') and control.data:
                need_break = control.data.get('row_break', False)
            
            if (current_row_count >= per_row and current_row_controls) or need_break:
                row_list.append(ft.Row(current_row_controls, spacing=h_spacing, vertical_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.END))
                current_row_controls = []
                current_row_count = 0
            
            current_row_controls.append(control)
            current_row_count += 1
        
        if current_row_controls:
            row_list.append(ft.Row(current_row_controls, spacing=h_spacing, vertical_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.END))
        
        controls_column.controls = row_list
    
    def _get_enabled(self, section: str) -> bool:
        """从配置服务获取开关状态"""
        return self._config_service.get_enabled(section, True)
    
    def _get_controls(self, section: str) -> List[Dict[str, Any]]:
        """从配置服务获取控件列表"""
        return self._config_service.get_controls(section)
    
    def get_all_values(self, section: str) -> Dict[str, Any]:
        """获取指定section所有控件的值"""
        values = {}
        controls_config = self._get_controls(section)
        for config in controls_config:
            control_id = config.get("id", "")
            control_type = config.get("type", "dropdown")
            
            if control_type == "dropdown":
                values[control_id] = self.dropdown.get_value(section, control_id)
            elif control_type == "input":
                values[control_id] = self._input_box.get_value(section, control_id)
        
        return values

# *** 标准测试格式: 仅调用被测模块,AI不得添加数据 ***
if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    
    from 前端.V2.业务层.服务.配置服务 import ConfigService
    
    def main(page: ft.Page):
        page.title = "卡片控件测试"
        
        config_service = ConfigService()
        CardControls.set_config_service(config_service)
        
        card_controls = CardControls(page, config_service)
        
        print(f"每行控件数: {CardControls.get_controls_per_row()}")
        print(f"水平间距: {CardControls.get_h_spacing()}")
        print(f"垂直间距: {CardControls.get_v_spacing()}")
        
        controls_area = card_controls.create(
            section="建筑设置.主帅主城",
            on_change=lambda s, k, v: print(f"变更: {s}.{k} = {v}"),
        )
        
        page.add(ft.Column([
            ft.Text("卡片控件测试", size=20, weight=ft.FontWeight.BOLD),
            ft.Container(content=controls_area, expand=True),
        ]))
    
    ft.run(main)
