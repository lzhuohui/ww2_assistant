# -*- coding: utf-8 -*-

"""
模块名称：关于界面.py
模块功能：关于信息界面

职责：
- 管理关于信息卡片
- 展示版本信息、功能介绍、联系方式、缴费说明、免责声明

不负责：
- 数据存储
- 界面布局（由界面容器负责）
"""

import flet as ft
from typing import Callable, Dict, Any

from 设置界面.层级0_数据管理.配置管理 import ConfigManager
from 设置界面.层级4_复合模块.信息卡片 import InfoCard
from 设置界面.层级3_功能卡片.界面容器 import InterfaceContainer


class AboutInterface:
    """关于界面 - V3版本"""
    
    INTERFACE_NAME = "关于界面"
    INTERFACE_TITLE = "关于"
    INTERFACE_HINT = "版本信息、功能介绍、联系方式、缴费说明"
    
    def __init__(self, page: ft.Page, config_manager: ConfigManager, on_scheme_change: Callable[[str], None] = None):
        self._page = page
        self._config_manager = config_manager
        self._on_scheme_change = on_scheme_change
        self._info_card = InfoCard(page, config_manager)
        self._interface_container = InterfaceContainer(page, config_manager)
        self._cards: Dict[str, ft.Container] = {}
        self._container: ft.Container = None
    
    def build(self) -> ft.Container:
        """构建关于界面"""
        theme_colors = self._config_manager.get_theme_colors()
        
        card_names = self._config_manager.get_card_names(self.INTERFACE_NAME)
        
        cards = []
        for card_name in card_names:
            card_info = self._config_manager.get_card_info(self.INTERFACE_NAME, card_name)
            controls = self._config_manager.get_controls(self.INTERFACE_NAME, card_name)
            card_info["控件列表"] = controls if controls else []
            card = self._info_card.create(
                interface=self.INTERFACE_NAME,
                card=card_name,
                card_info=card_info,
                theme_colors=theme_colors,
            )
            cards.append(card)
            self._cards[card_name] = card
        
        self._container = self._interface_container.create(
            title=self.INTERFACE_TITLE,
            hint=self.INTERFACE_HINT,
            cards=cards,
            on_scheme_change=self._on_scheme_change,
        )
        
        return self._container
    
    def destroy(self):
        """销毁界面"""
        self._info_card.destroy()
        self._cards.clear()
        self._container = None


if __name__ == "__main__":
    def main(page: ft.Page):
        from 设置界面.层级0_数据管理.配置管理 import ConfigManager
        config_manager = ConfigManager()
        InfoCard.set_config_manager(config_manager)
        
        interface = AboutInterface(page, config_manager)
        page.add(interface.build())
    
    ft.app(target=main)
