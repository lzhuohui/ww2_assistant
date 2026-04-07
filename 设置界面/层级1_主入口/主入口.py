# -*- coding: utf-8 -*-

"""
模块名称：主入口.py
模块功能：V3版本主入口，管理导航和界面切换

职责：
- 初始化配置管理
- 创建导航栏
- 管理界面切换
- 主题管理

不负责：
- 具体界面内容
- 方案下拉框和保存按钮（由界面容器负责）
"""

import flet as ft
from typing import Dict, Any, Optional

from 设置界面.层级0_数据管理.配置管理 import ConfigManager
from 设置界面.层级2_功能界面.系统界面 import SystemInterface
from 设置界面.层级2_功能界面.账号界面 import AccountInterface
from 设置界面.层级2_功能界面.建筑界面 import BuildingInterface
from 设置界面.层级2_功能界面.策略界面 import StrategyInterface
from 设置界面.层级2_功能界面.任务界面 import TaskInterface
from 设置界面.层级2_功能界面.集资界面 import FundraiseInterface
from 设置界面.层级2_功能界面.打野界面 import HuntInterface
from 设置界面.层级2_功能界面.打扫界面 import CleanInterface
from 设置界面.层级2_功能界面.个性化界面 import PersonalizationInterface
from 设置界面.层级2_功能界面.注册界面 import RegisterInterface
from 设置界面.层级2_功能界面.关于界面 import AboutInterface
from 设置界面.层级4_复合模块.用户信息 import UserInfoCard
from 设置界面.层级5_基础模块.标签 import Label
from 设置界面.层级5_基础模块.下拉框 import Dropdown
from 设置界面.层级5_基础模块.方案选择器 import SchemeSelector

# ============================================
# 公开接口
# ============================================

