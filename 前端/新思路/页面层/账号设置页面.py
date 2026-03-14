# -*- coding: utf-8 -*-
"""
账号设置页面 - 页面层

设计思路:
    使用通用卡片创建账号设置页面。
    固定15个账号栏，开关控制参与挂机状态。

功能:
    1. 显示15个账号卡片
    2. 开关控制参与挂机状态
    3. 开关状态不影响控件操作
    4. 计数机制：开关打开且输入有效时计数+1
    5. 授权限制：超过授权数量禁止打开开关
    6. 输入格式验证：格式错误时副标题显示提示

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
from 新思路.组件层.通用卡片 import UniversalCard
from 新思路.零件层.标签下拉框 import LabelDropdown
from 新思路.零件层.标签输入框 import LabelInput
from 配置.账号配置 import MAX_ACCOUNTS, DEFAULT_AUTHORIZED_COUNT
from 新思路.工具层.输入验证 import validate_account_input, get_subtitle_by_state, can_participate


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
            enabled = config_manager.get_value(f"{i:02d}账号", "开关", False)
            input_value = config_manager.get_value(f"{i:02d}账号", "输入框", "")
            AccountSettingsPage.账号开关状态[i] = enabled
            if can_participate(enabled, input_value):
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
        input_value = config_manager.get_value(f"{index:02d}账号", "输入框", "")
        subtitle_text = get_subtitle_by_state(initial_enabled, input_value)
        
        card = None
        
        def update_subtitle_and_count(enabled: bool, input_text: str):
            """更新副标题和计数"""
            nonlocal card
            
            old_can_participate = can_participate(
                AccountSettingsPage.账号开关状态.get(index, False),
                config_manager.get_value(f"{index:02d}账号", "输入框", "")
            )
            
            new_can_participate = can_participate(enabled, input_text)
            
            if new_can_participate and not old_can_participate:
                if AccountSettingsPage.当前参与数量 >= AccountSettingsPage.授权数量:
                    return False
                AccountSettingsPage.当前参与数量 += 1
            elif not new_can_participate and old_can_participate:
                AccountSettingsPage.当前参与数量 -= 1
            
            AccountSettingsPage.账号开关状态[index] = enabled
            
            subtitle = get_subtitle_by_state(enabled, input_text)
            if card:
                card.set_subtitle(subtitle)
            
            count_text.value = f"已启用: {AccountSettingsPage.当前参与数量}/{AccountSettingsPage.授权数量}"
            try:
                if count_text.page:
                    count_text.update()
            except RuntimeError:
                pass
            
            return True
        
        def on_state_change(enabled: bool):
            config_manager.set_value(f"{index:02d}账号", "开关", enabled)
            current_input = config_manager.get_value(f"{index:02d}账号", "输入框", "")
            return update_subtitle_and_count(enabled, current_input)
        
        def on_role_change(value: str):
            config_manager.set_value(f"{index:02d}账号", "统帅种类", value)
        
        def on_input_change(value: str):
            config_manager.set_value(f"{index:02d}账号", "输入框", value)
            current_enabled = config_manager.get_value(f"{index:02d}账号", "开关", False)
            update_subtitle_and_count(current_enabled, value)
        
        def on_platform_change(value: str):
            config_manager.set_value(f"{index:02d}账号", "平台", value)
        
        role_value = config_manager.get_value(f"{index:02d}账号", "统帅种类", "主帅" if index == 1 else "副帅")
        input_value = config_manager.get_value(f"{index:02d}账号", "输入框", "")
        platform_value = config_manager.get_value(f"{index:02d}账号", "平台", "Tap")
        switch_value = config_manager.get_value(f"{index:02d}账号", "开关", False)
        
        config_manager.set_value(f"{index:02d}账号", "开关", switch_value)
        config_manager.set_value(f"{index:02d}账号", "统帅种类", role_value)
        config_manager.set_value(f"{index:02d}账号", "输入框", input_value)
        config_manager.set_value(f"{index:02d}账号", "平台", platform_value)
        
        role_dropdown = LabelDropdown.create(
            config=config,
            label="",
            options=["主帅", "副帅"],
            value=role_value,
            width=80,
            on_change=on_role_change,
        )
        
        input_control = LabelInput.create(
            config=config,
            label="",
            value=input_value,
            width=350,
            hint_text="输入格式:名称/账号/密码",
            on_change=on_input_change,
        )
        
        platform_dropdown = LabelDropdown.create(
            config=config,
            label="",
            options=["Tap", "九游", "Fan", "小7", "Vivo", "Opop"],
            value=platform_value,
            width=80,
            on_change=on_platform_change,
        )
        
        card = UniversalCard.create(
            config=config,
            title=f"{index:02d}账号",
            icon="ACCOUNT_CIRCLE",
            enabled=initial_enabled,
            on_state_change=on_state_change,
            controls=[role_dropdown, input_control, platform_dropdown],
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
