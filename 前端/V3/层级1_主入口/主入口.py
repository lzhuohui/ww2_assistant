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
"""

import flet as ft
from typing import Dict, Any

from 前端.V3.层级0_数据管理.配置管理 import ConfigManager
from 前端.V3.层级2_功能界面.系统界面 import SystemInterface
from 前端.V3.层级2_功能界面.账号界面 import AccountInterface
from 前端.V3.层级2_功能界面.建筑界面 import BuildingInterface
from 前端.V3.层级2_功能界面.策略界面 import StrategyInterface
from 前端.V3.层级2_功能界面.任务界面 import TaskInterface
from 前端.V3.层级2_功能界面.集资界面 import FundraiseInterface
from 前端.V3.层级2_功能界面.打野界面 import HuntInterface
from 前端.V3.层级2_功能界面.打扫界面 import CleanInterface
from 前端.V3.层级4_复合模块.用户信息 import UserInfoCard
from 前端.V3.层级5_基础模块.下拉框 import Dropdown

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
    """
    
    def __init__(self, page: ft.Page):
        self._page = page
        self._config_manager = ConfigManager()
        self._interfaces: Dict[str, Any] = {}
        self._current_interface: str = None
        self._nav_indicator: ft.Container = None
        self._nav_item_positions: Dict[str, int] = {}
        
        self._init_modules()
        self._setup_page()
        self._build_ui()
    
    def _init_modules(self):
        """初始化模块配置管理（级联设置底层模块）"""
        UserInfoCard.set_config_manager(self._config_manager)
    
    def _setup_page(self):
        """设置页面基本属性"""
        theme_colors = self._config_manager.get_theme_colors()
        
        self._page.title = "二战风云 V3"
        self._page.theme_mode = ft.ThemeMode.DARK
        self._page.bgcolor = theme_colors.get("bg_primary", "#202020")
        self._page.window.width = 1200
        self._page.window.height = 540
    
    def _build_nav_item(self, icon, label: str, selected: bool = False, on_click=None) -> ft.Control:
        """构建单个导航项 - Win11风格
        
        交互状态规范：
        - 默认：transparent背景，无边框，text_secondary文字/图标
        - 悬停：bg_hover背景，无边框，text_primary文字/图标
        - 激活：bg_selected背景，text_primary文字，accent图标
        
        指示条由全局管理，不在单个导航项中
        """
        theme_colors = self._config_manager.get_theme_colors()
        
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
            animate=167,
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
    
    def _build_ui(self):
        """构建UI"""
        theme_colors = self._config_manager.get_theme_colors()
        
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
            self._nav_items[name] = nav_item
        
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
        
        self._content_area = ft.Container(
            content=ft.Container(),
            expand=True,
            alignment=ft.Alignment(-1, -1),
        )
        
        self._page.add(
            ft.Container(
                content=ft.Row(
                    [
                        nav_container,
                        ft.VerticalDivider(width=1),
                        self._content_area,
                    ],
                    expand=True,
                    spacing=0,
                ),
                expand=True,
            )
        )
        
        if interface_names:
            self._switch_interface(interface_names[0])
    
    def _on_nav_item_click(self, interface_name: str):
        """导航项点击回调"""
        if interface_name == self._current_interface:
            return
        
        old_interface = self._current_interface
        
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
        
        nav_item._icon_control.color = icon_color
        nav_item._label_control.color = label_color
        nav_item._content_container.bgcolor = bgcolor
        nav_item._selected = selected
        
        nav_item._content_container.update()
    
    def _switch_interface(self, interface_name: str):
        """切换界面（懒加载模式）
        
        懒加载逻辑：
        1. 切换界面时，销毁上一界面的所有资源
        2. 销毁所有下拉框选项数据
        3. 创建新界面实例
        4. 不缓存界面实例，每次切换都重新创建
        """
        if interface_name == self._current_interface:
            return
        
        if self._current_interface and self._current_interface in self._interfaces:
            old_interface = self._interfaces[self._current_interface]
            if hasattr(old_interface, 'destroy'):
                old_interface.destroy()
            del self._interfaces[self._current_interface]
        
        Dropdown.destroy_all_instances()
        
        interface_map = {
            "系统界面": SystemInterface,
            "策略界面": StrategyInterface,
            "任务界面": TaskInterface,
            "建筑界面": BuildingInterface,
            "集资界面": FundraiseInterface,
            "账号界面": AccountInterface,
            "打扫界面": CleanInterface,
            "打野界面": HuntInterface,
        }
        
        interface_class = interface_map.get(interface_name)
        if interface_class:
            interface = interface_class(self._page, self._config_manager)
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
