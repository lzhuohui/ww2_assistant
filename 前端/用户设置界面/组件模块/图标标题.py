# -*- coding: utf-8 -*-
"""
模块名称：图标标题 | 层级：组件模块层
设计思路：
    调用标签文本模块实现图标标题布局。
    以分割线为基准的布局模式。
    分割线高度可外部传入，与卡片高度联动。
    除分割线外，所有控件自适应。

功能：
    1. 图标：上方
    2. 主标题：下方（调用标签文本模块）
    3. 分割线：垂直分割线（可选）
    4. 副标题：分割线左侧（可选）
    5. 状态切换：内置切换逻辑

布局规则：
    0. 全部控件边距为0
    1. 除分割线外，所有控件自适应
    2. 以分割线为基准
    3. 图标/主标题上下布置且中间对齐，交线与分割线中点水平对齐
    4. 副标题右侧和分割线左侧重合
    5. 副标题下部和主标题下部水平对齐

对外接口：
    - create(): 创建图标标题
    - set_state(): 设置状态
    - toggle_state(): 切换状态
    - get_state(): 获取状态
    - set_subtitle(): 设置副标题
"""

import flet as ft
from typing import Callable, Optional
from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider
from 前端.用户设置界面.单元模块.文本标签 import LabelText
from 前端.配置.界面配置 import 界面配置

# *** 用户指定变量 - AI不得修改 ***
DEFAULT_ICON_SIZE = 24
DEFAULT_TITLE_SIZE = 14
DEFAULT_SUBTITLE_SIZE = 12
ICON_TITLE_SPACING = 4
ICON_AREA_WIDTH = 98
DEFAULT_DIVIDER_WIDTH = 2
CONTAINER_WIDTH = 10
# *********************************


