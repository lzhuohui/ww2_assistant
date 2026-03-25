# -*- coding: utf-8 -*-
"""
模块名称：SystemPage
设计思路: 系统配置界面，包含挂机模式、指令速度等配置
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


class SystemPage:
    """系统配置界面"""
    
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
                controls_per_row=4,
                on_save=handle_save,
                on_expand=handle_expand,
                config=config,
            )
            
            card_list.append(card)
            return card
        
        create_card(
            card_id="hangup_mode",
            title="挂机模式",
            icon="POWER_SETTINGS_NEW",
            subtitle="全自动:自动挂机,无需人为干预 | 半自动:点击头像,自动切换账号",
            controls_config=[
                {"type": "dropdown", "config_key": "挂机模式", "label": "模式选择:", "value": "全自动", "options": ["全自动", "半自动"]},
            ],
        )
        
        create_card(
            card_id="command_speed",
            title="指令速度",
            icon="SPEED",
            subtitle="运行指令间隔频率(毫秒)，数值越小速度越快",
            controls_config=[
                {"type": "dropdown", "config_key": "指令速度", "label": "速度选择:", "value": "100", "options": ["100", "150", "200", "250", "300", "350", "400", "450", "500"]},
            ],
        )
        
        create_card(
            card_id="retry_count",
            title="尝试次数",
            icon="REFRESH",
            subtitle="连续操作失败达到最大尝试次数后,触发自动纠错系统",
            controls_config=[
                {"type": "dropdown", "config_key": "尝试次数", "label": "次数选择:", "value": "15", "options": ["10", "15", "20", "25", "30"]},
            ],
        )
        
        create_card(
            card_id="cache_limit",
            title="清缓限量",
            icon="DELETE_SWEEP",
            subtitle="达到设置系统缓存清理阈值(M)后,自动清理缓存",
            controls_config=[
                {"type": "dropdown", "config_key": "清缓限量", "label": "限量选择:", "value": "1.0", "options": ["1.0", "1.5", "2.0", "2.5", "3.0", "3.5", "4.0", "4.5", "5.0"]},
            ],
        )
        
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
    ft.run(lambda page: page.add(SystemPage.create()))
