# -*- coding: utf-8 -*-
"""
模块名称：StrategyPage
设计思路: 游戏策略配置界面，包含建筑速建、资源速产等配置
模块隔离: 界面层依赖组件层和业务层
"""

import flet as ft
from typing import Dict, Any, List, Callable, Optional

from 前端.新界面_v2.核心.配置.界面配置 import UIConfig
from 前端.新界面_v2.表示层.组件.复合.折叠卡片 import CollapsibleCard
from 前端.新界面_v2.核心.常量.全局常量 import USER_SPACING, USER_CARD_HEIGHT, USER_CARD_SPACING


# *** 用户指定变量 - AI不得修改, 变量值必须生效 ***
# （用户未指定变量）
# *********************************


class StrategyPage:
    """游戏策略配置界面"""
    
    current_loaded_card: Optional[ft.Container] = None
    
    @staticmethod
    def create(
        config: UIConfig=None,
        save_callback: Callable[[str, str, str], None]=None,
    ) -> ft.Container:
        if config is None:
            config = UIConfig()
        
        theme_colors = config.当前主题颜色
        card_list: List[ft.Control] = []
        card_data: Dict[str, Dict[str, Any]] = {}
        current_loaded_card = [None]
        
        # 从配置服务获取已保存的配置
        from 前端.新界面_v2.业务层.服务.配置服务 import ConfigService
        config_service = ConfigService()
        
        def destroy_loaded_card():
            if current_loaded_card[0] and hasattr(current_loaded_card[0], 'is_loaded'):
                if current_loaded_card[0].is_loaded():
                    current_loaded_card[0].unload_options_only()
            current_loaded_card[0] = None
        
        def create_card(
            card_id: str,
            title: str,
            icon: str,
            subtitle: str,
            controls_config: List[Dict[str, Any]],
            enabled: bool=True,
        ) -> ft.Container:
            # 加载已保存的开关状态，如果没有则保存默认值
            saved_enabled = config_service.get_value(card_id, "enabled")
            if saved_enabled is None:
                saved_enabled = enabled
                if save_callback:
                    save_callback(card_id, "enabled", enabled)
            
            # 加载已保存的配置值，如果没有则保存默认值
            for control_config in controls_config:
                config_key = control_config.get("config_key")
                if config_key:
                    saved_value = config_service.get_value(card_id, config_key)
                    if saved_value is not None:
                        control_config["value"] = saved_value
                    else:
                        # 如果没有保存的值，使用默认值并保存
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
            
            def handle_expand():
                if current_loaded_card[0] and current_loaded_card[0] != card:
                    if current_loaded_card[0].is_loaded():
                        current_loaded_card[0].unload_options_only()
                current_loaded_card[0] = card
            
            card = CollapsibleCard.create(
                title=title,
                icon=icon,
                subtitle=subtitle,
                enabled=saved_enabled,
                controls_config=controls_config,
                controls_per_row=1,
                on_save=handle_save,
                on_expand=handle_expand,
                config=config,
            )
            
            card_list.append(card)
            return card
        
        create_card(
            card_id="quick_build",
            title="建筑速建",
            icon="APARTMENT",
            subtitle="达到设置主城等级后,允许加速建筑建设",
            controls_config=[
                {"type": "dropdown", "config_key": "速建限级", "label": "限级:", "value": "08", "options": ["05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15"]},
                {"type": "dropdown", "config_key": "速建类型", "label": "类型:", "value": "城资建筑", "options": ["城资建筑", "城市建筑", "资源建筑"]},
            ],
        )
        
        create_card(
            card_id="quick_produce",
            title="资源速产",
            icon="INVENTORY_2",
            subtitle="达到设置主城等级后,允许加速资源生产",
            controls_config=[
                {"type": "dropdown", "config_key": "速产限级", "label": "限级:", "value": "07", "options": ["05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15"]},
                {"type": "dropdown", "config_key": "速产类型", "label": "类型:", "value": "平衡资源", "options": ["平衡资源", "战时经济", "钢铁熔炉", "橡胶采集", "石油开采"]},
            ],
        )
        
        create_card(
            card_id="point_reserve",
            title="策点保留",
            icon="SAVINGS",
            subtitle="达到设置保留的策略点数后,允许使用策略",
            controls_config=[
                {"type": "dropdown", "config_key": "保留点数", "label": "点数:", "value": "60", "options": ["30", "60", "90", "120", "150", "180", "210", "240"]},
            ],
        )
        
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
        
        def get_all_values() -> Dict[str, Dict[str, str]]:
            result = {}
            for i, card in enumerate(card_list):
                if hasattr(card, 'get_values'):
                    card_id = list(card_data.keys())[i] if i < len(card_data) else f"card_{i}"
                    result[card_id] = card.get_values()
            return result
        
        def set_all_values(value_dict: Dict[str, Dict[str, str]]):
            for i, card in enumerate(card_list):
                if hasattr(card, 'set_values'):
                    card_id = list(card_data.keys())[i] if i < len(card_data) else f"card_{i}"
                    if card_id in value_dict:
                        card.set_values(value_dict[card_id])
        
        content_column.get_all_values = get_all_values
        content_column.set_all_values = set_all_values
        content_column.destroy_loaded_card = destroy_loaded_card
        
        return ft.Container(
            content=content_column,
            expand=True,
        )


# *** 调试逻辑 ***
if __name__ == "__main__":
    ft.run(lambda page: page.add(StrategyPage.create()))
