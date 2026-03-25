# -*- coding: utf-8 -*-
"""
模块名称：AboutPage
设计思路: 关于信息界面，使用折叠卡片只读模式展示信息
模块隔离: 界面层依赖组件层
"""

import flet as ft
from typing import Callable, List

from 前端.新界面_v2.核心.配置.界面配置 import UIConfig
from 前端.新界面_v2.表示层.组件.复合.折叠卡片 import CollapsibleCard
from 前端.新界面_v2.核心.常量.全局常量 import USER_SPACING, USER_CARD_SPACING, GlobalConstants


# *** 用户指定变量 - AI不得修改, 变量值必须生效 ***
# （用户未指定变量）
# *********************************


class AboutPage:
    """关于信息界面"""
    
    VERSION = "v1.0.0"
    UPDATE_DATE = "2026-03-23"
    
    QQ_GROUP = "123456789"
    WECHAT = "WW2_Helper"
    EMAIL = "ww2_helper@example.com"
    
    PRICE_MONTH = "30"
    PRICE_QUARTER = "80"
    PRICE_YEAR = "280"
    
    @staticmethod
    def create(
        config: UIConfig=None,
        save_callback: Callable[[str, str, str], None]=None,
    ) -> ft.Container:
        if config is None:
            config = UIConfig()
        
        theme_colors = config.当前主题颜色
        card_list: List[ft.Control] = []
        
        def create_info_row(label: str, value: str) -> ft.Row:
            return ft.Row([
                ft.Text(label, size=14, color=theme_colors.get("text_secondary"), width=80) if label else ft.Container(),
                ft.Text(value, size=14, color=theme_colors.get("text_primary")),
            ], spacing=8, vertical_alignment=ft.CrossAxisAlignment.CENTER)
        
        def create_card(title: str, icon: str, info_list: List[tuple]) -> ft.Container:
            controls = [create_info_row(label, value) for label, value in info_list]
            
            card = CollapsibleCard.create(
                title=title,
                icon=icon,
                read_only=True,
                controls=controls,
                config=config,
            )
            card_list.append(card)
            return card
        
        create_card(
            title="版本信息",
            icon="INFO",
            info_list=[
                ("软件名称", GlobalConstants.APP_NAME),
                ("当前版本", AboutPage.VERSION),
                ("更新日期", AboutPage.UPDATE_DATE),
            ],
        )
        
        create_card(
            title="联系方式",
            icon="CONTACTS",
            info_list=[
                ("QQ群", AboutPage.QQ_GROUP),
                ("微信", AboutPage.WECHAT),
                ("邮箱", AboutPage.EMAIL),
            ],
        )
        
        create_card(
            title="缴费说明",
            icon="PAYMENT",
            info_list=[
                ("", "授权价格"),
                ("月卡", f"{AboutPage.PRICE_MONTH}元/月"),
                ("季卡", f"{AboutPage.PRICE_QUARTER}元/季"),
                ("年卡", f"{AboutPage.PRICE_YEAR}元/年"),
                ("", "授权流程"),
                ("", "1. 添加微信或QQ群联系作者"),
                ("", "2. 选择授权时长并付款"),
                ("", "3. 获取授权码并激活"),
            ],
        )
        
        create_card(
            title="免责声明",
            icon="WARNING_AMBER",
            info_list=[
                ("", "本软件仅供学习研究使用，请勿用于商业用途。"),
                ("", "使用本软件产生的任何后果由用户自行承担。"),
                ("", "请遵守游戏服务条款，合理使用。"),
            ],
        )
        
        title_bar = ft.Row([
            ft.Icon(ft.Icons.INFO, size=20, color=theme_colors.get("accent")),
            ft.Container(width=6),
            ft.Text("关于", size=16, weight=ft.FontWeight.BOLD, color=theme_colors.get("text_primary")),
        ], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER)
        
        card_column = ft.Column(
            controls=card_list,
            spacing=USER_CARD_SPACING,
            scroll=ft.ScrollMode.HIDDEN,
            expand=True,
        )
        
        content_column = ft.Column(
            controls=[
                title_bar,
                ft.Container(height=USER_SPACING),
                card_column,
            ],
            spacing=0,
            expand=True,
        )
        
        return ft.Container(
            content=content_column,
            expand=True,
        )


# *** 调试逻辑 ***
if __name__ == "__main__":
    ft.run(lambda page: page.add(AboutPage.create()))
