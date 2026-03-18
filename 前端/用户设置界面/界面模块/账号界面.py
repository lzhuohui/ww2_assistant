# -*- coding: utf-8 -*-
"""
模块名称：账号界面 | 层级：界面模块层
设计思路：
    账号界面，包含15个账号设置卡片。
    每个账号包含：统帅种类、输入框、平台。
    使用配置管理器获取和保存配置值。

功能：
    1. 15个账号设置卡片
    2. 每个账号支持统帅种类、输入框、平台设置

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
from 前端.用户设置界面.单元模块.输入框 import Input


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
        
        def create_dropdown_control(label: str, options: list, value: str, card_name: str, config_key: str, width: int = 80):
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
        
        def create_input_control(label: str, value: str, card_name: str, config_key: str, width: int = 100):
            """创建输入框控件"""
            input_control = Input.create(
                config=配置,
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
                [label_text, input_control],
                alignment=ft.MainAxisAlignment.END,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8,
                expand=True,
            )
        
        account_cards = []
        
        for i in range(1, 16):
            card_name = f"{i:02d}账号"
            default_role = "主帅" if i == 1 else "副帅"
            
            role_value = config_manager.get_value(card_name, "统帅种类", default_role) if config_manager else default_role
            role_control = create_dropdown_control(
                label="统帅:",
                options=["主帅", "副帅"],
                value=role_value,
                card_name=card_name,
                config_key="统帅种类",
                width=80,
            )
            
            input_value = config_manager.get_value(card_name, "输入框", "") if config_manager else ""
            input_control = create_input_control(
                label="账号:",
                value=input_value,
                card_name=card_name,
                config_key="输入框",
                width=100,
            )
            
            platform_value = config_manager.get_value(card_name, "平台", "Tap") if config_manager else "Tap"
            platform_control = create_dropdown_control(
                label="平台:",
                options=["Tap", "九游", "Fan", "小7", "Vivo", "Opop"],
                value=platform_value,
                card_name=card_name,
                config_key="平台",
                width=80,
            )
            
            card = UniversalCard.create(
                title=card_name,
                icon="ACCOUNT_CIRCLE",
                enabled=True,
                controls=[role_control, input_control, platform_control],
                controls_per_row=3,
            )
            account_cards.append(card)
        
        return FunctionContainer.create(
            config=配置,
            title="账号设置",
            icon="ACCOUNT_CIRCLE",
            cards=account_cards,
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
    ft.app(target=main)
