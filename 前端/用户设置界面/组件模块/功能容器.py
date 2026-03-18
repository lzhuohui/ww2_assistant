# -*- coding: utf-8 -*-
"""
模块名称：功能容器 | 层级：组件模块层
设计思路：
    作为页面层的容器，包含通用容器、图标、标签、水平灰色隔断和卡片列表。
    支持两种方式传入卡片：cards（自定义控件）和card_configs（自动创建通用卡片）。
功能：
    1. 通用容器包装
    2. 图标显示（对应导航栏功能按钮图标）
    3. 标签显示（对应导航栏功能按钮名称）
    4. 水平灰色隔断
    5. 卡片列表（支持自定义控件或自动创建通用卡片）
数据来源：
    所有配置数据从配置目录获取。
使用场景：
    被页面层模块调用。
可独立运行调试: python 功能容器.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft
from typing import List, Optional, Dict, Any
from 前端.配置.界面配置 import 界面配置
from 前端.用户设置界面.单元模块.通用容器 import GenericContainer
from 前端.用户设置界面.单元模块.文本标签 import LabelText


# *** 用户指定变量 - AI不得修改 ***
# *********************************


class FunctionContainer:
    """功能容器 - 包含通用容器、图标、标签、水平灰色隔断和卡片列表"""
    
    @staticmethod
    def create(
        config: 界面配置,
        title: str = "功能标题",
        icon: str = None,
        cards: List[ft.Control] = None,
        card_configs: List[Dict[str, Any]] = None,
        width: int = None,
        height: int = None,
        expand: bool = False,
        **kwargs
    ) -> ft.Container:
        """
        创建功能容器
        
        参数:
            config: 界面配置对象
            title: 功能标题（对应导航栏功能按钮名称）
            icon: 图标名称（对应导航栏功能按钮图标）
            cards: 卡片控件列表（自定义控件）
            card_configs: 卡片配置列表（自动创建通用卡片）
            width: 容器宽度
            height: 容器高度
            expand: 是否扩展
            **kwargs: 其他参数
        
        返回:
            ft.Container: 功能容器
        
        使用方式:
            方式一：传入已创建好的卡片控件
            ```python
            FunctionContainer.create(
                config=配置,
                title="系统设置",
                icon="SETTINGS",
                cards=[card1, card2, card3],
            )
            ```
            
            方式二：传入卡片配置，自动创建通用卡片
            ```python
            FunctionContainer.create(
                config=配置,
                title="系统设置",
                icon="SETTINGS",
                card_configs=[
                    {"title": "挂机模式", "icon": "POWER_SETTINGS_NEW", "subtitle": "..."},
                    {"title": "指令速度", "icon": "SPEED", "subtitle": "..."},
                ],
            )
            ```
        """
        # 处理卡片列表
        final_cards = []
        
        # 如果提供了card_configs，调用通用卡片创建
        if card_configs:
            from 前端.用户设置界面.组件模块.通用卡片 import UniversalCard
            for card_config in card_configs:
                card = UniversalCard.create(**card_config)
                final_cards.append(card)
        
        # 如果提供了cards，添加到列表
        if cards:
            final_cards.extend(cards)
        
        # 图标
        icon_control = None
        if icon:
            if isinstance(icon, str):
                icon_upper = icon.upper()
                actual_icon = getattr(ft.Icons, icon_upper, ft.Icons.SETTINGS)
            else:
                actual_icon = icon
            # Win11风格图标：使用主题强调色
            icon_control = ft.Icon(
                actual_icon,
                size=20,
                color=config.当前主题颜色.get("accent"),
            )
        
        # 使用文本标签组件（统一主题颜色管理）
        label_text = LabelText.create(
            text=title,
            role="primary",
            size=16,
        )
        
        # Win11风格图标和标签组合
        header_content = ft.Row(
            [
                icon_control,
                ft.Container(width=8),
                label_text,
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ) if icon_control else label_text
        
        # Win11风格水平灰色隔断线：更柔和、更自然
        divider = ft.Container(
            content=ft.Divider(
                height=1,
                thickness=1,
                color=config.当前主题颜色.get("border"),
            ),
            opacity=0.5,
        )
        
        # Win11风格卡片列表：间距更合理
        card_list = ft.Column(
            controls=final_cards,
            spacing=5,
            expand=expand,
        )
        
        # 内容
        content = ft.Column(
            controls=[
                header_content,
                divider,
                card_list,
            ],
            spacing=8,
            expand=expand,
        )
        
        # 使用通用容器包装
        return GenericContainer.create(
            content=content,
            width=width,
            height=height,
            expand=expand,
            padding=16,
            **kwargs
        )


# 兼容别名
功能容器 = FunctionContainer


# *** 调试逻辑 ***
if __name__ == "__main__":
    from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider
    
    DEFAULT_TITLE = "功能标题"
    DEFAULT_ICON = "SETTINGS"
    DEFAULT_WIDTH = 400
    DEFAULT_CARD_CONFIGS = [
        {"title": "测试卡片1", "icon": "SETTINGS", "subtitle": "这是第一个测试卡片", "enabled": True},
        {"title": "测试卡片2", "icon": "SPEED", "subtitle": "这是第二个测试卡片", "enabled": True},
    ]
    
    配置 = 界面配置()
    ThemeProvider.initialize(配置)
    
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        page.add(FunctionContainer.create(
            config=配置,
            title=DEFAULT_TITLE,
            icon=DEFAULT_ICON,
            card_configs=DEFAULT_CARD_CONFIGS,
            width=DEFAULT_WIDTH,
        ))
    
    ft.run(main)
