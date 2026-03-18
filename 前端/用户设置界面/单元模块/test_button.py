# -*- coding: utf-8 -*-
"""测试导航按钮显示"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft
from 前端.配置.界面配置 import 界面配置
from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider
from 前端.用户设置界面.单元模块.通用按钮 import Button

配置 = 界面配置()
ThemeProvider.initialize(配置)

def main(page: ft.Page):
    page.title = "导航按钮测试"
    page.bgcolor = ThemeProvider.get_color("bg_primary")
    
    # 测试导航按钮
    nav_button = Button.create(
        text="系统设置",
        icon="SETTINGS",
        style="nav",
        selected=True,
        width=250,
        height=36,
    )
    
    # 测试普通按钮
    normal_button = Button.create(
        text="普通按钮",
        icon="SETTINGS",
        style="text",
        selected=False,
        width=250,
        height=36,
    )
    
    page.add(
        ft.Column([
            ft.Text("导航按钮测试", size=20, color=ThemeProvider.get_color("text_primary")),
            ft.Container(height=20),
            nav_button,
            ft.Container(height=10),
            normal_button,
        ], spacing=10)
    )

ft.run(main)
