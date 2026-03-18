# -*- coding: utf-8 -*-
"""简单测试Icon和Text显示"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft
from 前端.配置.界面配置 import 界面配置
from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider

配置 = 界面配置()
ThemeProvider.initialize(配置)

def main(page: ft.Page):
    page.title = "Icon和Text测试"
    page.bgcolor = ThemeProvider.get_color("bg_primary")
    
    # 测试1：直接使用Icon和Text
    test1 = ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.SETTINGS, color="#FFFFFF", size=18),
            ft.Text("系统设置", color="#FFFFFF", size=14),
        ], spacing=8, alignment=ft.MainAxisAlignment.START, expand=True),
        width=250,
        height=36,
        bgcolor="#0078D4",
        border_radius=8,
        padding=ft.padding.symmetric(horizontal=12, vertical=8),
        alignment=ft.Alignment(-1, 0),
    )
    
    # 测试2：使用ft.IconButton
    test2 = ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.SETTINGS, color="#C5C5C5", size=18),
            ft.Text("策略设置", color="#C5C5C5", size=14),
        ], spacing=8, alignment=ft.MainAxisAlignment.START, expand=True),
        width=250,
        height=36,
        bgcolor="#2D2D2D",
        border_radius=8,
        border=ft.border.all(1, "#0078D4"),
        padding=ft.padding.symmetric(horizontal=12, vertical=8),
        alignment=ft.Alignment(-1, 0),
    )
    
    page.add(
        ft.Column([
            ft.Text("Icon和Text显示测试", size=20, color="#FFFFFF"),
            ft.Container(height=20),
            test1,
            ft.Container(height=10),
            test2,
        ], spacing=10)
    )

ft.run(main)
