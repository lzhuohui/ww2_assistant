# -*- coding: utf-8 -*-
"""
模块名称：GameSettingsPage
设计思路: 游戏设置界面，整合系统配置、策略配置、账号配置
模块隔离: 界面层依赖组件层和业务层

模块化设计:
    - 使用CardGroupManager统一管理卡片行为
    - 系统配置区: 使用unload_options策略
    - 策略配置区: 使用unload_options策略
    - 账号配置区: 使用none策略（不销毁控件）

功能模块:
    1. 系统配置: 挂机模式、指令速度、尝试次数、清缓限量
    2. 策略配置: 建筑速建、资源速产、策点保留
    3. 账号配置: 15个账号卡片，支持参与状态计算和授权限制
"""

import flet as ft
from typing import Dict, Any, List, Callable, Optional

from 前端.新界面_v2.核心.配置.界面配置 import UIConfig
from 前端.新界面_v2.表示层.组件.复合.卡片组管理器 import CardGroupManager, create_managed_card
from 前端.新界面_v2.表示层.组件.基础.下拉框 import Dropdown, USER_WIDTH as DROPDOWN_WIDTH
from 前端.新界面_v2.表示层.组件.基础.输入框 import InputBox, USER_WIDTH as INPUT_WIDTH
from 前端.新界面_v2.核心.常量.全局常量 import USER_SPACING, USER_CARD_SPACING


USER_MAX_ACCOUNTS = 15
USER_DROPDOWN_WIDTH = 70
USER_INPUT_WIDTH = 190
USER_AUTHORIZED_COUNT = 15


class SystemConfigSection:
    """系统配置区 - 使用unload_options策略"""
    
    @staticmethod
    def create(
        config: UIConfig,
        config_service,
        save_callback: Callable[[str, str, str], None],
    ) -> tuple[ft.Column, CardGroupManager]:
        theme_colors = config.当前主题颜色
        manager = CardGroupManager(destroy_strategy="unload_options")
        card_data: Dict[str, Dict[str, Any]] = {}
        
        def create_card(
            card_id: str,
            title: str,
            icon: str,
            subtitle: str,
            controls_config: List[Dict[str, Any]],
            enabled: bool = True,
        ) -> ft.Container:
            saved_enabled = config_service.get_value(card_id, "enabled")
            if saved_enabled is None:
                saved_enabled = enabled
                if save_callback:
                    save_callback(card_id, "enabled", enabled)
            
            for control_config in controls_config:
                config_key = control_config.get("config_key")
                if config_key:
                    saved_value = config_service.get_value(card_id, config_key)
                    if saved_value is not None:
                        control_config["value"] = saved_value
                    else:
                        default_value = control_config.get("value")
                        if default_value is not None:
                            control_config["value"] = default_value
                            if save_callback:
                                save_callback(card_id, config_key, default_value)
            
            def handle_save(config_key: str, value: str):
                if card_id not in card_data:
                    card_data[card_id] = {}
                card_data[card_id][config_key] = value
                if save_callback:
                    save_callback(card_id, config_key, value)
            
            card = create_managed_card(
                manager=manager,
                title=title,
                icon=icon,
                subtitle=subtitle,
                enabled=saved_enabled,
                controls_config=controls_config,
                controls_per_row=4,
                on_save=handle_save,
                config=config,
            )
            
            return card
        
        card_list = []
        
        card_list.append(create_card(
            card_id="hangup_mode",
            title="挂机模式",
            icon="POWER_SETTINGS_NEW",
            subtitle="全自动:自动挂机,无需人为干预 | 半自动:点击头像,自动切换账号",
            controls_config=[
                {"type": "dropdown", "config_key": "挂机模式", "label": "模式选择:", "value": "全自动", "options": ["全自动", "半自动"]},
            ],
        ))
        
        card_list.append(create_card(
            card_id="command_speed",
            title="指令速度",
            icon="SPEED",
            subtitle="运行指令间隔频率(毫秒)，数值越小速度越快",
            controls_config=[
                {"type": "dropdown", "config_key": "指令速度", "label": "速度选择:", "value": "100", "options": ["100", "150", "200", "250", "300", "350", "400", "450", "500"]},
            ],
        ))
        
        card_list.append(create_card(
            card_id="retry_count",
            title="尝试次数",
            icon="REFRESH",
            subtitle="连续操作失败达到最大尝试次数后,触发自动纠错系统",
            controls_config=[
                {"type": "dropdown", "config_key": "尝试次数", "label": "次数选择:", "value": "15", "options": ["10", "15", "20", "25", "30"]},
            ],
        ))
        
        card_list.append(create_card(
            card_id="cache_limit",
            title="清缓限量",
            icon="DELETE_SWEEP",
            subtitle="达到设置系统缓存清理阈值(M)后,自动清理缓存",
            controls_config=[
                {"type": "dropdown", "config_key": "清缓限量", "label": "限量选择:", "value": "1.0", "options": ["1.0", "1.5", "2.0", "2.5", "3.0", "3.5", "4.0", "4.5", "5.0"]},
            ],
        ))
        
        title_bar = ft.Row([
            ft.Icon(ft.Icons.SETTINGS, size=20, color=theme_colors.get("accent")),
            ft.Container(width=6),
            ft.Text("系统配置", size=16, weight=ft.FontWeight.BOLD, color=theme_colors.get("text_primary")),
        ], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER)
        
        card_column = ft.Column(
            controls=card_list,
            spacing=USER_CARD_SPACING,
            scroll=ft.ScrollMode.HIDDEN,
            expand=True,
        )
        
        content_column = ft.Column(
            controls=[
                title_bar,
                ft.Container(height=USER_SPACING),
                card_column,
            ],
            spacing=0,
            expand=True,
        )
        
        content_column.card_manager = manager
        
        return content_column, manager


