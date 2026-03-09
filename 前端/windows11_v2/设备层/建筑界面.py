# -*- coding: utf-8 -*-
"""
建筑界面 - 设备层

设计思路:
    本模块是设备层模块，提供建筑界面。

功能:
    1. 继承基础界面
    2. 提供建筑相关功能
    3. 包含主帅主城、付帅主城、所有分城、军团城市配置

数据来源:
    主题颜色从界面配置获取。
    选项数据从按键精灵界面布局获取。

使用场景:
    被系统层调用，提供建筑界面。

可独立运行调试: python 建筑界面.py
"""

import flet as ft
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from 原子层.界面配置 import 界面配置
from 设备层.基础界面 import BaseInterface
from 组件层.建筑卡片 import BuildingCard


# ==================== 用户指定变量区 ====================
# 选项数据（从按键精灵界面布局获取）
CITY_LEVELS = [f"{i:02d}" for i in range(1, 41)]      # 城市：01-40
CITY_LEVELS_0 = [f"{i:02d}" for i in range(0, 41)]    # 城市：00-40
WORKSHOP_LEVELS = [f"{i:02d}" for i in range(0, 26)]  # 兵工：00-25
ARMY_LEVELS = [f"{i:02d}" for i in range(0, 16)]      # 陆军：00-15
AIR_LEVELS = [f"{i:02d}" for i in range(0, 7)]        # 空军：00-06
OTHER_LEVELS = [f"{i:02d}" for i in range(0, 7)]      # 其他：00-06
LEGION_LEVELS = [f"{i:02d}" for i in range(0, 11)]    # 军团：00-10
LEGION_LEVELS_1 = [f"{i:02d}" for i in range(1, 11)]  # 军团：01-10
# ========================================================


class BuildingInterface(BaseInterface):  # 建筑界面
    """建筑界面 - 提供建筑功能"""
    
    def __init__(self, config: 界面配置, page: ft.Page):
        super().__init__(config, page, title="建筑设置", subtitle="建筑相关配置")
    
    def _create_content_area(self) -> ft.Control:  # 创建内容区域
        spacing_config = self._config.定义尺寸.get("间距", {})
        card_spacing = spacing_config.get("spacing_md", 12)
        
        cards = [
            self._create_main_city_card(),
            ft.Divider(height=card_spacing, color="transparent"),
            self._create_vice_city_card(),
            ft.Divider(height=card_spacing, color="transparent"),
            self._create_branch_city_card(),
            ft.Divider(height=card_spacing, color="transparent"),
            self._create_legion_city_card(),
        ]
        
        return ft.Column(
            cards,
            spacing=0,
            expand=True,
        )
    
    def _create_main_city_card(self) -> ft.Container:  # 创建主帅主城卡片
        return BuildingCard.create(
            config=self._config,
            title="主帅主城",
            icon="HOME",
            items=[
                {"label": "城市", "options": CITY_LEVELS, "value": "17"},
                {"label": "兵工", "options": WORKSHOP_LEVELS, "value": "17"},
                {"label": "陆军", "options": ARMY_LEVELS, "value": "14"},
                {"label": "空军", "options": AIR_LEVELS, "value": "03"},
                {"label": "商业", "options": OTHER_LEVELS, "value": "04"},
                {"label": "补给", "options": OTHER_LEVELS, "value": "03"},
                {"label": "内塔", "options": OTHER_LEVELS, "value": "04"},
                {"label": "村庄", "options": OTHER_LEVELS, "value": "03"},
                {"label": "资源", "options": OTHER_LEVELS, "value": "03"},
                {"label": "军工", "options": OTHER_LEVELS, "value": "03"},
                {"label": "港口", "options": OTHER_LEVELS, "value": "03"},
                {"label": "外塔", "options": OTHER_LEVELS, "value": "03"},
            ],
        )
    
    def _create_vice_city_card(self) -> ft.Container:  # 创建付帅主城卡片
        return BuildingCard.create(
            config=self._config,
            title="付帅主城",
            icon="BUSINESS",
            items=[
                {"label": "城市", "options": CITY_LEVELS, "value": "15"},
                {"label": "兵工", "options": WORKSHOP_LEVELS, "value": "10"},
                {"label": "陆军", "options": ARMY_LEVELS, "value": "10"},
                {"label": "空军", "options": AIR_LEVELS, "value": "03"},
                {"label": "商业", "options": OTHER_LEVELS, "value": "04"},
                {"label": "补给", "options": OTHER_LEVELS, "value": "03"},
                {"label": "内塔", "options": OTHER_LEVELS, "value": "03"},
                {"label": "村庄", "options": OTHER_LEVELS, "value": "03"},
                {"label": "资源", "options": OTHER_LEVELS, "value": "03"},
                {"label": "军工", "options": OTHER_LEVELS, "value": "03"},
                {"label": "港口", "options": OTHER_LEVELS, "value": "03"},
                {"label": "外塔", "options": OTHER_LEVELS, "value": "03"},
            ],
        )
    
    def _create_branch_city_card(self) -> ft.Container:  # 创建所有分城卡片
        return BuildingCard.create(
            config=self._config,
            title="所有分城",
            icon="APARTMENT",
            items=[
                {"label": "城市", "options": CITY_LEVELS, "value": "15"},
                {"label": "兵工", "options": WORKSHOP_LEVELS, "value": "10"},
                {"label": "陆军", "options": ARMY_LEVELS, "value": "10"},
                {"label": "空军", "options": AIR_LEVELS, "value": "03"},
                {"label": "商业", "options": OTHER_LEVELS, "value": "04"},
                {"label": "补给", "options": OTHER_LEVELS, "value": "03"},
                {"label": "内塔", "options": OTHER_LEVELS, "value": "03"},
                {"label": "村庄", "options": OTHER_LEVELS, "value": "03"},
                {"label": "资源", "options": OTHER_LEVELS, "value": "03"},
                {"label": "军工", "options": OTHER_LEVELS, "value": "03"},
                {"label": "港口", "options": OTHER_LEVELS, "value": "03"},
                {"label": "外塔", "options": OTHER_LEVELS, "value": "03"},
            ],
        )
    
    def _create_legion_city_card(self) -> ft.Container:  # 创建军团城市卡片
        return BuildingCard.create(
            config=self._config,
            title="军团城市",
            icon="FORT",
            enabled=False,
            items=[
                {"label": "城号", "options": LEGION_LEVELS_1, "value": "01"},
                {"label": "城市", "options": LEGION_LEVELS_1, "value": "05"},
                {"label": "兵工", "options": LEGION_LEVELS_1, "value": "05"},
                {"label": "军需", "options": LEGION_LEVELS_1, "value": "05"},
                {"label": "陆军", "options": LEGION_LEVELS, "value": "00"},
                {"label": "空军", "options": LEGION_LEVELS, "value": "00"},
                {"label": "炮塔", "options": LEGION_LEVELS, "value": "00"},
            ],
        )


# 兼容别名
建筑界面 = BuildingInterface


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    config = 界面配置()
    
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = config.获取颜色("bg_primary")
        interface = BuildingInterface(config, page)
        page.add(interface.render())
    
    ft.run(main)
