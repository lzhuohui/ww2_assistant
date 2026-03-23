# -*- coding: utf-8 -*-
"""
模块名称：打野界面 | 设计思路：配置驱动架构，通过设置面板自动创建卡片 | 模块隔离原则：不直接创建被调用模块的内容，不覆盖被调用模块的计算结果，用户指定变量除外
"""

import flet as ft

from 前端.用户设置界面.配置.界面配置 import 界面配置
from 前端.用户设置界面.组件模块.设置面板 import SettingsPanel, USER_WIDTH


# *** 用户指定变量 - AI不得修改, 变量值必须生效 ***
USER_CARD_NAMES = ["自动打野"]
# *********************************


class WildInterface:
    """打野界面 - 配置驱动"""
    
    @staticmethod
    def create(width: int=USER_WIDTH) -> ft.Container:
        配置 = 界面配置()
        
        return SettingsPanel.create(
            config=配置,
            title="打野设置",
            icon="EXPLORE",
            card_names=USER_CARD_NAMES,
            width=width,
            expand=True,
        )


# *** 调试逻辑 ***
if __name__ == "__main__":
    ft.run(lambda page: page.add(WildInterface.create()))
