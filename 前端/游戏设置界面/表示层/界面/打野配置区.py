# -*- coding: utf-8 -*-
"""
模块名称：HuntingConfigSection
模块功能：打野配置区，包含自动打野配置
"""

import flet as ft
from typing import Dict, Any, List, Callable

from 前端.游戏设置界面.核心层.配置.界面配置 import UIConfig
from 前端.游戏设置界面.表示层.组件.复合.卡片组管理器 import CardGroupManager, create_managed_card
from 前端.游戏设置界面.业务层.服务.配置服务 import ConfigService


# *** 用户指定变量: 变量值必须生效,AI不得更改数据 ***
USER_CARD_SPACING = 10  # 卡片间距
# *********************************


class HuntingConfigSection:
    """打野配置区"""
    
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
                controls_per_row=1,
                on_save=handle_save,
                config=config,
            )
            return card
        
        card_list = []
        
        card_list.append(create_card(
            card_id="auto_hunting",
            title="自动打野",
            icon="EXPLORE",
            subtitle="自动搜索并攻击野怪",
            controls_config=[
                {"type": "dropdown", "config_key": "level", "label": "野怪等级选择:", "value": "全部", "options": ["全部", "1-3级", "4-6级", "7-9级", "10级以上"]},
                {"type": "dropdown", "config_key": "frequency", "label": "搜索频率选择:", "value": "每小时", "options": ["每30分钟", "每小时", "每2小时", "每4小时"]},
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
        section, manager = HuntingConfigSection.create(config=config, config_service=service)
        page.add(section)
    
    ft.app(target=main)
