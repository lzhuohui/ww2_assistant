# -*- coding: utf-8 -*-
"""
模块名称：账号界面 | 层级：界面模块层
设计思路：
    账号界面，包含15个账号设置卡片。
    固定15个账号栏，开关控制参与挂机状态。
    输入框拆分为名称、账号、密码三个独立输入框。
    计数机制：开关打开且输入有效时计数+1。
    授权限制：超过授权数量禁止打开开关。

功能：
    1. 15个账号设置卡片
    2. 开关控制参与挂机状态
    3. 计数机制
    4. 授权限制
    5. 输入验证

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
DROPDOWN_WIDTH = 80  # 下拉框宽度
INPUT_WIDTH = 240    # 输入框宽度
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
        
        try:
            config_manager = ConfigManager()
        except ImportError:
            config_manager = None
        
        AccountInterface.授权数量 = DEFAULT_AUTHORIZED_COUNT
        AccountInterface.当前参与数量 = 0
        AccountInterface.账号开关状态 = {}
        
        def on_value_change(card_name: str, config_key: str, value):
            """值变化回调 - 保存配置"""
            print(f"配置变化: {card_name}.{config_key} = {value}")
            if config_manager:
                config_manager.set_value(card_name, config_key, value)
        
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
        
        def update_subtitle(card_name: str, card: ft.Container, enabled: bool):
            """更新副标题"""
            if enabled:
                name = config_manager.get_value(card_name, "名称", "") if config_manager else ""
                account = config_manager.get_value(card_name, "账号", "") if config_manager else ""
                password = config_manager.get_value(card_name, "密码", "") if config_manager else ""
                is_valid = bool(name and account and password)
                if is_valid:
                    card.set_subtitle("有效账号")
                else:
                    card.set_subtitle("信息不完整")
            else:
                card.set_subtitle("未参与挂机")
        
        def check_and_update_count():
            """检查并更新参与数量"""
            count = 0
            for i in range(1, MAX_ACCOUNTS + 1):
                card_name = f"{i:02d}账号"
                if AccountInterface.账号开关状态.get(card_name, False):
                    name = config_manager.get_value(card_name, "名称", "") if config_manager else ""
                    account = config_manager.get_value(card_name, "账号", "") if config_manager else ""
                    password = config_manager.get_value(card_name, "密码", "") if config_manager else ""
                    if name and account and password:
                        count += 1
            AccountInterface.当前参与数量 = count
        
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
            
            AccountInterface.账号开关状态[card_name] = switch_value
            
            if switch_value:
                name = name_value
                account = account_value
                password = password_value
                if name and account and password:
                    AccountInterface.当前参与数量 += 1
            
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
                    AccountInterface.账号开关状态[cn] = enabled
                    
                    if enabled:
                        check_and_update_count()
                        if AccountInterface.当前参与数量 > AccountInterface.授权数量:
                            AccountInterface.账号开关状态[cn] = False
                            if card_ref:
                                card_ref.set_state(False)
                            if config_manager:
                                config_manager.set_value(cn, "开关", False)
                            AccountInterface.当前参与数量 -= 1
                            return
                        
                        if config_manager:
                            config_manager.set_value(cn, "开关", enabled)
                        
                        if card_ref:
                            update_subtitle(cn, card_ref, enabled)
                    else:
                        if config_manager:
                            config_manager.set_value(cn, "开关", False)
                        check_and_update_count()
                        if card_ref:
                            update_subtitle(cn, card_ref, False)
                return handler
            
            initial_enabled = switch_value
            subtitle_text = "有效账号" if initial_enabled and name_value and account_value and password_value else ("未参与挂机" if not initial_enabled else "信息不完整")
            
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
    ft.run(main)
