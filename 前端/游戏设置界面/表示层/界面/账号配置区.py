# -*- coding: utf-8 -*-
"""
模块名称：AccountConfigSection
模块功能：账号配置区，包含15个账号卡片
实现步骤：
- 创建账号配置卡片
- 使用none销毁策略（不销毁控件）
- 支持参与状态计算
- 支持授权限制
- 支持副标题动态更新
"""

import flet as ft
from typing import Dict, Any, List, Callable, Optional

from 前端.游戏设置界面.核心层.配置.界面配置 import UIConfig
from 前端.游戏设置界面.表示层.组件.复合.卡片组管理器 import CardGroupManager, create_managed_card
from 前端.游戏设置界面.表示层.组件.基础.下拉框 import Dropdown
from 前端.游戏设置界面.表示层.组件.基础.输入框 import InputBox
from 前端.游戏设置界面.业务层.服务.配置服务 import ConfigService
from 前端.游戏设置界面.表示层.界面.配置方案区 import ConfigSchemeSection


# *** 用户指定变量: 变量值必须生效,AI不得更改数据 ***
USER_MAX_ACCOUNTS = 15  # 最大账号数量
USER_DROPDOWN_WIDTH = 68  # 下拉框宽度
USER_INPUT_WIDTH = 166  # 输入框宽度
USER_SCHEME_WIDTH = 100  # 配置方案下拉框宽度
USER_AUTHORIZED_COUNT = 15  # 授权账号数量
USER_CARD_SPACING = 10  # 卡片间距
USER_SPACING = 10  # 通用间距
# *********************************


