# -*- coding: utf-8 -*-
"""
模块名称：CleaningPage
设计思路: 打扫配置界面，使用折叠卡片模式
模块隔离: 界面层依赖组件层和业务层
"""

import flet as ft
from typing import Dict, Any, List, Callable, Optional

from 前端.新界面_v2.核心.配置.界面配置 import UIConfig
from 前端.新界面_v2.表示层.组件.复合.折叠卡片 import CollapsibleCard
from 前端.新界面_v2.核心.常量.全局常量 import USER_SPACING, USER_CARD_SPACING


# *** 用户指定变量 - AI不得修改, 变量值必须生效 ***
# （用户未指定变量）
# *********************************


class CleaningPage:
    """打扫配置界面"""
    
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
        
        def create_card(
            card_id: str,
            title: str,
            icon: str,
            info_text: str,
            enabled: bool=True,
        ) -> ft.Container:
            info_row = ft.Text(info_text, size=14, color=theme_colors.get("text_secondary"))
            
            card = CollapsibleCard.create(
                title=title,
                icon=icon,
                subtitle=info_text,
                enabled=enabled,
                controls=[info_row],
                config=config,
            )
            card_list.append(card)
            return card
        
        create_card(
            card_id="city_cleaning",
            title="打扫城区",
            icon="CLEANING_SERVICES",
            info_text="自动打扫城区战场战利品",
        )
        
        create_card(
            card_id="district_cleaning",
            title="打扫政区",
            icon="DELETE_SWEEP",
            info_text="自动打扫政区战场战利品",
        )
        
        title_bar = ft.Row([
            ft.Icon(ft.Icons.CLEANING_SERVICES, size=20, color=theme_colors.get("accent")),
            ft.Container(width=6),
            ft.Text("打扫设置", size=16, weight=ft.FontWeight.BOLD, color=theme_colors.get("text_primary")),
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
        
        content_column.destroy_loaded_card = destroy_loaded_card
        
        return ft.Container(
            content=content_column,
            expand=True,
        )


# *** 调试逻辑 ***
if __name__ == "__main__":
    ft.run(lambda page: page.add(CleaningPage.create()))
