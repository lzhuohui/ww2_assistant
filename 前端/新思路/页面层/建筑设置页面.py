# -*- coding: utf-8 -*-
"""
建筑设置页面 - 页面层（新思路）

设计思路:
    组装组件，构建建筑设置页面。

功能:
    1. 主帅主城卡片
    2. 主帅分城卡片
    3. 付帅主城卡片
    4. 付帅分城卡片
    5. 军团城市卡片

数据来源:
    所有配置数据从配置目录获取。

使用场景:
    被主界面调用。

可独立运行调试: python 建筑设置页面.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft
from typing import Callable
from 配置.界面配置 import 界面配置
from 配置.配置管理器 import ConfigManager
from 新思路.组件层.通用卡片 import UniversalCard

# *** 用户指定变量 - AI不得修改 ***
DEFAULT_DROPDOWN_WIDTH = 60  # 下拉框默认宽度（建筑设置页面专用）
# *********************************


class BuildingSettingsPage:
    """建筑设置页面 - 页面层"""
    
    @staticmethod
    def create(config: 界面配置, page: ft.Page = None, on_refresh: Callable[[], None] = None) -> ft.Container:
        """
        创建建筑设置页面
        
        参数:
            config: 界面配置对象
            page: 页面对象（可选，用于更新页面显示）
            on_refresh: 刷新回调（主题/调色板切换后调用）
        
        返回:
            ft.Container: 建筑设置页面容器
        """
        theme_colors = config.当前主题颜色
        
        # 创建配置管理器
        config_manager = ConfigManager()
        
        # 为建筑配置中的所有下拉框添加width参数
        for card_name, card_config in config_manager.building_configs.items():
            if "controls" in card_config:
                for control in card_config["controls"]:
                    if control.get("type") == "dropdown" and "width" not in control:
                        control["width"] = DEFAULT_DROPDOWN_WIDTH
        
        # 创建值变化回调
        def on_value_change(config_key: str, value: any):
            """值变化回调"""
            print(f"配置变化: {config_key} = {value}")
        
        # 使用配置驱动创建五个卡片
        main_commander_card = UniversalCard.create_from_config(
            config=config,
            card_name="主帅主城",
            config_manager=config_manager,
            on_value_change=on_value_change,
        )
        
        main_branch_card = UniversalCard.create_from_config(
            config=config,
            card_name="主帅分城",
            config_manager=config_manager,
            on_value_change=on_value_change,
        )
        
        vice_commander_card = UniversalCard.create_from_config(
            config=config,
            card_name="付帅主城",
            config_manager=config_manager,
            on_value_change=on_value_change,
        )
        
        vice_branch_card = UniversalCard.create_from_config(
            config=config,
            card_name="付帅分城",
            config_manager=config_manager,
            on_value_change=on_value_change,
        )
        
        legion_card = UniversalCard.create_from_config(
            config=config,
            card_name="军团城市",
            config_manager=config_manager,
            on_value_change=on_value_change,
        )
        
        # ========== 页面容器 ==========
        page_content = ft.Column(
            [
                # 页面标题
                ft.Text(
                    "建筑设置",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=theme_colors.get("text_primary"),
                ),
                ft.Container(height=20),
                # 主帅主城卡片
                main_commander_card,
                ft.Container(height=15),
                # 主帅分城卡片
                main_branch_card,
                ft.Container(height=15),
                # 付帅主城卡片
                vice_commander_card,
                ft.Container(height=15),
                # 付帅分城卡片
                vice_branch_card,
                ft.Container(height=15),
                # 军团城市卡片
                legion_card,
            ],
            spacing=0,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )
        
        # 页面容器
        page_container = ft.Container(
            content=page_content,
            padding=ft.Padding.all(20),
            expand=True,
        )
        
        return page_container


# 兼容别名
建筑设置页面 = BuildingSettingsPage


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    # 1. 界面配置初始化
    配置 = 界面配置()
    
    # 2. 自动加载用户数据覆盖默认值（在界面配置.__init__中自动完成）
    
    # 3. 正常启动被测模块
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        page.add(BuildingSettingsPage.create(配置))
    
    ft.run(main)
