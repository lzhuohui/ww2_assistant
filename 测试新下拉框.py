# -*- coding: utf-8 -*-
"""
自定义下拉框v2 - 零件层（原始增强版）

基于原始 LazyDropDown 实现，增加悬浮菜单和点击外部关闭功能。
坐标获取失败时使用可调估算参数，确保菜单在按钮附近显示。

功能:
    1. 懒加载：第一次展开时才创建选项列表
    2. 精准销毁：点击下一个下拉框时，销毁上一个下拉框的选项
    3. 延迟保存：点到下一个下拉框时，保存上一个下拉框的值
    4. 显示默认值：创建按钮时显示默认值，界面美观
    5. 悬浮菜单：菜单通过 overlay 添加，不挤压下方控件
    6. 点击外部关闭：透明背景层捕获点击事件
    7. 完整接口：get_value, set_value, set_enabled, set_state
"""

import sys
import asyncio
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft
from typing import Callable, List, Optional

# ==================== 可调参数（当无法获取坐标时使用） ====================
ESTIMATE_LEFT = 20          # 菜单左边缘与页面左边缘的距离（像素），通常等于 page.padding
ESTIMATE_START_Y = 80       # 第一个下拉框按钮左下角的估算纵坐标
ESTIMATE_STEP_Y = 50        # 相邻下拉框纵坐标的增量
# ========================================================================

DEFAULT_WIDTH = 120
DEFAULT_HEIGHT = 32


class DropdownManager:
    """下拉框管理器（全局）"""
    last_dropdown = None

    @classmethod
    def open_dropdown(cls, dropdown):
        if cls.last_dropdown and cls.last_dropdown != dropdown:
            if cls.last_dropdown.on_change:
                cls.last_dropdown.on_change(cls.last_dropdown.current_value)
            cls.last_dropdown.destroy_options()
        if not dropdown.options_created:
            dropdown.create_options()
        cls.last_dropdown = dropdown

    @classmethod
    def close_all(cls):
        if cls.last_dropdown:
            cls.last_dropdown.destroy_options()
            cls.last_dropdown = None


