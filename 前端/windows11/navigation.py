#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows 11风格 - 导航组件

创建日期: 2026-03-08
作者: AI
版本: v1.0.0

说明：Windows 11风格的导航组件，支持响应式布局
"""

import flet as ft
from windows11.styles import get_color, SPACING, BORDER_RADIUS


class NavigationItem(ft.Container):
    """导航项组件"""
    def __init__(self, text, on_click=None, active=False, is_subitem=False):
        super().__init__()
        self.text = text
        self.on_click = on_click
        self.active = active
        self.is_subitem = is_subitem
        self._build()
    
    def _build(self):
        """构建导航项"""
        padding_left = SPACING["md"] + 24 if self.is_subitem else SPACING["md"]
        
        self.content = ft.Row([
            ft.Text(
                self.text,
                color=get_color("accent") if self.active else get_color("text_primary"),
                size=14,
                weight=ft.FontWeight.BOLD if self.active else ft.FontWeight.NORMAL
            )
        ], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER)
        
        self.bgcolor = get_color("accent_light") if self.active else "transparent"
        self.padding = ft.padding.only(
            top=SPACING["sm"],
            bottom=SPACING["sm"],
            left=padding_left,
            right=SPACING["md"]
        )
        self.border_radius = BORDER_RADIUS["sm"]
        self.height = 44 if self.is_subitem else 48
        self.on_click = self.on_click
    
    def update_active(self, active):
        """更新激活状态"""
        self.active = active
        self._build()
        try:
            self.update()
        except RuntimeError:
            # 组件还没有添加到页面，暂时不更新
            pass


class NavigationGroup(ft.Column):
    """导航分组组件"""
    def __init__(self, title, items):
        super().__init__()
        self.title = title
        self.items = items
        self._build()
    
    def _build(self):
        """构建导航分组"""
        self.controls = [
            ft.Container(
                content=ft.Text(
                    self.title.upper(),
                    size=12,
                    weight=ft.FontWeight.BOLD,
                    color=get_color("text_secondary")
                ),
                padding=ft.padding.only(left=SPACING["md"])
            ),
            ft.Divider(height=SPACING["sm"], color="transparent")
        ]
        
        for item in self.items:
            self.controls.append(item)
        
        self.spacing = SPACING["xs"]


class NavigationBar(ft.Container):
    """导航栏组件"""
    def __init__(self, navigation_data, on_nav_change):
        super().__init__()
        self.navigation_data = navigation_data
        self.on_nav_change = on_nav_change
        self.active_group = None
        self.active_item = None
        self.active_subitem = None
        self.expanded_groups = set()  # 存储展开的分组
        self._build()
    
    def _build(self):
        """构建导航栏"""
        controls = [
            ft.Text(
                "设置",
                size=20,
                weight=ft.FontWeight.BOLD,
                color=get_color("text_primary")
            ),
            ft.Divider(height=SPACING["md"])
        ]
        
        # 构建分组和子项
        for group_name, group_data in self.navigation_data.items():
            # 分组标题
            is_expanded = group_name in self.expanded_groups
            group_title = ft.Container(
                content=ft.Row([
                    ft.Text(
                        group_name,
                        color=get_color("accent") if group_name == self.active_group else get_color("text_primary"),
                        size=14,
                        weight=ft.FontWeight.BOLD
                    ),
                    ft.Text(
                        "▼" if is_expanded else "▶",
                        size=12,
                        color=get_color("text_secondary")
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=ft.padding.only(left=SPACING["md"], right=SPACING["md"], top=SPACING["sm"], bottom=SPACING["sm"]),
                on_click=lambda e, group=group_name: self._on_group_click(group)
            )
            controls.append(group_title)
            
            # 子项
            if is_expanded:
                for item_data in group_data["items"]:
                    # 主项
                    is_active = item_data["id"] == self.active_item
                    main_item = ft.Container(
                        content=ft.Row([
                            ft.Text(
                                item_data["text"],
                                color=get_color("accent") if is_active else get_color("text_primary"),
                                size=14,
                                weight=ft.FontWeight.BOLD if is_active else ft.FontWeight.NORMAL
                            )
                        ]),
                        padding=ft.padding.only(left=SPACING["md"] + 24, right=SPACING["md"], top=SPACING["sm"], bottom=SPACING["sm"]),
                        bgcolor=get_color("accent_light") if is_active else "transparent",
                        border_radius=BORDER_RADIUS["sm"],
                        on_click=lambda e, data=item_data: self._on_item_click(data)
                    )
                    controls.append(main_item)
                    
                    # 子项的子项
                    if is_active and "subitems" in item_data:
                        for subitem_data in item_data["subitems"]:
                            is_subactive = subitem_data["id"] == self.active_subitem
                            subitem = ft.Container(
                                content=ft.Row([
                                    ft.Text(
                                        subitem_data["text"],
                                        color=get_color("accent") if is_subactive else get_color("text_primary"),
                                        size=13
                                    )
                                ]),
                                padding=ft.padding.only(left=SPACING["md"] + 48, right=SPACING["md"], top=SPACING["xs"], bottom=SPACING["xs"]),
                                bgcolor=get_color("accent_light") if is_subactive else "transparent",
                                border_radius=BORDER_RADIUS["sm"],
                                on_click=lambda e, data=subitem_data: self._on_subitem_click(data)
                            )
                            controls.append(subitem)
        
        self.content = ft.Column(controls, spacing=0)  # 移除滚动，避免下拉滑块
        
        self.width = 240
        self.padding = SPACING["lg"]
        self.bgcolor = get_color("bg_primary")  # 使用主背景色，确保与页面背景一致
    
    def _on_group_click(self, group_name):
        """分组点击事件"""
        print(f"[DEBUG] 分组点击事件触发: {group_name}")
        print(f"[DEBUG] 当前展开的分组: {self.expanded_groups}")
        
        # 切换分组展开状态
        if group_name in self.expanded_groups:
            self.expanded_groups.remove(group_name)
            print(f"[DEBUG] 折叠分组: {group_name}")
        else:
            self.expanded_groups.add(group_name)
            print(f"[DEBUG] 展开分组: {group_name}")
        
        print(f"[DEBUG] 更新后的展开分组: {self.expanded_groups}")
        
        # 如果点击的是当前激活的分组，则不改变激活状态
        if group_name != self.active_group:
            self.active_group = group_name
            # 激活该分组的第一个子项
            if group_name in self.navigation_data and self.navigation_data[group_name]["items"]:
                first_item = self.navigation_data[group_name]["items"][0]
                self.active_item = first_item["id"]
                self.active_subitem = None
                if self.on_nav_change:
                    self.on_nav_change(first_item)
        
        self._build()
        try:
            self.update()
            print(f"[DEBUG] 导航栏更新成功")
        except RuntimeError as e:
            # 组件还没有添加到页面，暂时不更新
            print(f"[DEBUG] 导航栏更新失败: {e}")
            pass
    
    def _on_item_click(self, item_data):
        """主项点击事件"""
        self.active_item = item_data["id"]
        self.active_subitem = None
        
        # 找到包含该item_id的分组
        for group_name, group_data in self.navigation_data.items():
            for item in group_data["items"]:
                if item["id"] == item_data["id"]:
                    self.active_group = group_name
                    # 展开该分组
                    self.expanded_groups.add(group_name)
                    break
            if self.active_group:
                break
        
        if self.on_nav_change:
            self.on_nav_change(item_data)
        
        self._build()
        try:
            self.update()
        except RuntimeError:
            # 组件还没有添加到页面，暂时不更新
            pass
    
    def _on_subitem_click(self, subitem_data):
        """子项点击事件"""
        self.active_subitem = subitem_data["id"]
        
        if self.on_nav_change:
            self.on_nav_change(subitem_data)
        
        self._build()
        try:
            self.update()
        except RuntimeError:
            # 组件还没有添加到页面，暂时不更新
            pass
    
    def set_active_item(self, item_id):
        """设置激活项"""
        self.active_item = item_id
        self.active_subitem = None
        
        # 找到包含该item_id的分组
        for group_name, group_data in self.navigation_data.items():
            for item in group_data["items"]:
                if item["id"] == item_id:
                    self.active_group = group_name
                    # 展开该分组
                    self.expanded_groups.add(group_name)
                    break
            if self.active_group:
                break
        
        self._build()
        try:
            self.update()
        except RuntimeError:
            # 组件还没有添加到页面，暂时不更新
            pass


class TopNavigationBar(ft.Container):
    """顶部导航栏组件（窄屏模式）"""
    def __init__(self, navigation_data, on_nav_change):
        super().__init__()
        self.navigation_data = navigation_data
        self.on_nav_change = on_nav_change
        self.active_group = None
        self.active_item = None
        self._build()
    
    def _build(self):
        """构建顶部导航栏"""
        tabs = []
        
        # 只显示分组标题作为标签
        for group_name, group_data in self.navigation_data.items():
            tab = ft.Tab(
                text=group_name,
                data=group_name,
                selected=group_name == self.active_group
            )
            tabs.append(tab)
        
        self.content = ft.Tabs(
            tabs=tabs,
            on_change=lambda e: self._on_tab_change(e)
        )
        
        self.padding = SPACING["md"]
        self.bgcolor = get_color("bg_secondary")
        self.border = ft.border.only(bottom=ft.BorderSide(1, get_color("border")))
    
    def _on_tab_change(self, e):
        """标签页切换事件"""
        selected_tab = e.control.tabs[e.control.selected_index]
        group_name = selected_tab.data
        self.active_group = group_name
        # 激活该分组的第一个子项
        if group_name in self.navigation_data and self.navigation_data[group_name]["items"]:
            first_item = self.navigation_data[group_name]["items"][0]
            self.active_item = first_item["id"]
            if self.on_nav_change:
                self.on_nav_change(first_item)
    
    def set_active_item(self, item_id):
        """设置激活项"""
        self.active_item = item_id
        # 找到包含该item_id的分组
        for group_name, group_data in self.navigation_data.items():
            for item in group_data["items"]:
                if item["id"] == item_id:
                    self.active_group = group_name
                    break
            if self.active_group:
                break
        self._build()
        try:
            self.update()
        except RuntimeError:
            # 组件还没有添加到页面，暂时不更新
            pass
