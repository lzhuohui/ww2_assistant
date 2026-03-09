# -*- coding: utf-8 -*-
"""
个性化界面 - 设备层

设计思路:
    本模块是设备层模块，提供个性化界面。

功能:
    1. 继承基础界面
    2. 提供个性化相关功能
    3. 包含主题模式、强调色等

数据来源:
    主题颜色从界面配置获取。

使用场景:
    被系统层调用，提供个性化界面。

可独立运行调试: python 个性化界面.py
"""

import flet as ft
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from 原子层.界面配置 import 界面配置
from 设备层.基础界面 import BaseInterface


class PersonalizationInterface(BaseInterface):  # 个性化界面
    """个性化界面 - 提供个性化功能"""
    
    def __init__(self, config: 界面配置, page: ft.Page):
        super().__init__(config, page, title="个性化设置", subtitle="界面个性化配置")
    
    def _create_content_area(self) -> ft.Control:  # 创建内容区域
        return ft.Column([
            self._create_theme_card(),
            ft.Divider(height=self._margin * 2, color="transparent"),
            self._create_appearance_card(),
        ], spacing=0)
    
    def _create_theme_card(self) -> ft.Container:  # 创建主题设置卡片
        items = [
            ft.Text("主题模式:", color=self._config.获取颜色("text_primary")),
            ft.Dropdown(
                options=[
                    ft.dropdown.Option("浅色"),
                    ft.dropdown.Option("深色")
                ],
                value="浅色",
                width=200,
                bgcolor=self._config.获取颜色("bg_secondary"),
                color=self._config.获取颜色("text_primary")
            ),
            ft.Divider(height=self._margin, color="transparent"),
            ft.Text("强调色:", color=self._config.获取颜色("text_primary")),
            ft.Dropdown(
                options=[
                    ft.dropdown.Option("蓝色"),
                    ft.dropdown.Option("红色"),
                    ft.dropdown.Option("绿色"),
                    ft.dropdown.Option("紫色"),
                    ft.dropdown.Option("橙色")
                ],
                value="蓝色",
                width=200,
                bgcolor=self._config.获取颜色("bg_secondary"),
                color=self._config.获取颜色("text_primary")
            ),
            ft.Row([
                ft.Text("强调色开关:", color=self._config.获取颜色("text_primary")),
                ft.Switch(value=True)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        ]
        return self._create_card("主题设置", items)
    
    def _create_appearance_card(self) -> ft.Container:  # 创建外观设置卡片
        items = [
            ft.Row([
                ft.Text("透明效果:", color=self._config.获取颜色("text_primary")),
                ft.Switch(value=False)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(height=self._margin, color="transparent"),
            ft.Text("字体:", color=self._config.获取颜色("text_primary")),
            ft.Dropdown(
                options=[
                    ft.dropdown.Option("微软雅黑"),
                    ft.dropdown.Option("宋体"),
                    ft.dropdown.Option("黑体"),
                    ft.dropdown.Option("Arial"),
                    ft.dropdown.Option("Times New Roman")
                ],
                value="微软雅黑",
                width=200,
                bgcolor=self._config.获取颜色("bg_secondary"),
                color=self._config.获取颜色("text_primary")
            ),
            ft.Divider(height=self._margin, color="transparent"),
            ft.Row([
                ft.Text("导航展开:", color=self._config.获取颜色("text_primary")),
                ft.Switch(value=False)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        ]
        return self._create_card("外观设置", items)


# 兼容别名
个性化界面 = PersonalizationInterface


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    config = 界面配置()
    
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = config.获取颜色("bg_primary")
        interface = PersonalizationInterface(config, page)
        page.add(interface.render())
    
    ft.run(main)
