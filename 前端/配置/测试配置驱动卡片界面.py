# -*- coding: utf-8 -*-
"""
测试配置驱动创建卡片的界面效果

测试目标:
    在实际界面中展示配置驱动创建的三个卡片。

测试步骤:
    1. 创建配置管理器
    2. 使用配置驱动创建三个卡片
    3. 在界面中展示卡片效果
"""

import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import flet as ft
from 前端.配置.配置管理器 import ConfigManager
from 前端.配置.界面配置 import 界面配置
from 前端.新思路.组件层.通用卡片配置驱动扩展 import UniversalCard


def main(page: ft.Page):
    """主函数"""
    page.title = "配置驱动卡片测试"
    page.padding = 20
    page.bgcolor = "#1A1A2E"
    
    # 创建配置管理器和界面配置
    config_manager = ConfigManager()
    ui_config = 界面配置()
    
    # 设置页面背景色
    page.bgcolor = ui_config.当前主题颜色.get("bg_primary", "#1A1A2E")
    
    # 创建标题
    title = ft.Text(
        "配置驱动卡片测试",
        size=24,
        weight=ft.FontWeight.BOLD,
        color=ui_config.当前主题颜色.get("text_primary", "#FFFFFF"),
    )
    
    # 创建值变化回调
    def on_value_change(config_key: str, value: any):
        """值变化回调"""
        print(f"配置变化: {config_key} = {value}")
        page.snack_bar = ft.SnackBar(
            content=ft.Text(f"配置变化: {config_key} = {value}"),
            bgcolor=ui_config.当前主题颜色.get("accent", "#0078D4"),
        )
        page.snack_bar.open = True
        page.update()
    
    # 使用配置驱动创建三个卡片
    print("创建基础设置卡片...")
    basic_card = UniversalCard.create_from_config(
        config=ui_config,
        card_name="基础设置",
        config_manager=config_manager,
        on_value_change=on_value_change,
    )
    
    print("创建主题设置卡片...")
    theme_card = UniversalCard.create_from_config(
        config=ui_config,
        card_name="主题设置",
        config_manager=config_manager,
        on_value_change=on_value_change,
    )
    
    print("创建调色板设置卡片...")
    palette_card = UniversalCard.create_from_config(
        config=ui_config,
        card_name="调色板设置",
        config_manager=config_manager,
        on_value_change=on_value_change,
    )
    
    # 创建页面内容
    content = ft.Column(
        [
            title,
            ft.Divider(height=20, color=ui_config.当前主题颜色.get("divider", "#E5E5E5")),
            basic_card,
            ft.Container(height=16),
            theme_card,
            ft.Container(height=16),
            palette_card,
        ],
        scroll=ft.ScrollMode.AUTO,
    )
    
    page.add(content)
    print("界面创建完成，请查看界面效果")


if __name__ == "__main__":
    ft.run(main)
