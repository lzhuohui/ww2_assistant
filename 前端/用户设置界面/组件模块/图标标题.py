# -*- coding: utf-8 -*-
"""
模块名称：图标标题 | 设计思路：以分割线为基准布局所有控件。图标纵中线距离分割线容器左侧指定偏移量，下部与分割线容器横中线重合；主标题纵中线与图标容器纵中线重合，上部与图标容器下部重合；副标题文字靠右，容器左下角与分割线容器右下角对齐。 | 模块隔离原则：不直接创建被调用模块的内容，不覆盖被调用模块的计算结果，用户指定变量除外
"""

import flet as ft
from typing import Callable

from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider
from 前端.用户设置界面.单元模块.分割线 import Divider, USER_CONTAINER_WIDTH, USER_CONTAINER_HEIGHT
from 前端.用户设置界面.单元模块.容器图标 import ContainerIcon
from 前端.用户设置界面.单元模块.容器标题 import ContainerTitle
from 前端.用户设置界面.配置.界面配置 import 界面配置


# *** 用户指定变量 - AI不得修改, 变量值必须生效 ***
USER_ICON_CENTER_OFFSET = 44  # 图标纵中线距离分割线容器左侧的偏移量
USER_TITLE_SIZE = 16  # 主标题文字大小
USER_SUBTITLE_SIZE = USER_TITLE_SIZE - 4  # 副标题文字大小
# *********************************


class IconTitle:
    """图标标题"""
    
    @staticmethod
    def create(
        title: str="测试标题",
        icon: str="HOME",
        enabled: bool=True,
        on_state_change: Callable[[bool], None]=None,
        on_click: Callable[[ft.ControlEvent], None]=None,
        subtitle: str="全自动:自动挂机,无需人为干预 | 半自动:点击头像,自动切换账号",
        divider_height: int=None,
        divider_left: int=100,
        divider_top: int=0
    ) -> ft.Container:
        配置 = 界面配置()
        ThemeProvider.initialize(配置)
        
        theme_colors = {
            "accent": ThemeProvider.get_color("accent"),
            "bg_card": ThemeProvider.get_color("bg_card"),
        }
        
        if divider_height is None:
            divider_height = USER_CONTAINER_HEIGHT
        
        divider = Divider.create(config=配置, height=divider_height, enabled=enabled)
        
        icon_obj = ft.Icon(
            getattr(ft.Icons, icon.upper(), ft.Icons.HOME),
            color=theme_colors.get("accent"),
            opacity=1.0 if enabled else 0.4,
        )
        icon_container_content = ContainerIcon.create(icon=icon_obj, enabled=enabled)
        
        icon_center_x = divider_left - USER_ICON_CENTER_OFFSET
        divider_center_y = divider_top + divider_height / 2
        
        icon_container_width = icon_container_content.width
        icon_container_height = icon_container_content.height
        icon_left = icon_center_x - icon_container_width / 2
        icon_bottom = divider_center_y
        icon_top = icon_bottom - icon_container_height
        
        main_title_container_content = ContainerTitle.create(
            title=title, text_size=USER_TITLE_SIZE, enabled=enabled, weight=ft.FontWeight.BOLD # 主标题文字加粗
        )
        main_title_container_width = main_title_container_content.width
        main_title_left = icon_center_x - main_title_container_width / 2
        main_title_top = icon_bottom
        
        subtitle_container_content = ContainerTitle.create(
            title=subtitle, text_size=USER_SUBTITLE_SIZE, enabled=enabled, weight=ft.FontWeight.NORMAL # 副标题文字正常加粗
        )
        subtitle_container_width = subtitle_container_content.width
        subtitle_container_height = subtitle_container_content.height
        subtitle_left = divider_left + USER_CONTAINER_WIDTH
        subtitle_top = divider_top + divider_height - subtitle_container_height
        
        divider.left = divider_left
        divider.top = divider_top
        
        icon_container_content.left = icon_left
        icon_container_content.top = icon_top
        
        main_title_container_content.left = main_title_left
        main_title_container_content.top = main_title_top
        
        subtitle_container_content.left = subtitle_left
        subtitle_container_content.top = subtitle_top
        subtitle_container_content.alignment = ft.Alignment(-1, 0.5)
        
        click_area_width = main_title_container_width + 20
        click_area = ft.Container(
            width=click_area_width,
            height=divider_height,
            bgcolor=None,
        )
        
        stack = ft.Stack(
            [
                divider,
                icon_container_content,
                main_title_container_content,
                subtitle_container_content,
                click_area,
            ],
            height=divider_height,
            clip_behavior=ft.ClipBehavior.NONE,
        )
        
        container = ft.Container(
            content=stack,
            bgcolor=None,
            padding=0,
            height=divider_height,
        )
        
        current_enabled = enabled
        
        def set_state(new_enabled: bool, notify: bool=True):
            nonlocal current_enabled
            current_enabled = new_enabled
            
            icon_obj.opacity = 1.0 if new_enabled else 0.4
            try:
                icon_obj.update()
            except:
                pass
            
            if main_title_container_content:
                main_title_container_content.content.opacity = 1.0 if new_enabled else 0.4
                try:
                    main_title_container_content.content.update()
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
            
            if subtitle_container_content:
                subtitle_container_content.content.opacity = 1.0 if new_enabled else 0.4
                try:
                    subtitle_container_content.update()
                except:
                    pass
            
            if notify and on_state_change:
                on_state_change(new_enabled)
        
        def toggle_state(e=None):
            set_state(not current_enabled)
        
        def get_state() -> bool:
            return current_enabled
        
        def set_subtitle(new_text: str):
            if subtitle_container_content:
                subtitle_container_content.content.value = new_text
                try:
                    subtitle_container_content.update()
                except:
                    pass
        
        def handle_click(e):
            toggle_state()
            if on_click:
                on_click(e)
        
        click_area.on_click = handle_click
        container.set_state = set_state
        container.toggle_state = toggle_state
        container.get_state = get_state
        container.set_subtitle = set_subtitle
        
        return container


# *** 调试逻辑 ***
if __name__ == "__main__":
    ft.run(lambda page: page.add(IconTitle.create()))
