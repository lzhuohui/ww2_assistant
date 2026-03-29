# -*- coding: utf-8 -*-
"""
模块名称：MainEntry
模块功能：应用入口，初始化界面
实现步骤：
- 初始化窗口配置
- 创建主布局（左侧导航+右侧内容）
- 支持导航切换
"""

import flet as ft
from typing import Dict, Any, Optional, List
import sys
import os

# 添加当前目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from 核心层.配置.界面配置 import UIConfig
from 业务层.服务.配置服务 import ConfigService
from 表示层.组件.复合.用户信息卡片 import UserInfoCard
from 表示层.组件.复合.导航按钮 import NavigationButtonGroup
from 表示层.界面.系统配置区 import SystemConfigSection
from 表示层.界面.策略配置区 import StrategyConfigSection
from 表示层.界面.任务配置区 import TaskConfigSection
from 表示层.界面.建筑配置区 import BuildingConfigSection
from 表示层.界面.集资配置区 import FundingConfigSection
from 表示层.界面.账号配置区 import AccountConfigSection
from 表示层.界面.打扫配置区 import CleaningConfigSection
from 表示层.界面.打野配置区 import HuntingConfigSection
from 表示层.界面.个性化配置区 import PersonalizationConfigSection
from 表示层.界面.配置方案区 import ConfigSchemeSection
from 表示层.界面.关于配置区 import AboutConfigSection


# *** 用户指定变量: 变量值必须生效,AI不得更改数据 ***
USER_WINDOW_WIDTH = 1200  # 窗口宽度
USER_WINDOW_HEIGHT = 540  # 窗口高度
USER_APP_TITLE = "二战风云辅助工具 - 游戏设置"  # 应用标题
USER_NAV_WIDTH = 240  # 导航栏宽度
USER_TITLE_BAR_HEIGHT = 40  # 标题栏高度
USER_SPACING = 10  # 间距
# *********************************


def refresh_page(page: ft.Page, config: UIConfig):
    """刷新页面主题,保持当前导航位置"""
    theme_colors = config.当前主题颜色
    page.bgcolor = theme_colors.get("bg_primary")
    current_nav_index = getattr(config, '_current_nav_index', 0)
    page.controls.clear()
    main_entry = MainEntry.create(
        config=config,
        page=page,
        initial_nav_index=current_nav_index,
    )
    page.add(main_entry)
    page.update()


