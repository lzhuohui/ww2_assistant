# -*- coding: utf-8 -*-

"""
模块名称：主入口.py
模块功能：应用主入口，导航和内容区

实现步骤：
- 创建左侧导航面板
- 创建右侧内容区
- 支持导航切换
- 支持销毁

职责：
- 导航按钮 + 调用功能界面
- 页面销毁时调用销毁方法

不负责：
- 功能界面内部逻辑
- 控件创建和管理
"""

import flet as ft
from typing import Callable, Dict, List, Optional, Any

from 前端.V2.业务层.服务.配置服务 import ConfigService
from 前端.V2.层级4_复合模块.导航按钮 import NavButton
from 前端.V2.层级4_复合模块.用户信息卡片 import UserInfoCard
from 前端.V2.层级2_功能界面.系统界面 import SystemPage
from 前端.V2.层级2_功能界面.策略界面 import StrategyPage
from 前端.V2.层级2_功能界面.任务界面 import TaskPage
from 前端.V2.层级2_功能界面.建筑界面 import BuildingPage
from 前端.V2.层级2_功能界面.集资界面 import FundingPage
from 前端.V2.层级2_功能界面.账号界面 import AccountPage
from 前端.V2.层级2_功能界面.打扫界面 import CleaningPage
from 前端.V2.层级2_功能界面.打野界面 import HuntingPage
from 前端.V2.层级2_功能界面.个性化界面 import PersonalizationPage
from 前端.V2.层级2_功能界面.配置方案界面 import ConfigSchemePage
from 前端.V2.层级2_功能界面.关于界面 import AboutPage

# ============================================
# 数据和文件接口（前置，方便查看和修改）
# ============================================

USER_WINDOW_WIDTH = 1200
USER_WINDOW_HEIGHT = 540
USER_APP_TITLE = "二战风云辅助工具 - 游戏设置 V2"
USER_NAV_WIDTH = 240
USER_TITLE_BAR_HEIGHT = 40
USER_SPACING = 10

# 界面名称到导航信息的映射
INTERFACE_NAV_MAP = {
    "系统界面": {"label": "系统", "icon": "SETTINGS"},
    "策略界面": {"label": "策略", "icon": "ROCKET_LAUNCH"},
    "任务界面": {"label": "任务", "icon": "ASSIGNMENT"},
    "建筑界面": {"label": "建筑", "icon": "APARTMENT"},
    "集资界面": {"label": "集资", "icon": "ATTACH_MONEY"},
    "账号界面": {"label": "账号", "icon": "ACCOUNT_CIRCLE"},
    "打扫界面": {"label": "打扫", "icon": "CLEANING_SERVICES"},
    "打野界面": {"label": "打野", "icon": "EXPLORE"},
    "个性化界面": {"label": "个性化", "icon": "PALETTE"},
    "配置方案界面": {"label": "配置方案", "icon": "FOLDER"},
    "关于界面": {"label": "关于", "icon": "INFO"},
}

# 界面名称到模块的映射
INTERFACE_MODULE_MAP = {
    "系统界面": SystemPage,
    "策略界面": StrategyPage,
    "任务界面": TaskPage,
    "建筑界面": BuildingPage,
    "集资界面": FundingPage,
    "账号界面": AccountPage,
    "打扫界面": CleaningPage,
    "打野界面": HuntingPage,
    "个性化界面": PersonalizationPage,
    "配置方案界面": ConfigSchemePage,
    "关于界面": AboutPage,
}

# ============================================
# 公开接口
# ============================================