class IconTitle:
    """图标标题 - 调用标签文本模块实现布局"""
    
    @staticmethod
    def create(
        title: str,
        icon: str = None,
        enabled: bool = True,
        on_state_change: Callable[[bool], None] = None,
        on_click: Callable = None,
        subtitle: str = None,
        divider_height: int = None,
        divider_left: int = None,
        **kwargs
    ) -> ft.Container:
        """
        创建图标标题组件
        
        参数：
            title: 标题文字
            icon: 图标名称（字符串）
            enabled: 初始启用状态
            on_state_change: 状态变化回调函数
            on_click: 点击回调函数（可选）
            subtitle: 副标题（可选）
            divider_height: 分割线高度（可选）
            divider_left: 分割线左侧位置（可选）
        
        返回：
            ft.Container: 包含图标标题的容器
        """
        配置 = 界面配置()
        theme_colors = {
            "accent": ThemeProvider.get_color("accent"),
            "text_primary": ThemeProvider.get_color("text_primary"),
            "text_secondary": ThemeProvider.get_color("text_secondary"),
            "border": ThemeProvider.get_color("border"),
        }
        
        ui_config = 配置.定义尺寸.get("界面", {})
        card_padding = ui_config.get("card_padding", 16)
        
        line_height = divider_height if divider_height is not None else 100
        
        icon_control = None
        if icon:
            if isinstance(icon, str):
                icon_name = icon.upper()
                icon_value = getattr(ft.Icons, icon_name, ft.Icons.SETTINGS)
            else:
                icon_value = icon
            icon_control = ft.Icon(
                icon_value,
                size=DEFAULT_ICON_SIZE,
                color=theme_colors["accent"],
                opacity=1.0 if enabled else 0.4,
            )
        
        title_control = LabelText.create(
            text=title,
            role="primary",
            enabled=enabled,
        )
        
        subtitle_control = None
        subtitle_actual_height = 0
        if subtitle:
            subtitle_actual_height = DEFAULT_SUBTITLE_SIZE * 1.5
            subtitle_control = ft.Container(
                content=ft.Text(
                    value=subtitle,
                    color=theme_colors["text_secondary"],
                    size=DEFAULT_SUBTITLE_SIZE,
                    opacity=1.0 if enabled else 0.4,
                ),
                height=subtitle_actual_height,
                alignment=ft.Alignment(-1, 1),
            )
        
        divider = ft.Container(
            width=DEFAULT_DIVIDER_WIDTH,
            height=line_height,
            bgcolor=theme_colors["accent"],
            opacity=0.7 if enabled else 0.2,
            border_radius=ft.BorderRadius.all(1),
        )
        
        icon_height = DEFAULT_ICON_SIZE if icon_control else 0
        title_height = DEFAULT_TITLE_SIZE
        subtitle_height = subtitle_actual_height if subtitle else 0
        
        divider_width = CONTAINER_WIDTH
        
        icon_title_total_height = icon_height + (ICON_TITLE_SPACING if icon_control else 0) + title_height
        
        icon_title_center_y = line_height / 2
        
        icon_title_top = icon_title_center_y - icon_title_total_height / 2
        
        title_top = icon_title_top + icon_height + (ICON_TITLE_SPACING if icon_control else 0)
        
        subtitle_top = line_height - subtitle_height
        
        stack_children = []
        
        if divider:
            # 计算分割线垂直居中的top位置
            divider_top = (line_height - divider.height) / 2
            divider_container = ft.Container(
                content=divider,
                left=ICON_AREA_WIDTH,
                top=divider_top,
            )
            stack_children.append(divider_container)
        
        icon_title_items = [title_control]
        icon_title_column = ft.Column(
            icon_title_items,
            spacing=ICON_TITLE_SPACING,
            horizontal_alignment=ft.CrossAxisAlignment.END,
            alignment=ft.MainAxisAlignment.START,
            tight=True,
        )
        
        title_center_to_divider = 50
        title_text_width = len(title) * DEFAULT_TITLE_SIZE
        title_container_left = ICON_AREA_WIDTH - title_text_width / 2 - title_center_to_divider
        
        icon_title_container = ft.Container(
            content=icon_title_column,
            left=title_container_left,
            top=title_top,
        )
        stack_children.append(icon_title_container)
        
        if icon_control:
            icon_center_to_divider = 50
            icon_left = ICON_AREA_WIDTH - DEFAULT_ICON_SIZE / 2 - icon_center_to_divider
            icon_top = title_top - DEFAULT_ICON_SIZE - ICON_TITLE_SPACING
            icon_container = ft.Container(
                content=icon_control,
                left=icon_left,
                top=icon_top,
            )
            stack_children.append(icon_container)
        
        if subtitle_control:
            subtitle_container = ft.Container(
                content=subtitle_control,
                left=ICON_AREA_WIDTH + divider_width + divider_width,
                top=subtitle_top,
            )
            stack_children.append(subtitle_container)
        
        subtitle_width = 100 if subtitle else 0
        overall_width = ICON_AREA_WIDTH + divider_width + divider_width + subtitle_width
        
        click_area = ft.Container(
            width=ICON_AREA_WIDTH,
            height=line_height,
        )
        stack_children.append(click_area)
        
        content_stack = ft.Stack(
            stack_children,
            width=overall_width,
            height=line_height,
            clip_behavior=ft.ClipBehavior.NONE,
        )
        
        container = ft.Container(
            content=content_stack,
            height=line_height,
            width=overall_width,
            alignment=ft.Alignment(-1, -1),
        )
        
        container._enabled = enabled
        
        def set_state(new_enabled: bool, notify: bool = True):
            container._enabled = new_enabled
            
            if icon_control:
                icon_control.opacity = 1.0 if new_enabled else 0.4
                try:
                    icon_control.update()
                except:
                    pass
            
            if title_control:
                title_control.opacity = 1.0 if new_enabled else 0.4
                try:
                    title_control.update()
                except:
                    pass
            
            if divider:
                divider.opacity = 0.7 if new_enabled else 0.2
                try:
                    divider.update()
                except:
                    pass
            
            if subtitle_control:
                subtitle_control.content.opacity = 1.0 if new_enabled else 0.4
                try:
                    subtitle_control.update()
                except:
                    pass
            
            if notify and on_state_change:
                on_state_change(new_enabled)
        
        def toggle_state(e=None):
            set_state(not container._enabled)
        
        def handle_click(e):
            toggle_state()
            if on_click:
                on_click(e)
        
        def get_state() -> bool:
            return container._enabled
        
        def set_subtitle(new_text: str):
            if subtitle_control:
                subtitle_control.content.value = new_text
                try:
                    subtitle_control.update()
                except:
                    pass
        
        click_area.on_click = handle_click
        container.set_state = set_state
        container.toggle_state = toggle_state
        container.get_state = get_state
        container.set_subtitle = set_subtitle
        
        return container


# *** 调试逻辑 ***
if __name__ == "__main__":
    配置 = 界面配置()
    from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider
    ThemeProvider.initialize(配置)
    def main(page: ft.Page):
        page.add(IconTitle.create(title="测试标题", icon="HOME", subtitle="这是副标题"))
    ft.run(main)
