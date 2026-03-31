# -*- coding: utf-8 -*-
"""
模块名称：StrategyConfigSection
模块功能：策略配置区，包含建筑速建、资源速产等配置
实现步骤：
- 创建策略配置卡片
- 使用unload_options销毁策略
- 支持配置保存和加载
"""

import flet as ft
from typing import Dict, Any, List, Callable, Optional

from 前端.游戏设置界面.核心层.配置.界面配置 import UIConfig
from 前端.游戏设置界面.表示层.组件.复合.卡片组管理器 import CardGroupManager, create_managed_card
from 前端.游戏设置界面.业务层.服务.配置服务 import ConfigService


# *** 用户指定变量: 变量值必须生效,AI不得更改数据 ***
USER_CARD_SPACING = 10  # 卡片间距
USER_SPACING = 10  # 通用间距
# *********************************


class StrategyConfigSection:
    """策略配置区 - 使用unload_options策略"""
    
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
                if save_callback:
                    save_callback(card_id, "enabled", str(enabled))
            
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
        section, manager = StrategyConfigSection.create(config=config, config_service=service)
        page.add(section)
    
    ft.run(main)
