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

from 前端.游戏设置界面.核心层.配置.界面配置 import UIConfig
from 前端.游戏设置界面.业务层.服务.配置服务 import ConfigService
from 前端.游戏设置界面.表示层.组件.复合.用户信息卡片 import UserInfoCard
from 前端.游戏设置界面.表示层.组件.复合.导航按钮 import NavigationButtonGroup
from 前端.游戏设置界面.表示层.界面.系统配置区 import SystemConfigSection
from 前端.游戏设置界面.表示层.界面.策略配置区 import StrategyConfigSection
from 前端.游戏设置界面.表示层.界面.账号配置区 import AccountConfigSection
from 前端.游戏设置界面.表示层.界面.个性化配置区 import PersonalizationConfigSection
from 前端.游戏设置界面.表示层.界面.配置方案区 import ConfigSchemeSection


USER_WINDOW_WIDTH = 1200
USER_WINDOW_HEIGHT = 540
USER_APP_TITLE = "二战风云辅助工具 - 游戏设置"
USER_NAV_WIDTH = 220
USER_TITLE_BAR_HEIGHT = 40
USER_SPACING = 10


class MainEntry:
    """主入口 - 整合导航和内容区"""
    
    @staticmethod
    def create(
        config: UIConfig = None,
    ) -> ft.Container:
        if config is None:
            config = UIConfig()
        
        config_service = ConfigService()
        config_service.load_config()
        
        theme_colors = config.当前主题颜色
        
        nav_items = [
            {"label": "系统配置", "icon": "SETTINGS"},
            {"label": "策略配置", "icon": "ROCKET_LAUNCH"},
            {"label": "账号设置", "icon": "ACCOUNT_CIRCLE"},
            {"label": "个性化", "icon": "PALETTE"},
            {"label": "配置方案", "icon": "FOLDER"},
        ]
        
        content_sections: Dict[str, ft.Control] = {}
        section_managers: Dict[str, Any] = {}
        
        user_card = UserInfoCard.create(
            config=config,
            user_name="二战风云玩家",
            authorized_count=0,
        )
        
        def create_section(label: str) -> ft.Control:
            if label in content_sections:
                return content_sections[label]
            
            if label == "系统配置":
                section, manager = SystemConfigSection.create(
                    config=config,
                    config_service=config_service,
                )
            elif label == "策略配置":
                section, manager = StrategyConfigSection.create(
                    config=config,
                    config_service=config_service,
                )
            elif label == "账号设置":
                section, manager = AccountConfigSection.create(
                    config=config,
                    config_service=config_service,
                )
            elif label == "个性化":
                section, manager = PersonalizationConfigSection.create(
                    config=config,
                    config_service=config_service,
                )
            elif label == "配置方案":
                section, manager = ConfigSchemeSection.create(
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
        
        current_label = [nav_items[0]["label"]]
        
        title_icon = ft.Icon(
            ft.Icons.SETTINGS,
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
        
        initial_section = create_section(current_label[0])
        
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
                if hasattr(old_manager, 'collapse_all'):
                    old_manager.collapse_all()
            
            current_label[0] = label
            
            title_text.value = label
            title_icon.name = getattr(ft.Icons, nav_items[index]["icon"].upper(), ft.Icons.HOME)
            
            new_section = create_section(label)
            content_container.content.controls[2].content = new_section
            
            try:
                if content_container.page:
                    content_container.update()
            except:
                pass
        
        nav_group = NavigationButtonGroup.create(
            items=nav_items,
            selected_index=0,
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
            padding=ft.padding.all(10),
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
    
    main_entry = MainEntry.create(config=config)
    page.add(main_entry)


# *** 标准测试格式: 仅调用被测模块,AI不得添加数据 ***
if __name__ == "__main__":
    ft.app(target=main)
