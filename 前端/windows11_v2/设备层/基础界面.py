# -*- coding: utf-8 -*-
"""
基础界面 - 设备层

设计思路:
    本模块是设备层模块，提供基础的界面模板。

功能:
    1. 提供统一的界面结构
    2. 提供卡片式布局
    3. 提供统一的样式

数据来源:
    主题颜色从界面配置获取。

使用场景:
    被系统层调用，提供各界面。

可独立运行调试: python 基础界面.py
"""

import flet as ft
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from 原子层.界面配置 import 界面配置
from 组件层.容器样式 import ContainerStyle
from 组件层.装饰框线 import DecorativeBorder
from typing import List, Any


class BaseInterface:  # 基础界面
    """基础界面 - 提供统一的界面结构"""
    
    def __init__(self, config: 界面配置, page: ft.Page, title: str = "设置", subtitle: str = "设置描述"):
        self._config = config
        self._page = page
        self._title = title
        self._subtitle = subtitle
        ui_config = config.定义尺寸.get("界面", {})
        self._margin = ui_config.get("peripheral_margin", 10)
    
    def render(self) -> ft.Container:  # 渲染界面
        content = ft.Column([
            ft.Row([
                ft.Text(self._title, size=20, weight=ft.FontWeight.BOLD, color=self._config.获取颜色("text_primary")),
                ft.Text(self._subtitle, size=12, color=self._config.获取颜色("text_secondary")),
            ], spacing=self._margin, vertical_alignment=ft.CrossAxisAlignment.END),
            ft.Divider(height=self._margin * 2, color="transparent"),
            self._create_content_area(),
        ], spacing=self._margin)
        
        return ContainerStyle.content_container(self._config, content=content, padding=self._margin * 2)
    
    def _create_content_area(self) -> ft.Control:  # 创建内容区域（子类重写）
        return ft.Text("设置内容", color=self._config.获取颜色("text_primary"))
    
    def _create_card(self, title: str, items: List[ft.Control]) -> ft.Container:  # 创建卡片
        card_content = ft.Column([
            ft.Text(title, size=16, weight=ft.FontWeight.BOLD, color=self._config.获取颜色("text_primary")),
            ft.Divider(height=self._margin, color=self._config.获取颜色("divider")),
            *items
        ], spacing=self._margin)
        
        return ContainerStyle.card_container(self._config, content=card_content, padding=self._margin * 2)


# 兼容别名
基础界面 = BaseInterface


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    config = 界面配置()
    
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = config.获取颜色("bg_primary")
        interface = BaseInterface(config, page, title="基础设置", subtitle="基础设置描述")
        page.add(interface.render())
    
    ft.run(main)
