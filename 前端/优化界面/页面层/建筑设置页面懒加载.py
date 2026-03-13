# -*- coding: utf-8 -*-
"""
建筑设置页面（懒加载版） - 页面层

设计思路:
    使用懒加载通用卡片，点击后才加载实际控件。
    切换时销毁上一个卡片，保持内存低占用。
    完全独立于新思路目录。

功能:
    1. 默认加载"主帅主城"
    2. 其他卡片显示"点击加载"
    3. 切换时保存上一个卡片数据并销毁

使用场景:
    被优化界面主界面调用。
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft
from typing import Callable
from 配置.界面配置 import 界面配置
from 配置.配置管理器 import ConfigManager
from 优化界面.组件层.懒加载通用卡片 import LazyUniversalCard, LazyCardManager

DEFAULT_DROPDOWN_WIDTH = 60


class BuildingSettingsPageLazy:
    """建筑设置页面（懒加载版）"""
    
    @staticmethod
    def create(config: 界面配置, page: ft.Page = None, on_refresh: Callable[[], None] = None) -> ft.Container:
        """
        创建建筑设置页面（懒加载版）
        
        参数:
            config: 界面配置对象
            page: 页面对象
            on_refresh: 刷新回调
        
        返回:
            ft.Container: 建筑设置页面容器
        """
        theme_colors = config.当前主题颜色
        
        # 创建配置管理器
        config_manager = ConfigManager()
        manager = LazyCardManager()
        manager.config_manager = config_manager
        
        # 为建筑配置中的所有下拉框添加width参数
        for card_name, card_config in config_manager.building_configs.items():
            if "controls" in card_config:
                for control in card_config["controls"]:
                    if control.get("type") == "dropdown" and "width" not in control:
                        control["width"] = DEFAULT_DROPDOWN_WIDTH
        
        # 创建值变化回调
        def on_value_change(config_key: str, value: any):
            """值变化回调"""
            print(f"配置变化: {config_key} = {value}")
        
        # 定义卡片顺序
        card_names = ["主帅主城", "主帅分城", "付帅主城", "付帅分城", "军团城市"]
        
        # 创建懒加载卡片
        lazy_cards = []
        for i, card_name in enumerate(card_names):
            card_config = config_manager.get_card_config(card_name)
            if card_config:
                is_default = (i == 0)  # 第一个卡片默认加载
                card = LazyUniversalCard(
                    config=config,
                    card_name=card_name,
                    card_config=card_config,
                    config_manager=config_manager,
                    on_value_change=on_value_change,
                    is_default=is_default,
                )
                lazy_cards.append(card.create())
        
        # 创建页面内容
        page_content = ft.Column(
            [
                ft.Text(
                    "建筑设置",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=theme_colors.get("text_primary"),
                ),
                ft.Container(height=20),
                *[ft.Container(content=card, margin=ft.Margin(bottom=15)) for card in lazy_cards],
            ],
            spacing=0,
            scroll=ft.ScrollMode.HIDDEN,
            expand=True,
        )
        
        # 页面容器
        page_container = ft.Container(
            content=page_content,
            padding=ft.Padding.all(20),
            expand=True,
        )
        
        return page_container


建筑设置页面懒加载 = BuildingSettingsPageLazy


if __name__ == "__main__":
    配置 = 界面配置()
    
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        page.add(BuildingSettingsPageLazy.create(配置))
    
    ft.run(main)
