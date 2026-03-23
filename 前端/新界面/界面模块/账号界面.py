# -*- coding: utf-8 -*-
"""模块名称：账号界面 | 设计思路：账号配置界面，15个账号设置 | 模块隔离原则"""

import flet as ft
from typing import Dict, Any, List, Callable

from 前端.新界面.核心接口.界面配置 import 界面配置
from 前端.新界面.核心接口.主题提供者 import ThemeProvider
from 前端.新界面.组件模块.折叠卡片 import CollapsibleCard
from 前端.新界面.组件模块.下拉框 import Dropdown


# *** 用户指定变量 - AI不得修改, 变量值必须生效 ***
USER_CARD_WIDTH = 500
USER_CARD_HEIGHT = 70
USER_CARD_SPACING = 8
MAX_ACCOUNTS = 15
DEFAULT_AUTHORIZED_COUNT = 15
# *********************************


class 账号界面:
    """账号配置界面"""
    
    授权数量 = DEFAULT_AUTHORIZED_COUNT
    当前参与数量 = 0
    账号开关状态: Dict[str, bool] = {}
    
    @staticmethod
    def create(
        config: 界面配置=None,
        on_save: Callable[[str, str, str], None]=None,
        width: int=USER_CARD_WIDTH,
    ) -> ft.Column:
        if config is None:
            config = 界面配置()
        
        ThemeProvider.initialize(config)
        theme_colors = config.当前主题颜色
        
        账号界面.当前参与数量 = 0
        账号界面.账号开关状态 = {}
        
        cards: List[ft.Control] = []
        card_data: Dict[str, Dict[str, Any]] = {}
        
        count_text = ft.Text(
            f"已启用: {账号界面.当前参与数量}/{账号界面.授权数量}",
            size=14,
            color=theme_colors.get("text_secondary"),
        )
        
        def create_input(value: str, hint: str, password: bool=False, width: int=120) -> ft.Container:
            input_field = ft.TextField(
                value=value,
                hint_text=hint,
                password=password,
                can_reveal_password=password,
                width=width,
                height=32,
                text_size=12,
                border_radius=6,
                bgcolor=theme_colors.get("bg_secondary"),
                border_color=theme_colors.get("border"),
                focused_border_color=theme_colors.get("accent"),
                text_style=ft.TextStyle(color=theme_colors.get("text_primary")),
                hint_style=ft.TextStyle(color=theme_colors.get("text_hint")),
            )
            return ft.Container(content=input_field, height=32)
        
        def create_card(
            card_id: str,
            title: str,
            icon: str,
            subtitle: str,
            enabled: bool=True,
        ) -> ft.Container:
            def handle_save(config_key: str, value: str):
                if card_id not in card_data:
                    card_data[card_id] = {}
                card_data[card_id][config_key] = value
                
                if on_save:
                    on_save(card_id, config_key, value)
            
            role_dropdown = Dropdown.create(
                options=["主帅", "副帅"],
                value="主帅" if card_id == "01账号" else "副帅",
                width=70,
                on_change=lambda v: handle_save("统帅种类", v),
            )
            
            platform_dropdown = Dropdown.create(
                options=["Tap", "九游", "Fan", "小7", "Vivo", "Opop"],
                value="Tap",
                width=70,
                on_change=lambda v: handle_save("平台", v),
            )
            
            name_input = create_input("", "名称")
            account_input = create_input("", "账号")
            password_input = create_input("", "密码", password=True)
            
            controls_config = [
                {"type": "custom", "control": role_dropdown},
                {"type": "custom", "control": name_input},
                {"type": "custom", "control": account_input},
                {"type": "custom", "control": password_input},
                {"type": "custom", "control": platform_dropdown},
            ]
            
            card = CollapsibleCard.create(
                title=title,
                icon=icon,
                subtitle=subtitle,
                enabled=enabled,
                controls_config=[],
                controls_per_row=5,
                width=width,
                on_save=handle_save,
            )
            
            cards.append(card)
            return card
        
        for i in range(1, MAX_ACCOUNTS + 1):
            card_id = f"{i:02d}账号"
            default_subtitle = "未参与挂机"
            
            create_card(
                card_id=card_id,
                title=card_id,
                icon="ACCOUNT_CIRCLE",
                subtitle=default_subtitle,
                enabled=False,
            )
        
        header = ft.Row([
            ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=20, color=theme_colors.get("accent")),
            ft.Container(width=8),
            ft.Text("账号设置", size=16, weight=ft.FontWeight.BOLD, color=theme_colors.get("text_primary")),
            ft.Container(width=20),
            count_text,
        ], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER)
        
        content = ft.Column(
            controls=[header, ft.Divider(height=1, color=theme_colors.get("border"))] + cards,
            spacing=USER_CARD_SPACING,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )
        
        def get_all_values() -> Dict[str, Dict[str, str]]:
            result = {}
            for i, card in enumerate(cards):
                if hasattr(card, 'get_values'):
                    card_id = list(card_data.keys())[i] if i < len(card_data) else f"card_{i}"
                    result[card_id] = card.get_values()
            return result
        
        def dispose():
            for card in cards:
                if hasattr(card, 'dispose'):
                    card.dispose()
        
        content.get_all_values = get_all_values
        content.dispose = dispose
        
        return content


if __name__ == "__main__":
    config = 界面配置()
    ThemeProvider.initialize(config)
    
    def on_save(card_id, key, value):
        print(f"保存: {card_id}.{key} = {value}")
    
    ft.run(lambda page: page.add(账号界面.create(config=config, on_save=on_save)))