class MainEntry:
    """主入口 - 整合导航和内容区"""
    
    @staticmethod
    def create(
        config: UIConfig = None,
        page: ft.Page = None,
        initial_nav_index: int = 0,
    ) -> ft.Container:
        if config is None:
            config = UIConfig()
        
        if page is not None:
            config._page = page
        
        config_service = ConfigService()
        config_service.load_config()
        
        theme_colors = config.当前主题颜色
        
        nav_items = [
            {"label": "系统", "icon": "SETTINGS"},
            {"label": "策略", "icon": "ROCKET_LAUNCH"},
            {"label": "任务", "icon": "ASSIGNMENT"},
            {"label": "建筑", "icon": "APARTMENT"},
            {"label": "集资", "icon": "ATTACH_MONEY"},
            {"label": "账号", "icon": "ACCOUNT_CIRCLE"},
            {"label": "打扫", "icon": "CLEANING_SERVICES"},
            {"label": "打野", "icon": "EXPLORE"},
            {"label": "个性化", "icon": "PALETTE"},
            {"label": "配置方案", "icon": "FOLDER"},
            {"label": "关于", "icon": "INFO"},
        ]
        
        content_sections: Dict[str, ft.Control] = {}
        section_managers: Dict[str, Any] = {}
        
        user_card = UserInfoCard.create(
            config=config,
            user_name="二战风云玩家",
            authorized_count=0,
            expire_days=30,
        )
        
        def update_user_card_count():
            if "账号" in section_managers:
                section = content_sections.get("账号")
                if section and hasattr(section, 'card_manager'):
                    current = AccountConfigSection.当前参与数量
                    max_count = AccountConfigSection.授权数量
                    user_card.update_authorized_count(current)
        
        def create_section(label: str, page: ft.Page) -> ft.Control:
            if label in content_sections:
                return content_sections[label]
            
            if label == "系统":
                section, manager = SystemConfigSection.create(
                    config=config,
                    config_service=config_service,
                )
            elif label == "策略":
                section, manager = StrategyConfigSection.create(
                    config=config,
                    config_service=config_service,
                )
            elif label == "任务":
                section, manager = TaskConfigSection.create(
                    config=config,
                    config_service=config_service,
                )
            elif label == "建筑":
                section, manager = BuildingConfigSection.create(
                    config=config,
                    config_service=config_service,
                )
            elif label == "集资":
                section, manager = FundingConfigSection.create(
                    config=config,
                    config_service=config_service,
                )
            elif label == "账号":
                section, manager = AccountConfigSection.create(
                    config=config,
                    config_service=config_service,
                    on_count_change=lambda c: user_card.update_authorized_count(c),
                )
            elif label == "打扫":
                section, manager = CleaningConfigSection.create(
                    config=config,
                    config_service=config_service,
                )
            elif label == "打野":
                section, manager = HuntingConfigSection.create(
                    config=config,
                    config_service=config_service,
                )
            elif label == "个性化":
                section, manager = PersonalizationConfigSection.create(
                    config=config,
                    config_service=config_service,
                    page=page,
                    on_theme_change=lambda: refresh_page(page, config),
                )
            elif label == "配置方案":
                section, manager = ConfigSchemeSection.create(
                    config=config,
                    config_service=config_service,
                )
            elif label == "关于":
                section, manager = AboutConfigSection.create(
                    config=config,
                    config_service=config_service,
                )
            else:
                section = ft.Container(content=ft.Text(f"未知页面: {label}"))
                manager = None
            
            content_sections[label] = section
            if manager:
                section_managers[label] = manager
            return section
        
        current_label = [nav_items[initial_nav_index]["label"]]
        config._current_nav_index = initial_nav_index
        
        initial_icon_name = nav_items[initial_nav_index]["icon"]
        
        title_icon = ft.Icon(
            getattr(ft.Icons, initial_icon_name.upper(), ft.Icons.HOME),
            size=20,
            color=theme_colors.get("accent"),
        )
        
        title_text = ft.Text(
            current_label[0],
            size=16,
            weight=ft.FontWeight.BOLD,
            color=theme_colors.get("text_primary"),
        )
        
        title_bar = ft.Row([
            title_icon,
            ft.Container(width=8),
            title_text,
        ], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER)
        
        initial_section = create_section(current_label[0], page)
        
        content_container = ft.Container(
            content=ft.Column([
                ft.Container(
                    content=title_bar,
                    height=USER_TITLE_BAR_HEIGHT,
                    padding=ft.padding.only(left=16),
                ),
                ft.Divider(height=1, thickness=1, color=theme_colors.get("border")),
                ft.Container(
                    content=initial_section,
                    expand=True,
                    padding=ft.padding.all(16),
                ),
            ], spacing=0, expand=True),
            expand=True,
            bgcolor=theme_colors.get("bg_primary"),
        )
        
        def handle_nav_change(label: str, index: int):
            if label == current_label[0]:
                return
            
            old_label = current_label[0]
            if old_label in section_managers:
                old_manager = section_managers[old_label]
                if hasattr(old_manager, 'destroy_all'):
                    old_manager.destroy_all()
            
            current_label[0] = label
            config._current_nav_index = index
            
            title_text.value = label
            title_icon.name = getattr(ft.Icons, nav_items[index]["icon"].upper(), ft.Icons.HOME)
            
            new_section = create_section(label, page)
            content_container.content.controls[2].content = new_section
            
            try:
                if content_container.page:
                    content_container.update()
            except:
                pass
        
        nav_group = NavigationButtonGroup.create(
            items=nav_items,
            selected_index=initial_nav_index,
            on_change=handle_nav_change,
            config=config,
        )
        
        left_nav = ft.Container(
            content=ft.Column([
                user_card,
                ft.Container(height=USER_SPACING),
                nav_group,
            ], spacing=0, expand=True),
            width=USER_NAV_WIDTH,
            bgcolor=theme_colors.get("bg_primary"),
            padding=ft.padding.only(left=10, top=0, right=10, bottom=10),
        )
        
        divider = ft.VerticalDivider(
            width=1,
            thickness=1,
            color=theme_colors.get("border"),
        )
        
        main_layout = ft.Row([
            left_nav,
            divider,
            content_container,
        ], expand=True, spacing=0)
        
        return ft.Container(
            content=main_layout,
            expand=True,
        )


def main(page: ft.Page):
    """应用入口函数"""
    config = UIConfig()
    theme_colors = config.当前主题颜色
    
    page.title = USER_APP_TITLE
    page.window.width = USER_WINDOW_WIDTH
    page.window.height = USER_WINDOW_HEIGHT
    page.window.resizable = False
    page.bgcolor = theme_colors.get("bg_primary")
    page.padding = 0
    
    main_entry = MainEntry.create(config=config, page=page)
    page.add(main_entry)


# *** 标准测试格式: 仅调用被测模块,AI不得添加数据 ***
if __name__ == "__main__":
    ft.app(target=main)
