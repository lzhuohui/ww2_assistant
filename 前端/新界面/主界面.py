# -*- coding: utf-8 -*-
"""
模块名称：主界面
设计思路: 新界面系统的主入口，集成所有功能界面和配置导出
模块隔离: 只负责界面组装，不包含游戏控制逻辑
"""

import flet as ft
from typing import Dict, Any, Callable, Optional
from datetime import datetime

from 前端.新界面.核心接口.界面配置 import 界面配置
from 前端.新界面.核心接口.主题提供者 import ThemeProvider
from 前端.新界面.界面模块.系统界面 import 系统界面
from 前端.新界面.界面模块.策略界面 import 策略界面
from 前端.新界面.界面模块.任务界面 import 任务界面
from 前端.新界面.界面模块.建筑界面 import 建筑界面
from 前端.新界面.界面模块.集资界面 import 集资界面
from 前端.新界面.界面模块.账号界面 import 账号界面
from 前端.新界面.界面模块.打扫界面 import 打扫界面
from 前端.新界面.界面模块.打野界面 import 打野界面
from 前端.新界面.界面模块.个性化界面 import 个性化界面
from 前端.新界面.界面模块.关于界面 import 关于界面
from 前端.新界面.服务.配置收集器 import ConfigCollector
from 前端.新界面.服务.数据输出服务 import DataOutputService


# *** 用户指定变量 - AI不得修改, 变量值必须生效 ***
USER_WINDOW_WIDTH = 1200
USER_WINDOW_HEIGHT = 540
USER_SPACING = 5
USER_NAV_WIDTH = 280
USER_USER_INFO_HEIGHT = 90
# *********************************


