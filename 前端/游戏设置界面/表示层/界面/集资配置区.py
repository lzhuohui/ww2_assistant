# -*- coding: utf-8 -*-
"""
模块名称：FundingConfigSection
模块功能：集资配置区，包含小号上贡、分城纳租配置
实现步骤：
- 创建集资配置卡片
- 实现主要统帅和次要统帅联动逻辑
- 从账号配置区获取参与挂机的主帅列表
"""

import flet as ft
from typing import Dict, Any, List, Callable

from 前端.游戏设置界面.核心层.配置.界面配置 import UIConfig
from 前端.游戏设置界面.表示层.组件.复合.卡片组管理器 import CardGroupManager, create_managed_card
from 前端.游戏设置界面.表示层.组件.基础.下拉框 import Dropdown
from 前端.游戏设置界面.业务层.服务.配置服务 import ConfigService


# *** 用户指定变量: 变量值必须生效,AI不得更改数据 ***
USER_CARD_SPACING = 10  # 卡片间距
USER_DROPDOWN_WIDTH = 120  # 下拉框宽度
USER_PLACEHOLDER = "请选统帅"  # 统帅选择占位符
# *********************************


def get_active_commanders(config_service: ConfigService) -> List[str]:
    """从账号配置中获取参与挂机的主帅列表"""
    commanders = []
    for i in range(1, 16):
        card_id = f"account_{i:02d}"
        account_type = config_service.get_value(card_id, "类型") or ""
        is_enabled = config_service.get_value(card_id, "enabled")
        name = config_service.get_value(card_id, "名称") or ""
        
        if account_type == "主帅" and is_enabled and name:
            commanders.append(name)
    return commanders


class FundingConfigSection:
    """集资配置区 - 包含统帅联动逻辑"""
    
    @staticmethod
    def create(
        config: UIConfig = None,
        config_service: ConfigService = None,
        save_callback: Callable[[str, str, str], None] = None,
    ) -> tuple:
        if config is None:
            config = UIConfig()
        if config_service is None:
            config_service = ConfigService()
        
        theme_colors = config.当前主题颜色
        manager = CardGroupManager()
        card_data: Dict[str, Dict[str, Any]] = {}
        
        commander_options = get_active_commanders(config_service)
        
        primary_dropdown = None
        secondary_dropdown = None
        
        def update_secondary_options():
            """更新次要统帅选项"""
            if primary_dropdown and secondary_dropdown:
                current_primary = primary_dropdown.get_value()
                secondary_options = [USER_PLACEHOLDER] + [c for c in commander_options if c != current_primary]
                secondary_dropdown.set_options(secondary_options)
                
                current_secondary = secondary_dropdown.get_value()
                if current_secondary not in secondary_options:
                    secondary_dropdown.set_value(USER_PLACEHOLDER)
                    if save_callback:
                        save_callback("small_account_tribute", "次要统帅", "")
        
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
            
            for control_config in controls_config:
                config_key = control_config.get("config_key")
                if config_key:
                    saved_value = config_service.get_value(card_id, config_key)
                    if saved_value is not None:
                        control_config["value"] = saved_value
            
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
                controls_per_row=2,
                on_save=handle_save,
                config=config,
            )
            return card
        
        def create_tribute_card() -> ft.Container:
            """创建小号上贡卡片（带联动逻辑）"""
            card_id = "small_account_tribute"
            
            saved_enabled = config_service.get_value(card_id, "enabled")
            if saved_enabled is None:
                saved_enabled = True
            
            saved_primary = config_service.get_value(card_id, "主要统帅") or ""
            saved_secondary = config_service.get_value(card_id, "次要统帅") or ""
            
            def handle_save(config_key: str, value: str):
                if card_id not in card_data:
                    card_data[card_id] = {}
                card_data[card_id][config_key] = value
                if save_callback:
                    save_callback(card_id, config_key, value)
            
            level_options = ["05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15"]
            amount_options = [str(i) for i in range(2, 21)]
            
            saved_level = config_service.get_value(card_id, "上贡限级") or "05"
            saved_amount = config_service.get_value(card_id, "上贡限量") or "2"
            
            level_dropdown = Dropdown.create(
                options=level_options,
                current_value=saved_level,
                width=USER_DROPDOWN_WIDTH,
                enabled=True,
                on_change=lambda v: handle_save("上贡限级", v),
                config=config,
            )
            
            amount_dropdown = Dropdown.create(
                options=amount_options,
                current_value=saved_amount,
                width=USER_DROPDOWN_WIDTH,
                enabled=True,
                on_change=lambda v: handle_save("上贡限量", v),
                config=config,
            )
            
            nonlocal primary_dropdown, secondary_dropdown
            
            primary_display = saved_primary if saved_primary in commander_options else (commander_options[0] if commander_options else USER_PLACEHOLDER)
            primary_options = commander_options if commander_options else [USER_PLACEHOLDER]
            
            primary_dropdown = Dropdown.create(
                options=primary_options,
                current_value=primary_display,
                width=USER_DROPDOWN_WIDTH,
                enabled=True,
                on_change=lambda v: [handle_save("主要统帅", v), update_secondary_options()],
                config=config,
            )
            
            secondary_initial_options = [USER_PLACEHOLDER] + commander_options
            secondary_display = saved_secondary if saved_secondary in commander_options else USER_PLACEHOLDER
            
            secondary_dropdown = Dropdown.create(
                options=secondary_initial_options,
                current_value=secondary_display,
                width=USER_DROPDOWN_WIDTH,
                enabled=True,
                on_change=lambda v: handle_save("次要统帅", "" if v == USER_PLACEHOLDER else v),
                config=config,
            )
            
            controls = [
                ft.Row([
                    ft.Text("限级选择:", size=14, color=theme_colors.get("text_secondary")),
                    level_dropdown,
                ], spacing=4, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Row([
                    ft.Text("限量选择:", size=14, color=theme_colors.get("text_secondary")),
                    amount_dropdown,
                ], spacing=4, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Row([
                    ft.Text("主要统帅:", size=14, color=theme_colors.get("text_secondary")),
                    primary_dropdown,
                ], spacing=4, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Row([
                    ft.Text("次要统帅:", size=14, color=theme_colors.get("text_secondary")),
                    secondary_dropdown,
                ], spacing=4, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            ]
            
            card = create_managed_card(
                manager=manager,
                title="小号上贡",
                icon="PAYMENTS",
                subtitle="小号达到等级后上贡资源",
                enabled=saved_enabled,
                controls=controls,
                controls_per_row=2,
                on_save=lambda k, v: handle_save(k, v),
                config=config,
            )
            
            return card
        
        card_list = []
        
        card_list.append(create_tribute_card())
        
        card_list.append(create_card(
            card_id="sub_city_rent",
            title="分城纳租",
            icon="ACCOUNT_BALANCE_WALLET",
            subtitle="分城达到等级后纳租",
            controls_config=[
                {"type": "dropdown", "config_key": "分城等级", "label": "等级选择:", "value": "05", "options": ["05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15"]},
                {"type": "dropdown", "config_key": "纳租限量", "label": "限量选择:", "value": "2", "options": [str(i) for i in range(2, 21)]},
            ],
        ))
        
        card_column = ft.Column(
            controls=card_list,
            spacing=USER_CARD_SPACING,
            scroll=ft.ScrollMode.HIDDEN,
            expand=True,
        )
        
        content_column = ft.Column(
            controls=[card_column],
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
        section, manager = FundingConfigSection.create(config=config, config_service=service)
        page.add(section)
    
    ft.run(main)
