# -*- coding: utf-8 -*-
"""
模块名称：任务界面 | 层级：界面模块层
设计思路：
    任务界面，包含主线任务、支线任务等设置卡片。
    使用配置管理器获取和保存配置值。
    使用统一的文本样式管理，确保文字视觉效果一致。

功能：
    1. 主线任务设置
    2. 支线任务设置

对外接口：
    - create(): 创建任务界面
"""

import flet as ft
from typing import Callable
from 前端.用户设置界面.配置.界面配置 import 界面配置
from 前端.用户设置界面.配置.配置管理器 import ConfigManager
from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider
from 前端.用户设置界面.组件模块.通用卡片 import UniversalCard
from 前端.用户设置界面.组件模块.功能容器 import FunctionContainer
from 前端.用户设置界面.单元模块.下拉框 import Dropdown
from 前端.用户设置界面.单元模块.文本标签 import LabelText


class TaskInterface:
    """任务界面 - 界面模块层"""
    
    @staticmethod
    def create() -> ft.Container:
        """
        创建任务界面
        
        返回:
            ft.Container: 任务界面容器
        """
        配置 = 界面配置()
        
        def on_value_change(card_name, config_key, value):
            config_manager = ConfigManager()
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
        
        # 主线任务卡片
        main_task_card = UniversalCard.create(
            title="主线任务",
            icon="TASK",
            enabled=True,
            controls=[
                create_dropdown_control(
                    label="任务类型",
                    options=["主线", "支线", "日常"],
                    value="主线",
                    card_name="主线任务",
                    config_key="task_type",
                    width=150,
                ),
            ],
        )
        
        # 支线任务卡片
        side_task_card = UniversalCard.create(
            title="支线任务",
            icon="TASK_ALT",
            enabled=True,
            controls=[
                create_dropdown_control(
                    label="任务类型",
                    options=["主线", "支线", "日常"],
                    value="支线",
                    card_name="支线任务",
                    config_key="task_type",
                    width=150,
                ),
            ],
        )
        
        # 使用功能容器包装
        return FunctionContainer.create(
            config=配置,
            title="任务设置",
            icon="TASK",
            cards=[main_task_card, side_task_card],
        )


if __name__ == "__main__":
    from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider
    
    配置 = 界面配置()
    ThemeProvider.initialize(配置)
    
    def main(page: ft.Page):
        page.add(TaskInterface.create())
    
    ft.run(main)