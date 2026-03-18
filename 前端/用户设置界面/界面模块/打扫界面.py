# -*- coding: utf-8 -*-
"""
模块名称：打扫界面 | 层级：界面模块层
设计思路：
    打扫界面，包含打扫城区、打扫政区等设置卡片。
    使用配置管理器获取和保存配置值。

功能：
    1. 打扫城区设置
    2. 打扫政区设置

对外接口：
    - create(): 创建打扫界面
"""

import flet as ft
from typing import Callable
from 前端.配置.界面配置 import 界面配置
from 前端.配置.配置管理器 import ConfigManager
from 前端.用户设置界面.组件模块.通用卡片 import UniversalCard
from 前端.用户设置界面.组件模块.功能容器 import FunctionContainer


class CleaningInterface:
    """打扫界面 - 界面模块层"""
    
    @staticmethod
    def create(page: ft.Page = None, on_refresh: Callable[[], None] = None) -> ft.Container:
        """
        创建打扫界面
        
        参数：
            page: 页面对象（可选，用于更新页面显示）
            on_refresh: 刷新回调
        
        返回：
            ft.Container: 打扫界面容器
        """
        配置 = 界面配置()
        
        try:
            config_manager = ConfigManager()
        except ImportError:
            config_manager = None
        
        district_enabled = config_manager.get_value("打扫城区", "开关", True) if config_manager else True
        region_enabled = config_manager.get_value("打扫政区", "开关", True) if config_manager else True
        
        if config_manager:
            config_manager.set_value("打扫城区", "开关", district_enabled)
            config_manager.set_value("打扫政区", "开关", region_enabled)
        
        def on_district_state_change(enabled: bool):
            if config_manager:
                config_manager.set_value("打扫城区", "开关", enabled)
        
        def on_region_state_change(enabled: bool):
            if config_manager:
                config_manager.set_value("打扫政区", "开关", enabled)
        
        district_card = UniversalCard.create(
            title="打扫城区",
            icon="CLEANING_SERVICES",
            enabled=district_enabled,
            on_state_change=on_district_state_change,
            subtitle="开启后执行打扫城区任务",
        )
        
        region_card = UniversalCard.create(
            title="打扫政区",
            icon="LOCATION_CITY",
            enabled=region_enabled,
            on_state_change=on_region_state_change,
            subtitle="开启后执行打扫政区任务",
        )
        
        return FunctionContainer.create(
            config=配置,
            title="打扫设置",
            icon="CLEANING_SERVICES",
            cards=[district_card, region_card],
            expand=True,
        )


# *** 调试逻辑 ***
if __name__ == "__main__":
    from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider
    ThemeProvider.initialize(配置)
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        page.add(CleaningInterface.create())
    ft.run(main)
