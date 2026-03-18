# -*- coding: utf-8 -*-
"""
模块名称：集资界面 | 层级：界面模块层
设计思路：
    集资界面，包含集资管理、资源分配等设置卡片。
    使用配置管理器获取和保存配置值。

功能：
    1. 集资管理设置
    2. 资源分配设置

对外接口：
    - create(): 创建集资界面
"""

import flet as ft
from typing import Callable
from 前端.配置.界面配置 import 界面配置
from 前端.配置.配置管理器 import ConfigManager
from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider
from 前端.用户设置界面.组件模块.通用卡片 import UniversalCard
from 前端.用户设置界面.组件模块.功能容器 import FunctionContainer
from 前端.用户设置界面.单元模块.下拉框 import Dropdown


class FundraisingInterface:
    """集资界面 - 界面模块层"""
    
    @staticmethod
    def create(page: ft.Page = None, on_refresh: Callable[[], None] = None) -> ft.Container:
        """
        创建集资界面
        
        参数：
            page: 页面对象（可选，用于更新页面显示）
            on_refresh: 刷新回调
        
        返回：
            ft.Container: 集资界面容器
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
        
        fundraising_value = config_manager.get_value("集资管理", "集资模式", "自动") if config_manager else "自动"
        fundraising_control = create_dropdown_control(
            label="集资模式:",
            options=["自动", "手动"],
            value=fundraising_value,
            card_name="集资管理",
            config_key="集资模式",
        )
        
        fundraising_card = UniversalCard.create(
            title="集资管理",
            icon="SHOPPING_CART",
            subtitle="自动参与联盟集资，提升联盟等级",
            enabled=True,
            controls=[fundraising_control],
        )
        
        allocation_value = config_manager.get_value("资源分配", "分配比例", "平均") if config_manager else "平均"
        allocation_control = create_dropdown_control(
            label="分配比例:",
            options=["平均", "侧重木材", "侧重铁矿", "侧重粮食"],
            value=allocation_value,
            card_name="资源分配",
            config_key="分配比例",
        )
        
        allocation_card = UniversalCard.create(
            title="资源分配",
            icon="EQUALIZER",
            subtitle="调整资源分配比例，优化资源使用",
            enabled=True,
            controls=[allocation_control],
        )
        
        return FunctionContainer.create(
            config=配置,
            title="集资设置",
            icon="SHOPPING_CART",
            cards=[fundraising_card, allocation_card],
            expand=True,
        )


# *** 调试逻辑 ***
if __name__ == "__main__":
    配置 = 界面配置()
    ThemeProvider.initialize(配置)
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        page.add(FundraisingInterface.create())
    ft.run(main)