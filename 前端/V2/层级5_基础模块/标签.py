# -*- coding: utf-8 -*-

"""
模块名称：标签.py
模块功能：文本标签组件

实现步骤：
- 创建文本标签
- 支持主题颜色
- 支持不同大小

职责：
- 文本显示
- 从用户偏好.json获取基础字体大小

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

# 标签无默认值配置，所有UI配置从用户偏好.json获取
# 如果用户偏好.json缺少配置，抛出错误而非掩盖

# ============================================
# 公开接口
# ============================================

class Label:
    """
    标签组件
    
    职责：
    - 文本显示
    - 从用户偏好.json获取基础字体大小
    
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
        if Label._config_service is None:
            raise RuntimeError(
                "Label模块未设置config_service，"
                "请先调用 Label.set_config_service(config_service)"
            )
    
    @staticmethod
    def get_base_size() -> int:
        """获取基础字体大小（从用户偏好.json获取）"""
        Label._check_config_service()
        size = Label._config_service.get_ui_config("字体", "基础大小")
        if size is None:
            raise RuntimeError("用户偏好.json缺少配置: 字体.基础大小")
        return size
    
    @staticmethod
    def _get_theme_colors() -> Dict[str, str]:
        """获取主题颜色"""
        Label._check_config_service()
        return Label._config_service.get_theme_colors()
    
    @staticmethod
    def create(
        text: str = "",
        size: int = None,
        weight: ft.FontWeight = ft.FontWeight.NORMAL,
        color_type: str = "primary",
        theme_colors: Dict[str, str] = None,
        no_wrap: bool = True,
        overflow: ft.TextOverflow = ft.TextOverflow.ELLIPSIS,
    ) -> ft.Text:
        """
        创建标签
        
        参数：
        - text: 文本内容
        - size: 字体大小（可选，默认从用户偏好.json获取基础大小）
        - weight: 字体粗细
        - color_type: 颜色类型 (primary/secondary/disabled)
        - theme_colors: 主题颜色
        - no_wrap: 是否不换行
        - overflow: 溢出处理
        """
        if size is None:
            size = Label.get_base_size()
        
        if theme_colors is None:
            theme_colors = Label._get_theme_colors()
        
        color_key = f"text_{color_type}" if color_type != "primary" else "text_primary"
        color = theme_colors.get(color_key, theme_colors.get("text_primary"))
        
        return ft.Text(
            text,
            size=size,
            weight=weight,
            color=color,
            no_wrap=no_wrap,
            overflow=overflow,
        )

# *** 标准测试格式: 仅调用被测模块,AI不得添加数据 ***
if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
    
    from 前端.V2.业务层.服务.配置服务 import ConfigService
    
    def main(page: ft.Page):
        page.title = "标签测试"
        
        config_service = ConfigService()
        Label.set_config_service(config_service)
        
        print(f"基础字体大小: {Label.get_base_size()}")
        
        column = ft.Column([
            Label.create("主标题", size=16, weight=ft.FontWeight.BOLD),
            Label.create("副标题", color_type="secondary"),
            Label.create("禁用文本", size=12, color_type="disabled"),
        ])
        page.add(column)
    
    ft.run(main)
