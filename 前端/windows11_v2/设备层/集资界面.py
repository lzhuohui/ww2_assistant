# -*- coding: utf-8 -*-
"""
集资界面 - 设备层

设计思路:
    本模块是设备层模块，提供集资界面。

功能:
    1. 继承基础界面
    2. 提供集资相关功能
    3. 包含小号上贡和分城纳租

数据来源:
    主题颜色从界面配置获取。

使用场景:
    被系统层调用，提供集资界面。

可独立运行调试: python 集资界面.py
"""

import flet as ft
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from 原子层.界面配置 import 界面配置
from 设备层.基础界面 import BaseInterface


class FundraisingInterface(BaseInterface):  # 集资界面
    """集资界面 - 提供集资功能"""
    
    def __init__(self, config: 界面配置, page: ft.Page):
        super().__init__(config, page, title="集资设置", subtitle="集资相关配置")
    
    def _create_content_area(self) -> ft.Control:  # 创建内容区域
        return ft.Column([
            self._create_tribute_card(),
            ft.Divider(height=self._margin * 2, color="transparent"),
            self._create_rent_card(),
        ], spacing=0)
    
    def _create_tribute_card(self) -> ft.Container:  # 创建小号上贡卡片
        items = [
            ft.Row([
                ft.Text("开启上贡:", color=self._config.获取颜色("text_primary")),
                ft.Switch(value=True)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(height=self._margin, color="transparent"),
            ft.Text("上贡限级:", color=self._config.获取颜色("text_primary")),
            ft.Dropdown(
                options=[ft.dropdown.Option(f"{i:02d}") for i in range(5, 16)],
                value="05",
                width=200,
                bgcolor=self._config.获取颜色("bg_secondary"),
                color=self._config.获取颜色("text_primary")
            ),
            ft.Divider(height=self._margin, color="transparent"),
            ft.Text("上贡限量:", color=self._config.获取颜色("text_primary")),
            ft.Dropdown(
                options=[ft.dropdown.Option(str(i)) for i in range(2, 21)],
                value="2",
                width=200,
                bgcolor=self._config.获取颜色("bg_secondary"),
                color=self._config.获取颜色("text_primary")
            ),
            ft.Divider(height=self._margin, color="transparent"),
            ft.Text("接贡统帅:", color=self._config.获取颜色("text_primary")),
            ft.Row([
                ft.TextField(label="主要", width=150, bgcolor=self._config.获取颜色("bg_secondary"), color=self._config.获取颜色("text_primary")),
                ft.TextField(label="备用", width=150, bgcolor=self._config.获取颜色("bg_secondary"), color=self._config.获取颜色("text_primary"))
            ], spacing=10)
        ]
        return self._create_card("小号上贡", items)
    
    def _create_rent_card(self) -> ft.Container:  # 创建分城纳租卡片
        items = [
            ft.Row([
                ft.Text("开启纳租:", color=self._config.获取颜色("text_primary")),
                ft.Switch(value=False)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(height=self._margin, color="transparent"),
            ft.Text("分城等级:", color=self._config.获取颜色("text_primary")),
            ft.Dropdown(
                options=[ft.dropdown.Option(f"{i:02d}") for i in range(5, 16)],
                value="05",
                width=200,
                bgcolor=self._config.获取颜色("bg_secondary"),
                color=self._config.获取颜色("text_primary")
            ),
            ft.Divider(height=self._margin, color="transparent"),
            ft.Text("纳租限量:", color=self._config.获取颜色("text_primary")),
            ft.Dropdown(
                options=[ft.dropdown.Option(str(i)) for i in range(2, 21)],
                value="2",
                width=200,
                bgcolor=self._config.获取颜色("bg_secondary"),
                color=self._config.获取颜色("text_primary")
            )
        ]
        return self._create_card("分城纳租", items)


# 兼容别名
集资界面 = FundraisingInterface


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    config = 界面配置()
    
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = config.获取颜色("bg_primary")
        interface = FundraisingInterface(config, page)
        page.add(interface.render())
    
    ft.run(main)
