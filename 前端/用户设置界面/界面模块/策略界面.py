# -*- coding: utf-8 -*-
"""
模块名称：策略界面 | 层级：界面模块层
设计思路：
    策略界面，包含建筑速建、资源速产、策点保留等设置卡片。
    使用配置管理器获取和保存配置值。

功能：
    1. 建筑速建设置
    2. 资源速产设置
    3. 策点保留设置

对外接口：
    - create(): 创建策略界面
"""

import flet as ft
from typing import Callable
from 前端.配置.界面配置 import 界面配置
from 前端.配置.配置管理器 import ConfigManager
from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider
from 前端.用户设置界面.组件模块.通用卡片 import UniversalCard
from 前端.用户设置界面.组件模块.功能容器 import FunctionContainer
from 前端.用户设置界面.单元模块.下拉框 import Dropdown

# *** 用户指定变量 - AI不得修改 ***
# *********************************


class StrategyInterface:
    """策略界面 - 界面模块层"""
    
    @staticmethod
    def create(page: ft.Page = None, on_refresh: Callable[[], None] = None) -> ft.Container:
        """
        创建策略界面
        
        参数：
            page: 页面对象（可选，用于更新页面显示）
            on_refresh: 刷新回调
        
        返回：
            ft.Container: 策略界面容器
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
                spacing=8,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            )
        
        building_level_value = config_manager.get_value("建筑速建", "速建限级", "08级") if config_manager else "08级"
        building_type_value = config_manager.get_value("建筑速建", "速建类型", "城资建筑") if config_manager else "城资建筑"
        building_switch_value = config_manager.get_value("建筑速建", "速建开关", True) if config_manager else True
        
        building_level_control = create_dropdown_control(
            label="速建限级:",
            options=["05级", "06级", "07级", "08级", "09级", "10级", "11级", "12级", "13级", "14级", "15级"],
            value=building_level_value,
            card_name="建筑速建",
            config_key="速建限级",
        )
        
        building_type_control = create_dropdown_control(
            label="建筑类型:",
            options=["城资建筑", "城市建筑", "资源建筑"],
            value=building_type_value,
            card_name="建筑速建",
            config_key="速建类型",
        )
        
        building_card = UniversalCard.create(
            title="建筑速建",
            icon="ROCKET_LAUNCH",
            enabled=building_switch_value,
            on_state_change=lambda v: on_value_change("建筑速建", "速建开关", v),
            subtitle="开启自动加速建设功能",
            controls=[building_level_control, building_type_control],
            controls_per_row=2,
        )
        
        resource_level_value = config_manager.get_value("资源速产", "速产限级", "07级") if config_manager else "07级"
        resource_type_value = config_manager.get_value("资源速产", "速产类型", "平衡资源") if config_manager else "平衡资源"
        resource_switch_value = config_manager.get_value("资源速产", "速产开关", True) if config_manager else True
        
        resource_level_control = create_dropdown_control(
            label="速产限级:",
            options=["05级", "06级", "07级", "08级", "09级", "10级", "11级", "12级", "13级", "14级", "15级"],
            value=resource_level_value,
            card_name="资源速产",
            config_key="速产限级",
        )
        
        resource_type_control = create_dropdown_control(
            label="策略类型:",
            options=["平衡资源", "战时经济", "钢铁熔炉", "橡胶采集", "石油开采"],
            value=resource_type_value,
            card_name="资源速产",
            config_key="速产类型",
        )
        
        resource_card = UniversalCard.create(
            title="资源速产",
            icon="BOLT",
            enabled=resource_switch_value,
            on_state_change=lambda v: on_value_change("资源速产", "速产开关", v),
            subtitle="开启自动加速生产功能",
            controls=[resource_level_control, resource_type_control],
            controls_per_row=2,
        )
        
        points_value = config_manager.get_value("策点保留", "保留点数", "60点") if config_manager else "60点"
        points_switch_value = config_manager.get_value("策点保留", "保留开关", True) if config_manager else True
        
        points_control = create_dropdown_control(
            label="保留点数:",
            options=["30点", "60点", "90点", "120点", "150点", "180点", "210点", "240点"],
            value=points_value,
            card_name="策点保留",
            config_key="保留点数",
        )
        
        points_card = UniversalCard.create(
            title="策点保留",
            icon="SAVINGS",
            enabled=points_switch_value,
            on_state_change=lambda v: on_value_change("策点保留", "保留开关", v),
            subtitle="达到设置保留的策略点数后允许使用策略",
            controls=[points_control],
        )
        
        return FunctionContainer.create(
            config=配置,
            title="策略设置",
            icon="ROCKET_LAUNCH",
            cards=[building_card, resource_card, points_card],
            expand=True,
        )


# *** 调试逻辑 ***
if __name__ == "__main__":
    配置 = 界面配置()
    ThemeProvider.initialize(配置)
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        page.add(StrategyInterface.create())
    ft.run(main)
