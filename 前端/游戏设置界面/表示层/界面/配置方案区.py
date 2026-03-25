# -*- coding: utf-8 -*-
"""
模块名称：ConfigSchemeSection
模块功能：配置方案界面，支持多套配置管理
实现步骤：
- 创建配置方案卡片列表
- 支持加载/保存配置
- 支持新建配置方案
"""

import flet as ft
from typing import Dict, Any, List, Callable, Optional
import json
import os
from datetime import datetime

from 前端.游戏设置界面.核心层.配置.界面配置 import UIConfig
from 前端.游戏设置界面.表示层.组件.复合.卡片组管理器 import CardGroupManager, create_managed_card
from 前端.游戏设置界面.业务层.服务.配置服务 import ConfigService


USER_CARD_SPACING = 10
USER_SPACING = 10
USER_SCHEME_DIR = "前端/游戏设置界面/配置/方案"


class ConfigSchemeSection:
    """配置方案界面 - 支持多套配置管理"""
    
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
        manager = CardGroupManager(destroy_strategy="none")
        scheme_list: List[Dict[str, Any]] = []
        card_refs: Dict[str, ft.Container] = {}
        
        def load_scheme_list():
            os.makedirs(USER_SCHEME_DIR, exist_ok=True)
            scheme_file = os.path.join(USER_SCHEME_DIR, "scheme_list.json")
            if os.path.exists(scheme_file):
                with open(scheme_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                default_schemes = [
                    {"id": "scheme_01", "name": "默认配置", "created": "2026-03-25"},
                    {"id": "scheme_02", "name": "高速模式", "created": "2026-03-25"},
                    {"id": "scheme_03", "name": "多账号挂机", "created": "2026-03-25"},
                ]
                with open(scheme_file, 'w', encoding='utf-8') as f:
                    json.dump(default_schemes, f, ensure_ascii=False, indent=2)
                return default_schemes
        
        def save_scheme_list():
            os.makedirs(USER_SCHEME_DIR, exist_ok=True)
            scheme_file = os.path.join(USER_SCHEME_DIR, "scheme_list.json")
            with open(scheme_file, 'w', encoding='utf-8') as f:
                json.dump(scheme_list, f, ensure_ascii=False, indent=2)
        
        scheme_list.extend(load_scheme_list())
        
        def load_scheme(scheme_id: str):
            scheme_file = os.path.join(USER_SCHEME_DIR, f"{scheme_id}.json")
            if os.path.exists(scheme_file):
                with open(scheme_file, 'r', encoding='utf-8') as f:
                    scheme_config = json.load(f)
                    for key, value in scheme_config.items():
                        config_service._repository.set_value(key, value)
                return True
            return False
        
        def save_scheme(scheme_id: str):
            os.makedirs(USER_SCHEME_DIR, exist_ok=True)
            scheme_file = os.path.join(USER_SCHEME_DIR, f"{scheme_id}.json")
            current_config = config_service._repository._cache.copy()
            with open(scheme_file, 'w', encoding='utf-8') as f:
                json.dump(current_config, f, ensure_ascii=False, indent=2)
            return True
        
        def create_scheme_card(scheme: Dict[str, Any]) -> ft.Container:
            scheme_id = scheme.get("id", "")
            scheme_name = scheme.get("name", "未命名方案")
            
            name_input = ft.TextField(
                value=scheme_name,
                width=200,
                text_size=14,
                border_color=theme_colors.get("border"),
                focused_border_color=theme_colors.get("accent"),
                text_style=ft.TextStyle(color=theme_colors.get("text_primary")),
                on_change=lambda e: update_scheme_name(scheme_id, e.control.value),
            )
            
            load_btn = ft.ElevatedButton(
                "加载",
                width=70,
                height=32,
                style=ft.ButtonStyle(
                    bgcolor=theme_colors.get("accent"),
                    color="#FFFFFF",
                ),
                on_click=lambda e: handle_load(scheme_id),
            )
            
            save_btn = ft.OutlinedButton(
                "保存",
                width=70,
                height=32,
                style=ft.ButtonStyle(
                    color=theme_colors.get("accent"),
                    side=ft.BorderSide(1, theme_colors.get("accent")),
                ),
                on_click=lambda e: handle_save(scheme_id),
            )
            
            controls = [
                name_input,
                ft.Container(width=20),
                load_btn,
                ft.Container(width=10),
                save_btn,
            ]
            
            card = create_managed_card(
                manager=manager,
                title=scheme_name,
                icon="FOLDER",
                subtitle=f"创建于: {scheme.get('created', '未知')}",
                enabled=True,
                controls=controls,
                controls_per_row=5,
                config=config,
            )
            
            card_refs[scheme_id] = card
            return card
        
        def update_scheme_name(scheme_id: str, new_name: str):
            for scheme in scheme_list:
                if scheme.get("id") == scheme_id:
                    scheme["name"] = new_name
                    break
            save_scheme_list()
        
        def handle_load(scheme_id: str):
            if load_scheme(scheme_id):
                print(f"已加载方案: {scheme_id}")
        
        def handle_save(scheme_id: str):
            if save_scheme(scheme_id):
                print(f"已保存方案: {scheme_id}")
        
        def create_new_scheme():
            new_id = f"scheme_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            new_scheme = {
                "id": new_id,
                "name": f"新方案 {len(scheme_list) + 1}",
                "created": datetime.now().strftime("%Y-%m-%d"),
            }
            scheme_list.append(new_scheme)
            save_scheme_list()
            
            new_card = create_scheme_card(new_scheme)
            card_column.controls.append(new_card)
            try:
                if card_column.page:
                    card_column.update()
            except:
                pass
        
        card_list = [create_scheme_card(scheme) for scheme in scheme_list]
        
        new_scheme_btn = ft.Container(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.ADD, size=20, color=theme_colors.get("accent")),
                    ft.Text("新建配置方案", size=14, color=theme_colors.get("accent")),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            height=50,
            border_radius=8,
            border=ft.border.all(1, theme_colors.get("border")),
            on_click=lambda e: create_new_scheme(),
            on_hover=lambda e: handle_hover(e),
        )
        
        def handle_hover(e):
            if e.data == "true":
                new_scheme_btn.border = ft.border.all(1, theme_colors.get("accent"))
            else:
                new_scheme_btn.border = ft.border.all(1, theme_colors.get("border"))
            try:
                if new_scheme_btn.page:
                    new_scheme_btn.update()
            except:
                pass
        
        title_bar = ft.Row([
            ft.Icon(ft.Icons.FOLDER, size=20, color=theme_colors.get("accent")),
            ft.Container(width=6),
            ft.Text("配置方案", size=16, weight=ft.FontWeight.BOLD, color=theme_colors.get("text_primary")),
        ], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER)
        
        card_column = ft.Column(
            controls=card_list + [ft.Container(height=USER_SPACING), new_scheme_btn],
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
        
        content_column.card_manager = manager
        
        return content_column, manager


# *** 标准测试格式: 仅调用被测模块,AI不得添加数据 ***
if __name__ == "__main__":
    def main(page: ft.Page):
        config = UIConfig()
        service = ConfigService()
        section, manager = ConfigSchemeSection.create(config=config, config_service=service)
        page.add(section)
    
    ft.app(target=main)
