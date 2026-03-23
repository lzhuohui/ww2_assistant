# -*- coding: utf-8 -*-
"""
模块名称：系统界面
设计思路及联动逻辑:
    系统界面，包含挂机模式、指令速度、尝试次数、清缓限量等设置卡片。
    使用配置驱动架构，通过设置面板自动创建卡片。
模块隔离原则:
    1. 不直接创建被调用模块的内容
    2. 不覆盖被调用模块的计算结果
    3. 用户指定变量除外
"""

import flet as ft

from 前端.用户设置界面.配置.界面配置 import 界面配置
from 前端.用户设置界面.组件模块.设置面板 import SettingsPanel, USER_WIDTH


# *** 用户指定变量 - AI不得修改, 变量值必须生效 ***
USER_CARD_NAMES = ["挂机模式", "指令速度", "尝试次数", "清缓限量"]
# *********************************


class SystemInterface:
    """系统界面 - 配置驱动"""
    
    @staticmethod
    def create(width: int=USER_WIDTH) -> ft.Container:
        配置 = 界面配置()
        
        return SettingsPanel.create(
            config=配置,
            title="系统设置",
            icon="SETTINGS",
            card_names=USER_CARD_NAMES,
            width=width,
            expand=True,
        )


# *** 调试逻辑 ***
if __name__ == "__main__":
    ft.run(lambda page: page.add(SystemInterface.create()))
