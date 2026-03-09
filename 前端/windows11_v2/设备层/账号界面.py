# -*- coding: utf-8 -*-
"""
账号界面 - 设备层

设计思路:
    本模块是设备层模块，提供账号界面。

功能:
    1. 继承基础界面
    2. 提供账号相关功能
    3. 包含多账号管理

数据来源:
    主题颜色从界面配置获取。

使用场景:
    被系统层调用，提供账号界面。

可独立运行调试: python 账号界面.py
"""

import flet as ft
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from 原子层.界面配置 import 界面配置
from 设备层.基础界面 import BaseInterface


class AccountInterface(BaseInterface):  # 账号界面
    """账号界面 - 提供账号功能"""
    
    def __init__(self, config: 界面配置, page: ft.Page):
        super().__init__(config, page, title="账号设置", subtitle="账号相关配置")
        self._account_count = 15
    
    def _create_content_area(self) -> ft.Control:  # 创建内容区域
        account_list = []
        for i in range(1, self._account_count + 1):
            account_list.append(self._create_account_row(i))
            if i < self._account_count:
                account_list.append(ft.Divider(height=self._margin, color="transparent"))
        
        return ft.Column([
            self._create_account_count_card(),
            ft.Divider(height=self._margin * 2, color="transparent"),
            self._create_account_list_card(account_list),
        ], spacing=0)
    
    def _create_account_count_card(self) -> ft.Container:  # 创建账号数量卡片
        items = [
            ft.Text("账号数量:", color=self._config.获取颜色("text_primary")),
            ft.Dropdown(
                options=[ft.dropdown.Option(str(i)) for i in range(1, 16)],
                value="15",
                width=200,
                bgcolor=self._config.获取颜色("bg_secondary"),
                color=self._config.获取颜色("text_primary")
            )
        ]
        return self._create_card("账号数量", items)
    
    def _create_account_row(self, index: int) -> ft.Row:  # 创建账号设置行
        return ft.Row([
            ft.Text(f"{index:02d}", width=30, color=self._config.获取颜色("text_primary")),
            ft.Switch(value=(index == 1)),
            ft.Dropdown(
                options=[
                    ft.dropdown.Option("主帅"),
                    ft.dropdown.Option("付帅")
                ],
                value="主帅" if index == 1 else "付帅",
                width=80,
                bgcolor=self._config.获取颜色("bg_secondary"),
                color=self._config.获取颜色("text_primary")
            ),
            ft.TextField(
                label="账号",
                width=200,
                bgcolor=self._config.获取颜色("bg_secondary"),
                color=self._config.获取颜色("text_primary")
            ),
            ft.Dropdown(
                options=[
                    ft.dropdown.Option("Tap"),
                    ft.dropdown.Option("官方"),
                    ft.dropdown.Option("其他")
                ],
                value="Tap",
                width=100,
                bgcolor=self._config.获取颜色("bg_secondary"),
                color=self._config.获取颜色("text_primary")
            )
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    
    def _create_account_list_card(self, account_list: list) -> ft.Container:  # 创建账号列表卡片
        return self._create_card("挂机账号", account_list)


# 兼容别名
账号界面 = AccountInterface


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    config = 界面配置()
    
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = config.获取颜色("bg_primary")
        interface = AccountInterface(config, page)
        page.add(interface.render())
    
    ft.run(main)
