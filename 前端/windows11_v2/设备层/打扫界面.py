# -*- coding: utf-8 -*-
"""
打扫界面 - 设备层

设计思路:
    本模块是设备层模块，提供打扫界面。

功能:
    1. 继承基础界面
    2. 提供打扫相关功能
    3. 包含打扫城区战场和打扫政区战场

数据来源:
    主题颜色从界面配置获取。

使用场景:
    被系统层调用，提供打扫界面。

可独立运行调试: python 打扫界面.py
"""

import flet as ft
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from 原子层.界面配置 import 界面配置
from 设备层.基础界面 import BaseInterface


class CleanupInterface(BaseInterface):  # 打扫界面
    """打扫界面 - 提供打扫功能"""
    
    def __init__(self, config: 界面配置, page: ft.Page):
        super().__init__(config, page, title="打扫战场", subtitle="打扫战场配置")
    
    def _create_content_area(self) -> ft.Control:  # 创建内容区域
        return ft.Column([
            self._create_cleanup_card(),
        ], spacing=0)
    
    def _create_cleanup_card(self) -> ft.Container:  # 创建打扫设置卡片
        items = [
            ft.Row([
                ft.Text("打扫城区战场:", color=self._config.获取颜色("text_primary")),
                ft.Switch(value=True)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(height=self._margin, color="transparent"),
            ft.Row([
                ft.Text("打扫政区战场:", color=self._config.获取颜色("text_primary")),
                ft.Switch(value=False)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        ]
        return self._create_card("打扫设置", items)


# 兼容别名
打扫界面 = CleanupInterface


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    config = 界面配置()
    
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = config.获取颜色("bg_primary")
        interface = CleanupInterface(config, page)
        page.add(interface.render())
    
    ft.run(main)
