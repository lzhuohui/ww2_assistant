# -*- coding: utf-8 -*-

"""
模块名称：导航按钮.py
模块功能：导航按钮组件，图标+文本

实现步骤：
- 创建图标
- 创建文本
- 创建按钮容器
- 添加点击事件

职责：
- 图标显示
- 文本显示
- 点击事件
- 从配置服务获取主题颜色

不负责：
- 布局
- 销毁（不需要销毁）

设计原则（符合V2版本模块化设计补充共识）：
- 定义1：自己获取主题颜色
- 定义2：上层只传递icon_name、text
- 定义3：theme_colors可覆盖
- 定义4：create()
"""

import flet as ft
from typing import Callable, Dict, Optional

from 前端.V2.层级5_基础模块.图标 import Icon
from 前端.V2.层级5_基础模块.标签 import Label

# ============================================
# 数据和文件接口（前置，方便查看和修改）
# ============================================

# 导航按钮无默认值配置，所有UI配置从用户偏好.json获取
# 如果用户偏好.json缺少配置，抛出错误而非掩盖

# ============================================
# 公开接口
# ============================================

class NavButton:
    """
    导航按钮组件（层级4：复合模块）
    
    职责：
    - 图标显示
    - 文本显示
    - 点击事件
    - 从配置服务获取主题颜色
    
    不负责：
    - 布局
    - 销毁（不需要销毁）
    """
    
    _config_service = None
    
    @classmethod
    def set_config_service(cls, config_service):
        """设置配置服务实例"""
        cls._config_service = config_service
        Icon.set_config_service(config_service)
        Label.set_config_service(config_service)
    
    @staticmethod
    def get_icon_size() -> int:
        """获取图标尺寸（从用户偏好.json获取基础大小*1.125）"""
        NavButton._check_config_service()
        base_size = Icon.get_base_size()
        return int(base_size * 1.125)
    
    @staticmethod
    def get_text_size() -> int:
        """获取文本尺寸（从用户偏好.json获取基础大小*0.86）"""
        NavButton._check_config_service()
        base_size = Label.get_base_size()
        return int(base_size * 0.86)
    
    @staticmethod
    def get_button_width() -> int:
        """获取按钮宽度（从用户偏好.json获取）"""
        NavButton._check_config_service()
        value = NavButton._config_service.get_ui_config("导航按钮", "宽度")
        if value is None:
            raise RuntimeError("用户偏好.json缺少配置: 导航按钮.宽度")
        return value
    
    @staticmethod
    def get_button_height() -> int:
        """获取按钮高度（从用户偏好.json获取）"""
        NavButton._check_config_service()
        value = NavButton._config_service.get_ui_config("导航按钮", "高度")
        if value is None:
            raise RuntimeError("用户偏好.json缺少配置: 导航按钮.高度")
        return value
    
    @staticmethod
    def _check_config_service():
        """检查配置服务是否已设置"""
        if NavButton._config_service is None:
            raise RuntimeError(
                "NavButton模块未设置config_service，"
                "请先调用 NavButton.set_config_service(config_service)"
            )
    
    @staticmethod
    def create(
        icon_name: str = "HOME",
        text: str = "首页",
        selected: bool = False,
        on_click: Callable[[str], None] = None,
        icon_size: int = None,
        text_size: int = None,
        theme_colors: Dict[str, str] = None,
    ) -> ft.Container:
        """
        创建导航按钮（不传递theme_colors给层级5模块）
        
        参数：
        - icon_name: 图标名称
        - text: 按钮文本
        - selected: 是否选中
        - on_click: 点击回调
        - icon_size: 图标尺寸（可选，默认从用户偏好.json获取）
        - text_size: 文本尺寸（可选，默认从用户偏好.json获取）
        - theme_colors: 主题颜色（可选，不传则从配置服务获取）
        """
        if NavButton._config_service is None:
            raise RuntimeError("NavButton模块未设置config_service，请先调用NavButton.set_config_service()")
        
        if theme_colors is None:
            theme_colors = NavButton._config_service.get_theme_colors()
        
        icon_size = icon_size or NavButton.get_icon_size()
        text_size = text_size or NavButton.get_text_size()
        button_width = NavButton.get_button_width()
        button_height = NavButton.get_button_height()
        
        icon_color_type = "accent" if selected else "secondary"
        
        icon_control = Icon.create(
            icon_name=icon_name,
            size=icon_size,
            color_type=icon_color_type,
        )
        
        text_color_type = "primary" if selected else "secondary"
        
        text_control = Label.create(
            text=text,
            size=text_size,
            color_type=text_color_type,
        )
        
        def handle_click(e):
            if on_click:
                on_click(icon_name)
        
        container = ft.Container(
            content=ft.Row([
                icon_control,
                text_control,
            ], spacing=8, alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            width=button_width,
            height=button_height,
            on_click=handle_click,
            border_radius=ft.BorderRadius.all(8),
            bgcolor=theme_colors.get("bg_secondary") if selected else None,
            alignment=ft.alignment.Alignment(0, 0),
            padding=ft.Padding.symmetric(horizontal=12, vertical=0),
        )
        
        return container

# *** 标准测试格式: 仅调用被测模块,AI不得添加数据 ***
if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    
    from 前端.V2.业务层.服务.配置服务 import ConfigService
    
    def main(page: ft.Page):
        page.title = "导航按钮测试"
        
        config_service = ConfigService()
        NavButton.set_config_service(config_service)
        
        def on_nav_click(icon_name):
            print(f"点击: {icon_name}")
        
        row = ft.Row([
            NavButton.create("HOME", "首页", True, on_nav_click),
            NavButton.create("SETTINGS", "设置", False, on_nav_click),
        ])
        page.add(row)
    
    ft.run(main)
