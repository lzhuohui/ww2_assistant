# -*- coding: utf-8 -*-
"""
模块名称：MainInterface
设计思路: 应用入口，组装各层模块
模块隔离: 入口层依赖所有层，不被任何层依赖
"""

import flet as ft
from typing import Dict, Any, Callable, Optional

from 前端.新界面_v2.核心.配置.界面配置 import UIConfig
from 前端.新界面_v2.核心.常量.全局常量 import GlobalConstants
from 前端.新界面_v2.业务层.服务.配置服务 import ConfigService
from 前端.新界面_v2.业务层.事件.事件总线 import EventBus
from 前端.新界面_v2.表示层.界面.系统界面 import SystemPage
from 前端.新界面_v2.表示层.界面.策略界面 import StrategyPage
from 前端.新界面_v2.表示层.界面.任务界面 import TaskPage
from 前端.新界面_v2.表示层.界面.建筑界面 import BuildingPage
from 前端.新界面_v2.表示层.界面.集资界面 import FundingPage
from 前端.新界面_v2.表示层.界面.账号界面 import AccountPage
from 前端.新界面_v2.表示层.界面.打扫界面 import CleaningPage
from 前端.新界面_v2.表示层.界面.打野界面 import HuntingPage
from 前端.新界面_v2.表示层.界面.个性化界面 import PersonalizationPage
from 前端.新界面_v2.表示层.界面.关于界面 import AboutPage
from 前端.新界面_v2.表示层.组件.基础.卡片容器 import CardContainer, USER_PADDING, USER_HEIGHT
from 前端.新界面_v2.表示层.组件.复合.用户信息卡片 import UserInfoCard
from 前端.新界面_v2.表示层.组件.复合.导航按钮 import NavigationButton


# *** 用户指定变量 - AI不得修改, 变量值必须生效 ***
USER_WINDOW_WIDTH = 1200  # 窗口宽度
USER_WINDOW_HEIGHT = 540  # 窗口高度
USER_NAV_WIDTH = 280  # 导航栏宽度
USER_SPACING = 10  # 默认间距
# *********************************


