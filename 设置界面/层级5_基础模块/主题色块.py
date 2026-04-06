# -*- coding: utf-8 -*-

"""
模块名称：主题色块.py
模块功能：主题色块选择器组件，用于主题模式和强调色选择

职责：
- 显示色块列表
- 支持选中状态
- 点击选择回调

不负责：
- 数据存储
"""

import flet as ft
from typing import Callable, Dict, List

from 设置界面.层级0_数据管理.配置管理 import ConfigManager


class ThemeColorBlock:
    """
    主题色块选择器 - V3版本
    
    职责：
    - 显示色块列表
    - 支持选中状态
    - 点击选择回调
    """
    
    _config_manager: ConfigManager = None
    
    @classmethod
    def set_config_manager(cls, config_manager: ConfigManager):
        cls._config_manager = config_manager
    
    @staticmethod
    def _check_config_manager():
        if ThemeColorBlock._config_manager is None:
            raise RuntimeError("ThemeColorBlock模块未设置config_manager")
    
    @staticmethod
    def get_block_size() -> int:
        return 40
    
    @staticmethod
    def get_border_radius() -> int:
        return 8
    
    @staticmethod
    def get_spacing() -> int:
        ThemeColorBlock._check_config_manager()
        spacing = ThemeColorBlock._config_manager.get_ui_size("边距", "色块间距")
        if spacing is None:
            spacing = 8
        return spacing
    
    def __init__(self, page: ft.Page = None, config_manager: ConfigManager = None):
        self._page = page
        self._config_manager = config_manager or ThemeColorBlock._config_manager
    
    def create_group(
        self,
        color_list: List[Dict[str, str]],
        selected_color: str,
        on_select: Callable[[str], None],
        theme_colors: Dict[str, str] = None,
    ) -> ft.Row:
        """
        创建色块组
        
        参数：
        - color_list: 颜色列表，格式 [{"key": "dark", "name": "深色", "value": "#202020"}, ...]
        - selected_color: 当前选中的颜色值
        - on_select: 选择回调，参数为颜色值
        - theme_colors: 主题颜色
        
        返回：
        - ft.Row: 色块组
        """
        if theme_colors is None:
            theme_colors = self._config_manager.get_theme_colors()
        
        block_size = ThemeColorBlock.get_block_size()
        border_radius = ThemeColorBlock.get_border_radius()
        spacing = ThemeColorBlock.get_spacing()
        
        accent_color = theme_colors.get("accent", "#0078D4")
        
        blocks = []
        for item in color_list:
            color_value = item.get("value", "#808080")
            color_name = item.get("name", "")
            is_selected = (color_value == selected_color)
            
            def make_click_handler(v):
                def handler(e):
                    on_select(v)
                return handler
            
            inner_block = ft.Container(
                width=block_size - 6,
                height=block_size - 6,
                bgcolor=color_value,
                border_radius=border_radius,
            )
            
            block = ft.Container(
                content=inner_block,
                width=block_size,
                height=block_size,
                border_radius=border_radius + 2,
                border=ft.Border.all(3, accent_color) if is_selected else None,
                padding=3,
                tooltip=color_name,
                on_click=make_click_handler(color_value),
            )
            block._is_selected = is_selected
            
            def make_hover_handler(sel, blk):
                def handler(e):
                    self._handle_hover(e, blk, sel, accent_color, theme_colors)
                return handler
            
            block.on_hover = make_hover_handler(is_selected, block)
            blocks.append(block)
        
        return ft.Row(
            controls=blocks,
            spacing=spacing,
            alignment=ft.MainAxisAlignment.CENTER,
        )
    
    def _handle_hover(self, e, block: ft.Container, is_selected: bool, accent_color: str, theme_colors: Dict[str, str]):
        if is_selected:
            return
        if e.data == "true":
            block.border = ft.Border.all(2, accent_color)
        else:
            block.border = None
        block.update()


if __name__ == "__main__":
    from 设置界面.层级0_数据管理.配置管理 import ConfigManager
    
    def main(page: ft.Page):
        page.title = "主题色块测试"
        config_manager = ConfigManager()
        ThemeColorBlock.set_config_manager(config_manager)
        
        theme_colors = config_manager.get_theme_colors()
        page.bgcolor = theme_colors.get("bg_primary", "#202020")
        
        color_block = ThemeColorBlock(page, config_manager)
        
        def on_select(color_value):
            print(f"选中颜色: {color_value}")
        
        color_list = [
            {"key": "light", "name": "浅色", "value": "#FFFFFF"},
            {"key": "dark", "name": "深色", "value": "#202020"},
        ]
        
        group = color_block.create_group(color_list, "#202020", on_select, theme_colors)
        page.add(group)
    
    ft.run(main)
