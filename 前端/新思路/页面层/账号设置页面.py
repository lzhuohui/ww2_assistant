# -*- coding: utf-8 -*-
"""
账号设置页面 - 页面层

设计思路:
    使用开关下拉卡片创建账号设置页面。
    固定15个账号栏，开关控制参与挂机状态。

功能:
    1. 显示15个账号卡片
    2. 开关控制参与挂机状态
    3. 开关状态不影响控件操作
    4. 计数机制：开关打开时计数+1
    5. 授权限制：超过授权数量禁止打开开关

使用场景:
    被主界面调用。
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft
from typing import Callable
from 配置.界面配置 import 界面配置
from 配置.配置管理器 import ConfigManager
from 新思路.组件层.开关下拉卡片 import SwitchDropdownCard
from 配置.账号配置 import MAX_ACCOUNTS, DEFAULT_AUTHORIZED_COUNT


class AccountSettingsPage:
    """账号设置页面"""
    
    授权数量 = DEFAULT_AUTHORIZED_COUNT
    当前参与数量 = 0
    账号开关状态 = {}
    
    @staticmethod
    def create(config: 界面配置, page: ft.Page = None, on_refresh: Callable[[], None] = None) -> ft.Container:
        """
        创建账号设置页面
        
        参数:
            config: 界面配置对象
            page: 页面对象
            on_refresh: 刷新回调
        
        返回:
            ft.Container: 账号设置页面容器
        """
        theme_colors = config.当前主题颜色
        
        config_manager = ConfigManager()
        
        AccountSettingsPage.授权数量 = DEFAULT_AUTHORIZED_COUNT
        AccountSettingsPage.当前参与数量 = 0
        AccountSettingsPage.账号开关状态 = {}
        
        for i in range(1, MAX_ACCOUNTS + 1):
            card_config = config_manager.get_card_config(f"{i:02d}账号")
            default_enabled = card_config.get("enabled", False) if card_config else False
            enabled = config_manager.get_value(f"{i:02d}账号", "enabled", default_enabled)
            AccountSettingsPage.账号开关状态[i] = enabled
            if enabled:
                AccountSettingsPage.当前参与数量 += 1
        
        count_text = ft.Text(
            f"已启用: {AccountSettingsPage.当前参与数量}/{AccountSettingsPage.授权数量}",
            size=14,
            color=theme_colors.get("text_secondary"),
        )
        
        account_cards = []
        for i in range(1, MAX_ACCOUNTS + 1):
            card = AccountSettingsPage._create_account_card(
                config=config,
                config_manager=config_manager,
                index=i,
                count_text=count_text,
            )
            account_cards.append(card)
            account_cards.append(ft.Container(height=10))
        
        page_content = ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(
                            "账号设置",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color=theme_colors.get("text_primary"),
                        ),
                        ft.Container(width=20),
                        count_text,
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Container(height=20),
                *account_cards,
            ],
            spacing=0,
            scroll=ft.ScrollMode.HIDDEN,
            expand=True,
        )
        
        page_container = ft.Container(
            content=page_content,
            padding=ft.Padding.all(20),
            expand=True,
        )
        
        return page_container
    
    @staticmethod
    def _create_account_card(
        config: 界面配置,
        config_manager: ConfigManager,
        index: int,
        count_text: ft.Text,
    ) -> ft.Container:
        """创建单个账号卡片"""
        
        initial_enabled = AccountSettingsPage.账号开关状态.get(index, False)
        subtitle_text = "参与挂机" if initial_enabled else "禁止挂机"
        
        def on_state_change(enabled: bool):
            if enabled:
                if AccountSettingsPage.当前参与数量 >= AccountSettingsPage.授权数量:
                    return False
                AccountSettingsPage.当前参与数量 += 1
                AccountSettingsPage.账号开关状态[index] = True
                card.set_subtitle("参与挂机")
            else:
                AccountSettingsPage.当前参与数量 -= 1
                AccountSettingsPage.账号开关状态[index] = False
                card.set_subtitle("禁止挂机")
            
            count_text.value = f"已启用: {AccountSettingsPage.当前参与数量}/{AccountSettingsPage.授权数量}"
            try:
                if count_text.page:
                    count_text.update()
            except RuntimeError:
                pass
            
            return True
        
        def on_value_change(config_key: str, value: any):
            pass
        
        card_config = config_manager.get_card_config(f"{index:02d}账号")
        default_role = "主帅" if index == 1 else "副帅"
        if card_config:
            for control in card_config.get("controls", []):
                if control.get("config_key") == "统帅种类":
                    default_role = control.get("default", "主帅" if index == 1 else "副帅")
                    break
        
        settings = [
            {
                "type": "dropdown",
                "label": "",
                "options": ["主帅", "副帅"],
                "value": config_manager.get_value(f"{index:02d}账号", "统帅种类", default_role),
                "width": 80,
                "on_change": lambda v, idx=index: on_value_change(f"{idx:02d}账号_统帅种类", v),
            },
            {
                "type": "input",
                "label": "",
                "value": config_manager.get_value(f"{index:02d}账号", "输入框", ""),
                "width": 300,
                "hint_text": "输入格式:名称/账号/密码",
                "on_change": lambda v, idx=index: on_value_change(f"{idx:02d}账号_输入框", v),
            },
            {
                "type": "dropdown",
                "label": "",
                "options": ["平台1", "平台2", "平台3", "平台4", "平台5"],
                "value": config_manager.get_value(f"{index:02d}账号", "平台", "平台1"),
                "width": 80,
                "on_change": lambda v, idx=index: on_value_change(f"{idx:02d}账号_平台", v),
            },
        ]
        
        card = SwitchDropdownCard.create(
            config=config,
            title=f"{index:02d}账号",
            icon="ACCOUNT_CIRCLE",
            enabled=AccountSettingsPage.账号开关状态.get(index, False),
            on_state_change=on_state_change,
            settings=settings,
            controls_per_row=3,
            subtitle=subtitle_text,
        )
        
        return card


账号设置页面 = AccountSettingsPage


if __name__ == "__main__":
    配置 = 界面配置()
    
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        page.add(AccountSettingsPage.create(配置))
    
    ft.run(main)
