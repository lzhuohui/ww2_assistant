# -*- coding: utf-8 -*-
"""
模块名称：BuildingConfigSection
模块功能：建筑配置区，包含主帅主城、付帅主城、分城、军团城市等建筑等级配置
"""

import flet as ft
from typing import Dict, Any, List, Callable

from 前端.游戏设置界面.核心层.配置.界面配置 import UIConfig
from 前端.游戏设置界面.表示层.组件.复合.卡片组管理器 import CardGroupManager, create_managed_card
from 前端.游戏设置界面.业务层.服务.配置服务 import ConfigService


# *** 用户指定变量: 变量值必须生效,AI不得更改数据 ***
USER_CARD_SPACING = 10  # 卡片间距
# *********************************


class BuildingConfigSection:
    """建筑配置区"""
    
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
        
        level_options = [f"{i:02d}" for i in range(1, 21)]
        level_options_with_zero = [f"{i:02d}" for i in range(0, 21)]
        dropdown_width = 70
        
        def create_card(
            card_id: str,
            title: str,
            icon: str,
            subtitle: str,
            controls_config: List[Dict[str, Any]],
            enabled: bool = True,
            controls_per_row: int = 6,
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
                controls_per_row=controls_per_row,
                on_save=handle_save,
                config=config,
            )
            return card
        
        card_list = []
        
        card_list.append(create_card(
            card_id="main_city",
            title="主帅主城",
            icon="DOMAIN",
            subtitle="设置主帅主城建筑等级",
            controls_config=[
                {"type": "dropdown", "config_key": "主帅主城_城市", "label": "城市:", "value": "17", "options": level_options, "width": dropdown_width},
                {"type": "dropdown", "config_key": "主帅主城_兵工", "label": "兵工:", "value": "17", "options": level_options, "width": dropdown_width},
                {"type": "dropdown", "config_key": "主帅主城_陆军", "label": "陆军:", "value": "14", "options": level_options, "width": dropdown_width},
                {"type": "dropdown", "config_key": "主帅主城_空军", "label": "空军:", "value": "03", "options": level_options, "width": dropdown_width},
                {"type": "dropdown", "config_key": "主帅主城_商业", "label": "商业:", "value": "04", "options": level_options, "width": dropdown_width},
                {"type": "dropdown", "config_key": "主帅主城_补给", "label": "补给:", "value": "03", "options": level_options, "width": dropdown_width},
                {"type": "dropdown", "config_key": "主帅主城_内塔", "label": "内塔:", "value": "04", "options": level_options, "width": dropdown_width},
                {"type": "dropdown", "config_key": "主帅主城_村庄", "label": "村庄:", "value": "03", "options": level_options, "width": dropdown_width},
                {"type": "dropdown", "config_key": "主帅主城_资源", "label": "资源:", "value": "03", "options": level_options, "width": dropdown_width},
                {"type": "dropdown", "config_key": "主帅主城_军工", "label": "军工:", "value": "03", "options": level_options, "width": dropdown_width},
                {"type": "dropdown", "config_key": "主帅主城_港口", "label": "港口:", "value": "03", "options": level_options, "width": dropdown_width},
                {"type": "dropdown", "config_key": "主帅主城_外塔", "label": "外塔:", "value": "03", "options": level_options, "width": dropdown_width},
            ],
            controls_per_row=6,
        ))
        
        card_list.append(create_card(
            card_id="vice_main_city",
            title="付帅主城",
            icon="APARTMENT",
            subtitle="设置付帅主城建筑等级",
            controls_config=[
                {"type": "dropdown", "config_key": "付帅主城_城市", "label": "城市:", "value": "15", "options": level_options, "width": dropdown_width},
                {"type": "dropdown", "config_key": "付帅主城_兵工", "label": "兵工:", "value": "10", "options": level_options, "width": dropdown_width},
                {"type": "dropdown", "config_key": "付帅主城_陆军", "label": "陆军:", "value": "10", "options": level_options, "width": dropdown_width},
                {"type": "dropdown", "config_key": "付帅主城_空军", "label": "空军:", "value": "03", "options": level_options, "width": dropdown_width},
                {"type": "dropdown", "config_key": "付帅主城_商业", "label": "商业:", "value": "04", "options": level_options, "width": dropdown_width},
                {"type": "dropdown", "config_key": "付帅主城_补给", "label": "补给:", "value": "03", "options": level_options, "width": dropdown_width},
                {"type": "dropdown", "config_key": "付帅主城_内塔", "label": "内塔:", "value": "03", "options": level_options, "width": dropdown_width},
                {"type": "dropdown", "config_key": "付帅主城_村庄", "label": "村庄:", "value": "03", "options": level_options, "width": dropdown_width},
                {"type": "dropdown", "config_key": "付帅主城_资源", "label": "资源:", "value": "03", "options": level_options, "width": dropdown_width},
                {"type": "dropdown", "config_key": "付帅主城_军工", "label": "军工:", "value": "03", "options": level_options, "width": dropdown_width},
                {"type": "dropdown", "config_key": "付帅主城_港口", "label": "港口:", "value": "03", "options": level_options, "width": dropdown_width},
                {"type": "dropdown", "config_key": "付帅主城_外塔", "label": "外塔:", "value": "03", "options": level_options, "width": dropdown_width},
            ],
            controls_per_row=6,
        ))
        
        card_list.append(create_card(
            card_id="sub_city",
            title="所有分城",
            icon="LOCATION_CITY",
            subtitle="设置所有分城建筑等级",
            controls_config=[
                {"type": "dropdown", "config_key": "所有分城_城市", "label": "城市:", "value": "15", "options": level_options, "width": dropdown_width},
                {"type": "dropdown", "config_key": "所有分城_兵工", "label": "兵工:", "value": "10", "options": level_options, "width": dropdown_width},
                {"type": "dropdown", "config_key": "所有分城_陆军", "label": "陆军:", "value": "10", "options": level_options, "width": dropdown_width},
                {"type": "dropdown", "config_key": "所有分城_空军", "label": "空军:", "value": "03", "options": level_options, "width": dropdown_width},
                {"type": "dropdown", "config_key": "所有分城_商业", "label": "商业:", "value": "04", "options": level_options, "width": dropdown_width},
                {"type": "dropdown", "config_key": "所有分城_补给", "label": "补给:", "value": "03", "options": level_options, "width": dropdown_width},
                {"type": "dropdown", "config_key": "所有分城_内塔", "label": "内塔:", "value": "03", "options": level_options, "width": dropdown_width},
                {"type": "dropdown", "config_key": "所有分城_村庄", "label": "村庄:", "value": "03", "options": level_options, "width": dropdown_width},
                {"type": "dropdown", "config_key": "所有分城_资源", "label": "资源:", "value": "03", "options": level_options, "width": dropdown_width},
                {"type": "dropdown", "config_key": "所有分城_军工", "label": "军工:", "value": "03", "options": level_options, "width": dropdown_width},
                {"type": "dropdown", "config_key": "所有分城_港口", "label": "港口:", "value": "03", "options": level_options, "width": dropdown_width},
                {"type": "dropdown", "config_key": "所有分城_外塔", "label": "外塔:", "value": "03", "options": level_options, "width": dropdown_width},
            ],
            controls_per_row=6,
        ))
        
        card_list.append(create_card(
            card_id="legion_city",
            title="军团城市",
            icon="ACCOUNT_BALANCE",
            subtitle="设置军团城市建筑等级",
            controls_config=[
                {"type": "dropdown", "config_key": "军团城市_城市", "label": "城市:", "value": "05", "options": level_options, "width": dropdown_width},
                {"type": "dropdown", "config_key": "军团城市_兵工", "label": "兵工:", "value": "05", "options": level_options, "width": dropdown_width},
                {"type": "dropdown", "config_key": "军团城市_军需", "label": "军需:", "value": "05", "options": level_options, "width": dropdown_width},
                {"type": "dropdown", "config_key": "军团城市_陆军", "label": "陆军:", "value": "00", "options": level_options_with_zero, "width": dropdown_width},
                {"type": "dropdown", "config_key": "军团城市_空军", "label": "空军:", "value": "00", "options": level_options_with_zero, "width": dropdown_width},
                {"type": "dropdown", "config_key": "军团城市_炮塔", "label": "炮塔:", "value": "00", "options": level_options_with_zero, "width": dropdown_width},
                {"type": "dropdown", "config_key": "军团城市_编号", "label": "编号:", "value": "01", "options": level_options, "width": dropdown_width},
            ],
            controls_per_row=4,
        ))
        
        card_list.append(create_card(
            card_id="priority",
            title="建筑优先",
            icon="HOME_WORK",
            subtitle="按选择顺序建设建筑",
            controls_config=[
                {"type": "dropdown", "config_key": "资源建筑", "label": "资源:", "value": "自动平衡", "options": ["自动平衡", "钢铁优先", "橡胶优先", "石油优先"]},
                {"type": "dropdown", "config_key": "塔防建筑", "label": "塔防:", "value": "炮塔优先", "options": ["炮塔优先", "岸防优先"]},
            ],
            controls_per_row=1,
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
        section, manager = BuildingConfigSection.create(config=config, config_service=service)
        page.add(section)
    
    ft.run(main)