class StrategyConfigSection:
    """策略配置区 - 使用unload_options策略"""
    
    @staticmethod
    def create(
        config: UIConfig,
        config_service,
        save_callback: Callable[[str, str, str], None],
    ) -> tuple[ft.Column, CardGroupManager]:
        theme_colors = config.当前主题颜色
        manager = CardGroupManager(destroy_strategy="unload_options")
        card_data: Dict[str, Dict[str, Any]] = {}
        
        def create_card(
            card_id: str,
            title: str,
            icon: str,
            subtitle: str,
            controls_config: List[Dict[str, Any]],
            enabled: bool = True,
        ) -> ft.Container:
            saved_enabled = config_service.get_value(card_id, "enabled")
            if saved_enabled is None:
                saved_enabled = enabled
                if save_callback:
                    save_callback(card_id, "enabled", enabled)
            
            for control_config in controls_config:
                config_key = control_config.get("config_key")
                if config_key:
                    saved_value = config_service.get_value(card_id, config_key)
                    if saved_value is not None:
                        control_config["value"] = saved_value
                    else:
                        default_value = control_config.get("value")
                        if default_value is not None:
                            control_config["value"] = default_value
                            if save_callback:
                                save_callback(card_id, config_key, default_value)
            
            def handle_save(config_key: str, value: str):
                if card_id not in card_data:
                    card_data[card_id] = {}
                card_data[card_id][config_key] = value
                if save_callback:
                    save_callback(card_id, config_key, value)
            
            card = create_managed_card(
                manager=manager,
                title=title,
                icon=icon,
                subtitle=subtitle,
                enabled=saved_enabled,
                controls_config=controls_config,
                controls_per_row=1,
                on_save=handle_save,
                config=config,
            )
            
            return card
        
        card_list = []
        
        card_list.append(create_card(
            card_id="quick_build",
            title="建筑速建",
            icon="APARTMENT",
            subtitle="达到设置主城等级后,允许加速建筑建设",
            controls_config=[
                {"type": "dropdown", "config_key": "速建限级", "label": "限级:", "value": "08", "options": ["05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15"]},
                {"type": "dropdown", "config_key": "速建类型", "label": "类型:", "value": "城资建筑", "options": ["城资建筑", "城市建筑", "资源建筑"]},
            ],
        ))
        
        card_list.append(create_card(
            card_id="quick_produce",
            title="资源速产",
            icon="INVENTORY_2",
            subtitle="达到设置主城等级后,允许加速资源生产",
            controls_config=[
                {"type": "dropdown", "config_key": "速产限级", "label": "限级:", "value": "07", "options": ["05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15"]},
                {"type": "dropdown", "config_key": "速产类型", "label": "类型:", "value": "平衡资源", "options": ["平衡资源", "战时经济", "钢铁熔炉", "橡胶采集", "石油开采"]},
            ],
        ))
        
        card_list.append(create_card(
            card_id="point_reserve",
            title="策点保留",
            icon="SAVINGS",
            subtitle="达到设置保留的策略点数后,允许使用策略",
            controls_config=[
                {"type": "dropdown", "config_key": "保留点数", "label": "点数:", "value": "60", "options": ["30", "60", "90", "120", "150", "180", "210", "240"]},
            ],
        ))
        
        title_bar = ft.Row([
            ft.Icon(ft.Icons.ROCKET_LAUNCH, size=20, color=theme_colors.get("accent")),
            ft.Container(width=6),
            ft.Text("策略配置", size=16, weight=ft.FontWeight.BOLD, color=theme_colors.get("text_primary")),
        ], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER)
        
        card_column = ft.Column(
            controls=card_list,
            spacing=USER_CARD_SPACING,
            scroll=ft.ScrollMode.HIDDEN,
            expand=True,
        )
        
        content_column = ft.Column(
            controls=[
                title_bar,
                ft.Container(height=USER_SPACING),
                card_column,
            ],
            spacing=0,
            expand=True,
        )
        
        content_column.card_manager = manager
        
        return content_column, manager


