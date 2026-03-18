# -*- coding: utf-8 -*-
"""
模块名称：打野界面 | 层级：界面模块层
设计思路：
    打野界面，包含自动打野等设置卡片。
    使用配置管理器获取和保存配置值。

功能：
    1. 自动打野设置

对外接口：
    - create(): 创建打野界面
"""

import flet as ft
from typing import Callable
from 前端.配置.界面配置 import 界面配置
from 前端.配置.配置管理器 import ConfigManager
from 前端.用户设置界面.组件模块.通用卡片 import UniversalCard
from 前端.用户设置界面.组件模块.功能容器 import FunctionContainer


class WildInterface:
    """打野界面 - 界面模块层"""
    
    @staticmethod
    def create(page: ft.Page = None, on_refresh: Callable[[], None] = None) -> ft.Container:
        """
        创建打野界面
        
        参数：
            page: 页面对象（可选，用于更新页面显示）
            on_refresh: 刷新回调
        
        返回：
            ft.Container: 打野界面容器
        """
        配置 = 界面配置()
        
        try:
            config_manager = ConfigManager()
        except ImportError:
            config_manager = None
        
        wild_enabled = config_manager.get_value("自动打野", "开关", True) if config_manager else True
        
        if config_manager:
            config_manager.set_value("自动打野", "开关", wild_enabled)
        
        def on_wild_state_change(enabled: bool):
            if config_manager:
                config_manager.set_value("自动打野", "开关", enabled)
        
        wild_card = UniversalCard.create(
            title="自动打野",
            icon="EXPLORE",
            enabled=wild_enabled,
            on_state_change=on_wild_state_change,
            subtitle="开启后执行自动打野任务",
        )
        
        return FunctionContainer.create(
            config=配置,
            title="打野设置",
            icon="EXPLORE",
            cards=[wild_card],
            expand=True,
        )


# *** 调试逻辑 ***
if __name__ == "__main__":
    from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider
    ThemeProvider.initialize(配置)
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        page.add(WildInterface.create())
    ft.run(main)
