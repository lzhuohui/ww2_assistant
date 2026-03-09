# -*- coding: utf-8 -*-
"""
主界面 - 系统层

设计思路:
    本模块是系统层模块，组装所有模块，创建主界面。

功能:
    1. 创建用户信息模块
    2. 创建导航栏模块
    3. 创建内容区域
    4. 使用ft.Stack布局组装所有模块
    5. 实现模块联动

数据来源:
    主题颜色从界面配置获取。

使用场景:
    被主入口调用，提供主界面。

可独立运行调试: python 主界面.py
"""

import flet as ft
import sys
from pathlib import Path

当前目录 = Path(__file__).parent
sys.path.insert(0, str(当前目录))

from 原子层.界面配置 import 界面配置
from 部件层.用户信息模块 import UserInfoModule
from 部件层.导航栏模块 import NavBar
from 设备层.系统界面 import SystemInterface
from 设备层.通用界面 import GeneralInterface
from 设备层.策略界面 import StrategyInterface
from 设备层.任务界面 import TaskInterface
from 设备层.建筑界面 import BuildingInterface
from 设备层.集资界面 import FundraisingInterface
from 设备层.打扫界面 import CleanupInterface
from 设备层.账号界面 import AccountInterface


class MainInterface:  # 主界面
    """主界面 - 组装所有模块"""
    
    def __init__(self, page: ft.Page):
        self._page = page
        self._config = 界面配置()
        
        ui_config = self._config.定义尺寸.get("界面", {})
        self._margin = ui_config.get("peripheral_margin", 10)
        self._nav_width = ui_config.get("nav_width", 240)
        self._user_info_height = ui_config.get("user_info_height", 80)
        
        self._user_info = UserInfoModule(self._config, page, width=self._nav_width, 获取窗口宽度=lambda: page.width)
        self._navbar = NavBar(self._config, page, width=self._nav_width)
        
        self._interfaces = {
            "系统设置": SystemInterface(self._config, page),
            "通用设置": GeneralInterface(self._config, page),
            "策略设置": StrategyInterface(self._config, page),
            "任务设置": TaskInterface(self._config, page),
            "建筑设置": BuildingInterface(self._config, page),
            "集资设置": FundraisingInterface(self._config, page),
            "打扫战场": CleanupInterface(self._config, page),
            "账号设置": AccountInterface(self._config, page),
        }
        
        self._current_interface = "系统设置"
    
    def render(self) -> ft.Stack:
        self._nav_divider = ft.Container(
            width=1,
            bgcolor=self._config.获取颜色("divider"),
            top=self._user_info_height,
            left=self._nav_width,
            bottom=0,
        )
        
        self._content_container = ft.Container(
            content=self._interfaces["系统设置"].render(),
            top=0,
            left=self._nav_width + 1,
            right=0,
            bottom=0,
            bgcolor=self._config.获取颜色("bg_primary"),
            clip_behavior=ft.ClipBehavior.NONE,
        )
        
        self._navbar_container = ft.Container(
            content=self._navbar.render(),
            width=self._nav_width,
            top=self._user_info_height,
            left=0,
            bottom=0,
            bgcolor=self._config.获取颜色("bg_primary")
        )
        
        self._user_info_container = ft.Container(
            content=self._user_info.render(),
            top=0,
            left=0,
            bgcolor=self._config.获取颜色("bg_primary")
        )
        
        self._user_info.add_callback(self._on_user_info_change)
        self._navbar.add_callback(self._on_nav_change)
        
        main_container = ft.Stack([
            self._content_container,
            self._navbar_container,
            self._user_info_container,
            self._nav_divider,
        ], expand=True)
        
        return main_container
    
    def _on_user_info_change(self, is_expanded: bool, width: int):  # 用户信息联动
        self._navbar_container.top = self._user_info_height
        self._navbar_container.update()
        self._content_container.update()
    
    def _on_nav_change(self, title: str, subtitle: str):  # 导航栏联动
        valid_interfaces = [k for k, v in self._interfaces.items() if v is not None]
        if title in valid_interfaces:
            if self._current_interface != title:
                self._current_interface = title
                self._content_container.content = self._interfaces[title].render()
                self._content_container.update()
        else:
            self._current_interface = title
            empty_content = ft.Container(
                content=ft.Column([
                    ft.Text(title, size=20, weight=ft.FontWeight.BOLD, color=self._config.获取颜色("text_primary")),
                    ft.Text(subtitle, size=12, color=self._config.获取颜色("text_secondary")),
                    ft.Text("该功能界面正在开发中...", size=14, color=self._config.获取颜色("text_hint")),
                ], spacing=10),
                padding=20,
            )
            self._content_container.content = empty_content
            self._content_container.update()


# 兼容别名
主界面 = MainInterface


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    def main(page: ft.Page):
        page.title = "二战风云"
        page.padding = 0
        page.window.width = 1200
        page.window.height = 540
        page.bgcolor = "#1C1C1C"
        
        interface = MainInterface(page)
        page.add(interface.render())
    
    ft.run(main)