class AccountConfigSection:
    """账号配置区 - 使用none策略（不销毁控件）"""
    
    授权数量 = USER_AUTHORIZED_COUNT
    当前参与数量 = 0
    账号开关状态: Dict[str, bool] = {}
    
    @staticmethod
    def create(
        config: UIConfig,
        config_service,
        save_callback: Callable[[str, str, str], None],
    ) -> tuple[ft.Column, CardGroupManager]:
        theme_colors = config.当前主题颜色
        manager = CardGroupManager(destroy_strategy="none")
        card_data: Dict[str, Dict[str, Any]] = {}
        card_refs: Dict[str, ft.Container] = {}
        
        AccountConfigSection.授权数量 = USER_AUTHORIZED_COUNT
        AccountConfigSection.当前参与数量 = 0
        AccountConfigSection.账号开关状态 = {}
        
        count_text = ft.Text(
            f"已启用: {AccountConfigSection.当前参与数量}/{AccountConfigSection.授权数量}",
            size=14,
            color=theme_colors.get("text_secondary"),
        )
        
        def get_subtitle(enabled: bool, name: str, account: str, password: str, is_expanded: bool = False) -> str:
            if not enabled:
                if is_expanded:
                    return "未参与挂机"
                else:
                    display_name = name if name else "未设置"
                    return f"{display_name} (未参与), 设置请进入 >>"
            
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
                    return f"{display_name} (信息不完整), 设置请进入 >>"
            
            if is_expanded:
                return f"已配置: {name}"
            else:
                return f"{name} (参与挂机), 设置请进入 >>"
        
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
            
            count_text.value = f"已启用: {AccountConfigSection.当前参与数量}/{AccountConfigSection.授权数量}"
            try:
                if count_text.page:
                    count_text.update()
            except:
                pass
            
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
            default_type: str = "付帅",
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
                    save_callback(card_id, "enabled", enabled)
            
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
            
            card_data[card_id] = {
                "名称": current_name,
                "账号": current_account,
                "密码": current_password,
                "enabled": saved_enabled,
                "类型": saved_type,
                "平台": saved_platform
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
            
            controls = [
                type_dropdown,
                name_input,
                account_input,
                password_input,
                platform_dropdown,
            ]
            
            card = create_managed_card(
                manager=manager,
                title=title,
                icon=icon,
                subtitle=subtitle,
                enabled=saved_enabled,
                controls=controls,
                controls_per_row=5,
                on_expand=handle_expand,
                on_collapse=handle_collapse,
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
        
        title_bar = ft.Row([
            ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=20, color=theme_colors.get("accent")),
            ft.Container(width=6),
            ft.Text("账号设置", size=16, weight=ft.FontWeight.BOLD, color=theme_colors.get("text_primary")),
            ft.Container(width=20),
            count_text,
        ], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER)
        
        divider = ft.Container(
            content=ft.Divider(
                height=1,
                thickness=1,
                color=theme_colors.get("border"),
            ),
            opacity=0.5,
        )
        
        card_column = ft.Column(
            controls=card_list,
            spacing=USER_CARD_SPACING,
            scroll=ft.ScrollMode.HIDDEN,
            expand=True,
        )
        
        content_column = ft.Column(
            controls=[
                title_bar,
                divider,
                ft.Container(height=USER_SPACING),
                card_column,
            ],
            spacing=0,
            expand=True,
        )
        
        content_column.card_manager = manager
        
        return content_column, manager


class GameSettingsPage:
    """游戏设置界面 - 整合系统、策略、账号配置"""
    
    @staticmethod
    def create(
        config: UIConfig = None,
        save_callback: Callable[[str, str, str], None] = None,
    ) -> ft.Container:
        if config is None:
            config = UIConfig()
        
        from 前端.新界面_v2.业务层.服务.配置服务 import ConfigService
        config_service = ConfigService()
        
        managers: List[CardGroupManager] = []
        
        system_section, system_manager = SystemConfigSection.create(config, config_service, save_callback)
        managers.append(system_manager)
        
        strategy_section, strategy_manager = StrategyConfigSection.create(config, config_service, save_callback)
        managers.append(strategy_manager)
        
        account_section, account_manager = AccountConfigSection.create(config, config_service, save_callback)
        managers.append(account_manager)
        
        main_column = ft.Column(
            controls=[
                system_section,
                ft.Container(height=USER_SPACING * 2),
                strategy_section,
                ft.Container(height=USER_SPACING * 2),
                account_section,
            ],
            spacing=0,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )
        
        def destroy_all_cards():
            for manager in managers:
                manager.collapse_all()
        
        main_column.destroy_all_cards = destroy_all_cards
        main_column.managers = managers
        
        return ft.Container(
            content=main_column,
            expand=True,
        )


if __name__ == "__main__":
    def main(page: ft.Page):
        page.add(GameSettingsPage.create())
    
    ft.app(target=main)
