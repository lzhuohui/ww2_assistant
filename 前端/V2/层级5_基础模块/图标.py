# -*- coding: utf-8 -*-

"""
模块名称：图标.py
模块功能：图标组件

实现步骤：
- 创建图标
- 支持主题颜色
- 支持不同大小

职责：
- 图标显示
- 从用户偏好.json获取基础图标大小

不负责：
- 布局
- 销毁（不需要销毁）

设计原则（符合V2版本模块化设计补充共识）：
- 用户偏好.json是UI配置唯一来源
- 如果用户偏好.json缺少配置，抛出错误
- 不使用DEFAULT_XXX掩盖问题
"""

import flet as ft
from typing import Dict, Optional

# ============================================
# 数据和文件接口（前置，方便查看和修改）
# ============================================

# 图标无默认值配置，所有UI配置从用户偏好.json获取
# 如果用户偏好.json缺少配置，抛出错误而非掩盖

# ============================================
# 公开接口
# ============================================

class Icon:
    """
    图标组件
    
    职责：
    - 图标显示
    - 从用户偏好.json获取基础图标大小
    
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
        if Icon._config_service is None:
            raise RuntimeError(
                "Icon模块未设置config_service，"
                "请先调用 Icon.set_config_service(config_service)"
            )
    
    @staticmethod
    def get_base_size() -> int:
        """获取基础图标大小（从用户偏好.json获取）"""
        Icon._check_config_service()
        size = Icon._config_service.get_ui_config("图标", "基础大小")
        if size is None:
            raise RuntimeError("用户偏好.json缺少配置: 图标.基础大小")
        return size
    
    @staticmethod
    def _get_theme_colors() -> Dict[str, str]:
        """获取主题颜色"""
        Icon._check_config_service()
        return Icon._config_service.get_theme_colors()
    
    @staticmethod
    def create(
        icon_name: str = "HOME",
        size: int = None,
        color_type: str = "accent",
        theme_colors: Dict[str, str] = None,
        opacity: float = 1.0,
    ) -> ft.Icon:
        """
        创建图标
        
        参数：
        - icon_name: 图标名称
        - size: 图标大小（可选，默认从用户偏好.json获取基础大小）
        - color_type: 颜色类型 (accent/primary/secondary)
        - theme_colors: 主题颜色
        - opacity: 透明度
        """
        if size is None:
            size = Icon.get_base_size()
        
        if theme_colors is None:
            theme_colors = Icon._get_theme_colors()
        
        color = theme_colors.get(color_type, theme_colors.get("accent"))
        
        icon_attr = getattr(ft.Icons, icon_name.upper(), ft.Icons.HOME)
        
        return ft.Icon(
            icon_attr,
            size=size,
            color=color,
            opacity=opacity,
        )

# *** 标准测试格式: 仅调用被测模块,AI不得添加数据 ***
if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
    
    from 前端.V2.业务层.服务.配置服务 import ConfigService
    
    def main(page: ft.Page):
        page.title = "图标测试"
        
        config_service = ConfigService()
        Icon.set_config_service(config_service)
        
        print(f"基础图标大小: {Icon.get_base_size()}")
        
        row = ft.Row([
            Icon.create("SETTINGS", color_type="accent"),
            Icon.create("HOME", color_type="primary"),
            Icon.create("INFO", color_type="secondary"),
        ])
        page.add(row)
    
    ft.run(main)
