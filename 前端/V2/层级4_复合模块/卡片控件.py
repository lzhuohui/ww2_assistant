# -*- coding: utf-8 -*-

"""
模块名称：卡片控件.py
模块功能：卡片控件组件，创建和管理控件

实现步骤：
- 创建下拉框实例
- 创建输入框实例
- 创建控件
- 布局控件
- 提供dropdown属性

职责：
- 创建下拉框
- 创建输入框
- 控件排列逻辑
- 提供dropdown属性
- 从配置服务获取UI配置

不负责：
- 开关逻辑
- 卡片布局
- 数据获取（由下拉框/输入框模块自己获取）

设计原则（符合V2版本模块化设计补充共识）：
- 从配置服务获取UI配置
- 定义DEFAULT_XXX作为fallback
"""

import flet as ft
from typing import Callable, Dict, List, Optional, Any

from 前端.V2.层级5_基础模块.下拉框 import Dropdown
from 前端.V2.层级5_基础模块.输入框 import InputBox
from 前端.V2.层级5_基础模块.标签 import Label
from 前端.V2.层级5_基础模块.卡片容器 import CardContainer

# ============================================
# 默认配置（fallback，用于模块独立测试）
# ============================================

DEFAULT_CONTROLS_PER_ROW = 6
DEFAULT_CONTROL_H_SPACING = 12
DEFAULT_CONTROL_V_SPACING = 8
DEFAULT_CONTROL_RIGHT_MARGIN = 16

# ============================================
# 公开接口
# ============================================

