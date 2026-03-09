# -*- coding: utf-8 -*-
"""
通用界面 - 设备层

设计思路:
    本模块是设备层模块，提供通用界面。

功能:
    1. 继承基础界面
    2. 提供通用相关功能
    3. 包含基本参数

数据来源:
    主题颜色从界面配置获取。

使用场景:
    被系统层调用，提供通用界面。

可独立运行调试: python 通用界面.py
"""

import flet as ft
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from 原子层.界面配置 import 界面配置
from 设备层.基础界面 import BaseInterface
from 组件层.下拉卡片 import DropDownCard


class GeneralInterface(BaseInterface):  # 通用界面
    """通用界面 - 提供通用功能"""
    
    def __init__(self, config: 界面配置, page: ft.Page):
        super().__init__(config, page, title="通用设置", subtitle="全局通用控制设置")
    
    def _create_content_area(self) -> ft.Control:  # 创建内容区域
        return DropDownCard.create_list(
            config=self._config,
            card_configs=[
                {
                    "title": "挂机模式",
                    "description": "全自动：自动挂机，无需人为干预；半自动：点击头像，自动切换账号",
                    "icon": "POWER_BUTTON",
                    "options": ["全自动", "半自动"],
                    "value": "全自动"
                },
                {
                    "title": "指令速度",
                    "description": "运行指令间隔频率（毫秒），数值越小速度越快",
                    "icon": "SPEED_HIGH",
                    "options": ["100", "150", "200", "250", "300"],
                    "value": "100"
                },
                {
                    "title": "尝试次数",
                    "description": "指令执行失败后的重试次数",
                    "icon": "REPLAY",
                    "options": ["3", "5", "7", "10", "15"],
                    "value": "5"
                },
                {
                    "title": "清缓限量",
                    "description": "清理缓存的图片数量上限",
                    "icon": "DELETE_SWEEP",
                    "options": ["50", "100", "200", "300", "500"],
                    "value": "100"
                },
            ]
        )


# 兼容别名
通用界面 = GeneralInterface


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    config = 界面配置()
    
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = config.获取颜色("bg_primary")
        interface = GeneralInterface(config, page)
        page.add(interface.render())
    
    ft.run(main)
