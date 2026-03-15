# -*- coding: utf-8 -*-
"""
关于设置页面 - 页面层

设计思路:
    展示软件版本信息、联系方式、免责声明和缴费说明。
    使用关于通用卡片组件，保持视觉风格统一。
    Win11风格：简洁明了、分组清晰、现代化排版、链接可点击。

功能:
    1. 版本信息卡片
    2. 联系方式卡片（链接可点击复制）
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
        
        def copy_to_clipboard(text: str, label: str):
            if page:
                page.set_clipboard(text)
                page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"{label}已复制: {text}"),
                    duration=2000,
                )
                page.snack_bar.open = True
                page.update()
        
        def on_qq_click(e):
            copy_to_clipboard(AboutSettingsPage.QQ_GROUP, "QQ群")
        
        def on_wechat_click(e):
            copy_to_clipboard(AboutSettingsPage.WECHAT, "微信")
        
        def on_email_click(e):
            copy_to_clipboard(AboutSettingsPage.EMAIL, "邮箱")
        
        version_card = AboutCard.create(
            config=config,
            title="版本信息",
            icon="INFO",
            content_items=[
                ("软件名称", "二战风云辅助工具", None),
                ("当前版本", AboutSettingsPage.VERSION, None),
                ("更新日期", AboutSettingsPage.UPDATE_DATE, None),
            ],
        )
        
        contact_card = AboutCard.create(
            config=config,
            title="联系方式",
            icon="CONTACTS",
            content_items=[
                ("QQ群", AboutSettingsPage.QQ_GROUP, on_qq_click),
                ("微信", AboutSettingsPage.WECHAT, on_wechat_click),
                ("邮箱", AboutSettingsPage.EMAIL, on_email_click),
            ],
        )
        
        payment_card = AboutCard.create(
            config=config,
            title="缴费说明",
            icon="PAYMENT",
            content_items=[
                ("", "授权价格", None),
                ("月卡", f"{AboutSettingsPage.PRICE_MONTH}元/月", None),
                ("季卡", f"{AboutSettingsPage.PRICE_QUARTER}元/季", None),
                ("年卡", f"{AboutSettingsPage.PRICE_YEAR}元/年", None),
                ("", "授权流程", None),
                ("", "1. 添加微信或QQ群联系作者", None),
                ("", "2. 选择授权时长并付款", None),
                ("", "3. 获取授权码并激活", None),
            ],
        )
        
        disclaimer_card = AboutCard.create(
            config=config,
            title="免责声明",
            icon="WARNING_AMBER",
            content_items=[
                ("", "本软件仅供学习研究使用，请勿用于商业用途。", None),
                ("", "使用本软件产生的任何后果由用户自行承担。", None),
                ("", "请遵守游戏服务条款，合理使用。", None),
            ],
        )
        
        page_title = ft.Container(
            content=ft.Text(
                "关于",
                size=24,
                weight=ft.FontWeight.BOLD,
                color=theme_colors.get("text_primary"),
            ),
            padding=ft.Padding(bottom=4),
        )
        
        scrollable_content = ft.Column(
            [
                version_card,
                ft.Container(height=5),
                contact_card,
                ft.Container(height=5),
                payment_card,
                ft.Container(height=5),
                disclaimer_card,
            ],
            spacing=0,
            scroll=ft.ScrollMode.HIDDEN,
            expand=True,
        )
        
        page_content = ft.Column(
            [
                page_title,
                scrollable_content,
            ],
            spacing=0,
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