class CardControls:
    """
    卡片控件（层级4：复合模块）
    
    职责：
    - 创建下拉框
    - 创建输入框
    - 控件排列逻辑
    - 提供dropdown属性
    - 从配置服务获取UI配置
    
    不负责：
    - 开关逻辑
    - 卡片布局
    - 数据获取（由下拉框/输入框模块自己获取）
    """
    
    _config_service = None
    
    @classmethod
    def set_config_service(cls, config_service):
        """设置配置服务实例"""
        cls._config_service = config_service
    
    @staticmethod
    def get_controls_per_row() -> int:
        """获取每行控件数（从配置服务获取）"""
        if CardControls._config_service:
            return CardControls._config_service.get_ui_config("控件布局", "每行控件数", DEFAULT_CONTROLS_PER_ROW)
        return DEFAULT_CONTROLS_PER_ROW
    
    @staticmethod
    def get_h_spacing() -> int:
        """获取控件水平间距（从配置服务获取）"""
        if CardControls._config_service:
            return CardControls._config_service.get_ui_config("控件布局", "水平间距", DEFAULT_CONTROL_H_SPACING)
        return DEFAULT_CONTROL_H_SPACING
    
    @staticmethod
    def get_v_spacing() -> int:
        """获取控件垂直间距（从配置服务获取）"""
        if CardControls._config_service:
            return CardControls._config_service.get_ui_config("控件布局", "垂直间距", DEFAULT_CONTROL_V_SPACING)
        return DEFAULT_CONTROL_V_SPACING
    
    @staticmethod
    def get_right_margin() -> int:
        """获取控件区右边距（从配置服务获取）"""
        if CardControls._config_service:
            return CardControls._config_service.get_ui_config("控件布局", "右边距", DEFAULT_CONTROL_RIGHT_MARGIN)
        return DEFAULT_CONTROL_RIGHT_MARGIN
    
    @staticmethod
    def calculate_control_rows(control_count: int) -> int:
        """
        计算控件行数
        
        参数：
        - control_count: 控件数量
        
        返回：
        - 控件行数
        """
        if control_count <= 0:
            return 0
        per_row = CardControls.get_controls_per_row()
        return (control_count + per_row - 1) // per_row
    
    def __init__(self, page: ft.Page, config_service):
        self._page = page
        self._config_service = config_service
        
        # 设置配置服务到基础模块
        if config_service:
            Dropdown.set_config_service(config_service)
            InputBox.set_config_service(config_service)
            CardControls.set_config_service(config_service)
        
        self._dropdown = Dropdown(page, config_service)
        self._input_box = InputBox(page, config_service)
    
    @property
    def dropdown(self) -> Dropdown:
        """提供下拉框实例访问（用于销毁）"""
        return self._dropdown
    
    def create(
        self,
        section: str,
        controls_config: List[Dict[str, Any]],
        on_change: Callable[[str, str, Any], None],
        theme_colors: Dict[str, str],
        controls_per_row: int = None,
    ) -> ft.Container:
        """
        创建控件区
        
        参数：
        - section: 配置节
        - controls_config: 控件配置列表
        - on_change: 值变更回调
        - theme_colors: 主题颜色
        - controls_per_row: 每行控件数（可选，默认从配置服务获取）
        
        注意：数据（enabled状态、选项列表、当前值、宽度）由模块自己从config_service获取
        """
        enabled = self._get_enabled(section)
        controls = self._create_controls(section, controls_config, enabled, on_change, theme_colors)
        
        v_spacing = self.get_v_spacing()
        controls_column = ft.Column([], spacing=v_spacing, alignment=ft.MainAxisAlignment.CENTER)
        self._layout_controls(controls_column, controls, controls_per_row)
        
        return ft.Container(
            content=controls_column,
            expand=True,
            padding=ft.Padding(16, 0, 16, 0),
        )
    
    def _create_controls(
        self,
        section: str,
        controls_config: List[Dict[str, Any]],
        enabled: bool,
        on_change: Callable,
        theme_colors: Dict[str, str],
    ) -> List[ft.Control]:
        """创建控件列表"""
        created_controls = []
        
        for config in controls_config:
            control_type = config.get("type", "dropdown")
            control_id = config.get("id", "")
            label = config.get("label", "")
            
            if control_type == "dropdown":
                control = self._create_dropdown_control(section, control_id, label, enabled, on_change, theme_colors)
            elif control_type == "input":
                control = self._create_input_control(section, control_id, label, config, enabled, on_change, theme_colors)
            else:
                continue
            
            created_controls.append(control)
        
        return created_controls
    
    def _create_dropdown_control(
        self,
        section: str,
        control_id: str,
        label: str,
        enabled: bool,
        on_change: Callable,
        theme_colors: Dict[str, str],
    ) -> ft.Row:
        """
        创建下拉框控件
        
        注意：选项列表、当前值、宽度由下拉框模块自己从config_service获取
        """
        dropdown_container = self._dropdown.create(
            section=section,
            control_id=control_id,
            enabled=enabled,
            on_change=on_change,
            theme_colors=theme_colors,
        )
        
        label_text = Label.create(
            text=label,
            size=14,
            color_type="secondary",
            theme_colors=theme_colors,
        )
        
        return ft.Row([label_text, dropdown_container], spacing=4, vertical_alignment=ft.CrossAxisAlignment.CENTER)
    
    def _create_input_control(
        self,
        section: str,
        control_id: str,
        label: str,
        config: Dict[str, Any],
        enabled: bool,
        on_change: Callable,
        theme_colors: Dict[str, str],
    ) -> ft.Row:
        """
        创建输入框控件
        
        注意：当前值由输入框模块自己从config_service获取
        """
        hint = config.get("hint", "")
        password_mode = config.get("password", False)
        max_length = config.get("max_length", None)
        
        input_field = self._input_box.create(
            section=section,
            control_id=control_id,
            hint_text=hint,
            enabled=enabled,
            password_mode=password_mode,
            max_length=max_length,
            on_change=on_change,
            theme_colors=theme_colors,
        )
        
        label_text = Label.create(
            text=label,
            size=14,
            color_type="secondary",
            theme_colors=theme_colors,
        )
        
        return ft.Row([label_text, input_field], spacing=4, vertical_alignment=ft.CrossAxisAlignment.CENTER)
    
    def _layout_controls(self, controls_column: ft.Column, controls: List[ft.Control], controls_per_row: int = None):
        """布局控件"""
        per_row = controls_per_row if controls_per_row is not None else self.get_controls_per_row()
        h_spacing = self.get_h_spacing()
        
        row_list = []
        current_row_controls = []
        current_row_count = 0
        
        for i, control in enumerate(controls):
            # 检查是否需要强制换行（通过controls_config中的row_break标记）
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
        """从配置服务获取开关状态（模块内部逻辑）"""
        if self._config_service:
            return self._config_service.get_enabled(section, True)
        return True

# *** 标准测试格式: 仅调用被测模块,AI不得添加数据 ***
if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    
    from 前端.V2.数据层.仓库.配置仓库 import ConfigRepository
    from 前端.V2.业务层.服务.配置服务 import ConfigService
    
    def main(page: ft.Page):
        page.title = "卡片控件测试"
        
        print("=" * 50)
        print("测试: 使用真实配置服务")
        print("=" * 50)
        
        repository = ConfigRepository()
        config_service = ConfigService(repository)
        
        card_controls = CardControls(page, config_service)
        
        print(f"每行控件数: {CardControls.get_controls_per_row()}")
        print(f"水平间距: {CardControls.get_h_spacing()}")
        print(f"垂直间距: {CardControls.get_v_spacing()}")
        
        theme_colors = config_service.get_theme_colors()
        
        controls_config = [
            {"id": "城市等级", "type": "dropdown", "label": "城市"},
            {"id": "兵工厂等级", "type": "dropdown", "label": "兵工"},
        ]
        
        controls_area = card_controls.create(
            section="建筑设置.主帅主城",
            controls_config=controls_config,
            on_change=lambda s, k, v: print(f"变更: {s}.{k} = {v}"),
            theme_colors=theme_colors,
        )
        
        page.add(ft.Column([
            ft.Text("卡片控件测试", size=20, weight=ft.FontWeight.BOLD),
            controls_area,
        ]))

ft.app(target=main)