class MainInterface:
    """主界面 - 应用入口"""
    
    current_nav = "系统"
    content_area = None
    current_page_content = None
    config_service: Optional[ConfigService] = None
    event_bus: Optional[EventBus] = None
    
    @staticmethod
    def setup_window(page: ft.Page, config: UIConfig=None) -> None:
        if config is None:
            config = UIConfig()
        
        theme_colors = config.当前主题颜色
        
        page.title = GlobalConstants.APP_NAME
        # 使用与旧版相同的API设置窗口尺寸
        page.window.width = USER_WINDOW_WIDTH
        page.window.height = USER_WINDOW_HEIGHT
        page.window.resizable = False
        
        page.bgcolor = theme_colors.get("bg_primary")
        page.padding = 0
    
    @staticmethod
    def get_page_content(nav_name: str, config: UIConfig, config_service: ConfigService) -> ft.Control:
        """获取页面内容"""
        theme_colors = config.当前主题颜色
        
        def save_callback(card_id: str, config_key: str, value: str):
            config_service.set_value(nav_name, card_id, config_key, value)
        
        if nav_name == "系统":
            return SystemPage.create(config=config, save_callback=save_callback)
        elif nav_name == "策略":
            return StrategyPage.create(config=config, save_callback=save_callback)
        elif nav_name == "任务":
            return TaskPage.create(config=config, save_callback=save_callback)
        elif nav_name == "建筑":
            return BuildingPage.create(config=config, save_callback=save_callback)
        elif nav_name == "集资":
            return FundingPage.create(config=config, save_callback=save_callback)
        elif nav_name == "账号":
            return AccountPage.create(config=config, save_callback=save_callback)
        elif nav_name == "打扫":
            return CleaningPage.create(config=config, save_callback=save_callback)
        elif nav_name == "打野":
            return HuntingPage.create(config=config, save_callback=save_callback)
        elif nav_name == "个性化":
            return PersonalizationPage.create(config=config, save_callback=save_callback)
        elif nav_name == "关于":
            return AboutPage.create(config=config, save_callback=save_callback)
        else:
            return ft.Column([
                ft.Text(nav_name, size=20, weight=ft.FontWeight.BOLD, color=theme_colors.get("text_primary")),
                ft.Container(height=24),
                ft.Text(f"{nav_name}页面开发中...", size=14, color=theme_colors.get("text_secondary")),
            ], spacing=0, expand=True)
    
    @staticmethod
    def handle_function_click(function_id: str, config: UIConfig, config_service: ConfigService, container: ft.Container):
        """处理功能按钮点击"""
        theme_colors = config.当前主题颜色
        page = container.page if container else None
        
        if function_id == "导出配置":
            try:
                file_path = config_service_instance.save_game_config()
                snackbar = ft.SnackBar(
                    content=ft.Text(f"配置已导出: {file_path}", color=theme_colors.get("text_primary")),
                    bgcolor=theme_colors.get("success"),
                )
                if page:
                    page.snack_bar = snackbar
                    snackbar.open = True
                    page.update()
            except Exception as e:
                snackbar = ft.SnackBar(
                    content=ft.Text(f"导出失败: {str(e)}", color=theme_colors.get("text_primary")),
                    bgcolor=theme_colors.get("error"),
                )
                if page:
                    page.snack_bar = snackbar
                    snackbar.open = True
                    page.update()
        elif function_id == "恢复默认":
            pass
        elif function_id == "配置方案":
            pass
    
    @staticmethod
    def create(
        config: UIConfig=None,
        page: ft.Page=None,
    ) -> ft.Container:
        if config is None:
            config = UIConfig()
        
        # 如果提供了page对象，直接设置窗口尺寸
        if page:
            MainInterface.setup_window(page, config)
        
        theme_colors = config.当前主题颜色
        
        MainInterface.config_service_instance = ConfigService()
        MainInterface.config_service_instance.load_config()  # 加载配置
        MainInterface.event_bus_instance = EventBus()
        
        nav_items = GlobalConstants.NAV_ITEMS
        
        nav_buttons = []
        current_selection = [0]
        
        def destroy_current_page_card():
            if MainInterface.current_page_content is not None:
                content = MainInterface.current_page_content.content
                if content and hasattr(content, 'destroy_loaded_card'):
                    content.destroy_loaded_card()
        
        def handle_nav_click(index: int):
            current_selection[0] = index
            nav_name = nav_items[index]["id"]
            MainInterface.current_nav = nav_name
            
            for i, button in enumerate(nav_buttons):
                NavigationButton.update_selection(button, i == index, config)
            
            if MainInterface.content_area:
                destroy_current_page_card()
                
                new_content = MainInterface.get_page_content(nav_name, config, MainInterface.config_service_instance)
                MainInterface.current_page_content = new_content
                MainInterface.content_area.content = new_content
                
                try:
                    MainInterface.content_area.update()
                except Exception as e:
                    print(f"更新内容区域失败: {e}")
            
            MainInterface.event_bus_instance.publish_page_switch(nav_name)
        
        for i, item in enumerate(nav_items):
            button = NavigationButton.create(
                config=config,
                item=item,
                index=i,
                current_selection=current_selection,
                on_navigate=handle_nav_click,
                selected=(i == 0),
                auto_height=True,
            )
            nav_buttons.append(button)
        
        user_info = UserInfoCard.create(config=config)
        
        function_items = [
            {"id": "导出配置", "icon": "SAVE"},
        ]
        
        function_buttons = []
        for function_item in function_items:
            def create_function_callback(fid=function_item.get("id")):
                def callback(idx):
                    MainInterface.handle_function_click(fid, config, MainInterface.config_service_instance, container)
                return callback
            
            button = NavigationButton.create(
                config=config,
                item=function_item,
                index=-1,
                on_navigate=create_function_callback(),
                selected=False,
                auto_height=True,
            )
            function_buttons.append(button)
        
        all_buttons = nav_buttons + function_buttons
        
        nav_column = ft.Column(
            controls=all_buttons,
            spacing=USER_SPACING // 2, # 导航按钮间距  
            expand=True,
        )
        
        nav_panel = ft.Container(
            content=ft.Column([
                user_info,
                ft.Container(height=USER_SPACING),
                nav_column,
            ], spacing=0),
            width=USER_NAV_WIDTH,
            padding=ft.Padding(
                left=USER_SPACING,
                top=USER_SPACING,
                right=USER_SPACING * 2,
                bottom=USER_SPACING,
            ),
            bgcolor=theme_colors.get("bg_primary"),
        )
        
        initial_content = MainInterface.get_page_content(MainInterface.current_nav, config, MainInterface.config_service_instance)
        MainInterface.current_page_content = initial_content
        
        content_column = ft.Column(
            controls=[initial_content],
            spacing=0,
            expand=True,
        )
        
        content_container = ft.Container(
            content=content_column,
            padding=ft.Padding(
                left=USER_SPACING * 2,
                top=USER_SPACING,  # 修复：改为USER_SPACING，与左侧导航面板对齐
                right=USER_SPACING,
                bottom=USER_SPACING * 2,
            ),
            expand=True,
        )
        
        MainInterface.content_area = content_container
        
        main_row = ft.Row([
            nav_panel,
            ft.VerticalDivider(width=1, color=theme_colors.get("border")),
            content_container,
        ], expand=True, spacing=0)
        
        container = ft.Container(
            content=main_row,
            bgcolor=theme_colors.get("bg_primary"),
            expand=True,
        )
        
        def handle_mount(e):
            if container.page:
                MainInterface.setup_window(container.page, config)
        
        container.on_mount = handle_mount
        
        return container
    
    @staticmethod
    def get_game_config() -> Dict[str, Any]:
        """获取游戏控制配置（供外部调用）"""
        if MainInterface.config_service_instance:
            return MainInterface.config_service_instance.export_game_config()
        return {}
    
    @staticmethod
    def save_game_config() -> str:
        """保存游戏控制配置（供外部调用）"""
        if MainInterface.config_service_instance:
            return MainInterface.config_service_instance.save_game_config()
        return ""


# *** 调试逻辑 ***
if __name__ == "__main__":
    ft.run(lambda page: page.add(MainInterface.create(page=page)))
