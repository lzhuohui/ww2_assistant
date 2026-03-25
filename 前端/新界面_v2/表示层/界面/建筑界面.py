# -*- coding: utf-8 -*-
"""
模块名称：BuildingPage
设计思路: 建筑配置界面，使用折叠卡片模式
模块隔离: 界面层依赖组件层和业务层
"""

import flet as ft
from typing import Dict, Any, List, Callable, Optional

from 前端.新界面_v2.核心.配置.界面配置 import UIConfig
from 前端.新界面_v2.表示层.组件.复合.折叠卡片 import CollapsibleCard
from 前端.新界面_v2.核心.常量.全局常量 import USER_SPACING, USER_CARD_SPACING


from 前端.新界面_v2.表示层.组件.复合.折叠卡片 import USER_DIVIDER_LEFT


# *** 用户指定变量 - AI不得修改, 变量值必须生效 ***
# （用户未指定变量）
# *********************************


class BuildingPage:
    """建筑配置界面"""
    
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
        
        def destroy_loaded_card():
            if current_loaded_card[0] and hasattr(current_loaded_card[0], 'is_loaded'):
                if current_loaded_card[0].is_loaded():
                    current_loaded_card[0].destroy_controls()
            current_loaded_card[0] = None
        
        def unload_loaded_card_options():
            if current_loaded_card[0] and hasattr(current_loaded_card[0], 'unload_options_only'):
                current_loaded_card[0].unload_options_only()
        
        def create_card(
            card_id: str,
            title: str,
            icon: str,
            subtitle: str,
            controls_config: List[Dict[str, Any]],
            enabled: bool=True,
            controls_per_row: int=6,
        ) -> ft.Container:
            def handle_save(config_key: str, value: str):
                if card_id not in card_data:
                    card_data[card_id] = {}
                card_data[card_id][config_key] = value
                if save_callback:
                    save_callback(card_id, config_key, value)
            
            def handle_expand():
                if current_loaded_card[0] and current_loaded_card[0] != card:
                    if hasattr(current_loaded_card[0], 'unload_options_only'):
                        current_loaded_card[0].unload_options_only()
                current_loaded_card[0] = card
            
            card = CollapsibleCard.create(
                title=title,
                icon=icon,
                subtitle=subtitle,
                enabled=enabled,
                controls_config=controls_config,
                controls_per_row=controls_per_row,
                on_save=handle_save,
                on_expand=handle_expand,
                config=config,
            )
            
            card_list.append(card)
            return card
        
        level_options = [f"{i:02d}" for i in range(1, 21)]
        level_options_with_zero = [f"{i:02d}" for i in range(0, 21)]
        dropdown_width = 70
        
        create_card(
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
        )
        
        create_card(
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
        )
        
        create_card(
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
        )
        
        create_card(
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
        )
        
        create_card(
            card_id="priority",
            title="建筑优先",
            icon="HOME_WORK",
            subtitle="按选择顺序建设建筑",
            controls_config=[
                {"type": "dropdown", "config_key": "资源建筑", "label": "资源:", "value": "自动平衡", "options": ["自动平衡", "钢铁优先", "橡胶优先", "石油优先"]},
                {"type": "dropdown", "config_key": "塔防建筑", "label": "塔防:", "value": "炮塔优先", "options": ["炮塔优先", "岸防优先"]},
            ],
            controls_per_row=1,
        )
        
        title_bar = ft.Row([
            ft.Icon(ft.Icons.DOMAIN, size=20, color=theme_colors.get("accent")),
            ft.Container(width=6),
            ft.Text("建筑设置", size=16, weight=ft.FontWeight.BOLD, color=theme_colors.get("text_primary")),
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
        
        container = ft.Container(
            content=content_column,
            expand=True,
        )
        
        container.destroy_loaded_card = destroy_loaded_card
        container.unload_loaded_card_options = unload_loaded_card_options
        
        return container


# *** 调试逻辑 ***
if __name__ == "__main__":
    ft.run(lambda page: page.add(BuildingPage.create()))
