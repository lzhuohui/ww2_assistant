# -*- coding: utf-8 -*-
"""
用户信息模块 - 部件层

设计思路:
    本模块是部件层模块，调用容器组件、装饰框线组件、头像组件、用户文本组件和展开箭头组件。

功能:
    1. 调用容器组件创建用户信息容器
    2. 调用装饰框线创建内框线
    3. 调用头像组件显示用户头像
    4. 调用用户文本组件显示用户信息
    5. 调用展开箭头组件显示展开状态
    6. 点击箭头展开/折叠容器
    7. 展开时通知联动模块

数据来源:
    主题颜色从界面配置获取。

使用场景:
    被设备层界面调用，提供用户信息展示区域。

可独立运行调试: python 用户信息模块.py
"""

import flet as ft
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from 原子层.界面配置 import 界面配置
from 组件层.容器样式 import ContainerStyle
from 组件层.装饰框线 import DecorativeBorder
from typing import Optional, Callable, List


class UserInfoModule:  # 用户信息模块
    """用户信息模块 - 调用容器组件、装饰框线组件、头像组件、用户文本组件和展开箭头组件"""
    
    def __init__(self, config: 界面配置, page: ft.Page, **kwargs):
        self._config = config
        self._page = page
        self._collapsed_width = kwargs.get("width", 240)
        self._width = self._collapsed_width
        self._height = kwargs.get("height", 80)
        ui_config = config.定义尺寸.get("界面", {})
        self._margin = ui_config.get("peripheral_margin", 10)
        self._expanded_width = 1200
        self._get_window_width = kwargs.get("获取窗口宽度", lambda: 1200)
        self._is_expanded = False
        self._container: Optional[ft.Container] = None
        self._inner_border: Optional[ft.Container] = None
        self._expanded_content: Optional[ft.Container] = None
        self._callbacks: List[Callable] = []
    
    def add_callback(self, callback: Callable):  # 添加联动回调函数
        self._callbacks.append(callback)
    
    def render(self) -> ft.Container:
        self._expanded_content = ft.Container(
            content=ft.Row([
                ft.Text("展开信息1", size=14, color=self._config.获取颜色("text_primary")),
                ft.Text("展开信息2", size=14, color=self._config.获取颜色("text_primary")),
                ft.Text("展开信息3", size=14, color=self._config.获取颜色("text_primary")),
            ], spacing=50, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            visible=self._is_expanded,
            alignment=ft.Alignment(0, 0),
        )
        
        avatar = ft.Container(
            content=ft.Text("👤", size=24),
            width=40,
            height=40,
            border_radius=20,
            bgcolor=self._config.获取颜色("bg_secondary"),
            alignment=ft.Alignment(0, 0),
        )
        
        user_text = ft.Column([
            ft.Text("用户名", size=14, weight=ft.FontWeight.BOLD, color=self._config.获取颜色("text_primary")),
            ft.Text("user@example.com", size=12, color=self._config.获取颜色("text_secondary")),
        ], spacing=2)
        
        self._expand_arrow = ft.Text(">", size=12, color=self._config.获取颜色("text_secondary"))
        
        self._inner_border = DecorativeBorder.inner_border(
            self._config,
            content=ft.Stack([
                ft.Container(
                    content=ft.Row(
                        controls=[
                            avatar,
                            user_text,
                            ft.Container(width=50),
                            self._expanded_content,
                        ],
                        spacing=self._margin,
                        alignment=ft.MainAxisAlignment.START,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    )
                ),
                ft.Container(
                    content=self._expand_arrow,
                    alignment=ft.Alignment(1, 0),
                    padding=ft.Padding(left=0, top=0, right=self._margin, bottom=0),
                    on_click=self._toggle_expand,
                ),
            ]),
            padding=self._margin,
            width=self._width - self._margin * 2,
            height=self._height - self._margin * 2,
        )
        
        self._container = ContainerStyle.user_info_container(
            self._config,
            content=self._inner_border,
            width=self._width,
            height=self._height,
            padding=self._margin,
        )
        return self._container
    
    def _toggle_expand(self, e):  # 切换展开状态
        self._is_expanded = not self._is_expanded
        if self._is_expanded:
            self._width = self._get_window_width()
        else:
            self._width = self._collapsed_width
        
        self._expand_arrow.value = "<" if self._is_expanded else ">"
        
        if self._container:
            self._container.width = self._width
        
        if self._inner_border:
            self._inner_border.width = self._width - self._margin * 2
        
        if self._expanded_content:
            self._expanded_content.visible = self._is_expanded
        
        if self._container:
            self._container.update()
        
        for callback in self._callbacks:
            callback(self._is_expanded, self._width)
    
    @property
    def collapsed_width(self):
        return self._collapsed_width
    
    @property
    def current_width(self):
        return self._width
    
    @property
    def height(self):
        return self._height
    
    @property
    def is_expanded(self):
        return self._is_expanded


# 兼容别名
用户信息模块 = UserInfoModule


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    def main(page: ft.Page):
        page.padding = 0
        config = 界面配置()
        user_info = UserInfoModule(config, page)
        page.add(user_info.render())
    
    ft.run(main)
