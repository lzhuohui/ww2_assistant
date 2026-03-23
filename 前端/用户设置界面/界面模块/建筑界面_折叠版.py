# -*- coding: utf-8 -*-
"""
模块名称：建筑界面_折叠版 | 设计思路：使用折叠卡片组件，每种建筑类型对应一个独立卡片，默认折叠状态 | 模块隔离原则：不直接创建被调用模块的内容，不覆盖被调用模块的计算结果，用户指定变量除外
"""

import flet as ft

from 前端.用户设置界面.配置.界面配置 import 界面配置
from 前端.用户设置界面.组件模块.折叠卡片 import CollapsibleCard
from 前端.用户设置界面.组件模块.通用功能容器 import GenericFunctionContainer, USER_WIDTH
from 前端.用户设置界面.配置.建筑配置 import get_building_config


# *** 用户指定变量 - AI不得修改, 变量值必须生效 ***
USER_CARD_NAMES = ["主帅主城", "主帅分城", "付帅主城", "付帅分城", "军团城市"]
# *********************************


class BuildingInterfaceV2:
    """建筑界面V2 - 折叠卡片版"""
    
    @staticmethod
    def create(width: int=USER_WIDTH) -> ft.Container:
        界面配置实例 = 界面配置()
        建筑配置数据 = get_building_config()
        
        cards = []
        for card_name in USER_CARD_NAMES:
            card_config = 建筑配置数据.get(card_name, {})
            if card_config:
                card = CollapsibleCard.create(
                    title=card_config.get("title", card_name),
                    icon=card_config.get("icon", "HOME"),
                    subtitle=card_config.get("subtitle", ""),
                    enabled=card_config.get("enabled", True),
                    expanded=False,
                    controls_config=card_config.get("controls", []),
                    controls_per_row=card_config.get("controls_per_row", 6),
                    width=width,
                )
                cards.append(card)
        
        return GenericFunctionContainer.create(
            config=界面配置实例,
            title="建筑设置",
            icon="DOMAIN",
            cards=cards,
            width=width,
            expand=True,
        )


# *** 调试逻辑 ***
if __name__ == "__main__":
    from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider
    
    ThemeProvider.initialize(界面配置())
    ft.run(lambda page: page.add(BuildingInterfaceV2.create()))