class 主界面:
    """主界面 - 集成所有功能界面"""
    
    current_nav = "系统"
    content_area = None
    config_collector: Optional[ConfigCollector] = None
    output_service: Optional[DataOutputService] = None
    
    @staticmethod
    def setup_window(page: ft.Page) -> None:
        page.title = "用户设置"
        page.window.width = USER_WINDOW_WIDTH
        page.window.height = USER_WINDOW_HEIGHT
        page.window.resizable = False
        page.bgcolor = ThemeProvider.get_color("bg_primary")
        page.padding = 0
    
    @staticmethod
    def create_user_info(config: 界面配置) -> ft.Container:
        """创建用户信息卡片"""
        theme_colors = config.当前主题颜色
        
        avatar = ft.Container(
            content=ft.Text("帅", size=24, weight=ft.FontWeight.BOLD, color="#FFD700"),
            width=48,
            height=48,
            bgcolor=theme_colors.get("bg_card"),
            border_radius=24,
            alignment=ft.Alignment(0, 0),
        )
        
        name_text = ft.Text("试用用户", size=14, weight=ft.FontWeight.BOLD, color=theme_colors.get("text_primary"))
        status_text = ft.Text("试用剩余 7 天", size=12, color=theme_colors.get("text_secondary"))
        
        content = ft.Row([
            avatar,
            ft.Container(width=12),
            ft.Column([name_text, status_text], spacing=4, alignment=ft.MainAxisAlignment.CENTER),
        ], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER)
        
        return ft.Container(
            content=content,
            height=USER_USER_INFO_HEIGHT,
            padding=16,
            bgcolor=theme_colors.get("bg_card"),
            border_radius=8,
        )
    
    @staticmethod
    def get_page_content(nav_name: str, config: 界面配置, collector: ConfigCollector) -> ft.Control:
        """获取页面内容"""
        def on_save(card_id: str, config_key: str, value: str):
            collector.set_value(nav_name, card_id, config_key, value)
        
        if nav_name == "系统":
            return 系统界面.create(config=config, on_save=on_save)
        elif nav_name == "策略":
            return 策略界面.create(config=config, on_save=on_save)
        elif nav_name == "任务":
            return 任务界面.create(config=config, on_save=on_save)
        elif nav_name == "建筑":
            return 建筑界面.create(config=config, on_save=on_save)
        elif nav_name == "集资":
            return 集资界面.create(config=config, on_save=on_save)
        elif nav_name == "账号":
            return 账号界面.create(config=config, on_save=on_save)
        elif nav_name == "打扫":
            return 打扫界面.create(config=config, on_save=on_save)
        elif nav_name == "打野":
            return 打野界面.create(config=config, on_save=on_save)
        elif nav_name == "个性化":
            return 个性化界面.create(config=config)
        elif nav_name == "关于":
            return 关于界面.create(config=config)
        else:
            return ft.Column([
                ft.Text(nav_name, size=20, weight=ft.FontWeight.BOLD, color=config.当前主题颜色.get("text_primary")),
                ft.Container(height=24),
                ft.Text(f"{nav_name}页面开发中...", size=14, color=config.当前主题颜色.get("text_secondary")),
            ], spacing=0, expand=True)
    
    @staticmethod
    def create_export_button(config: 界面配置, collector: ConfigCollector, page: ft.Page) -> ft.Container:
        """创建导出按钮"""
        theme_colors = config.当前主题颜色
        
        def on_export_click(e):
            try:
                game_config = collector.export_for_game()
                file_path = 主界面.output_service.save_game_config(game_config)
                
                snack = ft.SnackBar(
                    content=ft.Text(f"配置已导出: {file_path}", color=theme_colors.get("text_primary")),
                    bgcolor=theme_colors.get("success"),
                )
                page.snack_bar = snack
                snack.open = True
                page.update()
            except Exception as ex:
                snack = ft.SnackBar(
                    content=ft.Text(f"导出失败: {str(ex)}", color=theme_colors.get("text_primary")),
                    bgcolor=theme_colors.get("error"),
                )
                page.snack_bar = snack
                snack.open = True
                page.update()
        
        return ft.Container(
            content=ft.ElevatedButton(
                content=ft.Row([
                    ft.Icon(ft.Icons.SAVE, size=16, color=theme_colors.get("text_primary")),
                    ft.Text("导出配置", size=12, color=theme_colors.get("text_primary")),
                ], spacing=4, alignment=ft.MainAxisAlignment.CENTER),
                style=ft.ButtonStyle(
                    bgcolor=theme_colors.get("accent"),
                    shape=ft.RoundedRectangleBorder(radius=6),
                ),
                on_click=on_export_click,
            ),
            padding=ft.Padding(left=12, right=12, top=8, bottom=8),
        )
    
    @staticmethod
    def create(
        config: 界面配置=None,
        on_save: Callable[[str, str, str], None]=None,
        page: ft.Page=None,
    ) -> ft.Container:
        if config is None:
            config = 界面配置()
        
        ThemeProvider.initialize(config)
        theme_colors = config.当前主题颜色
        
        主界面.config_collector = ConfigCollector()
        主界面.output_service = DataOutputService()
        
        nav_items = [
            {"id": "系统", "icon": ft.Icons.SETTINGS},
            {"id": "策略", "icon": ft.Icons.ROCKET_LAUNCH},
            {"id": "任务", "icon": ft.Icons.ASSIGNMENT},
            {"id": "建筑", "icon": ft.Icons.DOMAIN},
            {"id": "集资", "icon": ft.Icons.SHOPPING_CART},
            {"id": "账号", "icon": ft.Icons.ACCOUNT_CIRCLE},
            {"id": "打扫", "icon": ft.Icons.CLEANING_SERVICES},
            {"id": "打野", "icon": ft.Icons.EXPLORE},
            {"id": "个性化", "icon": ft.Icons.PALETTE},
            {"id": "关于", "icon": ft.Icons.INFO},
        ]
        
        nav_buttons = []
        current_selected = [0]
        
        def handle_nav_click(index: int):
            current_selected[0] = index
            nav_name = nav_items[index]["id"]
            
            for i, btn in enumerate(nav_buttons):
                btn.bgcolor = theme_colors.get("accent") if i == index else theme_colors.get("bg_secondary")
                if btn.page:
                    btn.update()
            
            if 主界面.content_area:
                content = 主界面.get_page_content(nav_name, config, 主界面.config_collector)
                主界面.content_area.content = content
                
                try:
                    主界面.content_area.update()
                except:
                    pass
        
        for i, item in enumerate(nav_items):
            initial_bgcolor = theme_colors.get("accent") if i == 0 else theme_colors.get("bg_secondary")
            btn = ft.Container(
                content=ft.Row([
                    ft.Icon(item["icon"], size=18, color=theme_colors.get("text_primary")),
                    ft.Container(width=8),
                    ft.Text(item["id"], size=13, color=theme_colors.get("text_primary")),
                ], spacing=0, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                padding=ft.Padding(left=12, right=12, top=10, bottom=10),
                bgcolor=initial_bgcolor,
                border_radius=6,
                on_click=lambda e, idx=i: handle_nav_click(idx),
            )
            nav_buttons.append(btn)
        
        user_info = 主界面.create_user_info(config)
        
        export_button = 主界面.create_export_button(config, 主界面.config_collector, page) if page else ft.Container()
        
        nav_column = ft.Column(
            controls=nav_buttons,
            spacing=3,
            expand=True,
        )
        
        nav_panel = ft.Container(
            content=ft.Column([
                user_info,
                ft.Container(height=USER_SPACING),
                nav_column,
                ft.Container(height=USER_SPACING),
                export_button,
            ], spacing=0),
            width=USER_NAV_WIDTH,
            padding=USER_SPACING,
            bgcolor=theme_colors.get("bg_secondary"),
        )
        
        content_container = ft.Container(
            content=主界面.get_page_content(主界面.current_nav, config, 主界面.config_collector),
            padding=USER_SPACING * 2,
            expand=True,
        )
        
        主界面.content_area = content_container
        
        main_row = ft.Row([
            nav_panel,
            ft.VerticalDivider(width=1, color=theme_colors.get("border")),
            content_container,
        ], expand=True, spacing=0)
        
        return ft.Container(
            content=main_row,
            bgcolor=theme_colors.get("bg_primary"),
            expand=True,
        )
    
    @staticmethod
    def get_game_config() -> Dict[str, Any]:
        """获取游戏控制配置（供外部调用）"""
        if 主界面.config_collector:
            return 主界面.config_collector.export_for_game()
        return {}
    
    @staticmethod
    def save_game_config() -> str:
        """保存游戏控制配置（供外部调用）"""
        if 主界面.config_collector and 主界面.output_service:
            game_config = 主界面.config_collector.export_for_game()
            return 主界面.output_service.save_game_config(game_config)
        return ""


if __name__ == "__main__":
    config = 界面配置()
    ThemeProvider.initialize(config)
    
    def main(page: ft.Page):
        主界面.setup_window(page)
        page.add(主界面.create(config=config, page=page))
    
    ft.run(main)
