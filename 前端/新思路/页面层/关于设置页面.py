# -*- coding: utf-8 -*-
"""
关于设置页面 - 页面层

设计思路:
    展示软件版本信息、联系方式、免责声明和缴费说明。

功能:
    1. 版本信息卡片
    2. 联系方式卡片
    3. 免责声明卡片
    4. 缴费说明卡片

使用场景:
    被主界面调用。
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft
from typing import Callable
from 配置.界面配置 import 界面配置


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
        
        version_card = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.INFO, color=theme_colors.get("accent"), size=24),
                            ft.Text("版本信息", size=16, weight=ft.FontWeight.BOLD, color=theme_colors.get("text_primary")),
                        ],
                        spacing=10,
                    ),
                    ft.Container(height=10),
                    ft.Text(f"软件名称：二战风云辅助工具", size=14, color=theme_colors.get("text_secondary")),
                    ft.Text(f"当前版本：{AboutSettingsPage.VERSION}", size=14, color=theme_colors.get("text_secondary")),
                    ft.Text(f"更新时间：{AboutSettingsPage.UPDATE_DATE}", size=14, color=theme_colors.get("text_secondary")),
                ],
                spacing=5,
            ),
            padding=ft.Padding.all(16),
            bgcolor=theme_colors.get("bg_secondary"),
            border_radius=8,
        )
        
        contact_card = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.CONTACTS, color=theme_colors.get("accent"), size=24),
                            ft.Text("联系方式", size=16, weight=ft.FontWeight.BOLD, color=theme_colors.get("text_primary")),
                        ],
                        spacing=10,
                    ),
                    ft.Container(height=10),
                    ft.Row(
                        [
                            ft.Text("QQ群：", size=14, color=theme_colors.get("text_secondary")),
                            ft.TextButton(
                                AboutSettingsPage.QQ_GROUP,
                                on_click=lambda e: copy_to_clipboard(AboutSettingsPage.QQ_GROUP, "QQ群"),
                            ),
                        ],
                    ),
                    ft.Row(
                        [
                            ft.Text("微信：", size=14, color=theme_colors.get("text_secondary")),
                            ft.TextButton(
                                AboutSettingsPage.WECHAT,
                                on_click=lambda e: copy_to_clipboard(AboutSettingsPage.WECHAT, "微信"),
                            ),
                        ],
                    ),
                    ft.Row(
                        [
                            ft.Text("邮箱：", size=14, color=theme_colors.get("text_secondary")),
                            ft.TextButton(
                                AboutSettingsPage.EMAIL,
                                on_click=lambda e: copy_to_clipboard(AboutSettingsPage.EMAIL, "邮箱"),
                            ),
                        ],
                    ),
                ],
                spacing=5,
            ),
            padding=ft.Padding.all(16),
            bgcolor=theme_colors.get("bg_secondary"),
            border_radius=8,
        )
        
        disclaimer_card = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.WARNING_AMBER, color=theme_colors.get("warning", "#FF8C00"), size=24),
                            ft.Text("免责声明", size=16, weight=ft.FontWeight.BOLD, color=theme_colors.get("text_primary")),
                        ],
                        spacing=10,
                    ),
                    ft.Container(height=10),
                    ft.Text(
                        "本软件仅供学习研究使用，请勿用于商业用途。使用本软件产生的任何后果由用户自行承担，与开发者无关。请遵守游戏服务条款，合理使用。",
                        size=14,
                        color=theme_colors.get("text_secondary"),
                    ),
                ],
                spacing=5,
            ),
            padding=ft.Padding.all(16),
            bgcolor=theme_colors.get("bg_secondary"),
            border_radius=8,
        )
        
        payment_card = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.PAYMENT, color=theme_colors.get("accent"), size=24),
                            ft.Text("缴费说明", size=16, weight=ft.FontWeight.BOLD, color=theme_colors.get("text_primary")),
                        ],
                        spacing=10,
                    ),
                    ft.Container(height=10),
                    ft.Text("授权价格：", size=14, weight=ft.FontWeight.BOLD, color=theme_colors.get("text_primary")),
                    ft.Text(f"  月卡：{AboutSettingsPage.PRICE_MONTH}元/月", size=14, color=theme_colors.get("text_secondary")),
                    ft.Text(f"  季卡：{AboutSettingsPage.PRICE_QUARTER}元/季", size=14, color=theme_colors.get("text_secondary")),
                    ft.Text(f"  年卡：{AboutSettingsPage.PRICE_YEAR}元/年", size=14, color=theme_colors.get("text_secondary")),
                    ft.Container(height=10),
                    ft.Text("获取授权流程：", size=14, weight=ft.FontWeight.BOLD, color=theme_colors.get("text_primary")),
                    ft.Text("  1. 添加微信或QQ群联系作者", size=14, color=theme_colors.get("text_secondary")),
                    ft.Text("  2. 选择授权时长并付款", size=14, color=theme_colors.get("text_secondary")),
                    ft.Text("  3. 获取授权码并激活", size=14, color=theme_colors.get("text_secondary")),
                ],
                spacing=5,
            ),
            padding=ft.Padding.all(16),
            bgcolor=theme_colors.get("bg_secondary"),
            border_radius=8,
        )
        
        page_content = ft.Column(
            [
                ft.Text(
                    "关于",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=theme_colors.get("text_primary"),
                ),
                ft.Container(height=20),
                version_card,
                ft.Container(height=15),
                contact_card,
                ft.Container(height=15),
                payment_card,
                ft.Container(height=15),
                disclaimer_card,
            ],
            spacing=0,
            scroll=ft.ScrollMode.HIDDEN,
            expand=True,
        )
        
        page_container = ft.Container(
            content=page_content,
            padding=ft.Padding.all(20),
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
