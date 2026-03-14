# -*- coding: utf-8 -*-
"""
集资设置页面 - 页面层

设计思路:
    使用通用卡片创建集资设置页面。

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
from typing import Callable, List, Tuple
from 配置.界面配置 import 界面配置
from 配置.配置管理器 import ConfigManager
from 新思路.组件层.通用卡片 import UniversalCard


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


def create_dynamic_card_config(
    config_manager: ConfigManager,
    card_name: str,
    base_config: dict,
    commander_options: List[str]
) -> dict:
    """
    创建动态卡片配置，更新统帅下拉框选项
    
    参数:
        config_manager: 配置管理器
        card_name: 卡片名称
        base_config: 基础配置
        commander_options: 统帅选项列表
    
    返回:
        dict: 更新后的配置
    """
    import copy
    config = copy.deepcopy(base_config)
    
    if card_name == "小号上贡":
        for control in config.get("controls", []):
            if control.get("config_key") in ["小号上贡_主要统帅", "小号上贡_备用统帅"]:
                control["options"] = commander_options
                if commander_options:
                    control["default"] = commander_options[0]
    
    return config


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
        
        def on_value_change(config_key: str, value: any):
            print(f"配置变化: {config_key} = {value}")
        
        small_account_card = UniversalCard.create_from_config(
            config=config,
            card_name="小号上贡",
            config_manager=config_manager,
            on_value_change=on_value_change,
            dynamic_options={"小号上贡_主要统帅": commander_options, "小号上贡_备用统帅": commander_options},
        )
        
        rent_card = UniversalCard.create_from_config(
            config=config,
            card_name="分城纳租",
            config_manager=config_manager,
            on_value_change=on_value_change,
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
        
        page_container = ft.Container(
            content=page_content,
            padding=ft.Padding.all(20),
            expand=True,
        )
        
        return page_container


集资设置页面 = FundraisingSettingsPage


if __name__ == "__main__":
    配置 = 界面配置()
    
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        page.add(FundraisingSettingsPage.create(配置))
    
    ft.run(main)
