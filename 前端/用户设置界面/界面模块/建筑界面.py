# -*- coding: utf-8 -*-
"""
模块名称：建筑界面 | 层级：界面模块层
设计思路：
    建筑界面，包含建筑升级、资源生产等设置卡片。
    使用配置管理器获取和保存配置值。

功能：
    1. 建筑升级设置
    2. 资源生产设置

对外接口：
    - create(): 创建建筑界面
"""

import flet as ft
from typing import Callable
from 前端.配置.界面配置 import 界面配置
from 前端.配置.配置管理器 import ConfigManager
from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider
from 前端.用户设置界面.组件模块.通用卡片 import UniversalCard
from 前端.用户设置界面.组件模块.功能容器 import FunctionContainer
from 前端.用户设置界面.单元模块.下拉框 import Dropdown


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
        
        def on_value_change(card_name: str, config_key: str, value):
            """值变化回调 - 保存配置"""
            print(f"配置变化: {card_name}.{config_key} = {value}")
            if config_manager:
                config_manager.set_value(card_name, config_key, value)
        
        def create_dropdown_control(label: str, options: list, value: str, card_name: str, config_key: str, width: int = None):
            """创建下拉框控件"""
            dropdown = Dropdown.create(
                options=options,
                value=value,
                width=width,
                on_change=lambda v: on_value_change(card_name, config_key, v),
            )
            
            label_text = ft.Text(
                label,
                color=ThemeProvider.get_color("text_secondary"),
                size=14,
            )
            
            return ft.Row(
                [label_text, dropdown],
                alignment=ft.MainAxisAlignment.END,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8,
                expand=True,
            )
        
        upgrade_value = config_manager.get_value("建筑升级", "升级模式", "自动") if config_manager else "自动"
        upgrade_control = create_dropdown_control(
            label="升级模式:",
            options=["自动", "手动"],
            value=upgrade_value,
            card_name="建筑升级",
            config_key="升级模式",
        )
        
        upgrade_card = UniversalCard.create(
            title="建筑升级",
            icon="DOMAIN",
            subtitle="自动升级建筑，优先升级核心建筑",
            enabled=True,
            controls=[upgrade_control],
        )
        
        resource_value = config_manager.get_value("资源生产", "生产模式", "平衡") if config_manager else "平衡"
        resource_control = create_dropdown_control(
            label="生产模式:",
            options=["平衡", "木材优先", "铁矿优先", "粮食优先"],
            value=resource_value,
            card_name="资源生产",
            config_key="生产模式",
        )
        
        resource_card = UniversalCard.create(
            title="资源生产",
            icon="PRODUCTION_QUANTITY_LIMITS",
            subtitle="调整资源生产优先级",
            enabled=True,
            controls=[resource_control],
        )
        
        return FunctionContainer.create(
            config=配置,
            title="建筑设置",
            icon="DOMAIN",
            cards=[upgrade_card, resource_card],
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