# -*- coding: utf-8 -*-

"""
模块名称：标签下拉框.py
模块功能：标签+下拉框组合组件

实现步骤：
- 创建标签
- 创建冒号分隔符
- 创建下拉框
- 组合布局

职责：
- 标签 + ":" + 下拉框 的组合
- 提供统一的接口

不负责：
- 数据获取（由下拉框模块自己获取）
- 销毁（由下拉框模块负责）

设计原则（符合V2版本模块化设计补充共识）：
- 用户偏好.json是UI配置唯一来源
- 组合标签和下拉框，简化上层调用
"""

import flet as ft
from typing import Callable, Dict, List, Optional, Any

from 前端.V2.层级5_基础模块.标签 import Label
from 前端.V2.层级5_基础模块.下拉框 import Dropdown

# ============================================
# 数据和文件接口（前置，方便查看和修改）
# ============================================

# 标签下拉框无独立配置变量
# 标签大小、下拉框宽度等配置从各子模块获取

# ============================================
# 公开接口
# ============================================

class LabeledDropdown:
    """
    标签下拉框（层级5：基础模块）
    
    职责：
    - 标签 + ":" + 下拉框 的组合
    - 提供统一的接口
    
    不负责：
    - 数据获取（由下拉框模块自己获取）
    - 销毁（由下拉框模块负责）
    """
    
    _config_service = None
    _dropdown_instance = None
    
    @classmethod
    def set_config_service(cls, config_service):
        """设置配置服务实例"""
        cls._config_service = config_service
        Label.set_config_service(config_service)
        Dropdown.set_config_service(config_service)
    
    @classmethod
    def set_page(cls, page: ft.Page):
        """设置页面实例"""
        cls._dropdown_instance = Dropdown(page, cls._config_service)
    
    @staticmethod
    def _check_config_service():
        """检查配置服务是否已设置"""
        if LabeledDropdown._config_service is None:
            raise RuntimeError(
                "LabeledDropdown模块未设置config_service，"
                "请先调用 LabeledDropdown.set_config_service(config_service)"
            )
    
    @staticmethod
    def create(
        section: str = "",
        control_id: str = "",
        label: str = "",
        enabled: bool = True,
        on_change: Callable[[str, str, Any], None] = None,
        label_size: int = 14,
        dropdown_width: int = None,
    ) -> ft.Row:
        """
        创建标签下拉框（标签 + ":" + 下拉框）
        
        参数：
        - section: 配置节
        - control_id: 控件ID
        - label: 标签文本
        - enabled: 是否启用
        - on_change: 值变更回调
        - label_size: 标签字体大小
        - dropdown_width: 下拉框宽度（可选，默认从配置获取）
        
        返回：
        - ft.Row: 标签 + ":" + 下拉框 的组合
        """
        LabeledDropdown._check_config_service()
        
        if LabeledDropdown._dropdown_instance is None:
            LabeledDropdown._dropdown_instance = Dropdown(None, LabeledDropdown._config_service)
        
        label_text = Label.create(
            text=label,
            size=label_size,
            color_type="secondary",
        )
        
        theme_colors = Label._get_theme_colors()
        colon_text = ft.Text(
            ":",
            size=label_size,
            color=theme_colors.get("text_secondary", theme_colors.get("text_primary")),
        )
        
        dropdown_container = LabeledDropdown._dropdown_instance.create(
            section=section,
            control_id=control_id,
            enabled=enabled,
            on_change=on_change,
            width=dropdown_width,
        )
        
        return ft.Row(
            [label_text, colon_text, dropdown_container],
            spacing=2,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

# *** 标准测试格式: 仅调用被测模块,AI不得添加数据 ***
if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    
    from 前端.V2.业务层.服务.配置服务 import ConfigService
    
    def main(page: ft.Page):
        page.title = "标签下拉框测试"
        
        config_service = ConfigService()
        LabeledDropdown.set_config_service(config_service)
        LabeledDropdown.set_page(page)
        
        def on_change(section, control_id, value):
            print(f"变更: {section}.{control_id} = {value}")
        
        labeled_dropdown = LabeledDropdown.create(
            section="建筑设置.主帅主城",
            control_id="城市等级",
            label="城市",
            enabled=True,
            on_change=on_change,
        )
        
        page.add(ft.Column([
            ft.Text("标签下拉框测试", size=20, weight=ft.FontWeight.BOLD),
            ft.Container(content=labeled_dropdown, padding=20),
        ]))
    
    ft.run(main)
