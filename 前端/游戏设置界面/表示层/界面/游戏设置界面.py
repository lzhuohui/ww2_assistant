# -*- coding: utf-8 -*-
"""
模块名称：GameSettingsPage
模块功能：游戏设置主界面，整合各配置区
实现步骤：
- 创建主界面布局
- 组装各配置区模块
- 提供统一接口
"""

import flet as ft
from typing import Dict, Any, List, Callable, Optional

from 前端.游戏设置界面.核心层.配置.界面配置 import UIConfig
from 前端.游戏设置界面.业务层.服务.配置服务 import ConfigService
from 前端.游戏设置界面.表示层.界面.系统配置区 import SystemConfigSection
from 前端.游戏设置界面.表示层.界面.策略配置区 import StrategyConfigSection
from 前端.游戏设置界面.表示层.界面.账号配置区 import AccountConfigSection
from 前端.游戏设置界面.表示层.界面.个性化配置区 import PersonalizationConfigSection


USER_SECTION_SPACING = 20


class GameSettingsPage:
    """游戏设置主界面 - 整合各配置区"""
    
    @staticmethod
    def create(
        config: UIConfig = None,
        save_callback: Callable[[str, str, str], None] = None,
    ) -> ft.Container:
        if config is None:
            config = UIConfig()
        
        config_service = ConfigService()
        config_service.load_config()
        
        managers = []
        
        def handle_save(card_id: str, config_key: str, value: str):
            config_service.set_value(card_id, config_key, value)
            if save_callback:
                save_callback(card_id, config_key, value)
        
        system_section, system_manager = SystemConfigSection.create(
            config=config,
            config_service=config_service,
            save_callback=handle_save,
        )
        managers.append(system_manager)
        
        strategy_section, strategy_manager = StrategyConfigSection.create(
            config=config,
            config_service=config_service,
            save_callback=handle_save,
        )
        managers.append(strategy_manager)
        
        account_section, account_manager = AccountConfigSection.create(
            config=config,
            config_service=config_service,
            save_callback=handle_save,
        )
        managers.append(account_manager)
        
        personalization_section, personalization_manager = PersonalizationConfigSection.create(
            config=config,
            config_service=config_service,
            save_callback=handle_save,
        )
        managers.append(personalization_manager)
        
        main_column = ft.Column(
            controls=[
                system_section,
                ft.Container(height=USER_SECTION_SPACING),
                strategy_section,
                ft.Container(height=USER_SECTION_SPACING),
                account_section,
                ft.Container(height=USER_SECTION_SPACING),
                personalization_section,
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


# *** 标准测试格式: 仅调用被测模块,AI不得添加数据 ***
if __name__ == "__main__":
    def main(page: ft.Page):
        config = UIConfig()
        page.add(GameSettingsPage.create(config=config))
    
    ft.run(main)
