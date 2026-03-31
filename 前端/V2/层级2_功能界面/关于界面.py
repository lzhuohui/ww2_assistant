# -*- coding: utf-8 -*-

"""
模块名称：关于界面.py
模块功能：关于界面 - 显示软件信息

显示内容：
- 软件名称
- 版本号
- 开发框架
- 设计规范
"""

import flet as ft
from typing import Callable, Dict, Any

class AboutPage:
    @staticmethod
    def create(page: ft.Page, config_service, on_change: Callable = None, theme_colors: Dict = None) -> ft.Control:
        if theme_colors is None:
            theme_colors = {"text_primary": "#000000", "text_secondary": "#666666", "bg_card": "#FFFFFF", "accent": "#0078D4"}
        
        content = ft.Column([
            ft.Container(
                content=ft.Text("二战风云辅助工具", size=20, weight=ft.FontWeight.BOLD, color=theme_colors.get("text_primary")),
                padding=ft.padding.only(bottom=8)
            ),
            ft.Container(
                content=ft.Text("版本: V2.0", size=14, color=theme_colors.get("text_secondary")),
                padding=ft.padding.only(bottom=4)
            ),
            ft.Container(
                content=ft.Text("基于Flet框架开发", size=14, color=theme_colors.get("text_secondary")),
                padding=ft.padding.only(bottom=4)
            ),
            ft.Container(
                content=ft.Text("遵循Windows 11设计规范", size=14, color=theme_colors.get("text_secondary")),
                padding=ft.padding.only(bottom=4)
            ),
            ft.Container(
                content=ft.Text("模块化架构设计", size=14, color=theme_colors.get("text_secondary")),
                padding=ft.padding.only(bottom=4)
            ),
            ft.Container(
                content=ft.Text("五层架构: 主入口→功能界面→卡片组→复合模块→基础模块", size=12, color=theme_colors.get("text_secondary")),
                padding=ft.padding.only(bottom=4)
            ),
        ], spacing=0)
        
        return ft.Container(content=content, padding=16)
    
    @staticmethod
    def destroy():
        pass

if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    
    from 前端.V2.数据层.仓库.配置仓库 import ConfigRepository
    from 前端.V2.业务层.服务.配置服务 import ConfigService
    
    def main(page: ft.Page):
        page.title = "关于界面测试"
        
        repository = ConfigRepository()
        config_service = ConfigService(repository)
        
        about_page = AboutPage.create(page, config_service)
        page.add(about_page)
    
    ft.run(main)
