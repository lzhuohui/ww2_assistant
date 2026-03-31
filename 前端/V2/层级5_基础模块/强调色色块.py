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
- 从用户偏好.json获取色块大小、圆角

不负责：
- 布局
- 销毁（不需要销毁）

设计原则（符合V2版本模块化设计补充共识）：
- 用户偏好.json是UI配置唯一来源
- 如果用户偏好.json缺少配置，抛出错误
- 不使用DEFAULT_XXX掩盖问题
"""

import flet as ft
from typing import Callable, Dict, Optional

# ============================================
# 数据和文件接口（前置，方便查看和修改）
# ============================================

# 强调色色块无默认值配置，所有UI配置从用户偏好.json获取
# 如果用户偏好.json缺少配置，抛出错误而非掩盖

# ============================================
# 公开接口
# ============================================

class AccentBlock:
    """
    强调色色块组件
    
    职责：
    - 强调色显示
    - 强调色选择
    - 从用户偏好.json获取色块大小、圆角
    
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
    def _check_config_service():
        """检查配置服务是否已设置"""
        if AccentBlock._config_service is None:
            raise RuntimeError(
                "AccentBlock模块未设置config_service，"
                "请先调用 AccentBlock.set_config_service(config_service)"
            )
    
    @staticmethod
    def get_size() -> int:
        """获取色块大小（从用户偏好.json获取）"""
        AccentBlock._check_config_service()
        size = AccentBlock._config_service.get_ui_config("色块", "大小")
        if size is None:
            raise RuntimeError("用户偏好.json缺少配置: 色块.大小")
        return size
    
    @staticmethod
    def get_border_radius() -> int:
        """获取圆角（从用户偏好.json获取）"""
        AccentBlock._check_config_service()
        radius = AccentBlock._config_service.get_ui_config("圆角", "小")
        if radius is None:
            raise RuntimeError("用户偏好.json缺少配置: 圆角.小")
        return radius
    
    @staticmethod
    def _get_accent_colors() -> Dict:
        """获取所有强调色配置"""
        AccentBlock._check_config_service()
        accents = AccentBlock._config_service.get_all_accents()
        return {a["name"]: a for a in accents}
    
    @staticmethod
    def create(
        accent_name: str = "blue",
        selected: bool = False,
        on_click: Callable[[str], None] = None,
        size: int = None,
        accent_colors: Dict = None,
    ) -> ft.Container:
        """
        创建强调色块
        
        参数：
        - accent_name: 强调色名称
        - selected: 是否选中
        - on_click: 点击回调
        - size: 色块大小（可选，默认从用户偏好.json获取）
        - accent_colors: 强调色配置字典（可选，不传则从配置服务获取）
        """
        if size is None:
            size = AccentBlock.get_size()
        
        border_radius = AccentBlock.get_border_radius()
        
        if accent_colors is None:
            accent_colors = AccentBlock._get_accent_colors()
        
        accent = accent_colors.get(accent_name, {"name": accent_name, "value": "#0078D4"})
        
        border = ft.Border.all(2, accent.get("value")) if selected else ft.Border.all(1, "#CCCCCC")
        
        container = ft.Container(
            bgcolor=accent.get("value"),
            width=size,
            height=size,
            border_radius=border_radius,
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
        
        print(f"色块大小: {AccentBlock.get_size()}")
        print(f"圆角: {AccentBlock.get_border_radius()}")
        
        def on_accent_click(accent_name):
            print(f"选择强调色: {accent_name}")
        
        accents = config_service.get_all_accents()
        current_accent = config_service.get_current_accent()
        row = ft.Row([
            AccentBlock.create(a["name"], a["name"] == current_accent, on_accent_click)
            for a in accents
        ])
        page.add(row)
    
    ft.run(main)
