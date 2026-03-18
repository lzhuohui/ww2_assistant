# -*- coding: utf-8 -*-
"""
模块名称：账号界面 | 层级：界面模块层
设计思路：
    使用通用卡片创建账号设置界面。
    固定15个账号栏，开关控制参与挂机状态。
    输入框拆分为名称/账号/密码三个独立输入框，防止用户输错格式。

功能：
    1. 显示15个账号卡片
    2. 开关控制参与挂机状态
    3. 开关状态不影响控件操作
    4. 计数机制：开关打开且输入有效时计数+1
    5. 授权限制：超过授权数量禁止打开开关
    6. 输入验证：名称/账号/密码都不为空时才有效
    7. 计数显示：页面顶部显示"已启用: X/Y"

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


# *** 用户指定变量 - AI不得修改 ***
DROPDOWN_WIDTH = 70  # 下拉框宽度
INPUT_WIDTH = 160    # 输入框宽度
CONTROL_HEIGHT = 32  # 控件高度
# *********************************

MAX_ACCOUNTS = 15
DEFAULT_AUTHORIZED_COUNT = 15


class AccountInterface:
    """账号界面 - 界面模块层"""
    
    授权数量 = DEFAULT_AUTHORIZED_COUNT
    当前参与数量 = 0
    账号开关状态 = {}
    
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
        theme_colors = 配置.当前主题颜色
        
        try:
            config_manager = ConfigManager()
        except ImportError:
            config_manager = None
        
        AccountInterface.授权数量 = DEFAULT_AUTHORIZED_COUNT
        AccountInterface.当前参与数量 = 0
        AccountInterface.账号开关状态 = {}
        
        for i in range(1, MAX_ACCOUNTS + 1):
            card_name = f"{i:02d}账号"
            enabled = config_manager.get_value(card_name, "开关", False) if config_manager else False
            name = config_manager.get_value(card_name, "名称", "") if config_manager else ""
            account = config_manager.get_value(card_name, "账号", "") if config_manager else ""
            password = config_manager.get_value(card_name, "密码", "") if config_manager else ""
            AccountInterface.账号开关状态[card_name] = enabled
            if enabled and name and account and password:
                AccountInterface.当前参与数量 += 1
        
        count_text = ft.Text(
            f"已启用: {AccountInterface.当前参与数量}/{AccountInterface.授权数量}",
            size=14,
            color=theme_colors.get("text_secondary"),
        )
        
        card_refs = {}
        
        def get_subtitle(enabled: bool, name: str, account: str, password: str) -> str:
            """获取副标题"""
            if not enabled:
                return "未参与挂机"
            if not name or not account or not password:
                return "请填写完整的账号信息"
            return f"已配置: {name}"
        
        def can_participate(enabled: bool, name: str, account: str, password: str) -> bool:
            """判断是否可以参与挂机"""
            return enabled and bool(name) and bool(account) and bool(password)
        
        def update_subtitle_and_count(card_name: str, card: ft.Container, enabled: bool, name: str, account: str, password: str) -> bool:
            """更新副标题和计数"""
            old_can = can_participate(
                AccountInterface.账号开关状态.get(card_name, False),
                config_manager.get_value(card_name, "名称", "") if config_manager else "",
                config_manager.get_value(card_name, "账号", "") if config_manager else "",
                config_manager.get_value(card_name, "密码", "") if config_manager else "",
            )
            
            new_can = can_participate(enabled, name, account, password)
            
            if new_can and not old_can:
                if AccountInterface.当前参与数量 >= AccountInterface.授权数量:
                    return False
                AccountInterface.当前参与数量 += 1
            elif not new_can and old_can:
                AccountInterface.当前参与数量 -= 1
            
            AccountInterface.账号开关状态[card_name] = enabled
            
            subtitle = get_subtitle(enabled, name, account, password)
            if card:
                card.set_subtitle(subtitle)
            
            count_text.value = f"已启用: {AccountInterface.当前参与数量}/{AccountInterface.授权数量}"
            try:
                if count_text.page:
                    count_text.update()
            except RuntimeError:
                pass
            
            return True
        
        def on_value_change(card_name: str, config_key: str, value):
            """值变化回调 - 保存配置并更新副标题"""
            print(f"配置变化: {card_name}.{config_key} = {value}")
            if config_manager:
                config_manager.set_value(card_name, config_key, value)
            
            if card_name in card_refs:
                card = card_refs[card_name]
                current_enabled = AccountInterface.账号开关状态.get(card_name, False)
                current_name = config_manager.get_value(card_name, "名称", "") if config_manager else ""
                current_account = config_manager.get_value(card_name, "账号", "") if config_manager else ""
                current_password = config_manager.get_value(card_name, "密码", "") if config_manager else ""
                
                subtitle = get_subtitle(current_enabled, current_name, current_account, current_password)
                card.set_subtitle(subtitle)
                
                try:
                    if card.page:
                        card.update()
                except RuntimeError:
                    pass
        
        def create_dropdown_control(options: list, value: str, card_name: str, config_key: str, width: int = DROPDOWN_WIDTH, height: int = CONTROL_HEIGHT):
            """创建下拉框控件（无标签）"""
            dropdown = Dropdown.create(
                options=options,
                value=value,
                width=width,
                height=height,
                on_change=lambda v: on_value_change(card_name, config_key, v),
            )
            return dropdown
        
        def create_input_control(value: str, card_name: str, config_key: str, width: int = INPUT_WIDTH, height: int = CONTROL_HEIGHT, hint_text: str = "", password: bool = False):
            """创建输入框控件（无标签）"""
            input_control = Input.create(
                config=配置,
                value=value,
                width=width,
                height=height,
                hint_text=hint_text,
                password=password,
                on_change=lambda v: on_value_change(card_name, config_key, v),
            )
            return input_control
        
        account_cards = []
        
        for i in range(1, MAX_ACCOUNTS + 1):
            card_name = f"{i:02d}账号"
            default_role = "主帅" if i == 1 else "副帅"
            
            role_value = config_manager.get_value(card_name, "统帅种类", default_role) if config_manager else default_role
            name_value = config_manager.get_value(card_name, "名称", "") if config_manager else ""
            account_value = config_manager.get_value(card_name, "账号", "") if config_manager else ""
            password_value = config_manager.get_value(card_name, "密码", "") if config_manager else ""
            platform_value = config_manager.get_value(card_name, "平台", "Tap") if config_manager else "Tap"
            switch_value = config_manager.get_value(card_name, "开关", False) if config_manager else False
            
            if config_manager:
                config_manager.set_value(card_name, "开关", switch_value)
                config_manager.set_value(card_name, "统帅种类", role_value)
                config_manager.set_value(card_name, "名称", name_value)
                config_manager.set_value(card_name, "账号", account_value)
                config_manager.set_value(card_name, "密码", password_value)
                config_manager.set_value(card_name, "平台", platform_value)
            
            role_control = create_dropdown_control(
                options=["主帅", "副帅"],
                value=role_value,
                card_name=card_name,
                config_key="统帅种类",
            )
            
            name_control = create_input_control(
                value=name_value,
                card_name=card_name,
                config_key="名称",
                hint_text="请输入统帅名称",
            )
            
            account_control = create_input_control(
                value=account_value,
                card_name=card_name,
                config_key="账号",
                hint_text="请输入统帅账号",
            )
            
            password_control = create_input_control(
                value=password_value,
                card_name=card_name,
                config_key="密码",
                hint_text="请输入统帅密码",
                password=True,
            )
            
            platform_control = create_dropdown_control(
                options=["Tap", "九游", "Fan", "小7", "Vivo", "Opop"],
                value=platform_value,
                card_name=card_name,
                config_key="平台",
            )
            
            def make_state_change_handler(cn, card_ref):
                """创建状态变化处理器"""
                def handler(enabled: bool):
                    current_name = config_manager.get_value(cn, "名称", "") if config_manager else ""
                    current_account = config_manager.get_value(cn, "账号", "") if config_manager else ""
                    current_password = config_manager.get_value(cn, "密码", "") if config_manager else ""
                    
                    if enabled:
                        if not update_subtitle_and_count(cn, card_ref, enabled, current_name, current_account, current_password):
                            AccountInterface.账号开关状态[cn] = False
                            if card_ref:
                                card_ref.set_state(False)
                            return
                    else:
                        if config_manager:
                            config_manager.set_value(cn, "开关", False)
                        update_subtitle_and_count(cn, card_ref, enabled, current_name, current_account, current_password)
                    
                    if config_manager:
                        config_manager.set_value(cn, "开关", enabled)
                return handler
            
            initial_enabled = switch_value
            subtitle_text = get_subtitle(initial_enabled, name_value, account_value, password_value)
            
            card = UniversalCard.create(
                title=card_name,
                icon="ACCOUNT_CIRCLE",
                enabled=initial_enabled,
                on_state_change=make_state_change_handler(card_name, None),
                controls=[role_control, name_control, account_control, password_control, platform_control],
                controls_per_row=5,
                subtitle=subtitle_text,
            )
            
            card._on_state_change = make_state_change_handler(card_name, card)
            
            card_refs[card_name] = card
            
            account_cards.append(card)
        
        header_content = ft.Row(
            [
                ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=20, color=theme_colors.get("accent")),
                ft.Container(width=8),
                ft.Text(
                    "账号设置",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color=theme_colors.get("text_primary"),
                ),
                ft.Container(width=20),
                count_text,
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        
        divider = ft.Container(
            content=ft.Divider(
                height=1,
                thickness=1,
                color=theme_colors.get("border"),
            ),
            opacity=0.5,
        )
        
        card_list = ft.Column(
            controls=account_cards,
            spacing=5,
            expand=True,
            scroll=ft.ScrollMode.HIDDEN,
        )
        
        content = ft.Column(
            controls=[
                header_content,
                divider,
                card_list,
            ],
            spacing=8,
            expand=True,
        )
        
        from 前端.用户设置界面.单元模块.通用容器 import GenericContainer
        return GenericContainer.create(
            content=content,
            expand=True,
            padding=16,
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