class LazyDropDown:
    """自定义下拉框（懒加载版本）"""

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
        index: int = 0,  # 用于估算位置的索引
    ):
        self.config = config
        self.options = options
        self.current_value = value if value else (options[0] if options else "")
        self.width = width if width is not None else DEFAULT_WIDTH
        self.height = height if height is not None else DEFAULT_HEIGHT
        self.on_change = on_change
        self.label = label or "dropdown"
        self.enabled = enabled
        self.index = index

        self.dropdown_opened = False
        self.options_created = False
        self.overlay_background = None
        self.menu_container = None

        self.create_ui()

    def create_ui(self):
        theme_colors = self.config.当前主题颜色

        self.selected_text = ft.Text(
            self.current_value,
            size=14,
            color=theme_colors.get("text_primary"),
            overflow=ft.TextOverflow.ELLIPSIS,
        )

        self.dropdown_icon = ft.Icon(
            ft.Icons.KEYBOARD_ARROW_DOWN,
            size=18,
            color=theme_colors.get("text_primary"),
        )

        self.button = ft.Container(
            content=ft.Row(
                [self.selected_text, self.dropdown_icon],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=self.width,
            height=self.height,
            border_radius=6,
            bgcolor=theme_colors.get("bg_secondary"),
            border=ft.Border.all(1, theme_colors.get("border")),
            padding=ft.Padding(left=12, right=8, top=0, bottom=0),
            alignment=ft.Alignment(-1.0, 0.0),
            ink=True,
            on_click=self.toggle_dropdown,
        )

        self.dropdown_list = ft.Column(
            controls=[],
            scroll=ft.ScrollMode.AUTO,
            height=min(200, len(self.options) * 32),
        )

        self.menu_container = ft.Container(
            content=self.dropdown_list,
            width=self.width,
            bgcolor=theme_colors.get("bg_card"),
            border_radius=6,
            border=ft.Border.all(1, theme_colors.get("border")),
            padding=ft.Padding.all(4),
            visible=True,
        )

        # 主容器只包含按钮，菜单通过 overlay 添加
        self.control = ft.Column([self.button], spacing=2, width=self.width)

    def create_options(self):
        theme_colors = self.config.当前主题颜色
        for option in self.options:
            item = ft.Container(
                content=ft.Text(
                    option,
                    size=14,
                    color=theme_colors.get("text_primary"),
                ),
                width=self.width - 8,
                height=32,
                padding=ft.Padding(left=12, right=8, top=0, bottom=0),
                alignment=ft.Alignment(-1.0, 0.0),
                on_click=lambda e, o=option: self.select_option(o),
                ink=True,
                border_radius=4,
            )
            self.dropdown_list.controls.append(item)
        self.options_created = True

    async def toggle_dropdown(self, e):
        if self.dropdown_opened:
            self.close_dropdown(e)
        else:
            DropdownManager.open_dropdown(self)
            self.dropdown_opened = True
            await self._show_menu()

    async def _show_menu(self):
        if not self.control.page:
            return

        page = self.control.page
        page.update()
        await asyncio.sleep(0.05)

        left, top = 0, 0
        position_obtained = False

        # 尝试精确获取按钮位置（兼容不同 Flet 版本）
        try:
            if hasattr(self.button, 'get_global_position'):
                pos = await self.button.get_global_position()
                if pos is not None:
                    # 如果有滚动容器，需减去滚动偏移（这里简化处理）
                    left = pos.x
                    top = pos.y + self.button.height
                    position_obtained = True
                    print(f"[{self.label}] 精确坐标: ({left:.1f}, {top:.1f})")
            elif hasattr(page, 'get_control_position'):
                pos = await page.get_control_position(self.button)
                if pos is not None:
                    left = pos.x
                    top = pos.y + self.button.height
                    position_obtained = True
                    print(f"[{self.label}] 备用坐标: ({left:.1f}, {top:.1f})")
        except Exception as ex:
            print(f"[{self.label}] 坐标获取异常: {ex}")

        if not position_obtained:
            # 使用估算位置
            left = ESTIMATE_LEFT
            top = ESTIMATE_START_Y + self.index * ESTIMATE_STEP_Y
            print(f"[{self.label}] 估算坐标: ({left:.1f}, {top:.1f}) (索引{self.index})")

        # 创建透明背景层（点击外部关闭）
        self.overlay_background = ft.Container(
            left=0, top=0,
            width=page.width, height=page.height,
            bgcolor=None,
            on_click=self.close_dropdown,
        )

        self.menu_container.left = left
        self.menu_container.top = top

        page.overlay.append(self.overlay_background)
        page.overlay.append(self.menu_container)
        page.update()

    def close_dropdown(self, e=None):
        if not self.dropdown_opened:
            return
        self.dropdown_opened = False
        self._hide_menu()

    def _hide_menu(self):
        if not self.control.page:
            return
        page = self.control.page
        if self.overlay_background in page.overlay:
            page.overlay.remove(self.overlay_background)
        if self.menu_container in page.overlay:
            page.overlay.remove(self.menu_container)
        page.update()

    def select_option(self, option: str):
        self.current_value = option
        self.selected_text.value = option
        self.selected_text.update()
        self.close_dropdown()
        if self.on_change:
            self.on_change(option)

    def destroy_options(self):
        if self.options_created:
            self.dropdown_list.controls.clear()
            self.options_created = False
            if self.dropdown_opened:
                self.close_dropdown()

    def get_value(self) -> str:
        return self.current_value

    def set_value(self, value: str):
        if value in self.options:
            self.current_value = value
            self.selected_text.value = value
            if self.selected_text.page:
                self.selected_text.update()

    def set_enabled(self, enabled: bool):
        self.button.opacity = 1.0 if enabled else 0.5
        self.button.disabled = not enabled
        if self.button.page:
            self.button.update()

    def get_enabled(self) -> bool:
        return not self.button.disabled

    def set_state(self, enabled: bool):
        self.set_enabled(enabled)

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
        index: int = 0,
    ):
        dropdown = LazyDropDown(
            config=config,
            options=options,
            value=value,
            width=width,
            height=height,
            on_change=on_change,
            label=label,
            enabled=enabled,
            index=index,
        )
        dropdown.control.get_value = dropdown.get_value
        dropdown.control.set_value = dropdown.set_value
        dropdown.control.set_enabled = dropdown.set_enabled
        dropdown.control.get_enabled = dropdown.get_enabled
        dropdown.control.set_state = dropdown.set_state
        return dropdown.control


# 兼容别名
自定义下拉框v2 = LazyDropDown


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    # 如果无法导入实际配置，请使用以下模拟配置
    try:
        from 配置.界面配置 import 界面配置
        配置 = 界面配置()
    except ImportError:
        print("使用模拟配置（请根据实际主题调整颜色）")
        class MockConfig:
            def __init__(self):
                self.当前主题颜色 = {
                    "text_primary": ft.Colors.BLACK,
                    "bg_secondary": ft.Colors.WHITE,
                    "border": ft.Colors.GREY_400,
                    "bg_card": ft.Colors.WHITE,
                }
        配置 = MockConfig()

    async def main(page: ft.Page):
        page.padding = 20
        page.bgcolor = 配置.当前主题颜色.get("bg_primary", ft.Colors.GREY_100)

        # 创建多个下拉框，传入索引以估算位置
        dropdowns = ft.Column(
            [
                ft.Text("测试下拉框（悬浮+点击外部关闭）", size=20, weight=ft.FontWeight.BOLD),
                ft.Container(height=20),
                LazyDropDown.create(
                    config=配置,
                    options=["01", "02", "03", "04", "05"],
                    value="03",
                    on_change=lambda v: print(f"下拉框1: {v}"),
                    label="DD1",
                    index=0,
                ),
                ft.Container(height=10),
                LazyDropDown.create(
                    config=配置,
                    options=["选项A", "选项B", "选项C", "选项D", "选项E"],
                    value="选项A",
                    on_change=lambda v: print(f"下拉框2: {v}"),
                    label="DD2",
                    index=1,
                ),
                ft.Container(height=10),
                LazyDropDown.create(
                    config=配置,
                    options=[f"{i:02d}" for i in range(1, 21)],
                    value="10",
                    on_change=lambda v: print(f"下拉框3: {v}"),
                    label="DD3",
                    index=2,
                ),
            ],
            scroll=ft.ScrollMode.AUTO,
        )

        page.add(dropdowns)

    ft.app(target=main)