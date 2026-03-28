# -*- coding: utf-8 -*-
"""
模块名称：AboutConfigSection
模块功能：关于信息区，展示版本信息、联系方式、缴费说明、免责声明
"""

import flet as ft
from typing import Callable, List

import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

try:
    from 核心层.配置.界面配置 import UIConfig
    from 核心层.常量.全局常量 import GlobalConstants
    from 表示层.组件.复合.卡片组管理器 import CardGroupManager, create_managed_card
except ImportError:
    # 尝试相对导入
    from ..核心层.配置.界面配置 import UIConfig
    from ..核心层.常量.全局常量 import GlobalConstants
    from ..表示层.组件.复合.卡片组管理器 import CardGroupManager, create_managed_card


# *** 用户指定变量: 变量值必须生效,AI不得更改数据 ***
USER_CARD_SPACING = 10  # 卡片间距
# *********************************


class AboutConfigSection:
    """关于信息区"""
    
    VERSION = "v1.0.0"
    UPDATE_DATE = "2026-03-25"
    QQ_GROUP = "123456789"
    WECHAT = "WW2_Helper"
    EMAIL = "ww2_helper@example.com"
    PRICE_MONTH = "30"
    PRICE_QUARTER = "80"
    PRICE_YEAR = "280"
    
    @staticmethod
    def create(
        config: UIConfig = None,
        config_service = None,
        save_callback: Callable[[str, str, str], None] = None,
    ) -> tuple:
        if config is None:
            config = UIConfig()
        
        theme_colors = config.当前主题颜色
        manager = CardGroupManager()
        
        def create_info_row(label: str, value: str) -> ft.Row:
            return ft.Row([
                ft.Text(label, size=14, color=theme_colors.get("text_secondary"), width=80) if label else ft.Container(),
                ft.Text(value, size=14, color=theme_colors.get("text_primary")),
            ], spacing=8, vertical_alignment=ft.CrossAxisAlignment.CENTER)
        
        def create_card(title: str, icon: str, info_list: List[tuple]) -> ft.Container:
            controls = [create_info_row(label, value) for label, value in info_list]
            
            card = create_managed_card(
                manager=manager,
                title=title,
                icon=icon,
                subtitle=info_list[0][1] if info_list else "",
                enabled=True,
                controls=controls,
                config=config,
            )
            return card
        
        card_list = []
        
        card_list.append(create_card(
            title="版本信息",
            icon="INFO",
            info_list=[
                ("软件名称", GlobalConstants.APP_NAME),
                ("当前版本", AboutConfigSection.VERSION),
                ("更新日期", AboutConfigSection.UPDATE_DATE),
            ],
        ))
        
        card_list.append(create_card(
            title="联系方式",
            icon="CONTACTS",
            info_list=[
                ("QQ群", AboutConfigSection.QQ_GROUP),
                ("微信", AboutConfigSection.WECHAT),
                ("邮箱", AboutConfigSection.EMAIL),
            ],
        ))
        
        card_list.append(create_card(
            title="缴费说明",
            icon="PAYMENT",
            info_list=[
                ("月卡", f"{AboutConfigSection.PRICE_MONTH}元/月"),
                ("季卡", f"{AboutConfigSection.PRICE_QUARTER}元/季"),
                ("年卡", f"{AboutConfigSection.PRICE_YEAR}元/年"),
            ],
        ))
        
        card_list.append(create_card(
            title="免责声明",
            icon="WARNING_AMBER",
            info_list=[
                ("", "本软件仅供学习研究使用，请勿用于商业用途。"),
                ("", "使用本软件产生的任何后果由用户自行承担。"),
            ],
        ))
        
        card_column = ft.Column(
            controls=card_list,
            spacing=USER_CARD_SPACING,
            scroll=ft.ScrollMode.HIDDEN,
            expand=True,
        )
        
        content_column = ft.Column(
            controls=[card_column],
            spacing=0,
            expand=True,
        )
        
        content_column.card_manager = manager
        

        
        return content_column, manager


# *** 标准测试格式: 仅调用被测模块,AI不得添加数据 ***
if __name__ == "__main__":
    def main(page: ft.Page):
        config = UIConfig()
        section, manager = AboutConfigSection.create(config=config)
        page.add(section)
    
    ft.app(target=main)
