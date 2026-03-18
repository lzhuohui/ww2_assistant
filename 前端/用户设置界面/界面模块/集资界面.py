# -*- coding: utf-8 -*-
"""
模块名称：集资界面 | 层级：界面模块层
设计思路：
    集资界面，包含集资管理、资源分配等设置卡片。
    使用配置管理器获取和保存配置值。

功能：
    1. 小号上贡设置
    2. 分城纳租设置

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
        
        def create_dropdown_control(options: list, value: str, card_name: str, config_key: str, width: int = 80):
            """创建下拉框控件（无标签）"""
            dropdown = Dropdown.create(
                options=options,
                value=value,
                width=width,
                on_change=lambda v: on_value_change(card_name, config_key, v),
            )
            return dropdown
        
        小号上贡_value = config_manager.get_value("小号上贡", "上贡限级", "05级") if config_manager else "05级"
        上贡限级_control = create_dropdown_control(
            options=["05级", "06级", "07级", "08级", "09级", "10级", "11级", "12级", "13级", "14级", "15级"],
            value=小号上贡_value,
            card_name="小号上贡",
            config_key="上贡限级",
        )
        
        上贡限量_value = config_manager.get_value("小号上贡", "上贡限量", "2万") if config_manager else "2万"
        上贡限量_control = create_dropdown_control(
            options=["2万", "3万", "4万", "5万", "6万", "7万", "8万", "9万", "10万", "11万", "12万", "13万", "14万", "15万", "16万", "17万", "18万", "19万", "20万"],
            value=上贡限量_value,
            card_name="小号上贡",
            config_key="上贡限量",
        )
        
        主要统帅_value = config_manager.get_value("小号上贡", "主要统帅", "统帅A") if config_manager else "统帅A"
        主要统帅_control = create_dropdown_control(
            options=["统帅A", "统帅B", "统帅C", "统帅D", "统帅E"],
            value=主要统帅_value,
            card_name="小号上贡",
            config_key="主要统帅",
        )
        
        备用统帅_value = config_manager.get_value("小号上贡", "备用统帅", "统帅B") if config_manager else "统帅B"
        备用统帅_control = create_dropdown_control(
            options=["统帅A", "统帅B", "统帅C", "统帅D", "统帅E"],
            value=备用统帅_value,
            card_name="小号上贡",
            config_key="备用统帅",
        )
        
        小号上贡_card = UniversalCard.create(
            title="小号上贡",
            icon="UPLOAD",
            subtitle="设置小号上贡相关参数",
            enabled=True,
            controls=[上贡限级_control, 上贡限量_control, 主要统帅_control, 备用统帅_control],
            controls_per_row=2,
        )
        
        纳租限级_value = config_manager.get_value("分城纳租", "纳租限级", "05级") if config_manager else "05级"
        纳租限级_control = create_dropdown_control(
            options=["05级", "06级", "07级", "08级", "09级", "10级", "11级", "12级", "13级", "14级", "15级"],
            value=纳租限级_value,
            card_name="分城纳租",
            config_key="纳租限级",
        )
        
        纳租限量_value = config_manager.get_value("分城纳租", "纳租限量", "2万") if config_manager else "2万"
        纳租限量_control = create_dropdown_control(
            options=["2万", "3万", "4万", "5万", "6万", "7万", "8万", "9万", "10万", "11万", "12万", "13万", "14万", "15万", "16万", "17万", "18万", "19万", "20万"],
            value=纳租限量_value,
            card_name="分城纳租",
            config_key="纳租限量",
        )
        
        分城纳租_card = UniversalCard.create(
            title="分城纳租",
            icon="ATTACH_MONEY",
            subtitle="设置分城纳租相关参数",
            enabled=True,
            controls=[纳租限级_control, 纳租限量_control],
            controls_per_row=2,
        )
        
        return FunctionContainer.create(
            config=配置,
            title="集资设置",
            icon="SHOPPING_CART",
            cards=[小号上贡_card, 分城纳租_card],
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
