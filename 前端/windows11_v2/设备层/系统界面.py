# -*- coding: utf-8 -*-
"""
系统界面 - 设备层

设计思路:
    本模块是设备层模块，提供系统界面。

功能:
    1. 继承基础界面
    2. 提供系统相关功能
    3. 包含设备管理、系统信息、授权管理等

数据来源:
    主题颜色从界面配置获取。

使用场景:
    被系统层调用，提供系统界面。

可独立运行调试: python 系统界面.py
"""

import flet as ft
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from 原子层.界面配置 import 界面配置
from 设备层.基础界面 import BaseInterface


class SystemInterface(BaseInterface):  # 系统界面
    """系统界面 - 提供系统功能"""
    
    def __init__(self, config: 界面配置, page: ft.Page):
        super().__init__(config, page, title="系统设置", subtitle="系统相关设置")
    
    def _create_content_area(self) -> ft.Control:  # 创建内容区域
        return ft.Column([
            self._create_device_card(),
            ft.Divider(height=self._margin * 2, color="transparent"),
            self._create_system_info_card(),
            ft.Divider(height=self._margin * 2, color="transparent"),
            self._create_license_card(),
        ], spacing=0)
    
    def _create_device_card(self) -> ft.Container:  # 创建设备管理卡片
        items = [
            ft.Text("ADB设备管理", size=14, weight=ft.FontWeight.BOLD, color=self._config.获取颜色("text_primary")),
            ft.Divider(height=self._margin, color=self._config.获取颜色("divider")),
            ft.Text("已连接设备:", color=self._config.获取颜色("text_primary")),
            ft.Text("127.0.0.1:5555 (蓝叠模拟器)", size=14, color=self._config.获取颜色("text_primary")),
            ft.Divider(height=self._margin, color="transparent"),
            ft.Row([
                ft.Button("刷新设备列表", style=ft.ButtonStyle(bgcolor=self._config.获取颜色("accent"), color="white", elevation=0)),
                ft.Button("连接新设备", style=ft.ButtonStyle(bgcolor=self._config.获取颜色("bg_secondary"), color=self._config.获取颜色("text_primary"), elevation=0))
            ])
        ]
        return self._create_card("设备管理", items)
    
    def _create_system_info_card(self) -> ft.Container:  # 创建系统信息卡片
        items = [
            ft.Text("系统版本: v1.0.0", color=self._config.获取颜色("text_primary")),
            ft.Text("Python版本: 3.11.0", color=self._config.获取颜色("text_primary")),
            ft.Text("Flet版本: 0.21.0", color=self._config.获取颜色("text_primary")),
        ]
        return self._create_card("系统信息", items)
    
    def _create_license_card(self) -> ft.Container:  # 创建授权管理卡片
        items = [
            ft.Text("授权状态: 已授权", color="#4CAF50"),
            ft.Text("授权类型: 专业版", color=self._config.获取颜色("text_primary")),
            ft.Text("到期时间: 2026-12-31", color=self._config.获取颜色("text_primary")),
            ft.Divider(height=self._margin, color="transparent"),
            ft.Button("验证授权", style=ft.ButtonStyle(bgcolor=self._config.获取颜色("accent"), color="white", elevation=0))
        ]
        return self._create_card("授权管理", items)


# 兼容别名
系统界面 = SystemInterface


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    config = 界面配置()
    
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = config.获取颜色("bg_primary")
        interface = SystemInterface(config, page)
        page.add(interface.render())
    
    ft.run(main)
