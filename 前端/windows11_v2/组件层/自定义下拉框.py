# -*- coding: utf-8 -*-
"""
自定义下拉框 - 组件层

设计思路：
- 基于 PopupMenuButton 实现
- 按钮和菜单项高度严格一致，视觉效果统一
- 用户指定变量集中管理，方便调试和维护

功能：
- 支持自定义宽度和高度
- 菜单宽度与按钮宽度一致
- 支持滚动选择
- 选中后自动关闭
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
# *********************************


class CustomDropDown:  # 自定义下拉框组件
    
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
        )
        
        # 构建菜单项（菜单宽度与按钮宽度一致，高度与按钮高度一致）
        self._menu_items = []
        for option in self._options:
            item = ft.PopupMenuItem(
                content=ft.Container(
                    content=ft.Text(option, size=DEFAULT_FONT_SIZE, color=self._text_color),
                    width=width,
                    height=height,
                    padding=ft.Padding(left=PADDING_LEFT, right=PADDING_RIGHT_MENU, top=0, bottom=0),
                    alignment=ft.Alignment(-1.0, 0.0),
                ),
                on_click=self._create_option_handler(option),
                padding=0,
                height=height,
            )
            self._menu_items.append(item)
        
        # 无选项时的提示项
        if not self._menu_items:
            self._menu_items.append(
                ft.PopupMenuItem(
                    content=ft.Container(
                        content=ft.Text("无选项", size=DEFAULT_FONT_SIZE, color="gray"),
                        width=width,
                        height=height,
                        padding=ft.Padding(left=PADDING_LEFT, right=PADDING_RIGHT_MENU, top=0, bottom=0),
                        alignment=ft.Alignment(-1.0, 0.0),
                    ),
                    padding=0,
                    height=height,
                    enabled=False,
                )
            )
        
        # 主控件（使用 size_constraints 限制菜单宽度，最小宽度为2个字符）
        min_menu_width = max(width, DEFAULT_FONT_SIZE * 2 + PADDING_LEFT + PADDING_RIGHT_MENU)
        self._control = ft.PopupMenuButton(
            content=self._button_container,
            items=self._menu_items,
            bgcolor=self._card_color,
            elevation=4,
            tooltip="",
            menu_padding=0,
            menu_position=ft.PopupMenuPosition.UNDER,
            size_constraints=ft.BoxConstraints(
                min_width=min_menu_width,
                max_width=max(width, min_menu_width),
            ),
        )
    
    def _create_option_handler(self, option_value):  # 创建选项点击处理器
        def handler(e):
            self._current_value = option_value
            self._selected_text.value = option_value
            self._button_container.update()
            if self._on_change:
                self._on_change(option_value)
        return handler
    
    def create(self):
        return self._control


if __name__ == "__main__":
    config = 界面配置()
    
    def main(page: ft.Page):
        page.padding = 20
        page.bgcolor = config.当前主题颜色["bg_primary"]
        
        level_options = [f"{i:02d}" for i in range(1, 41)]
        
        page.add(ft.Text("下拉框测试（01-40选项）", color=config.获取颜色("text_primary")))
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
