# -*- coding: utf-8 -*-
"""
模块名称：建筑界面 | 层级：界面模块层
设计思路：
    建筑界面，包含多个建筑等级设置卡片。
    使用懒加载机制，默认加载"主帅主城"，其他卡片点击后加载。
    切换时销毁上一个卡片，保持内存低占用。

功能：
    1. 默认加载"主帅主城"
    2. 其他卡片显示"点击加载"
    3. 切换时保存上一个卡片数据并销毁

对外接口：
    - create(): 创建建筑界面
"""

import flet as ft
from typing import Callable
from 前端.用户设置界面.配置.界面配置 import 界面配置
from 前端.用户设置界面.配置.配置管理器 import ConfigManager
from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider
from 前端.用户设置界面.组件模块.懒加载卡片 import LazyCard
from 前端.用户设置界面.组件模块.懒加载状态管理器 import LazyState
from 前端.用户设置界面.组件模块.通用功能容器 import GenericFunctionContainer


class BuildingInterface:
    """建筑界面 - 界面模块层"""
    
    @staticmethod
    def create(page: ft.Page = None, on_refresh: Callable[[], None] = None) -> ft.Container:
        """
        创建建筑界面
        
        参数：
            page: 页面对象（可选，用于更新页面显示）
            on_refresh: 刷新回调
        
        返回：
            ft.Container: 建筑界面容器
        """
        配置 = 界面配置()
        
        try:
            config_manager = ConfigManager()
        except ImportError:
            config_manager = None
        
        state = LazyState()
        state.set_config_manager(config_manager)
        
        def on_value_change(config_key: str, value):
            """值变化回调 - 保存配置"""
            print(f"配置变化: {config_key} = {value}")
        
        card_names = ["主帅主城", "主帅分城", "付帅主城", "付帅分城", "军团城市"]
        
        lazy_cards = []
        for i, card_name in enumerate(card_names):
            card_config = config_manager.get_card_config(card_name) if config_manager else None
            if card_config:
                is_default = (i == 0)
                card = LazyCard(
                    card_name=card_name,
                    card_config=card_config,
                    config_manager=config_manager,
                    on_value_change=on_value_change,
                    is_default=is_default,
                )
                lazy_cards.append(card.create())
        
        return GenericFunctionContainer.create(
            config=配置,
            title="建筑设置",
            icon="DOMAIN",
            cards=lazy_cards,
            expand=True,
        )


# *** 调试逻辑 ***
if __name__ == "__main__":
    配置 = 界面配置()
    ThemeProvider.initialize(配置)
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        page.add(BuildingInterface.create())
    ft.run(main)
