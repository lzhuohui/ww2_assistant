# -*- coding: utf-8 -*-
"""
自定义下拉框v2 - 零件层（新思路）

设计思路:
    使用PopupMenuButton实现下拉菜单，自动处理菜单位置。

功能:
    1. 显示默认值：创建按钮时显示默认值，界面美观
    2. 自动定位：菜单自动跟随按钮位置
    3. 菜单宽度优化

数据来源:
    所有配置数据从配置目录获取。

使用场景:
    被组件层、页面层调用。

可独立运行调试: python 自定义下拉框v2.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft
from typing import Callable, List, Optional

DEFAULT_WIDTH = 100
DEFAULT_HEIGHT = 32


class CustomDropDown:
    """自定义下拉框（PopupMenuButton实现，自动定位）"""
    
    def __init__(
        self,
        config,
        options: List[str],
        value: str = None,
        width: int = None,
        height: int = None,
        on_change: Callable[[str], None] = None,
        label: str = None,
        enabled: bool = True,
    ):
        """
        初始化下拉框
        
        参数:
            config: 界面配置对象
            options: 选项列表
            value: 默认值
            width: 宽度（默认为DEFAULT_WIDTH）
            height: 高度（默认为DEFAULT_HEIGHT）
            on_change: 值变化回调
            label: 标签（可选）
            enabled: 启用状态（默认True)
        """
        self.config = config
        self.options = options
        self.current_value = value if value else (options[0] if options else "")
        self.width = width if width is not None else DEFAULT_WIDTH
        self.height = height if height is not None else DEFAULT_HEIGHT
        self.on_change = on_change
        self.label = label
        self.enabled = enabled
        
        self.create_ui()
    
    def create_ui(self):
        """创建UI"""
        theme_colors = self.config.当前主题颜色
        
        self.selected_text = ft.Text(
            self.current_value,
            size=14,
            color=theme_colors.get("text_primary"),
            overflow=ft.TextOverflow.ELLIPSIS,
        )
        
        self.button_content = ft.Row(
            [self.selected_text, ft.Icon(ft.Icons.KEYBOARD_ARROW_DOWN, size=18)],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        
        self.button_container = ft.Container(
            content=self.button_content,
            width=self.width,
            height=self.height,
            border_radius=6,
            bgcolor=theme_colors.get("bg_secondary"),
            border=ft.Border.all(1, theme_colors.get("border")),
            padding=ft.Padding(left=12, right=8, top=0, bottom=0),
        )
        
        self.menu_items = []
        for option in self.options:
            item = ft.PopupMenuItem(
                content=ft.Text(option),
                on_click=lambda e, o=option: self.select_option(o),
            )
            self.menu_items.append(item)
        
        self.popup_button = ft.PopupMenuButton(
            content=self.button_container,
            items=self.menu_items,
            disabled=not self.enabled,
            tooltip="",
            menu_padding=ft.Padding.all(0),
        )
        
        self.control = ft.Container(
            content=self.popup_button,
            width=self.width,
            height=self.height,
        )
    
    def select_option(self, option: str):
        """选择选项"""
        self.current_value = option
        self.selected_text.value = option
        if self.selected_text.page:
            self.selected_text.update()
        
        if self.on_change:
            self.on_change(option)
    
    def get_value(self) -> str:
        """获取当前值"""
        return self.current_value
    
    def set_value(self, value: str):
        """设置当前值"""
        if value in self.options:
            self.current_value = value
            self.selected_text.value = value
        if self.selected_text.page:
            self.selected_text.update()
    
    def set_enabled(self, enabled: bool):
        """设置启用状态"""
        self.popup_button.disabled = not enabled
        if self.popup_button.page:
            self.popup_button.update()
    
    def get_enabled(self) -> bool:
        """获取启用状态"""
        return not self.popup_button.disabled
    
    def set_state(self, enabled: bool):
        """设置启用状态（兼容别名）"""
        self.set_enabled(enabled)
    
    def set_options(self, options: List[str]):
        """设置选项列表"""
        self.options = options
        self.menu_items.clear()
        for option in self.options:
            item = ft.PopupMenuItem(
                content=ft.Text(option),
                on_click=lambda e, o=option: self.select_option(o),
            )
            self.menu_items.append(item)
        self.popup_button.items = self.menu_items
        if self.popup_button.page:
            self.popup_button.update()
    
    @staticmethod
    def create(
        config,
        options: List[str],
        value: str = None,
        width: int = None,
        height: int = None,
        on_change: Callable[[str], None] = None,
        label: str = None,
        enabled: bool = True,
    ):
        """
        创建下拉框
        
        参数:
            config: 界面配置对象
            options: 选项列表
            value: 默认值
            width: 宽度（默认为DEFAULT_WIDTH）
            height: 高度（默认为DEFAULT_HEIGHT）
            on_change: 值变化回调
            label: 标签（可选）
            enabled: 启用状态（默认True）
        
        返回:
            ft.Container: 下拉框控件
        """
        dropdown = CustomDropDown(
            config=config,
            options=options,
            value=value,
            width=width,
            height=height,
            on_change=on_change,
            label=label,
            enabled=enabled,
        )
        
        dropdown.control.get_value = dropdown.get_value
        dropdown.control.set_value = dropdown.set_value
        dropdown.control.set_enabled = dropdown.set_enabled
        dropdown.control.get_enabled = dropdown.get_enabled
        dropdown.control.set_state = dropdown.set_state
        
        return dropdown.control


自定义下拉框v2 = CustomDropDown


if __name__ == "__main__":
    from 配置.界面配置 import 界面配置
    配置 = 界面配置()
    
    def main(page: ft.Page):
        page.padding = 20
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        
        print("\n" + "="*60)
        print("PopupMenuButton下拉框测试")
        print("菜单自动跟随按钮位置")
        print("="*60 + "\n")
        
        dropdown1 = CustomDropDown.create(
            config=配置,
            options=["01", "02", "03", "04", "05"],
            value="03",
            on_change=lambda v: print(f"下拉框#1选择: {v}"),
        )
        dropdown2 = CustomDropDown.create(
            config=配置,
            options=["选项A", "选项B", "选项C", "选项D", "选项E"],
            value="选项A",
            on_change=lambda v: print(f"下拉框#2选择: {v}"),
        )
        dropdown3 = CustomDropDown.create(
            config=配置,
            options=[f"{i:02d}" for i in range(1, 21)],
            value="10",
            on_change=lambda v: print(f"下拉框#3选择: {v}"),
        )
        dropdown4 = CustomDropDown.create(
            config=配置,
            options=["测试X", "测试Y", "测试Z"],
            value="测试Y",
            on_change=lambda v: print(f"下拉框#4选择: {v}"),
        )
        dropdown5 = CustomDropDown.create(
            config=配置,
            options=["红", "绿", "蓝", "黄"],
            value="蓝",
            on_change=lambda v: print(f"下拉框#5选择: {v}"),
        )
        
        page.add(
            ft.Column([
                ft.Text("PopupMenuButton下拉框测试", size=20, weight=ft.FontWeight.BOLD),
                ft.Text("菜单自动跟随按钮位置", size=14),
                ft.Container(height=20),
                ft.Text("【下拉框 #1】", size=14, weight=ft.FontWeight.BOLD),
                dropdown1,
                ft.Container(height=15),
                ft.Text("【下拉框 #2】", size=14, weight=ft.FontWeight.BOLD),
                dropdown2,
                ft.Container(height=15),
                ft.Text("【下拉框 #3】", size=14, weight=ft.FontWeight.BOLD),
                dropdown3,
                ft.Container(height=15),
                ft.Text("【下拉框 #4】", size=14, weight=ft.FontWeight.BOLD),
                dropdown4,
                ft.Container(height=15),
                ft.Text("【下拉框 #5】", size=14, weight=ft.FontWeight.BOLD),
                dropdown5,
            ], scroll=ft.ScrollMode.AUTO)
        )
    
    ft.run(main)
