# -*- coding: utf-8 -*-
"""
模块名称：图标标题

设计思路及联动逻辑:
    所有控件自适应。
    1. 布局基准: 分割线为基准
    2. 图标布局:
       - 纵中线到分割线左侧距离 = 2个主题文字宽度
       - 下部和分割线横中线对齐
    3. 主标题布局:
       - 纵中线与图标纵中线对齐
       - 上部与图标下部对齐
    4. 副标题布局: 左下角和分割线右下角对齐

模块隔离原则:
    1. 不直接创建被调用模块的内容
    2. 不覆盖被调用模块的计算结果
    3. 用户指定变量除外
"""

import flet as ft
from typing import Callable
from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider
from 前端.用户设置界面.单元模块.分割线 import Divider
from 前端.用户设置界面.单元模块.容器图标 import ContainerIcon
from 前端.用户设置界面.单元模块.容器标题 import ContainerTitle
from 前端.用户设置界面.配置.界面配置 import 界面配置


# *** 用户指定变量 - AI不得修改, 变量值必须生效 ***
USER_TITLE_SIZE = 16  # 用户指定主标题文字大小
USER_SUBTITLE_SIZE = USER_TITLE_SIZE - 4  # 用户指定副标题文字大小
USER_ICON_SIZE = USER_TITLE_SIZE + 10  # 用户指定图标大小
# *********************************

# 默认值常量 - 供调用者获取
DEFAULT_TITLE = "测试标题"
DEFAULT_ICON = "HOME"
DEFAULT_SUBTITLE = "这是副标题"

class IconTitle:
    """图标标题 - 调用单元模块实现布局"""
    
    @staticmethod
    def create(
        title: str=DEFAULT_TITLE,
        icon: str=DEFAULT_ICON,
        enabled: bool=True,
        on_state_change: Callable[[bool], None]=None,
        on_click: Callable=None,
        subtitle: str=DEFAULT_SUBTITLE,
        divider_height: int=None,
        divider_left: int=None,
        divider: ft.Container=None
    ) -> ft.Container:
        配置 = 界面配置()
        ThemeProvider.initialize(配置)
        
        line_height = divider_height if divider_height is not None else 100
        
        theme_colors = {
            "accent": ThemeProvider.get_color("accent"),
        }
        
        icon_control = None
        if icon:
            icon_name = icon.upper()
            icon_value = getattr(ft.Icons, icon_name, ft.Icons.SETTINGS)
            icon_control = ft.Icon(
                icon_value,
                size=USER_ICON_SIZE,
                color=theme_colors["accent"],
                opacity=1.0 if enabled else 0.4,
            )
        
        # 创建标题容器
        title_container_content = ContainerTitle.create(
            title=title,
            text_size=USER_TITLE_SIZE,
            padding=3,
            enabled=enabled,
            role="h3",
        )
        title_container_width = title_container_content.width
        
        # 创建副标题容器
        subtitle_control = None
        subtitle_actual_height = 0
        subtitle_actual_width = 0
        if subtitle:
            subtitle_container_content = ContainerTitle.create(
                title=subtitle,
                text_size=USER_SUBTITLE_SIZE,
                padding=3,
                enabled=enabled,
                role="caption",
            )
            subtitle_actual_width = subtitle_container_content.width
            subtitle_actual_height = subtitle_container_content.height
            subtitle_control = subtitle_container_content
        
        if divider is None:
            divider = Divider.create(
                config=配置,
                height=line_height,
                enabled=enabled
            )
        
        stack_children = []
        
        divider_position = divider_left if divider_left is not None else 200
        
        actual_divider_width = divider.width if hasattr(divider, 'width') and divider.width is not None else 100
        actual_divider_height = divider.height if hasattr(divider, 'height') and divider.height is not None else line_height
        
        # 创建图标容器
        if icon_control:
            icon_container_content = ContainerIcon.create(
                icon=icon_control,
                icon_size=USER_ICON_SIZE,
                padding=3,
                enabled=enabled,
            )
            icon_container_width = icon_container_content.width
            icon_container_height = icon_container_content.height
        else:
            icon_container_width = 0
            icon_container_height = 0
            icon_container_content = None
        
        # 计算图标容器位置
        two_char_width = 2 * USER_TITLE_SIZE
        icon_center_x = divider_position - two_char_width
        
        icon_bottom_y = actual_divider_height / 2
        icon_top_y = icon_bottom_y - icon_container_height
        icon_left_x = icon_center_x - icon_container_width / 2
        
        # 计算标题容器位置
        title_center_x = icon_center_x
        title_left_x = title_center_x - title_container_width / 2
        title_top_y = icon_bottom_y
        
        # 添加图标容器
        if icon_container_content:
            icon_container = ft.Container(
                content=icon_container_content,
                left=icon_left_x,
                top=icon_top_y,
            )
            stack_children.append(icon_container)
        
        # 添加标题容器
        title_container = ft.Container(
            content=title_container_content,
            left=title_left_x,
            top=title_top_y,
        )
        stack_children.append(title_container)
        
        # 添加分割线
        divider_container = ft.Container(
            content=divider,
            left=divider_position,
            top=0,
        )
        stack_children.append(divider_container)
        
        # 添加副标题
        if subtitle_control:
            subtitle_container = ft.Container(
                content=subtitle_control,
                left=divider_position + actual_divider_width,
                top=actual_divider_height - subtitle_actual_height,
                width=subtitle_actual_width,
                height=subtitle_actual_height,
                alignment=ft.Alignment(-1, 1),
            )
            stack_children.append(subtitle_container)
        
        # 添加点击区域
        click_area_width = title_container_width + 20
        click_area = ft.Container(
            width=click_area_width,
            height=actual_divider_height,
        )
        stack_children.append(click_area)
        
        content_stack = ft.Stack(
            stack_children,
            height=actual_divider_height,
            clip_behavior=ft.ClipBehavior.NONE,
        )
        
        container = ft.Container(
            content=content_stack,
            height=actual_divider_height,
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
            
            if title_container_content:
                title_container_content.content.opacity = 1.0 if new_enabled else 0.4
                try:
                    title_container_content.content.update()
                except:
                    pass
            
            if divider:
                try:
                    if hasattr(divider, 'content') and divider.content:
                        if hasattr(divider.content, 'opacity'):
                            divider.content.opacity = 0.7 if new_enabled else 0.2
                            divider.content.update()
                    elif hasattr(divider, 'opacity'):
                        divider.opacity = 0.7 if new_enabled else 0.2
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
    ft.run(lambda page: page.add(IconTitle.create()))  # 只能更改此处**被测调用模块名称**
