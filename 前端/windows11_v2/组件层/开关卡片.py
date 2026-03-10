# -*- coding: utf-8 -*-
"""
开关卡片 - 组件层（兼容别名）

设计思路:
    本模块是通用卡片的兼容别名，保持向后兼容。

功能:
    单行卡片，左侧图标+标题+描述，右侧开关。

使用场景:
    被需要开关功能的模块调用。

可独立运行调试: python 开关卡片.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from 组件层.通用卡片 import UniversalCard

# 兼容别名
SwitchCard = UniversalCard
开关卡片 = UniversalCard

# 保留原有的用户指定变量（向后兼容）
DEFAULT_CARD_HEIGHT = 70
DEFAULT_CARD_SPACING = 10


if __name__ == "__main__":
    import flet as ft
    from 原子层.界面配置 import 界面配置
    from 组件层.椭圆开关 import EllipseSwitch
    
    config = 界面配置()
    
    def main(page: ft.Page):
        page.padding = 20
        page.bgcolor = config.获取颜色("bg_primary")
        
        switch = EllipseSwitch(config=config, value=False)
        
        page.add(SwitchCard.create(
            config=config,
            title="功能开关",
            description="开启或关闭此功能",
            icon="POWER_SETTINGS_NEW",
            controls=[switch.create()],
        ))
    
    ft.run(main)
