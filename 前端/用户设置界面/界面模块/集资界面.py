# -*- coding: utf-8 -*-
"""
模块名称：集资界面
设计思路及联动逻辑:
    集资界面，包含集资管理、资源分配等设置卡片。
    使用配置驱动架构，通过设置面板自动创建卡片。
模块隔离原则:
    1. 不直接创建被调用模块的内容
    2. 不覆盖被调用模块的计算结果
    3. 用户指定变量除外
"""

import flet as ft
from typing import Callable

from 前端.用户设置界面.配置.界面配置 import 界面配置
from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider
from 前端.用户设置界面.组件模块.设置面板 import SettingsPanel


# *** 用户指定变量 - AI不得修改, 变量值必须生效 ***
# （用户未指定变量）
# *********************************


class FundraisingInterface:
    """集资界面 - 配置驱动"""
    
    @staticmethod
    def create(page: ft.Page=None, on_refresh: Callable[[], None]=None) -> ft.Container:
        配置 = 界面配置()
        
        return SettingsPanel.create(
            config=配置,
            title="集资设置",
            icon="ACCOUNT_BALANCE",
            card_names=["小号上贡", "分城纳租"],
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
