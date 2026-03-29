# -*- coding: utf-8 -*-
"""
模块名称：CleaningConfigSection
模块功能：打扫配置区，包含打扫城区、打扫政区配置
"""

import flet as ft
from typing import Dict, Any, List, Callable

from 前端.游戏设置界面.核心层.配置.界面配置 import UIConfig
from 前端.游戏设置界面.表示层.组件.复合.卡片组管理器 import CardGroupManager, create_managed_card
from 前端.游戏设置界面.业务层.服务.配置服务 import ConfigService


# *** 用户指定变量: 变量值必须生效,AI不得更改数据 ***
USER_CARD_SPACING = 10  # 卡片间距
# *********************************


class CleaningConfigSection:
    """打扫配置区"""
    
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
        
        def create_card(
            card_id: str,
            title: str,
            icon: str,
            subtitle: str,
            enabled: bool = True,
        ) -> ft.Container:
            saved_enabled = config_service.get_value(card_id, "enabled")
            if saved_enabled is None:
                saved_enabled = enabled
            
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
                on_save=handle_save,
                config=config,
            )
            return card
        
        card_list = []
        
        card_list.append(create_card(
            card_id="city_cleaning",
            title="打扫城区",
            icon="CLEANING_SERVICES",
            subtitle="自动打扫城区战场战利品",
            enabled=True,
        ))
        
        card_list.append(create_card(
            card_id="district_cleaning",
            title="打扫政区",
            icon="DELETE_SWEEP",
            subtitle="自动打扫政区战场战利品",
            enabled=True,
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
        section, manager = CleaningConfigSection.create(config=config, config_service=service)
        page.add(section)
    
    ft.app(target=main)
