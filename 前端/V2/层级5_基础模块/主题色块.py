# -*- coding: utf-8 -*-

"""
模块名称：主题色块.py
模块功能：主题颜色选择块

实现步骤：
- 创建主题颜色块
- 支持选中状态
- 支持点击选择

职责：
- 主题颜色显示
- 主题选择
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

# 主题色块无默认值配置，所有UI配置从用户偏好.json获取
# 如果用户偏好.json缺少配置，抛出错误而非掩盖

# ============================================
# 公开接口
# ============================================

class ThemeBlock:
    """
    主题色块组件
    
    职责：
    - 主题颜色显示
    - 主题选择
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
        if ThemeBlock._config_service is None:
            raise RuntimeError(
                "ThemeBlock模块未设置config_service，"
                "请先调用 ThemeBlock.set_config_service(config_service)"
            )
    
    @staticmethod
    def get_size() -> int:
        """获取色块大小（从用户偏好.json获取）"""
        ThemeBlock._check_config_service()
        size = ThemeBlock._config_service.get_ui_config("色块", "大小")
        if size is None:
            raise RuntimeError("用户偏好.json缺少配置: 色块.大小")
        return size
    
    @staticmethod
    def get_border_radius() -> int:
        """获取圆角（从用户偏好.json获取）"""
        ThemeBlock._check_config_service()
        radius = ThemeBlock._config_service.get_ui_config("圆角", "中")
        if radius is None:
            raise RuntimeError("用户偏好.json缺少配置: 圆角.中")
        return radius
    
    @staticmethod
    def _get_theme_data(theme_name: str) -> Dict:
        """获取主题数据"""
        ThemeBlock._check_config_service()
        return ThemeBlock._config_service.get_theme_colors(theme_name)
    
    @staticmethod
    def create(
        theme_name: str = "light",
        selected: bool = False,
        on_click: Callable[[str], None] = None,
        size: int = None,
        theme_data: Dict = None,
    ) -> ft.Container:
        """
        创建主题色块
        
        参数：
        - theme_name: 主题名称
        - selected: 是否选中
        - on_click: 点击回调
        - size: 色块大小（可选，默认从用户偏好.json获取）
        - theme_data: 主题数据（可选，不传则从配置服务获取）
        """
        if size is None:
            size = ThemeBlock.get_size()
        
        border_radius = ThemeBlock.get_border_radius()
        
        if theme_data is None:
            theme_data = ThemeBlock._get_theme_data(theme_name)
        
        border = ft.Border.all(2, theme_data.get("accent")) if selected else ft.Border.all(1, theme_data.get("border"))
        
        container = ft.Container(
            content=ft.Container(
                bgcolor=theme_data.get("bg_primary"),
                border_radius=border_radius,
                expand=True,
            ),
            width=size,
            height=size,
            border_radius=border_radius,
            border=border,
            tooltip=theme_data.get("name", theme_name),
            on_click=lambda e: on_click(theme_name) if on_click else None,
        )
        
        return container

# *** 标准测试格式: 仅调用被测模块,AI不得添加数据 ***
if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
    
    from 前端.V2.业务层.服务.配置服务 import ConfigService
    
    def main(page: ft.Page):
        page.title = "主题色块测试"
        
        config_service = ConfigService()
        ThemeBlock.set_config_service(config_service)
        
        print(f"色块大小: {ThemeBlock.get_size()}")
        print(f"圆角: {ThemeBlock.get_border_radius()}")
        
        def on_theme_click(theme_name):
            print(f"选择主题: {theme_name}")
        
        themes = config_service.get_all_themes()
        row = ft.Row([
            ThemeBlock.create(theme, theme == themes[0], on_theme_click)
            for theme in themes
        ])
        page.add(row)
    
    ft.run(main)
