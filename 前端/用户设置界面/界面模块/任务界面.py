# -*- coding: utf-8 -*-
"""
模块名称：任务界面 | 层级：界面模块层
设计思路：
    任务界面，包含主线任务、支线任务等设置卡片。
    使用配置管理器获取和保存配置值。

功能：
    1. 主线任务设置
    2. 支线任务设置

对外接口：
    - create(): 创建任务界面
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


class TaskInterface:
    """任务界面 - 界面模块层"""
    
    @staticmethod
    def create(page: ft.Page = None, on_refresh: Callable[[], None] = None) -> ft.Container:
        """
        创建任务界面
        
        参数：
            page: 页面对象（可选，用于更新页面显示）
            on_refresh: 刷新回调
        
        返回：
            ft.Container: 任务界面容器
        """
        配置 = 界面配置()
        
        try:
            config_manager = ConfigManager()
        except ImportError:
            config_manager = None
        
        def on_value_change(card_name: str, config_key: str, value):
            """值变化回调 - 保存配置"""
            save_value = value.replace("级", "") if value.endswith("级") else value
            print(f"配置变化: {card_name}.{config_key} = {save_value}")
            if config_manager:
                config_manager.set_value(card_name, config_key, save_value)
        
        def create_dropdown_control(options: list, value: str, card_name: str, config_key: str, width: int = 80):
            """创建下拉框控件（无标签）"""
            dropdown = Dropdown.create(
                options=options,
                value=value,
                width=width,
                on_change=lambda v: on_value_change(card_name, config_key, v),
            )
            return dropdown
        
        main_level_options = [f"{i:02d}级" for i in range(1, 16)]
        side_level_options = [f"{i:02d}级" for i in range(5, 16)]
        
        main_level_value = config_manager.get_value("主线任务", "主线限级", "05") if config_manager else "05"
        main_display_value = f"{main_level_value}级" if not main_level_value.endswith("级") else main_level_value
        
        main_level_control = create_dropdown_control(
            options=main_level_options,
            value=main_display_value,
            card_name="主线任务",
            config_key="主线限级",
        )
        
        main_card = UniversalCard.create(
            title="主线任务",
            icon="TASK",
            enabled=True,
            subtitle="达到设置主城等级后,允许执行主线任务",
            controls=[main_level_control],
        )
        
        side_level_value = config_manager.get_value("支线任务", "支线限级", "10") if config_manager else "10"
        side_display_value = f"{side_level_value}级" if not side_level_value.endswith("级") else side_level_value
        
        side_level_control = create_dropdown_control(
            options=side_level_options,
            value=side_display_value,
            card_name="支线任务",
            config_key="支线限级",
        )
        
        side_card = UniversalCard.create(
            title="支线任务",
            icon="TASK_ALT",
            enabled=True,
            subtitle="达到设置主城等级后,允许执行支线任务",
            controls=[side_level_control],
        )
        
        return FunctionContainer.create(
            config=配置,
            title="任务设置",
            icon="ASSIGNMENT",
            cards=[main_card, side_card],
            expand=True,
        )


# *** 调试逻辑 ***
if __name__ == "__main__":
    配置 = 界面配置()
    ThemeProvider.initialize(配置)
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        page.add(TaskInterface.create())
    ft.run(main)
