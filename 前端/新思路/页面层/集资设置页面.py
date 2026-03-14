# -*- coding: utf-8 -*-
"""
集资设置页面 - 页面层

设计思路:
    使用通用卡片创建集资设置页面。
    实现主要统帅和次要统帅的联动逻辑。

功能:
    1. 小号上贡卡片（4个下拉框）
    2. 分城纳租卡片（2个下拉框）

数据来源:
    部分数据来自按键精灵脚本。

使用场景:
    被主界面调用。
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft
from typing import Callable, List
from 配置.界面配置 import 界面配置
from 配置.配置管理器 import ConfigManager
from 新思路.组件层.通用卡片 import UniversalCard
from 新思路.零件层.标签下拉框 import LabelDropdown


def get_active_commanders(config_manager: ConfigManager) -> List[str]:
    """
    从账号配置中获取参与挂机的主帅列表
    
    参数:
        config_manager: 配置管理器
    
    返回:
        List[str]: 参与挂机的主帅名称列表（从输入框中提取第一个"/"前的数据段）
    """
    commanders = []
    for i in range(1, 16):
        card_name = f"{i:02d}账号"
        account_type = config_manager.get_value(card_name, "统帅种类", "")
        is_enabled = config_manager.get_value(card_name, "开关", False)
        input_text = config_manager.get_value(card_name, "输入框", "")
        
        if account_type == "主帅" and is_enabled and input_text:
            parts = input_text.split("/")
            if parts and parts[0].strip():
                commanders.append(parts[0].strip())
    
    return commanders


class FundraisingSettingsPage:
    """集资设置页面"""
    
    @staticmethod
    def create(config: 界面配置, page: ft.Page = None, on_refresh: Callable[[], None] = None) -> ft.Container:
        """
        创建集资设置页面
        
        参数:
            config: 界面配置对象
            page: 页面对象
            on_refresh: 刷新回调
        
        返回:
            ft.Container: 集资设置页面容器
        """
        theme_colors = config.当前主题颜色
        config_manager = ConfigManager()
        
        commander_options = get_active_commanders(config_manager)
        
        primary_value = config_manager.get_value("小号上贡", "小号上贡_主要统帅", "")
        secondary_value = config_manager.get_value("小号上贡", "小号上贡_备用统帅", "")
        
        primary_dropdown = None
        secondary_dropdown = None
        
        def update_secondary_options():
            nonlocal secondary_dropdown
            
            if primary_dropdown:
                current_primary = primary_dropdown.get_value()
                secondary_options = ["请选统帅"] + [c for c in commander_options if c != current_primary]
                
                if secondary_dropdown:
                    secondary_dropdown.set_options(secondary_options)
                    if secondary_dropdown.get_value() not in secondary_options:
                        secondary_dropdown.set_value("请选统帅")
                        config_manager.set_value("小号上贡", "小号上贡_备用统帅", "")
        
        def on_primary_change(value: str):
            config_manager.set_value("小号上贡", "小号上贡_主要统帅", value)
            update_secondary_options()
        
        def on_secondary_change(value: str):
            if value == "请选统帅":
                config_manager.set_value("小号上贡", "小号上贡_备用统帅", "")
            else:
                config_manager.set_value("小号上贡", "小号上贡_备用统帅", value)
        
        primary_options = commander_options
        primary_display = primary_value if primary_value in primary_options else (primary_options[0] if primary_options else "")
        
        primary_dropdown = LabelDropdown.create(
            config=config,
            label="主要统帅",
            options=primary_options,
            value=primary_display,
            on_change=on_primary_change,
        )
        
        secondary_initial_options = ["请选统帅"] + commander_options
        secondary_display = secondary_value if secondary_value in commander_options else "请选统帅"
        
        secondary_dropdown = LabelDropdown.create(
            config=config,
            label="次要统帅",
            options=secondary_initial_options,
            value=secondary_display,
            on_change=on_secondary_change,
        )
        
        limit_level_value = config_manager.get_value("小号上贡", "小号上贡_上贡限级", "05")
        limit_amount_value = config_manager.get_value("小号上贡", "小号上贡_上贡限量", "2")
        
        config_manager.set_value("小号上贡", "小号上贡_主要统帅", primary_display)
        config_manager.set_value("小号上贡", "小号上贡_备用统帅", secondary_value if secondary_value != "请选统帅" else "")
        
        limit_level_options = [f"{i:02d}级" for i in range(5, 16)]
        limit_amount_options = [f"{i}万" for i in range(2, 21)]
        
        limit_level_display = f"{limit_level_value}级" if not limit_level_value.endswith("级") else limit_level_value
        limit_amount_display = f"{limit_amount_value}万" if not limit_amount_value.endswith("万") else limit_amount_value
        
        config_manager.set_value("小号上贡", "小号上贡_上贡限级", limit_level_value)
        config_manager.set_value("小号上贡", "小号上贡_上贡限量", limit_amount_value)
        
        def on_limit_level_change(value: str):
            save_value = value.replace("级", "")
            config_manager.set_value("小号上贡", "小号上贡_上贡限级", save_value)
        
        def on_limit_amount_change(value: str):
            save_value = value.replace("万", "")
            config_manager.set_value("小号上贡", "小号上贡_上贡限量", save_value)
        
        limit_level_dropdown = LabelDropdown.create(
            config=config,
            label="上贡限级",
            options=limit_level_options,
            value=limit_level_display,
            on_change=on_limit_level_change,
        )
        
        limit_amount_dropdown = LabelDropdown.create(
            config=config,
            label="上贡限量",
            options=limit_amount_options,
            value=limit_amount_display,
            on_change=on_limit_amount_change,
        )
        
        small_account_card = UniversalCard.create(
            config=config,
            title="小号上贡",
            icon="ACCOUNT_BALANCE",
            enabled=True,
            subtitle="设置小号上贡的统帅和限制",
            controls=[primary_dropdown, secondary_dropdown, limit_level_dropdown, limit_amount_dropdown],
            controls_per_row=2,
        )
        
        rent_level_value = config_manager.get_value("分城纳租", "分城纳租_纳租限级", "05")
        rent_amount_value = config_manager.get_value("分城纳租", "分城纳租_纳租限量", "2")
        
        config_manager.set_value("分城纳租", "分城纳租_纳租限级", rent_level_value)
        config_manager.set_value("分城纳租", "分城纳租_纳租限量", rent_amount_value)
        
        rent_level_options = [f"{i:02d}级" for i in range(5, 16)]
        rent_amount_options = [f"{i}万" for i in range(2, 21)]
        
        rent_level_display = f"{rent_level_value}级" if not rent_level_value.endswith("级") else rent_level_value
        rent_amount_display = f"{rent_amount_value}万" if not rent_amount_value.endswith("万") else rent_amount_value
        
        def on_rent_level_change(value: str):
            save_value = value.replace("级", "")
            config_manager.set_value("分城纳租", "分城纳租_纳租限级", save_value)
        
        def on_rent_amount_change(value: str):
            save_value = value.replace("万", "")
            config_manager.set_value("分城纳租", "分城纳租_纳租限量", save_value)
        
        rent_card = UniversalCard.create(
            config=config,
            title="分城纳租",
            icon="APARTMENT",
            enabled=True,
            subtitle="设置分城纳租的限制",
            controls=[
                LabelDropdown.create(
                    config=config,
                    label="纳租限级",
                    options=rent_level_options,
                    value=rent_level_display,
                    on_change=on_rent_level_change,
                ),
                LabelDropdown.create(
                    config=config,
                    label="纳租限量",
                    options=rent_amount_options,
                    value=rent_amount_display,
                    on_change=on_rent_amount_change,
                ),
            ],
            controls_per_row=2,
        )
        
        page_content = ft.Column(
            [
                ft.Text(
                    "集资设置",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=theme_colors.get("text_primary"),
                ),
                ft.Container(height=20),
                small_account_card,
                ft.Container(height=15),
                rent_card,
            ],
            spacing=0,
            scroll=ft.ScrollMode.HIDDEN,
            expand=True,
        )
        
        return ft.Container(
            content=page_content,
            padding=ft.Padding.all(20),
            expand=True,
        )


集资设置页面 = FundraisingSettingsPage


if __name__ == "__main__":
    配置 = 界面配置()
    
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        page.add(FundraisingSettingsPage.create(配置))
    
    ft.run(main)