class AccountConfigSection:
    """账号配置区 - 使用none策略（不销毁控件）"""
    
    授权数量 = USER_AUTHORIZED_COUNT
    当前参与数量 = 0
    账号开关状态: Dict[str, bool] = {}
    
    @staticmethod
    def create(
        config: UIConfig = None,
        config_service: ConfigService = None,
        save_callback: Callable[[str, str, str], None] = None,
        on_count_change: Callable[[int], None] = None,
    ) -> tuple:
        if config is None:
            config = UIConfig()
        if config_service is None:
            config_service = ConfigService()
        
        theme_colors = config.当前主题颜色
        manager = CardGroupManager()
        card_data: Dict[str, Dict[str, Any]] = {}
        card_refs: Dict[str, ft.Container] = {}
        
        AccountConfigSection.授权数量 = USER_AUTHORIZED_COUNT
        AccountConfigSection.当前参与数量 = 0
        AccountConfigSection.账号开关状态 = {}
        
        def get_subtitle(enabled: bool, name: str, account: str, password: str, is_expanded: bool = False) -> str:
            if not enabled:
                if is_expanded:
                    return "未参与挂机"
                else:
                    display_name = name if name else "未设置"
                    return f"{display_name} (未参与), 设置请进入"
            
            if not name or not account or not password:
                if is_expanded:
                    missing = []
                    if not name:
                        missing.append("名称")
                    if not account:
                        missing.append("账号")
                    if not password:
                        missing.append("密码")
                    return f"缺少: {'/'.join(missing)}"
                else:
                    display_name = name if name else "未设置"
                    return f"{display_name} (信息不完整), 设置请进入"
            
            if is_expanded:
                return f"已配置: {name}"
            else:
                return f"{name} (参与挂机), 设置请进入"
        
        def can_participate(enabled: bool, name: str, account: str, password: str) -> bool:
            return enabled and bool(name) and bool(account) and bool(password)
        
        def update_subtitle_and_count(
            card_name: str,
            card: ft.Container,
            enabled: bool,
            name: str,
            account: str,
            password: str,
            is_expanded: bool = False
        ) -> bool:
            old_can = can_participate(
                AccountConfigSection.账号开关状态.get(card_name, False),
                card_data.get(card_name, {}).get("名称", ""),
                card_data.get(card_name, {}).get("账号", ""),
                card_data.get(card_name, {}).get("密码", ""),
            )
            
            new_can = can_participate(enabled, name, account, password)
            
            if new_can and not old_can:
                if AccountConfigSection.当前参与数量 >= AccountConfigSection.授权数量:
                    return False
                AccountConfigSection.当前参与数量 += 1
            elif not new_can and old_can:
                AccountConfigSection.当前参与数量 -= 1
            
            AccountConfigSection.账号开关状态[card_name] = enabled
            
            subtitle = get_subtitle(enabled, name, account, password, is_expanded)
            if card and hasattr(card, 'set_subtitle'):
                card.set_subtitle(subtitle, is_expanded)
            
            if on_count_change:
                on_count_change(AccountConfigSection.当前参与数量)
            
            return True
        
        def handle_save(card_id: str, config_key: str, value: str):
            if card_id not in card_data:
                card_data[card_id] = {}
            card_data[card_id][config_key] = value
            if save_callback:
                save_callback(card_id, config_key, value)
            
            if card_id in card_refs:
                card = card_refs[card_id]
                current_enabled = AccountConfigSection.账号开关状态.get(card_id, False)
                current_name = card_data.get(card_id, {}).get("名称", "")
                current_account = card_data.get(card_id, {}).get("账号", "")
                current_password = card_data.get(card_id, {}).get("密码", "")
                is_expanded = card.is_loaded() if hasattr(card, 'is_loaded') else False
                
                update_subtitle_and_count(card_id, card, current_enabled, current_name, current_account, current_password, is_expanded)
        
        def create_card(
            card_id: str,
            title: str,
            icon: str,
            default_type: str = "副帅",
            enabled: bool = False,
        ) -> ft.Container:
            current_name = config_service.get_value(card_id, "名称")
            if current_name is None:
                current_name = ""
                if save_callback:
                    save_callback(card_id, "名称", "")
            
            current_account = config_service.get_value(card_id, "账号")
            if current_account is None:
                current_account = ""
                if save_callback:
                    save_callback(card_id, "账号", "")
            
            current_password = config_service.get_value(card_id, "密码")
            if current_password is None:
                current_password = ""
                if save_callback:
                    save_callback(card_id, "密码", "")
            
            saved_enabled = config_service.get_value(card_id, "enabled")
            if saved_enabled is None:
                saved_enabled = enabled
                if save_callback:
                    save_callback(card_id, "enabled", str(enabled))
            
            saved_type = config_service.get_value(card_id, "类型")
            if saved_type is None:
                saved_type = default_type
                if save_callback:
                    save_callback(card_id, "类型", default_type)
           
            
            saved_platform = config_service.get_value(card_id, "平台")
            if saved_platform is None:
                saved_platform = "Tap"
                if save_callback:
                    save_callback(card_id, "平台", "Tap")
            
            saved_scheme = config_service.get_value(card_id, "配置方案") or ""
            
            card_data[card_id] = {
                "名称": current_name,
                "账号": current_account,
                "密码": current_password,
                "enabled": saved_enabled,
                "类型": saved_type,
                "平台": saved_platform,
                "配置方案": saved_scheme,
            }
            
            AccountConfigSection.账号开关状态[card_id] = saved_enabled
            
            if saved_enabled and current_name and current_account and current_password:
                AccountConfigSection.当前参与数量 += 1
            
            subtitle = get_subtitle(saved_enabled, current_name, current_account, current_password, False)
            
            def handle_expand():
                current_enabled = AccountConfigSection.账号开关状态.get(card_id, False)
                current_name = card_data.get(card_id, {}).get("名称", "")
                current_account = card_data.get(card_id, {}).get("账号", "")
                current_password = card_data.get(card_id, {}).get("密码", "")
                update_subtitle_and_count(card_id, card, current_enabled, current_name, current_account, current_password, True)
            
            def handle_collapse():
                current_enabled = AccountConfigSection.账号开关状态.get(card_id, False)
                current_name = card_data.get(card_id, {}).get("名称", "")
                current_account = card_data.get(card_id, {}).get("账号", "")
                current_password = card_data.get(card_id, {}).get("密码", "")
                update_subtitle_and_count(card_id, card, current_enabled, current_name, current_account, current_password, False)
            
            type_dropdown = Dropdown.create(
                options=["主帅", "副帅"],
                current_value=saved_type,
                width=USER_DROPDOWN_WIDTH,
                enabled=True,
                on_change=lambda v: handle_save(card_id, "类型", v),
                config=config,
            )
            
            platform_dropdown = Dropdown.create(
                options=["Tap", "九游", "Fan", "小7", "Vivo", "Opop"],
                current_value=saved_platform,
                width=USER_DROPDOWN_WIDTH,
                enabled=True,
                on_change=lambda v: handle_save(card_id, "平台", v),
                config=config,
            )
            
            name_input = InputBox.create(
                config=config,
                hint_text="输入统帅名称",
                width=USER_INPUT_WIDTH,
                enabled=True,
                on_change=lambda v: handle_save(card_id, "名称", v),
                value=current_name,
            )
            
            account_input = InputBox.create(
                config=config,
                hint_text="输入统帅账号",
                width=USER_INPUT_WIDTH,
                enabled=True,
                on_change=lambda v: handle_save(card_id, "账号", v),
                value=current_account,
            )
            
            password_input = InputBox.create(
                config=config,
                hint_text="输入统帅密码",
                width=USER_INPUT_WIDTH,
                password_mode=True,
                enabled=True,
                on_change=lambda v: handle_save(card_id, "密码", v),
                value=current_password,
            )
            
            scheme_names = ConfigSchemeSection.get_scheme_names()
            scheme_options = ["默认配置"] + scheme_names if scheme_names else ["默认配置"]
            scheme_display = saved_scheme if saved_scheme in scheme_options else "默认配置"
            
            scheme_dropdown = Dropdown.create(
                options=scheme_options,
                current_value=scheme_display,
                width=USER_SCHEME_WIDTH,
                enabled=True,
                on_change=lambda v: handle_save(card_id, "配置方案", v),
                config=config,
            )
            
            controls = [
                type_dropdown,
                name_input,
                account_input,
                password_input,
                scheme_dropdown,
                platform_dropdown,
            ]
            
            card = create_managed_card(
                manager=manager,
                title=title,
                icon=icon,
                subtitle=subtitle,
                enabled=saved_enabled,
                controls=controls,
                controls_per_row=6,
                on_save=lambda key, value: handle_save(card_id, key, value),
                config=config,
            )
            
            card_refs[card_id] = card
            return card
        
        card_list = []
        
        for i in range(1, USER_MAX_ACCOUNTS + 1):
            card_id = f"account_{i:02d}"
            title = f"{i:02d}账号"
            default_type = "主帅" if i == 1 else "副帅"
            
            card_list.append(create_card(
                card_id=card_id,
                title=title,
                icon="ACCOUNT_CIRCLE",
                default_type=default_type,
            ))
        
        card_column = ft.Column(
            controls=card_list,
            spacing=USER_CARD_SPACING,
            scroll=ft.ScrollMode.HIDDEN,
            expand=True,
        )
        
        content_column = ft.Column(
            controls=[
                card_column,
            ],
            spacing=0,
            expand=True,
        )
        
        content_column.card_manager = manager
        

        
        return content_column, manager


# *** 标准测试格式: 仅调用被测模块,AI不得添加数据 ***
if __name__ == "__main__":
    def main(page: ft.Page):
        config = UIConfig()
        service = ConfigService()
        section, manager = AccountConfigSection.create(config=config, config_service=service)
        page.add(section)
    
    ft.run(main)
