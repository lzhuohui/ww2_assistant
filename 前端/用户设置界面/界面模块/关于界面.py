# -*- coding: utf-8 -*-
"""
模块名称：关于界面 | 层级：界面模块层
设计思路：
    关于界面，展示软件版本信息、联系方式、免责声明和缴费说明。
    使用关于卡片组件，保持视觉风格统一。

功能：
    1. 版本信息卡片
    2. 联系方式卡片（链接可点击复制）
    3. 缴费说明卡片
    4. 免责声明卡片

对外接口：
    - create(): 创建关于界面
"""

import flet as ft
from 前端.用户设置界面.配置.界面配置 import 界面配置
from 前端.用户设置界面.组件模块.关于卡片 import AboutCard
from 前端.用户设置界面.组件模块.通用功能容器 import GenericFunctionContainer, USER_WIDTH


class AboutInterface:
    """关于界面 - 界面模块层"""
    
    VERSION = "v1.0.0"
    UPDATE_DATE = "2026-03-14"
    
    QQ_GROUP = "123456789"
    WECHAT = "WW2_Helper"
    EMAIL = "ww2_helper@example.com"
    
    PRICE_MONTH = "30"
    PRICE_QUARTER = "80"
    PRICE_YEAR = "280"
    
    @staticmethod
    def create(width: int=USER_WIDTH) -> ft.Container:
        """
        创建关于界面
        
        参数：
            width: 内容区域宽度
        
        返回：
            ft.Container: 关于界面容器
        """
        配置 = 界面配置()
        
        version_card = AboutCard.create(
            config=配置,
            title="版本信息",
            icon="INFO",
            content_items=[
                ("软件名称", "二战风云辅助工具", None),
                ("当前版本", AboutInterface.VERSION, None),
                ("更新日期", AboutInterface.UPDATE_DATE, None),
            ],
        )
        
        contact_card = AboutCard.create(
            config=配置,
            title="联系方式",
            icon="CONTACTS",
            content_items=[
                ("QQ群", AboutInterface.QQ_GROUP, None),
                ("微信", AboutInterface.WECHAT, None),
                ("邮箱", AboutInterface.EMAIL, None),
            ],
        )
        
        payment_card = AboutCard.create(
            config=配置,
            title="缴费说明",
            icon="PAYMENT",
            content_items=[
                ("", "授权价格", None),
                ("月卡", f"{AboutInterface.PRICE_MONTH}元/月", None),
                ("季卡", f"{AboutInterface.PRICE_QUARTER}元/季", None),
                ("年卡", f"{AboutInterface.PRICE_YEAR}元/年", None),
                ("", "授权流程", None),
                ("", "1. 添加微信或QQ群联系作者", None),
                ("", "2. 选择授权时长并付款", None),
                ("", "3. 获取授权码并激活", None),
            ],
        )
        
        disclaimer_card = AboutCard.create(
            config=配置,
            title="免责声明",
            icon="WARNING_AMBER",
            content_items=[
                ("", "本软件仅供学习研究使用，请勿用于商业用途。", None),
                ("", "使用本软件产生的任何后果由用户自行承担。", None),
                ("", "请遵守游戏服务条款，合理使用。", None),
            ],
        )
        
        return GenericFunctionContainer.create(
            config=配置,
            title="关于",
            icon="INFO",
            cards=[version_card, contact_card, payment_card, disclaimer_card],
            width=width,
            expand=True,
        )


# *** 调试逻辑 ***
if __name__ == "__main__":
    ft.run(lambda page: page.add(AboutInterface.create()))
