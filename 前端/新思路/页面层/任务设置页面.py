# -*- coding: utf-8 -*-
"""
任务设置页面 - 页面层

设计思路:
    使用配置驱动方式创建卡片，支持数据保存/加载。

功能:
    1. 主线任务卡片
    2. 支线任务卡片

数据来源:
    所有配置数据从配置目录获取。

使用场景:
    被主界面调用。

可独立运行调试: python 任务设置页面.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft
from typing import Callable
from 配置.界面配置 import 界面配置
from 配置.配置管理器 import ConfigManager
from 新思路.组件层.通用卡片 import UniversalCard
from 新思路.零件层.标签下拉框 import LabelDropdown


class TaskSettingsPage:
    """任务设置页面"""
    
    @staticmethod
    def create(config: 界面配置, page: ft.Page = None, on_refresh: Callable[[], None] = None) -> ft.Container:
        """
        创建任务设置页面
        
        参数:
            config: 界面配置对象
            page: 页面对象
            on_refresh: 刷新回调
        
        返回:
            ft.Container: 任务设置页面容器
        """
        theme_colors = config.当前主题颜色
        config_manager = ConfigManager()
        
        # 主城等级选项 (01-15级)
        main_level_options = [f"{i:02d}级" for i in range(1, 16)]
        # 支线主城等级选项 (05-15级)
        side_level_options = [f"{i:02d}级" for i in range(5, 16)]
        
        # 获取保存的值
        main_level_value = config_manager.get_value("主线任务", "主线限级", "05")
        side_level_value = config_manager.get_value("支线任务", "支线限级", "10")
        
        # 保存默认值到配置
        config_manager.set_value("主线任务", "主线限级", main_level_value)
        config_manager.set_value("支线任务", "支线限级", side_level_value)
        
        # 显示值添加单位
        main_display_value = f"{main_level_value}级" if not main_level_value.endswith("级") else main_level_value
        side_display_value = f"{side_level_value}级" if not side_level_value.endswith("级") else side_level_value
        
        def on_main_level_change(value: str):
            save_value = value.replace("级", "")
            config_manager.set_value("主线任务", "主线限级", save_value)
        
        def on_side_level_change(value: str):
            save_value = value.replace("级", "")
            config_manager.set_value("支线任务", "支线限级", save_value)
        
        # ========== 主线任务卡片 ==========
        main_dropdown = LabelDropdown.create(
            config=config,
            label="主线限级",
            options=main_level_options,
            value=main_display_value,
            on_change=on_main_level_change,
        )
        
        main_card = UniversalCard.create(
            config=config,
            title="主线任务",
            icon="TASK",
            enabled=True,
            subtitle="达到设置主城等级后,允许执行主线任务",
            controls=[main_dropdown],
        )
        
        # ========== 支线任务卡片 ==========
        side_dropdown = LabelDropdown.create(
            config=config,
            label="支线限级",
            options=side_level_options,
            value=side_display_value,
            on_change=on_side_level_change,
        )
        
        side_card = UniversalCard.create(
            config=config,
            title="支线任务",
            icon="TASK_ALT",
            enabled=True,
            subtitle="达到设置主城等级后,允许执行支线任务",
            controls=[side_dropdown],
        )
        
        # ========== 页面容器 ==========
        page_content = ft.Column(
            [
                ft.Text(
                    "任务设置",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=theme_colors.get("text_primary"),
                ),
                ft.Container(height=4),
                main_card,
                ft.Container(height=4),
                side_card,
            ],
            spacing=0,
            scroll=ft.ScrollMode.HIDDEN,
            expand=True,
        )
        
        page_container = ft.Container(
            content=page_content,
            padding=ft.Padding.all(0),
            expand=True,
        )
        
        page_container.main_card = main_card
        page_container.side_card = side_card
        
        return page_container


任务设置页面 = TaskSettingsPage


if __name__ == "__main__":
    配置 = 界面配置()
    
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        page.add(TaskSettingsPage.create(配置))
    
    ft.run(main)
