# -*- coding: utf-8 -*-
"""
模块名称：建筑界面 | 设计思路：使用懒加载机制，默认加载主帅主城，其他卡片点击后加载 | 模块隔离原则：不直接创建被调用模块的内容，不覆盖被调用模块的计算结果，用户指定变量除外
"""

import flet as ft
from 前端.用户设置界面.配置.界面配置 import 界面配置
from 前端.用户设置界面.配置.配置管理器 import ConfigManager
from 前端.用户设置界面.组件模块.懒加载卡片 import LazyCard
from 前端.用户设置界面.组件模块.懒加载状态管理器 import LazyState
from 前端.用户设置界面.组件模块.通用功能容器 import GenericFunctionContainer, USER_WIDTH


# *** 用户指定变量 - AI不得修改, 变量值必须生效 ***
USER_CARD_NAMES = ["主帅主城", "主帅分城", "付帅主城", "付帅分城", "军团城市"]
# *********************************


class BuildingInterface:
    """建筑界面 - 界面模块层"""
    
    @staticmethod
    def create(width: int=USER_WIDTH) -> ft.Container:
        """
        创建建筑界面
        
        参数：
            width: 内容区域宽度
        
        返回：
            ft.Container: 建筑界面容器
        """
        配置 = 界面配置()
        
        try:
            config_manager = ConfigManager()
        except ImportError:
            config_manager = None
        
        state = LazyState()
        state.set_config_manager(config_manager)
        
        def on_value_change(config_key: str, value):
            """值变化回调 - 保存配置"""
            print(f"配置变化: {config_key} = {value}")
        
        lazy_cards = []
        for i, card_name in enumerate(USER_CARD_NAMES):
            card_config = config_manager.get_card_config(card_name) if config_manager else None
            if card_config:
                is_default = (i == 0)
                card = LazyCard(
                    card_name=card_name,
                    card_config=card_config,
                    config_manager=config_manager,
                    on_value_change=on_value_change,
                    is_default=is_default,
                )
                lazy_cards.append(card.create())
        
        return GenericFunctionContainer.create(
            config=配置,
            title="建筑设置",
            icon="DOMAIN",
            cards=lazy_cards,
            width=width,
            expand=True,
        )


# *** 调试逻辑 ***
if __name__ == "__main__":
    ft.run(lambda page: page.add(BuildingInterface.create()))
