# -*- coding: utf-8 -*-
"""
关于设置页面 - 页面层

设计思路:
    展示软件版本信息、联系方式、免责声明和缴费说明。
    使用关于通用卡片组件，保持视觉风格统一。
    Win11风格：简洁明了、分组清晰、现代化排版。

功能:
    1. 版本信息卡片
    2. 联系方式卡片
    3. 缴费说明卡片
    4. 免责声明卡片

使用场景:
    被主界面调用。
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft
from typing import Callable
from 配置.界面配置 import 界面配置
from 新思路.组件层.关于通用卡片 import AboutCard


class AboutSettingsPage:
    """关于设置页面"""
    
    VERSION = "v1.0.0"
    UPDATE_DATE = "2026-03-14"
    
    QQ_GROUP = "123456789"
    WECHAT = "WW2_Helper"
    EMAIL = "ww2_helper@example.com"
    
    PRICE_MONTH = "30"
    PRICE_QUARTER = "80"
    PRICE_YEAR = "280"
    
    @staticmethod
    def create(config: 界面配置, page: ft.Page = None, on_refresh: Callable[[], None] = None) -> ft.Container:
        """
        创建关于设置页面
        
        参数:
            config: 界面配置对象
            page: 页面对象
            on_refresh: 刷新回调
        
        返回:
            ft.Container: 关于设置页面容器
        """
        theme_colors = config.当前主题颜色
        
        version_card = AboutCard.create(
            config=config,
            title="版本信息",
            icon="INFO",
            content_lines=[
                f"软件名称  二战风云辅助工具",
                f"当前版本  {AboutSettingsPage.VERSION}",
                f"更新日期  {AboutSettingsPage.UPDATE_DATE}",
            ],
        )
        
        contact_card = AboutCard.create(
            config=config,
            title="联系方式",
            icon="CONTACTS",
            content_lines=[
                f"QQ群  {AboutSettingsPage.QQ_GROUP}",
                f"微信  {AboutSettingsPage.WECHAT}",
                f"邮箱  {AboutSettingsPage.EMAIL}",
            ],
        )
        
        payment_card = AboutCard.create(
            config=config,
            title="缴费说明",
            icon="PAYMENT",
            content_lines=[
                f"授权价格",
                f"  月卡  {AboutSettingsPage.PRICE_MONTH}元/月",
                f"  季卡  {AboutSettingsPage.PRICE_QUARTER}元/季",
                f"  年卡  {AboutSettingsPage.PRICE_YEAR}元/年",
                f"授权流程",
                f"  1. 添加微信或QQ群联系作者",
                f"  2. 选择授权时长并付款",
                f"  3. 获取授权码并激活",
            ],
        )
        
        disclaimer_card = AboutCard.create(
            config=config,
            title="免责声明",
            icon="WARNING_AMBER",
            content_lines=[
                "本软件仅供学习研究使用，请勿用于商业用途。",
                "使用本软件产生的任何后果由用户自行承担。",
                "请遵守游戏服务条款，合理使用。",
            ],
        )
        
        page_content = ft.Column(
            [
                ft.Text(
                    "关于",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=theme_colors.get("text_primary"),
                ),
                ft.Container(height=4),
                version_card,
                ft.Container(height=4),
                contact_card,
                ft.Container(height=4),
                payment_card,
                ft.Container(height=4),
                disclaimer_card,
            ],
            spacing=0,
            scroll=ft.ScrollMode.HIDDEN,
            expand=True,
        )
        
        page_container = ft.Container(
            content=page_content,
            padding=ft.Padding.all(0),
            expand=True,
        )
        
        return page_container


关于设置页面 = AboutSettingsPage


if __name__ == "__main__":
    配置 = 界面配置()
    
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        page.add(AboutSettingsPage.create(配置, page))
    
    ft.run(main)
