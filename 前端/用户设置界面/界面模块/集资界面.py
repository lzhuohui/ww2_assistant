# -*- coding: utf-8 -*-
"""
模块名称：集资界面 | 层级：界面模块层
设计思路：
    集资界面，包含集资管理、资源分配等设置卡片。
    实现主要统帅和次要统帅的联动逻辑。

功能：
    1. 小号上贡卡片（4个下拉框）
    2. 分城纳租卡片（2个下拉框）
    3. 主要统帅和次要统帅联动

数据来源：
    部分数据来自按键精灵脚本。

对外接口：
    - create(): 创建集资界面
"""

import flet as ft
from typing import Callable, List
from 前端.配置.界面配置 import 界面配置
from 前端.配置.配置管理器 import ConfigManager
from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider
from 前端.用户设置界面.组件模块.通用卡片 import UniversalCard
from 前端.用户设置界面.组件模块.功能容器 import FunctionContainer
from 前端.用户设置界面.单元模块.下拉框 import Dropdown


def get_active_commanders(config_manager: ConfigManager) -> List[str]:
    """
    从账号配置中获取参与挂机的主帅列表
    
    参数:
        config_manager: 配置管理器
    
    返回:
        List[str]: 参与挂机的主帅名称列表（从输入框中提取第一个"/"前的数据段）
    """
    commanders = []
    for i in range(1, 16):
        card_name = f"{i:02d}账号"
        account_type = config_manager.get_value(card_name, "统帅种类", "") if config_manager else ""
        is_enabled = config_manager.get_value(card_name, "开关", False) if config_manager else False
        input_text = config_manager.get_value(card_name, "输入框", "") if config_manager else ""
        
        if account_type == "主帅" and is_enabled and input_text:
            parts = input_text.split("/")
            if parts and parts[0].strip():
                commanders.append(parts[0].strip())
    
    return commanders


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
        
        commander_options = get_active_commanders(config_manager)
        
        primary_value = config_manager.get_value("小号上贡", "主要统帅", "") if config_manager else ""
        secondary_value = config_manager.get_value("小号上贡", "备用统帅", "") if config_manager else ""
        
        primary_dropdown = None
        secondary_dropdown = None
        
        def update_secondary_options():
            """更新次要统帅选项"""
            nonlocal secondary_dropdown
            
            if primary_dropdown:
                current_primary = primary_dropdown.get_value()
                secondary_options = ["请选统帅"] + [c for c in commander_options if c != current_primary]
                
                if secondary_dropdown:
                    secondary_dropdown.set_options(secondary_options)
                    if secondary_dropdown.get_value() not in secondary_options:
                        secondary_dropdown.set_value("请选统帅")
                        if config_manager:
                            config_manager.set_value("小号上贡", "备用统帅", "")
        
        def on_primary_change(value: str):
            """主要统帅变化回调"""
            if config_manager:
                config_manager.set_value("小号上贡", "主要统帅", value)
            update_secondary_options()
        
        def on_secondary_change(value: str):
            """次要统帅变化回调"""
            if value == "请选统帅":
                if config_manager:
                    config_manager.set_value("小号上贡", "备用统帅", "")
            else:
                if config_manager:
                    config_manager.set_value("小号上贡", "备用统帅", value)
        
        def on_value_change(card_name: str, config_key: str, value):
            """值变化回调 - 保存配置"""
            print(f"配置变化: {card_name}.{config_key} = {value}")
            if config_manager:
                config_manager.set_value(card_name, config_key, value)
        
        def create_dropdown_control(label: str, options: list, value: str, card_name: str, config_key: str, width: int = None, on_change: Callable = None):
            """创建下拉框控件"""
            dropdown = Dropdown.create(
                options=options,
                value=value,
                width=width,
                on_change=on_change if on_change else lambda v: on_value_change(card_name, config_key, v),
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
            ), dropdown
        
        limit_level_options = [f"{i:02d}级" for i in range(5, 16)]
        limit_amount_options = [f"{i}万" for i in range(2, 21)]
        
        上贡限级_value = config_manager.get_value("小号上贡", "上贡限级", "05级") if config_manager else "05级"
        上贡限级_control, _ = create_dropdown_control(
            label="上贡限级:",
            options=limit_level_options,
            value=上贡限级_value,
            card_name="小号上贡",
            config_key="上贡限级",
            width=80,
        )
        
        上贡限量_value = config_manager.get_value("小号上贡", "上贡限量", "2万") if config_manager else "2万"
        上贡限量_control, _ = create_dropdown_control(
            label="上贡限量:",
            options=limit_amount_options,
            value=上贡限量_value,
            card_name="小号上贡",
            config_key="上贡限量",
            width=80,
        )
        
        primary_options = commander_options
        primary_display = primary_value if primary_value in primary_options else (primary_options[0] if primary_options else "")
        
        主要统帅_control, primary_dropdown = create_dropdown_control(
            label="主要统帅:",
            options=primary_options,
            value=primary_display,
            card_name="小号上贡",
            config_key="主要统帅",
            width=80,
            on_change=on_primary_change,
        )
        
        if config_manager:
            config_manager.set_value("小号上贡", "主要统帅", primary_display)
        
        secondary_initial_options = ["请选统帅"] + commander_options
        secondary_display = secondary_value if secondary_value in commander_options else "请选统帅"
        
        备用统帅_control, secondary_dropdown = create_dropdown_control(
            label="备用统帅:",
            options=secondary_initial_options,
            value=secondary_display,
            card_name="小号上贡",
            config_key="备用统帅",
            width=80,
            on_change=on_secondary_change,
        )
        
        if config_manager:
            config_manager.set_value("小号上贡", "备用统帅", secondary_value if secondary_value != "请选统帅" else "")
        
        小号上贡_card = UniversalCard.create(
            title="小号上贡",
            icon="UPLOAD",
            subtitle="设置小号上贡相关参数",
            enabled=True,
            controls=[上贡限级_control, 上贡限量_control, 主要统帅_control, 备用统帅_control],
            controls_per_row=2,
        )
        
        纳租限级_value = config_manager.get_value("分城纳租", "纳租限级", "05级") if config_manager else "05级"
        纳租限级_control, _ = create_dropdown_control(
            label="纳租限级:",
            options=limit_level_options,
            value=纳租限级_value,
            card_name="分城纳租",
            config_key="纳租限级",
            width=80,
        )
        
        纳租限量_value = config_manager.get_value("分城纳租", "纳租限量", "2万") if config_manager else "2万"
        纳租限量_control, _ = create_dropdown_control(
            label="纳租限量:",
            options=limit_amount_options,
            value=纳租限量_value,
            card_name="分城纳租",
            config_key="纳租限量",
            width=80,
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
