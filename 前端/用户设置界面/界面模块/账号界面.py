# -*- coding: utf-8 -*-
"""
模块名称：账号界面 | 层级：界面模块层
设计思路：
    账号界面，包含账号管理、自动切换等设置卡片。
    使用配置管理器获取和保存配置值。

功能：
    1. 账号管理设置
    2. 自动切换设置

对外接口：
    - create(): 创建账号界面
"""

import flet as ft
from typing import Callable
from 前端.配置.界面配置 import 界面配置
from 前端.配置.配置管理器 import ConfigManager
from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider
from 前端.用户设置界面.组件模块.通用卡片 import UniversalCard
from 前端.用户设置界面.组件模块.功能容器 import FunctionContainer
from 前端.用户设置界面.单元模块.下拉框 import Dropdown


class AccountInterface:
    """账号界面 - 界面模块层"""
    
    @staticmethod
    def create(page: ft.Page = None, on_refresh: Callable[[], None] = None) -> ft.Container:
        """
        创建账号界面
        
        参数：
            page: 页面对象（可选，用于更新页面显示）
            on_refresh: 刷新回调
        
        返回：
            ft.Container: 账号界面容器
        """
        配置 = 界面配置()
        
        try:
            config_manager = ConfigManager()
        except ImportError:
            config_manager = None
        
        def on_value_change(card_name: str, config_key: str, value):
            """值变化回调 - 保存配置"""
            print(f"配置变化: {card_name}.{config_key} = {value}")
            if config_manager:
                config_manager.set_value(card_name, config_key, value)
        
        def create_dropdown_control(label: str, options: list, value: str, card_name: str, config_key: str, width: int = None):
            """创建下拉框控件"""
            dropdown = Dropdown.create(
                options=options,
                value=value,
                width=width,
                on_change=lambda v: on_value_change(card_name, config_key, v),
            )
            
            label_text = ft.Text(
                label,
                color=ThemeProvider.get_color("text_secondary"),
                size=14,
            )
            
            return ft.Row(
                [label_text, dropdown],
                alignment=ft.MainAxisAlignment.END,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8,
                expand=True,
            )
        
        account_value = config_manager.get_value("账号管理", "管理模式", "自动") if config_manager else "自动"
        account_control = create_dropdown_control(
            label="管理模式:",
            options=["自动", "手动"],
            value=account_value,
            card_name="账号管理",
            config_key="管理模式",
        )
        
        account_card = UniversalCard.create(
            title="账号管理",
            icon="ACCOUNT_CIRCLE",
            subtitle="管理多个游戏账号，支持自动切换",
            enabled=True,
            controls=[account_control],
        )
        
        switch_value = config_manager.get_value("自动切换", "切换模式", "顺序") if config_manager else "顺序"
        switch_control = create_dropdown_control(
            label="切换模式:",
            options=["顺序", "随机", "按等级"],
            value=switch_value,
            card_name="自动切换",
            config_key="切换模式",
        )
        
        switch_card = UniversalCard.create(
            title="自动切换",
            icon="SWAP_HORIZ",
            subtitle="设置账号切换模式，优化多账号管理",
            enabled=True,
            controls=[switch_control],
        )
        
        return FunctionContainer.create(
            config=配置,
            title="账号设置",
            icon="ACCOUNT_CIRCLE",
            cards=[account_card, switch_card],
            expand=True,
        )


# *** 调试逻辑 ***
if __name__ == "__main__":
    配置 = 界面配置()
    ThemeProvider.initialize(配置)
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        page.add(AccountInterface.create())
    ft.run(main)