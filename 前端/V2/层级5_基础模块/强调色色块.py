# -*- coding: utf-8 -*-

"""
模块名称：强调色色块.py
模块功能：强调色选择块

实现步骤：
- 创建强调色块
- 支持选中状态
- 支持点击选择

职责：
- 强调色显示
- 强调色选择

不负责：
- 布局
- 销毁（不需要销毁）
"""

import flet as ft
from typing import Callable, Dict, Optional

# ============================================
# 数据和文件接口（前置，方便查看和修改）
# ============================================

DEFAULT_SIZE = 24
DEFAULT_BORDER_RADIUS = 4

# ============================================
# 公开接口
# ============================================

class AccentBlock:
    """
    强调色色块组件
    
    职责：
    - 强调色显示
    - 强调色选择
    
    不负责：
    - 布局
    - 销毁（不需要销毁）
    """
    
    _config_service = None
    
    @classmethod
    def set_config_service(cls, config_service):
        """设置配置服务实例"""
        cls._config_service = config_service
    
    @staticmethod
    def _get_accent_colors() -> Dict:
        """获取所有强调色配置"""
        accents = AccentBlock._config_service.get_all_accents()
        return {a["name"]: a for a in accents}
    
    @staticmethod
    def create(
        accent_name: str = "blue",
        selected: bool = False,
        on_click: Callable[[str], None] = None,
        size: int = DEFAULT_SIZE,
        accent_colors: Dict = None,
    ) -> ft.Container:
        """
        创建强调色块
        
        参数：
        - accent_name: 强调色名称
        - selected: 是否选中
        - on_click: 点击回调
        - size: 色块大小
        - accent_colors: 强调色配置字典（可选，不传则从配置服务获取）
        """
        if accent_colors is None:
            accent_colors = AccentBlock._get_accent_colors()
        
        accent = accent_colors.get(accent_name, {"name": accent_name, "value": "#0078D4"})
        
        border = ft.border.all(2, accent.get("value")) if selected else ft.border.all(1, "#CCCCCC")
        
        container = ft.Container(
            bgcolor=accent.get("value"),
            width=size,
            height=size,
            border_radius=DEFAULT_BORDER_RADIUS,
            border=border,
            tooltip=accent.get("name", accent_name),
            on_click=lambda e: on_click(accent_name) if on_click else None,
        )
        
        return container

# *** 标准测试格式: 仅调用被测模块,AI不得添加数据 ***
if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
    
    from 前端.V2.业务层.服务.配置服务 import ConfigService
    
    def main(page: ft.Page):
        page.title = "强调色色块测试"
        
        config_service = ConfigService()
        AccentBlock.set_config_service(config_service)
        
        def on_accent_click(accent_name):
            print(f"选择强调色: {accent_name}")
        
        accents = config_service.get_all_accents()
        current_accent = config_service.get_current_accent()
        row = ft.Row([
            AccentBlock.create(a["name"], a["name"] == current_accent, on_accent_click)
            for a in accents
        ])
        page.add(row)
    
    ft.app(target=main)
