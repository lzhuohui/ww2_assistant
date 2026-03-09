# -*- coding: utf-8 -*-
"""
自定义下拉框 - 组件层（懒加载版本）

设计思路：
- 懒加载：初始只显示文本+箭头，不创建选项
- 点击时：动态创建选项并弹出
- 全局管理：点击新下拉框时销毁旧选项，保持内存最低
- 交互：点击选项后更新文本显示，触发on_change回调

功能：
- 支持自定义宽度和高度
- 菜单宽度与按钮宽度一致
- 支持滚动选择
- 选中后自动关闭
- 懒加载优化性能
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
import flet as ft
from typing import Callable, List, Optional
from 原子层.界面配置 import 界面配置

# *** 用户指定变量 - AI不得修改 ***
DEFAULT_WIDTH = 120        # 下拉框默认宽度
DEFAULT_HEIGHT = 32        # 下拉框默认高度
DEFAULT_FONT_SIZE = 14     # 默认字体大小
PADDING_LEFT = 12          # 左内边距
PADDING_RIGHT_BUTTON = 8   # 按钮右内边距（留空间给下拉图标）
PADDING_RIGHT_MENU = 12    # 菜单项右内边距
MAX_MENU_HEIGHT = 300      # 菜单最大高度（超过此高度启用滚动）
# *********************************


class DropdownManager:
    """下拉框全局管理器 - 管理当前激活的下拉框选项"""
    
    _current_menu: Optional[ft.Container] = None
    _current_dropdown: Optional['CustomDropDown'] = None
    
    @classmethod
    def close_current_menu(cls):
        """关闭当前激活的下拉菜单"""
        if cls._current_dropdown is not None:
            try:
                cls._current_dropdown._close_menu()
            except:
                pass
        cls._current_menu = None
        cls._current_dropdown = None
    
    @classmethod
    def register_dropdown(cls, dropdown: 'CustomDropDown'):
        """注册新的下拉框"""
        if cls._current_dropdown is not None and cls._current_dropdown != dropdown:
            cls.close_current_menu()
        cls._current_dropdown = dropdown


class CustomDropDown:  # 自定义下拉框组件（懒加载版本）
    
    def __init__(
        self,
        config: 界面配置,
        options: List[str] = None,
        value: str = None,
        width: int = DEFAULT_WIDTH,
        height: int = DEFAULT_HEIGHT,
        on_change: Optional[Callable[[str], None]] = None,
    ):
        self._config = config
        self._options = options or ["选项A", "选项B", "选项C"]
        self._current_value = value if value else (self._options[0] if self._options else "")
        self._width = width
        self._height = height
        self._on_change = on_change
        self._menu_visible = False
        self._menu_created = False
        
        theme_colors = config.当前主题颜色
        self._bg_color = theme_colors.get("bg_secondary")
        self._border_color = theme_colors.get("border")
        self._text_color = theme_colors.get("text_primary")
        self._card_color = theme_colors.get("bg_card")
        self._hover_color = theme_colors.get("bg_hover")
        
        self._selected_text = ft.Text(
            self._current_value,
            size=DEFAULT_FONT_SIZE,
            color=self._text_color,
            overflow=ft.TextOverflow.ELLIPSIS,
        )
        
        self._dropdown_icon = ft.Icon(
            ft.Icons.KEYBOARD_ARROW_DOWN,
            size=18,
            color=self._text_color,
        )
        
        self._button_container = ft.Container(
            content=ft.Row(
                [
                    self._selected_text,
                    self._dropdown_icon,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=width,
            height=height,
            border_radius=config.获取尺寸("界面", "border_radius") or 6,
            bgcolor=self._bg_color,
            border=ft.Border.all(1, self._border_color),
            padding=ft.Padding(left=PADDING_LEFT, right=PADDING_RIGHT_BUTTON, top=0, bottom=0),
            alignment=ft.Alignment(-1.0, 0.0),
            on_click=self._toggle_menu,
            ink=True,
        )
        
        menu_height = min(len(self._options) * height, MAX_MENU_HEIGHT)
        
        self._menu_container = ft.Container(
            content=None,
            width=width,
            height=menu_height,
            bgcolor=self._card_color,
            border_radius=config.获取尺寸("界面", "border_radius") or 6,
            visible=False,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=4,
                color=theme_colors.get("shadow", "#00000040"),
            ),
            border=ft.Border.all(1, self._border_color),
            top=height + 2,
            left=0,
        )
        
        self._stack = ft.Stack(
            [
                self._button_container,
                self._menu_container,
            ],
            width=width,
            height=height,
            clip_behavior=ft.ClipBehavior.NONE,
        )
    
    def _create_menu_items(self):  # 懒加载：动态创建菜单项
        if self._menu_created:
            return
        
        menu_items = []
        for option in self._options:
            item = ft.Container(
                content=ft.Text(option, size=DEFAULT_FONT_SIZE, color=self._text_color),
                width=self._width,
                height=self._height,
                padding=ft.Padding(left=PADDING_LEFT, right=PADDING_RIGHT_MENU, top=0, bottom=0),
                alignment=ft.Alignment(-1.0, 0.0),
                bgcolor=self._card_color,
                on_click=lambda e, o=option: self._select_option(o),
                on_hover=self._on_item_hover,
            )
            menu_items.append(item)
        
        menu_height = min(len(self._options) * self._height, MAX_MENU_HEIGHT)
        
        self._menu_container.content = ft.Column(
            menu_items,
            scroll=ft.ScrollMode.AUTO if len(self._options) * self._height > MAX_MENU_HEIGHT else None,
            spacing=0,
        )
        self._menu_container.height = menu_height
        self._menu_created = True
    
    def _toggle_menu(self, e):  # 切换菜单显示
        DropdownManager.register_dropdown(self)
        
        if self._menu_visible:
            self._close_menu()
        else:
            self._open_menu()
    
    def _open_menu(self):  # 打开菜单
        self._create_menu_items()  # 懒加载：打开时才创建菜单项
        self._menu_visible = True
        self._menu_container.visible = True
        self._dropdown_icon.rotate = ft.Rotate(0.5)
        self._stack.update()
    
    def _close_menu(self):  # 关闭菜单
        self._menu_visible = False
        self._menu_container.visible = False
        self._dropdown_icon.rotate = ft.Rotate(0)
        self._stack.update()
    
    def _select_option(self, option_value):  # 选择选项
        self._current_value = option_value
        self._selected_text.value = option_value
        self._close_menu()
        if self._on_change:
            self._on_change(option_value)
    
    def _on_item_hover(self, e):  # 菜单项悬停效果
        if e.data == "true":
            e.control.bgcolor = self._hover_color
        else:
            e.control.bgcolor = self._card_color
        e.control.update()
    
    def create(self):
        return self._stack


if __name__ == "__main__":
    config = 界面配置()
    
    def main(page: ft.Page):
        page.padding = 20
        page.bgcolor = config.当前主题颜色["bg_primary"]
        
        level_options = [f"{i:02d}" for i in range(1, 41)]
        
        page.add(ft.Text("下拉框测试（懒加载版本，01-40选项）", color=config.获取颜色("text_primary")))
        page.add(ft.Divider(height=20, color="transparent"))
        page.add(ft.Text("宽度70px:", color=config.获取颜色("text_secondary")))
        page.add(CustomDropDown(config=config, width=70, options=level_options, value="17").create())
        page.add(ft.Divider(height=20, color="transparent"))
        page.add(ft.Text("默认宽度120px:", color=config.获取颜色("text_secondary")))
        page.add(CustomDropDown(config=config, options=level_options, value="25").create())
    
    ft.run(main)


# 兼容性别名
下拉框 = CustomDropDown
自定义下拉框 = CustomDropDown
