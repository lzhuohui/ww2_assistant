# -*- coding: utf-8 -*-
"""
模块名称：集资界面 | 层级：界面模块层
设计思路：
    集资界面，包含集资管理、资源分配等设置卡片。
    实现主要统帅和次要统帅的联动逻辑。
    使用统一的文本样式管理，确保文字视觉效果一致。

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
from 前端.用户设置界面.配置.界面配置 import 界面配置
from 前端.用户设置界面.配置.配置管理器 import ConfigManager
from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider
from 前端.用户设置界面.组件模块.通用卡片 import UniversalCard
from 前端.用户设置界面.组件模块.功能容器 import FunctionContainer
from 前端.用户设置界面.单元模块.下拉框 import Dropdown
from 前端.用户设置界面.单元模块.文本标签 import LabelText


def get_active_commanders(config_manager: ConfigManager) -> List[str]:
    """获取活跃的统帅列表"""
    commanders = []
    for i in range(1, 5):
        commander = config_manager.get_value("小号上贡", f"commander_{i}", "")
        if commander:
            commanders.append(commander)
    return commanders


class FundraisingInterface:
    """集资界面 - 界面模块层"""
    
    @staticmethod
    def create() -> ft.Container:
        """
        创建集资界面
        
        返回:
            ft.Container: 集资界面容器
        """
        配置 = 界面配置()
        config_manager = ConfigManager()
        
        def on_value_change(card_name, config_key, value):
            config_manager.set_value(card_name, config_key, value)
        
        def create_dropdown_control(label, options, value, card_name, config_key, width=None):
            """创建下拉框控件"""
            dropdown = Dropdown.create(
                options=options,
                value=value,
                width=width,
                on_change=lambda v: on_value_change(card_name, config_key, v),
            )
            
            label_text = LabelText.create(
                text=label,
                role="caption",
                win11_style=True
            )
            
            return ft.Row(
                [label_text, dropdown],
                alignment=ft.MainAxisAlignment.END,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8,
                expand=True,
            )
        
        # 小号上贡卡片
        tribute_card = UniversalCard.create(
            title="小号上贡",
            icon="ACCOUNT_BALANCE",
            enabled=True,
            controls=[
                create_dropdown_control(
                    label="统帅1",
                    options=["统帅A", "统帅B", "统帅C"],
                    value="统帅A",
                    card_name="小号上贡",
                    config_key="commander_1",
                    width=150,
                ),
            ],
        )
        
        # 分城纳租卡片
        tax_card = UniversalCard.create(
            title="分城纳租",
            icon="APARTMENT",
            enabled=True,
            controls=[
                create_dropdown_control(
                    label="城市",
                    options=["城市A", "城市B", "城市C"],
                    value="城市A",
                    card_name="分城纳租",
                    config_key="city",
                    width=150,
                ),
            ],
        )
        
        # 使用功能容器包装
        return FunctionContainer.create(
            config=配置,
            title="集资设置",
            icon="ACCOUNT_BALANCE",
            cards=[tribute_card, tax_card],
        )


if __name__ == "__main__":
    from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider
    
    配置 = 界面配置()
    ThemeProvider.initialize(配置)
    
    def main(page: ft.Page):
        page.add(FundraisingInterface.create())
    
    ft.run(main)