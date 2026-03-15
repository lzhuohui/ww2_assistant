# -*- coding: utf-8 -*-
"""
账号设置页面 - 页面层

设计思路:
    使用通用卡片创建账号设置页面。
    固定15个账号栏，开关控制参与挂机状态。
    输入框拆分为名称/账号/密码三个独立输入框，防止用户输错格式。

功能:
    1. 显示15个账号卡片
    2. 开关控制参与挂机状态
    3. 开关状态不影响控件操作
    4. 计数机制：开关打开且输入有效时计数+1
    5. 授权限制：超过授权数量禁止打开开关
    6. 输入验证：名称/账号/密码都不为空时才有效

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
            name = config_manager.get_value(f"{i:02d}账号", "名称", "")
            account = config_manager.get_value(f"{i:02d}账号", "账号", "")
            password = config_manager.get_value(f"{i:02d}账号", "密码", "")
            AccountSettingsPage.账号开关状态[i] = enabled
            if enabled and name and account and password:
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
            account_cards.append(ft.Container(height=5))
        
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
                ft.Container(height=4),
                *account_cards,
            ],
            spacing=0,
            scroll=ft.ScrollMode.HIDDEN,
            expand=True,
        )
        
        page_container = ft.Container(
            content=page_content,
            padding=ft.Padding.all(0),
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
        name_value = config_manager.get_value(f"{index:02d}账号", "名称", "")
        account_value = config_manager.get_value(f"{index:02d}账号", "账号", "")
        password_value = config_manager.get_value(f"{index:02d}账号", "密码", "")
        
        def get_subtitle(enabled: bool, name: str, account: str, password: str) -> str:
            """获取副标题"""
            if not enabled:
                return "未参与挂机"
            if not name or not account or not password:
                return "请填写完整的账号信息"
            return f"已配置: {name}"
        
        subtitle_text = get_subtitle(initial_enabled, name_value, account_value, password_value)
        
        card = None
        
        def can_participate(enabled: bool, name: str, account: str, password: str) -> bool:
            """判断是否可以参与挂机"""
            return enabled and bool(name) and bool(account) and bool(password)
        
        def update_subtitle_and_count(enabled: bool, name: str, account: str, password: str):
            """更新副标题和计数"""
            nonlocal card
            
            old_can = can_participate(
                AccountSettingsPage.账号开关状态.get(index, False),
                config_manager.get_value(f"{index:02d}账号", "名称", ""),
                config_manager.get_value(f"{index:02d}账号", "账号", ""),
                config_manager.get_value(f"{index:02d}账号", "密码", ""),
            )
            
            new_can = can_participate(enabled, name, account, password)
            
            if new_can and not old_can:
                if AccountSettingsPage.当前参与数量 >= AccountSettingsPage.授权数量:
                    return False
                AccountSettingsPage.当前参与数量 += 1
            elif not new_can and old_can:
                AccountSettingsPage.当前参与数量 -= 1
            
            AccountSettingsPage.账号开关状态[index] = enabled
            
            subtitle = get_subtitle(enabled, name, account, password)
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
            current_name = config_manager.get_value(f"{index:02d}账号", "名称", "")
            current_account = config_manager.get_value(f"{index:02d}账号", "账号", "")
            current_password = config_manager.get_value(f"{index:02d}账号", "密码", "")
            return update_subtitle_and_count(enabled, current_name, current_account, current_password)
        
        def on_role_change(value: str):
            config_manager.set_value(f"{index:02d}账号", "统帅种类", value)
        
        def on_name_change(value: str):
            config_manager.set_value(f"{index:02d}账号", "名称", value)
            current_enabled = config_manager.get_value(f"{index:02d}账号", "开关", False)
            current_account = config_manager.get_value(f"{index:02d}账号", "账号", "")
            current_password = config_manager.get_value(f"{index:02d}账号", "密码", "")
            update_subtitle_and_count(current_enabled, value, current_account, current_password)
        
        def on_account_change(value: str):
            config_manager.set_value(f"{index:02d}账号", "账号", value)
            current_enabled = config_manager.get_value(f"{index:02d}账号", "开关", False)
            current_name = config_manager.get_value(f"{index:02d}账号", "名称", "")
            current_password = config_manager.get_value(f"{index:02d}账号", "密码", "")
            update_subtitle_and_count(current_enabled, current_name, value, current_password)
        
        def on_password_change(value: str):
            config_manager.set_value(f"{index:02d}账号", "密码", value)
            current_enabled = config_manager.get_value(f"{index:02d}账号", "开关", False)
            current_name = config_manager.get_value(f"{index:02d}账号", "名称", "")
            current_account = config_manager.get_value(f"{index:02d}账号", "账号", "")
            update_subtitle_and_count(current_enabled, current_name, current_account, value)
        
        def on_platform_change(value: str):
            config_manager.set_value(f"{index:02d}账号", "平台", value)
        
        role_value = config_manager.get_value(f"{index:02d}账号", "统帅种类", "主帅" if index == 1 else "副帅")
        platform_value = config_manager.get_value(f"{index:02d}账号", "平台", "Tap")
        switch_value = config_manager.get_value(f"{index:02d}账号", "开关", False)
        
        config_manager.set_value(f"{index:02d}账号", "开关", switch_value)
        config_manager.set_value(f"{index:02d}账号", "统帅种类", role_value)
        config_manager.set_value(f"{index:02d}账号", "名称", name_value)
        config_manager.set_value(f"{index:02d}账号", "账号", account_value)
        config_manager.set_value(f"{index:02d}账号", "密码", password_value)
        config_manager.set_value(f"{index:02d}账号", "平台", platform_value)
        
        role_dropdown = LabelDropdown.create(
            config=config,
            label="",
            options=["主帅", "副帅"],
            value=role_value,
            width=80,
            on_change=on_role_change,
        )
        
        name_input = LabelInput.create(
            config=config,
            label="",
            value=name_value,
            width=200,
            hint_text="请输入统帅名称",
            on_change=on_name_change,
        )
        
        account_input = LabelInput.create(
            config=config,
            label="",
            value=account_value,
            width=200,
            hint_text="请输入统帅账号",
            on_change=on_account_change,
        )
        
        password_input = LabelInput.create(
            config=config,
            label="",
            value=password_value,
            width=200,
            hint_text="请输入统帅密码",
            password=True,
            on_change=on_password_change,
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
            controls=[role_dropdown, name_input, account_input, password_input, platform_dropdown],
            controls_per_row=5,
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
