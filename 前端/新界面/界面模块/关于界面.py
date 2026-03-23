# -*- coding: utf-8 -*-
"""模块名称：关于界面 | 设计思路：关于信息界面，版本/联系方式/缴费说明/免责声明 | 模块隔离原则"""

import flet as ft
from typing import Dict, Any, List, Callable

from 前端.新界面.核心接口.界面配置 import 界面配置
from 前端.新界面.核心接口.主题提供者 import ThemeProvider
from 前端.新界面.组件模块.卡片容器 import CardContainer


# *** 用户指定变量 - AI不得修改, 变量值必须生效 ***
USER_CARD_WIDTH = 500
USER_CARD_SPACING = 8
# *********************************


class 关于界面:
    """关于信息界面"""
    
    VERSION = "v1.0.0"
    UPDATE_DATE = "2026-03-22"
    QQ_GROUP = "123456789"
    WECHAT = "WW2_Helper"
    EMAIL = "ww2_helper@example.com"
    PRICE_MONTH = "30"
    PRICE_QUARTER = "80"
    PRICE_YEAR = "280"
    
    @staticmethod
    def create(
        config: 界面配置=None,
        width: int=USER_CARD_WIDTH,
    ) -> ft.Column:
        if config is None:
            config = 界面配置()
        
        ThemeProvider.initialize(config)
        theme_colors = config.当前主题颜色
        
        def create_info_card(title: str, icon: str, items: List[tuple]) -> ft.Container:
            rows = []
            for label, value in items:
                if label:
                    rows.append(ft.Row([
                        ft.Text(f"{label}:", size=12, color=theme_colors.get("text_secondary"), width=60),
                        ft.Text(value, size=12, color=theme_colors.get("text_primary")),
                    ], spacing=4))
                else:
                    rows.append(ft.Text(value, size=12, color=theme_colors.get("text_primary")))
            
            return CardContainer.create(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(getattr(ft.Icons, icon.upper(), ft.Icons.INFO), size=20, color=theme_colors.get("accent")),
                        ft.Container(width=8),
                        ft.Text(title, size=14, weight=ft.FontWeight.BOLD, color=theme_colors.get("text_primary")),
                    ], spacing=0),
                    ft.Container(height=12),
                    ft.Column(rows, spacing=6),
                ], spacing=0),
                config=config,
                width=width,
                padding=16,
            )
        
        version_card = create_info_card(
            "版本信息", "INFO",
            [
                ("软件名称", "二战风云辅助工具"),
                ("当前版本", 关于界面.VERSION),
                ("更新日期", 关于界面.UPDATE_DATE),
            ]
        )
        
        contact_card = create_info_card(
            "联系方式", "CONTACTS",
            [
                ("QQ群", 关于界面.QQ_GROUP),
                ("微信", 关于界面.WECHAT),
                ("邮箱", 关于界面.EMAIL),
            ]
        )
        
        payment_card = create_info_card(
            "缴费说明", "PAYMENT",
            [
                ("", "授权价格:"),
                ("月卡", f"{关于界面.PRICE_MONTH}元/月"),
                ("季卡", f"{关于界面.PRICE_QUARTER}元/季"),
                ("年卡", f"{关于界面.PRICE_YEAR}元/年"),
                ("", "授权流程:"),
                ("", "1. 添加微信或QQ群联系作者"),
                ("", "2. 选择授权时长并付款"),
                ("", "3. 获取授权码并激活"),
            ]
        )
        
        disclaimer_card = create_info_card(
            "免责声明", "WARNING_AMBER",
            [
                ("", "本软件仅供学习研究使用，请勿用于商业用途。"),
                ("", "使用本软件产生的任何后果由用户自行承担。"),
                ("", "请遵守游戏服务条款，合理使用。"),
            ]
        )
        
        content = ft.Column(
            controls=[version_card, contact_card, payment_card, disclaimer_card],
            spacing=USER_CARD_SPACING,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )
        
        def dispose():
            pass
        
        content.dispose = dispose
        
        return content


if __name__ == "__main__":
    config = 界面配置()
    ThemeProvider.initialize(config)
    
    ft.run(lambda page: page.add(关于界面.create(config=config)))
