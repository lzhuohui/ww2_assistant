# -*- coding: utf-8 -*-
"""
模块名称：关于界面
设计思路: 关于信息界面，使用折叠卡片只读模式展示信息
模块隔离: 界面层依赖组件层
"""

import flet as ft
from typing import Callable, List

from 前端.新界面_v2.核心.配置.界面配置 import 界面配置
from 前端.新界面_v2.表示层.组件.复合.折叠卡片 import 折叠卡片
from 前端.新界面_v2.核心.常量.全局常量 import USER_SPACING, USER_CARD_SPACING, 全局常量


# *** 用户指定变量 - AI不得修改 ***
# （用户未指定变量）
# *********************************


class 关于界面:
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
    def 创建(
        配置: 界面配置=None,
        保存回调: Callable[[str, str, str], None]=None,
    ) -> ft.Container:
        if 配置 is None:
            配置 = 界面配置()
        
        主题颜色 = 配置.当前主题颜色
        卡片列表: List[ft.Control] = []
        
        def 创建信息行(标签: str, 值: str) -> ft.Row:
            return ft.Row([
                ft.Text(标签, size=14, color=主题颜色.get("text_secondary"), width=80) if 标签 else ft.Container(),
                ft.Text(值, size=14, color=主题颜色.get("text_primary")),
            ], spacing=8, vertical_alignment=ft.CrossAxisAlignment.CENTER)
        
        def 创建卡片(标题: str, 图标: str, 信息列表: List[tuple]) -> ft.Container:
            控件列表 = [创建信息行(标签, 值) for 标签, 值 in 信息列表]
            
            卡片 = 折叠卡片.创建(
                标题=标题,
                图标=图标,
                只读模式=True,
                控件=控件列表,
                配置=配置,
            )
            卡片列表.append(卡片)
            return 卡片
        
        创建卡片(
            标题="版本信息",
            图标="INFO",
            信息列表=[
                ("软件名称", 全局常量.APP_NAME),
                ("当前版本", 关于界面.VERSION),
                ("更新日期", 关于界面.UPDATE_DATE),
            ],
        )
        
        创建卡片(
            标题="联系方式",
            图标="CONTACTS",
            信息列表=[
                ("QQ群", 关于界面.QQ_GROUP),
                ("微信", 关于界面.WECHAT),
                ("邮箱", 关于界面.EMAIL),
            ],
        )
        
        创建卡片(
            标题="缴费说明",
            图标="PAYMENT",
            信息列表=[
                ("", "授权价格"),
                ("月卡", f"{关于界面.PRICE_MONTH}元/月"),
                ("季卡", f"{关于界面.PRICE_QUARTER}元/季"),
                ("年卡", f"{关于界面.PRICE_YEAR}元/年"),
                ("", "授权流程"),
                ("", "1. 添加微信或QQ群联系作者"),
                ("", "2. 选择授权时长并付款"),
                ("", "3. 获取授权码并激活"),
            ],
        )
        
        创建卡片(
            标题="免责声明",
            图标="WARNING_AMBER",
            信息列表=[
                ("", "本软件仅供学习研究使用，请勿用于商业用途。"),
                ("", "使用本软件产生的任何后果由用户自行承担。"),
                ("", "请遵守游戏服务条款，合理使用。"),
            ],
        )
        
        标题栏 = ft.Row([
            ft.Icon(ft.Icons.INFO, size=20, color=主题颜色.get("accent")),
            ft.Container(width=6),
            ft.Text("关于", size=16, weight=ft.FontWeight.BOLD, color=主题颜色.get("text_primary")),
        ], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER)
        
        卡片列 = ft.Column(
            controls=卡片列表,
            spacing=USER_CARD_SPACING,
            scroll=ft.ScrollMode.HIDDEN,
            expand=True,
        )
        
        内容列 = ft.Column(
            controls=[
                标题栏,
                ft.Container(height=USER_SPACING),
                卡片列,
            ],
            spacing=0,
            expand=True,
        )
        
        return ft.Container(
            content=内容列,
            expand=True,
        )


# *** 调试逻辑 ***
if __name__ == "__main__":
    ft.run(lambda page: page.add(关于界面.创建()))