class MainEntry:
    """
    主入口 - 整合导航和内容区
    
    职责：
    - 导航按钮 + 调用功能界面
    - 页面销毁时调用销毁方法
    
    不负责：
    - 功能界面内部逻辑
    - 控件创建和管理
    """
    
    def __init__(self, page: ft.Page):
        self._page = page
        self._config_service = ConfigService()
        self._current_page_module = None
        self._content_area = ft.Container()
        self._theme_colors = self._get_theme_colors()
        self._interfaces = self._get_interfaces()
        
        self._setup_page()
    
    def _get_interfaces(self) -> List[str]:
        """获取界面列表（从配置服务）"""
        return self._config_service.get_interfaces()
    
    def _get_theme_colors(self) -> Dict[str, str]:
        """获取主题颜色（从配置服务获取）"""
        return self._config_service.get_theme_colors()
    
    def _setup_page(self):
        """设置页面"""
        self._page.title = USER_APP_TITLE
        self._page.window.width = USER_WINDOW_WIDTH
        self._page.window.height = USER_WINDOW_HEIGHT
        self._page.window.resizable = False
        self._page.bgcolor = self._theme_colors.get("bg_primary")
        self._page.padding = 0
        
        main_layout = self._create_main_layout()
        self._page.add(main_layout)
    
    def _create_main_layout(self) -> ft.Container:
        """创建主布局"""
        user_card = self._create_user_card()
        
        nav_buttons = []
        for i, interface in enumerate(self._interfaces):
            nav_info = INTERFACE_NAV_MAP.get(interface, {"label": interface, "icon": "HOME"})
            btn = NavButton.create(
                icon_name=nav_info["icon"],
                text=nav_info["label"],
                selected=(i == 0),
                on_click=lambda e, idx=i: self._handle_nav_click(idx),
                theme_colors=self._theme_colors,
            )
            nav_buttons.append(btn)
        
        nav_group = ft.Column(nav_buttons, spacing=4)
        
        left_nav = ft.Container(
            content=ft.Column([
                user_card,
                ft.Container(height=USER_SPACING),
                nav_group,
            ], spacing=0),
            width=USER_NAV_WIDTH,
            bgcolor=self._theme_colors.get("bg_primary"),
            padding=ft.Padding(left=10, top=0, right=10, bottom=10),
        )
        
        divider = ft.VerticalDivider(
            width=1,
            thickness=1,
            color=self._theme_colors.get("border"),
        )
        
        self._content_area = self._create_content_area(0)
        
        return ft.Container(
            content=ft.Row([
                left_nav,
                divider,
                self._content_area,
            ], expand=True, spacing=0),
            expand=True,
        )
    
    def _create_user_card(self) -> ft.Container:
        """创建用户信息卡片"""
        user_card = UserInfoCard(self._config_service)
        return user_card.create(theme_colors=self._theme_colors)
    
    def _create_content_area(self, nav_index: int) -> ft.Container:
        """创建内容区"""
        interface = self._interfaces[nav_index] if nav_index < len(self._interfaces) else ""
        nav_info = INTERFACE_NAV_MAP.get(interface, {"label": interface, "icon": "HOME"})
        
        title_icon = ft.Icon(
            getattr(ft.Icons, nav_info["icon"].upper(), ft.Icons.HOME),
            size=20,
            color=self._theme_colors.get("accent"),
        )
        
        title_text = ft.Text(
            nav_info["label"],
            size=16,
            weight=ft.FontWeight.BOLD,
            color=self._theme_colors.get("text_primary"),
        )
        
        title_bar = ft.Row([
            title_icon,
            ft.Container(width=8),
            title_text,
        ], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER)
        
        initial_section = self._create_section(nav_index)
        
        return ft.Container(
            content=ft.Column([
                ft.Container(
                    content=title_bar,
                    height=USER_TITLE_BAR_HEIGHT,
                    padding=ft.Padding(16, 0, 0, 0),
                ),
                ft.Divider(height=1, thickness=1, color=self._theme_colors.get("border")),
                ft.Container(
                    content=initial_section,
                    expand=True,
                    padding=ft.Padding(16, 16, 16, 16),
                ),
            ], spacing=0, expand=True),
            expand=True,
            bgcolor=self._theme_colors.get("bg_primary"),
        )
    
    def _create_section(self, nav_index: int) -> ft.Control:
        """创建功能界面"""
        interface = self._interfaces[nav_index] if nav_index < len(self._interfaces) else ""
        self._current_page_module = INTERFACE_MODULE_MAP.get(interface)
        
        if self._current_page_module:
            if interface == "个性化界面":
                return self._current_page_module.create(
                    page=self._page,
                    config_service=self._config_service,
                    on_change=None,
                    theme_colors=self._theme_colors,
                    on_theme_change=self._refresh_page,
                )
            return self._current_page_module.create(
                page=self._page,
                config_service=self._config_service,
                theme_colors=self._theme_colors,
            )
        
        return ft.Container(content=ft.Text("未知页面"))
    
    def _handle_nav_change(self, index: int):
        """处理导航切换"""
        if self._current_page_module and hasattr(self._current_page_module, 'destroy'):
            self._current_page_module.destroy()
        
        interface = self._interfaces[index] if index < len(self._interfaces) else ""
        nav_info = INTERFACE_NAV_MAP.get(interface, {"label": interface, "icon": "HOME"})
        
        title_icon = ft.Icon(
            getattr(ft.Icons, nav_info["icon"].upper(), ft.Icons.HOME),
            size=20,
            color=self._theme_colors.get("accent"),
        )
        
        title_bar = self._content_area.content.controls[0]
        title_bar.content.controls[0] = title_icon
        title_bar.content.controls[2].value = nav_info["label"]
        
        new_section = self._create_section(index)
        self._content_area.content.controls[2].content = new_section
        
        try:
            if self._content_area.page:
                self._content_area.update()
        except:
            pass
    
    def _handle_nav_click(self, index: int):
        """处理导航按钮点击"""
        self._handle_nav_change(index)
    
    def _refresh_page(self):
        """刷新页面主题"""
        self._theme_colors = self._get_theme_colors()
        self._page.bgcolor = self._theme_colors.get("bg_primary")
        self._page.controls.clear()
        main_layout = self._create_main_layout()
        self._page.add(main_layout)
        self._page.update()

# *** 标准测试格式: 仅调用被测模块,AI不得添加数据 ***
if __name__ == "__main__":
    def main(page: ft.Page):
        entry = MainEntry(page)
    
    ft.run(main)