class MainEntry:
    """
    主入口 - V3版本
    
    职责：
    - 初始化配置管理
    - 创建导航栏
    - 管理界面切换
    - 主题管理
    
    不负责：
    - 具体界面内容
    - 方案下拉框和保存按钮（由界面容器负责）
    """
    
    def __init__(self, page: ft.Page):
        self._page = page
        self._config_manager = ConfigManager()
        self._interfaces: Dict[str, Any] = {}
        self._current_interface: Optional[str] = None
        self._nav_indicator: Optional[ft.Container] = None
        self._nav_item_positions: Dict[str, int] = {}
        self._main_column: Optional[ft.Column] = None
        self._nav_items: Dict[str, ft.Container] = {}
        
        self._config_manager.register_on_change(self._on_config_change)
        
        self._init_modules()
        self._setup_page()
        self._build_ui()
    
    def _init_modules(self):
        """
        初始化模块配置管理（级联设置底层模块）
        
        重要说明：
        - 此方法在__init__中调用，必须在创建任何UI组件之前执行
        - 使用类属性注入方式，将配置管理实例传递给底层模块
        - 初始化顺序：UserInfoCard -> Label/Dropdown/SchemeSelector
        
        设计考虑：
        - 使用类属性注入而非实例属性，简化模块间的依赖关系
        - 所有底层模块都有_check_config_manager方法，确保初始化顺序正确
        - 错误提示清晰，便于排查初始化顺序问题
        
        注意：
        - 不要在初始化完成前创建任何UI组件
        - 如果添加新的底层模块，需要在此方法中添加对应的set_config_manager调用
        """
        UserInfoCard.set_config_manager(self._config_manager)
        UserInfoCard.set_on_click_callback(self._on_user_info_click)
        Label.set_config_manager(self._config_manager)
        Dropdown.set_config_manager(self._config_manager)
        SchemeSelector.set_config_manager(self._config_manager)
    
    def _on_user_info_click(self):
        """用户信息点击回调 - 跳转到注册界面"""
        self._on_nav_item_click("注册界面")
    
    def _setup_page(self):
        """设置页面基本属性"""
        theme_colors = self._config_manager.get_theme_colors()
        
        self._page.title = "二战风云 V3"
        self._page.theme_mode = ft.ThemeMode.DARK
        self._page.bgcolor = theme_colors.get("bg_primary", "#202020")
        self._page.padding = 0
        
        # 设置窗口/页面尺寸（桌面模式/Web模式通用）
        self._page.width = 1200
        self._page.height = 540
        self._page.window.width = 1200
        self._page.window.height = 540
        self._page.window.title_bar_hidden = True
        self._page.window.draggable = True  # type: ignore
    
    def _build_nav_item(self, icon, label: str, selected: bool = False, on_click=None) -> ft.Control:
        """构建单个导航项 - Win11风格
        
        交互状态规范：
        - 默认：transparent背景，无边框，text_secondary文字/图标
        - 悬停：bg_hover背景，无边框，text_primary文字/图标
        - 激活：bg_selected背景，text_primary文字，accent图标
        
        指示条由全局管理，不在单个导航项中
        """
        theme_colors = self._config_manager.get_theme_colors()
        animation_config = self._config_manager.get_animation_config()
        
        accent = theme_colors.get("accent", "#0078D4")
        text_primary = theme_colors.get("text_primary", "#FFFFFF")
        text_secondary = theme_colors.get("text_secondary", "#B0B0B0")
        bg_selected = theme_colors.get("bg_selected", "#3A3A3A")
        bg_hover = theme_colors.get("bg_hover", "#3A3A3A")
        
        icon_size = self._config_manager.get_nav_config("图标大小", 20)
        font_size = self._config_manager.get_nav_config("字体大小", 14)
        item_spacing = self._config_manager.get_nav_config("项间距", 8)
        item_padding = self._config_manager.get_nav_config("项内边距", 12)
        item_radius = self._config_manager.get_nav_item_radius()
        item_height = self._config_manager.get_nav_item_height()
        transition_duration = animation_config.get("transition_duration", 167)
        
        icon_control = ft.Icon(icon, color=accent if selected else text_secondary, size=icon_size)
        label_control = ft.Text(label, color=text_primary if selected else text_secondary, size=font_size)
        
        content_container = ft.Container(
            content=ft.Row([
                icon_control,
                label_control,
            ], spacing=item_spacing, alignment=ft.MainAxisAlignment.START),
            padding=ft.Padding.symmetric(horizontal=item_padding, vertical=item_padding // 2),
            bgcolor=bg_selected if selected else "transparent",
            border_radius=item_radius,
            animate=transition_duration,
            on_click=on_click,
        )
        
        container = ft.Container(
            content=content_container,
            height=item_height,
        )
        
        container._icon_control = icon_control
        container._label_control = label_control
        container._content_container = content_container
        container._selected = selected
        container._accent = accent
        container._text_primary = text_primary
        container._text_secondary = text_secondary
        container._bg_selected = bg_selected
        container._bg_hover = bg_hover
        
        def on_hover(e):
            if container._selected:
                return
            if e.data:
                container._content_container.bgcolor = container._bg_hover
                container._icon_control.color = container._text_primary
                container._label_control.color = container._text_primary
            else:
                container._content_container.bgcolor = "transparent"
                container._icon_control.color = container._text_secondary
                container._label_control.color = container._text_secondary
            container._content_container.update()
        
        content_container.on_hover = on_hover
        
        return container
    
    def _build_title_bar(self, theme_colors: Dict[str, str]) -> ft.Container:
        """构建自定义标题栏"""
        text_primary = theme_colors.get("text_primary", "#FFFFFF")
        text_secondary = theme_colors.get("text_secondary", "#B0B0B0")
        bg_secondary = theme_colors.get("bg_secondary", "#1E1E1E")
        accent = theme_colors.get("accent", "#0078D4")
        
        title_text = ft.Text(
            value="二战风云 V3",
            size=14,
            color=text_primary,
            weight=ft.FontWeight.BOLD,
        )
        
        def on_minimize(e):
            self._page.window.minimized = True
            self._page.update()
        
        def on_maximize(e):
            self._page.window.maximized = not self._page.window.maximized
            self._page.update()
        
        async def on_close(e):
            self._page.window.prevent_close = False
            await self._page.window.close()
        
        minimize_btn = ft.IconButton(
            icon=ft.Icons.REMOVE,
            icon_size=16,
            icon_color=text_secondary,
            on_click=on_minimize,
            style=ft.ButtonStyle(
                padding=ft.Padding.all(4),
                shape=ft.RoundedRectangleBorder(radius=4),
            ),
        )
        
        maximize_btn = ft.IconButton(
            icon=ft.Icons.CROP_SQUARE,
            icon_size=14,
            icon_color=text_secondary,
            on_click=on_maximize,
            style=ft.ButtonStyle(
                padding=ft.Padding.all(4),
                shape=ft.RoundedRectangleBorder(radius=4),
            ),
        )
        
        close_btn = ft.IconButton(
            icon=ft.Icons.CLOSE,
            icon_size=16,
            icon_color=text_secondary,
            on_click=on_close,
            style=ft.ButtonStyle(
                padding=ft.Padding.all(4),
                shape=ft.RoundedRectangleBorder(radius=4),
            ),
        )
        
        def on_hover_close(e):
            close_btn.icon_color = ft.Colors.RED if e.data else text_secondary
            close_btn.update()
        
        close_btn.on_hover = on_hover_close
        
        title_bar = ft.Container(
            content=ft.Row([
                ft.Container(width=100),
                ft.Container(
                    content=title_text,
                    expand=True,
                    alignment=ft.Alignment(0, 0),
                ),
                ft.Row([
                    minimize_btn,
                    maximize_btn,
                    close_btn,
                ], spacing=0),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=bg_secondary,
            height=32,
            padding=ft.Padding.symmetric(horizontal=8, vertical=0),
        )
        
        return title_bar
    
    def _build_ui(self, preserve_interface: str = None):
        """构建UI
        
        参数:
            preserve_interface: 重建后要保持的界面名称（主题切换时使用）
        """
        theme_colors = self._config_manager.get_theme_colors()
        
        title_bar = self._build_title_bar(theme_colors)
        
        user_info_card = UserInfoCard.create(theme_colors=theme_colors)
        
        interface_names = self._config_manager.get_interface_names()
        
        self._nav_items: Dict[str, ft.Container] = {}
        nav_items_list = []
        
        item_height = self._config_manager.get_nav_item_height()
        item_spacing = 4
        
        indicator_size = self._config_manager.get_nav_indicator_size()
        indicator_height = indicator_size["height"]
        indicator_top = self._config_manager.calc_nav_indicator_top()
        accent = theme_colors.get("accent", "#0078D4")
        
        for i, name in enumerate(interface_names):
            card_names = self._config_manager.get_card_names(name)
            if card_names:
                first_card = card_names[0]
                card_info = self._config_manager.get_card_info(name, first_card)
                icon_name = card_info.get("icon", "HOME")
            else:
                icon_name = "HOME"
            
            icon_attr = getattr(ft.Icons, icon_name.upper(), ft.Icons.HOME)
            label = name.replace("界面", "")
            
            if preserve_interface:
                is_selected = (name == preserve_interface)
            else:
                is_selected = (i == 0)
            
            nav_top = i * (item_height + item_spacing)
            self._nav_item_positions[name] = nav_top
            
            nav_item = self._build_nav_item(
                icon_attr, 
                label, 
                selected=is_selected,
                on_click=lambda e, n=name: self._on_nav_item_click(n)
            )
            nav_items_list.append(nav_item)
            self._nav_items[name] = nav_item  # type: ignore
        
        self._nav_indicator = ft.Container(
            width=indicator_size["width"],
            height=indicator_height,
            bgcolor=accent,
            border_radius=2,
            top=self._nav_item_positions.get(interface_names[0], 0) + indicator_top,
            left=0,
            animate=250,
        )
        
        nav_items_column = ft.Column(nav_items_list, spacing=item_spacing, scroll=ft.ScrollMode.AUTO)
        
        nav_stack = ft.Stack([
            nav_items_column,
            self._nav_indicator,
        ], expand=True)
        
        nav_column_content = ft.Column([
            user_info_card,
            ft.Container(height=8),
            nav_stack,
        ], spacing=0, expand=True)
        
        nav_padding = self._config_manager.get_ui_size("边距", "界面内边距")
        nav_width = self._config_manager.get_ui_config("导航", "宽度") or 200
        
        nav_container = ft.Container(
            content=nav_column_content,
            padding=nav_padding,
            width=nav_width,
        )
        
        divider = ft.Container(
            content=ft.VerticalDivider(width=1),
            padding=ft.Padding(0, nav_padding, 0, nav_padding),
        )
        
        self._content_area = ft.Container(
            content=ft.Container(),
            expand=True,
            alignment=ft.Alignment(-1, -1),
            clip_behavior=ft.ClipBehavior.NONE,
        )
        
        main_content = ft.Row([
            nav_container,
            divider,
            self._content_area,
        ], expand=True, spacing=0)
        
        main_column = ft.Column([
            title_bar,
            main_content,
        ], expand=True, spacing=0)
        
        self._main_column = main_column
        
        self._page.add(main_column)
        
        target_interface = preserve_interface if preserve_interface else (interface_names[0] if interface_names else None)
        if target_interface:
            self._switch_interface(target_interface)
            if target_interface in self._nav_item_positions:
                self._move_indicator(target_interface)
    
    def _on_config_change(self, key: str, value: Any):
        """配置变更回调"""
        if key in ["theme", "accent"]:
            self._rebuild_ui()
    
    def _rebuild_ui(self):
        """重建整个UI（主题/强调色变更时调用）"""
        current_interface = self._current_interface
        
        Dropdown.cleanup_page_overlay(self._page)
        Dropdown.destroy_all_instances()
        
        for interface in self._interfaces.values():
            if hasattr(interface, 'destroy'):
                interface.destroy()
        self._interfaces.clear()
        self._current_interface = None
        
        if self._main_column:
            self._page.remove(self._main_column)
        
        self._setup_page()
        self._build_ui(preserve_interface=current_interface)
    
    def _on_nav_item_click(self, interface_name: str):
        """导航项点击回调"""
        if interface_name == self._current_interface:
            return
        
        Dropdown.cleanup_page_overlay(self._page)
        
        if self._current_interface:
            Dropdown.destroy_interface_instances(self._current_interface)
        
        for name, item in self._nav_items.items():
            is_selected = (name == interface_name)
            self._update_nav_item_selection(item, is_selected)
        
        self._move_indicator(interface_name)
        
        self._switch_interface(interface_name)
    
    def _move_indicator(self, interface_name: str):
        """移动导航指示条到目标位置"""
        if interface_name in self._nav_item_positions:
            indicator_top = self._config_manager.calc_nav_indicator_top()
            target_top = self._nav_item_positions[interface_name] + indicator_top
            if self._nav_indicator:
                self._nav_indicator.top = target_top
                self._nav_indicator.update()
    
    def _update_nav_item_selection(self, nav_item: ft.Container, selected: bool):
        """更新导航项选中状态 - Win11风格
        
        状态变化：
        - 选中：bg_selected背景，accent图标，text_primary文字
        - 未选中：transparent背景，text_secondary图标/文字
        """
        theme_colors = self._config_manager.get_theme_colors()
        
        accent = theme_colors.get("accent", "#0078D4")
        text_primary = theme_colors.get("text_primary", "#FFFFFF")
        text_secondary = theme_colors.get("text_secondary", "#B0B0B0")
        bg_selected = theme_colors.get("bg_selected", "#3A3A3A")
        
        icon_color = accent if selected else text_secondary
        label_color = text_primary if selected else text_secondary
        bgcolor = bg_selected if selected else "transparent"
        
        nav_item._icon_control.color = icon_color  # type: ignore
        nav_item._label_control.color = label_color  # type: ignore
        nav_item._content_container.bgcolor = bgcolor  # type: ignore
        nav_item._selected = selected  # type: ignore
        
        nav_item._content_container.update()  # type: ignore
    
    def _on_scheme_change(self, scheme_name: str):
        """方案切换回调（由界面容器调用）
        
        方案切换时需要：
        1. 清理所有下拉框实例
        2. 清空界面缓存
        3. 重新创建当前界面
        """
        Dropdown.cleanup_page_overlay(self._page)
        Dropdown.destroy_all_instances()
        
        current = self._current_interface
        self._interfaces.clear()
        self._current_interface = None
        
        if current:
            self._switch_interface(current)
    
    def _switch_interface(self, interface_name: str):
        """切换界面（缓存模式）
        
        缓存逻辑：
        1. 检查界面是否已缓存，如果已缓存则直接使用
        2. 如果未缓存，创建新界面实例并缓存
        3. 切换界面时，只销毁下拉框实例，不销毁界面实例
        
        性能优化：
        - 避免重复创建界面实例
        - 界面状态由ConfigManager管理，缓存安全
        - 主题切换时清空缓存（通过_rebuild_ui）
        - 方案切换时清空缓存（通过_on_scheme_change）
        """
        if interface_name == self._current_interface:
            return
        
        if interface_name in self._interfaces:
            interface = self._interfaces[interface_name]
        else:
            interface_map = {
                "系统界面": SystemInterface,
                "策略界面": StrategyInterface,
                "任务界面": TaskInterface,
                "建筑界面": BuildingInterface,
                "集资界面": FundraiseInterface,
                "账号界面": AccountInterface,
                "打扫界面": CleanInterface,
                "打野界面": HuntInterface,
                "个性化界面": PersonalizationInterface,
                "注册界面": RegisterInterface,
                "关于界面": AboutInterface,
            }
            
            interface_class = interface_map.get(interface_name)
            if interface_class:
                interface = interface_class(self._page, self._config_manager, self._on_scheme_change)
                self._interfaces[interface_name] = interface
            else:
                return
        
        self._current_interface = interface_name
        
        content = interface.build()
        self._content_area.content = content
        self._page.update()
    
    def destroy(self):
        """销毁主入口"""
        for interface in self._interfaces.values():
            if hasattr(interface, 'destroy'):
                interface.destroy()
        
        self._config_manager.clear_cache()
        self._interfaces.clear()


def main(page: ft.Page):
    """主函数"""
    MainEntry(page)


if __name__ == "__main__":
    ft.run(main)
