# -*- coding: utf-8 -*-
"""
控件构建器 - 核心接口

设计思路:
    提供统一的控件创建接口，负责根据主题和配置创建各种Flet控件。

功能:
    1. 文本控件：创建文本标签
    2. 按钮控件：创建各种按钮
    3. 输入控件：创建输入框
    4. 容器控件：创建各种容器
    5. 其他控件：创建其他常用控件

数据来源:
    控件样式从主题提供者获取。

使用场景:
    被界面层、组件层、单元层调用，用于创建统一风格的控件。

可独立运行调试: python 控件构建器.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft
from typing import Callable, Optional, List, Dict, Any

from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider


class ControlBuilder:
    """控件构建器 - 核心接口"""
    
    _instance = None
    
    def __new__(cls):
        """单例模式"""
        if cls._instance is None:
            cls._instance = super(ControlBuilder, cls).__new__(cls)
        return cls._instance
    
    @classmethod
    def create_text(cls, text: str, size: str = "md", color: str = "text_primary", weight: str = "normal", **kwargs) -> ft.Text:
        """
        创建文本控件
        
        参数:
            text: 文本内容
            size: 字体大小 (sm, md, lg)
            color: 文本颜色
            weight: 字体粗细
            **kwargs: 其他参数
        
        返回:
            ft.Text: 文本控件
        """
        font_size_map = {
            "sm": ThemeProvider.get_size("字体", "font_size_sm"),
            "md": ThemeProvider.get_size("字体", "font_size_md"),
            "lg": ThemeProvider.get_size("字体", "font_size_lg"),
        }
        
        weight_map = {
            "normal": ft.FontWeight.NORMAL,
            "bold": ft.FontWeight.BOLD,
            "light": ft.FontWeight.W_300,
        }
        
        return ft.Text(
            value=text,
            size=font_size_map.get(size, font_size_map["md"]),
            color=ThemeProvider.get_color(color),
            weight=weight_map.get(weight, weight_map["normal"]),
            **kwargs
        )
    
    @classmethod
    def create_button(cls, text: str, on_click: Callable = None, variant: str = "filled", size: str = "md", **kwargs) -> ft.Button:
        """
        创建按钮控件
        
        参数:
            text: 按钮文本
            on_click: 点击事件处理函数
            variant: 按钮变体 (filled, outlined, text)
            size: 按钮大小 (sm, md, lg)
            **kwargs: 其他参数
        
        返回:
            ft.Button: 按钮控件
        """
        size_map = {
            "sm": {
                "height": 32,
            },
            "md": {
                "height": 40,
            },
            "lg": {
                "height": 48,
            },
        }
        
        button = ft.Button(
            content=ft.Text(text),
            on_click=on_click,
            height=size_map.get(size, size_map["md"])["height"],
            style=ft.ButtonStyle(
                bgcolor=ThemeProvider.get_color("primary"),
                color=ThemeProvider.get_color("text_on_primary"),
                shape=ft.RoundedRectangleBorder(
                    radius=ThemeProvider.get_size("圆角", "radius_md")
                ),
            ),
            **kwargs
        )
        
        if variant == "outlined":
            button = ft.Button(
                content=ft.Text(text),
                on_click=on_click,
                height=size_map.get(size, size_map["md"])["height"],
                style=ft.ButtonStyle(
                    border=ft.BorderSide(
                        width=1,
                        color=ThemeProvider.get_color("primary")
                    ),
                    color=ThemeProvider.get_color("primary"),
                    shape=ft.RoundedRectangleBorder(
                        radius=ThemeProvider.get_size("圆角", "radius_md")
                    ),
                ),
                **kwargs
            )
        elif variant == "text":
            button = ft.Button(
                content=ft.Text(text),
                on_click=on_click,
                height=size_map.get(size, size_map["md"])["height"],
                style=ft.ButtonStyle(
                    color=ThemeProvider.get_color("primary"),
                ),
                **kwargs
            )
        
        return button
    
    @classmethod
    def create_input(cls, label: str, value: str = "", on_change: Callable = None, password: bool = False, **kwargs) -> ft.TextField:
        """
        创建输入框控件
        
        参数:
            label: 输入框标签
            value: 默认值
            on_change: 值变化事件处理函数
            password: 是否为密码输入
            **kwargs: 其他参数
        
        返回:
            ft.TextField: 输入框控件
        """
        return ft.TextField(
            label=label,
            value=value,
            on_change=on_change,
            password=password,
            can_reveal_password=password,
            border_color=ThemeProvider.get_color("border"),
            focused_border_color=ThemeProvider.get_color("primary"),
            label_style=ft.TextStyle(
                color=ThemeProvider.get_color("text_secondary")
            ),
            **kwargs
        )
    
    @classmethod
    def create_container(cls, content: ft.Control = None, padding: Optional[ft.Padding] = None, margin: Optional[ft.Margin] = None, bgcolor: str = "bg_primary", **kwargs) -> ft.Container:
        """
        创建容器控件
        
        参数:
            content: 容器内容
            padding: 内边距
            margin: 外边距
            bgcolor: 背景颜色
            **kwargs: 其他参数
        
        返回:
            ft.Container: 容器控件
        """
        return ft.Container(
            content=content,
            padding=padding,
            margin=margin,
            bgcolor=ThemeProvider.get_color(bgcolor),
            **kwargs
        )
    
    @classmethod
    def create_card(cls, content: ft.Control = None, padding: ft.Padding = ft.Padding.all(16), **kwargs) -> ft.Card:
        """
        创建卡片控件
        
        参数:
            content: 卡片内容
            padding: 内边距
            **kwargs: 其他参数
        
        返回:
            ft.Card: 卡片控件
        """
        return ft.Card(
            content=ft.Container(
                content=content,
                padding=padding,
            ),
            elevation=2,
            **kwargs
        )
    
    @classmethod
    def create_row(cls, controls: List[ft.Control] = None, spacing: int = None, **kwargs) -> ft.Row:
        """
        创建行容器控件
        
        参数:
            controls: 子控件列表
            spacing: 控件间距
            **kwargs: 其他参数
        
        返回:
            ft.Row: 行容器控件
        """
        if spacing is None:
            spacing = ThemeProvider.get_size("间距", "spacing_md")
        
        return ft.Row(
            controls=controls or [],
            spacing=spacing,
            **kwargs
        )
    
    @classmethod
    def create_column(cls, controls: List[ft.Control] = None, spacing: int = None, **kwargs) -> ft.Column:
        """
        创建列容器控件
        
        参数:
            controls: 子控件列表
            spacing: 控件间距
            **kwargs: 其他参数
        
        返回:
            ft.Column: 列容器控件
        """
        if spacing is None:
            spacing = ThemeProvider.get_size("间距", "spacing_md")
        
        return ft.Column(
            controls=controls or [],
            spacing=spacing,
            **kwargs
        )
    
    @classmethod
    def create_icon(cls, icon: str, size: int = None, color: str = "text_primary", **kwargs) -> ft.Icon:
        """
        创建图标控件
        
        参数:
            icon: 图标名称
            size: 图标大小
            color: 图标颜色
            **kwargs: 其他参数
        
        返回:
            ft.Icon: 图标控件
        """
        if size is None:
            size = ThemeProvider.get_size("图标", "icon_size_md")
        
        return ft.Icon(
            icon=icon,
            size=size,
            color=ThemeProvider.get_color(color),
            **kwargs
        )


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    from 前端.用户设置界面.配置.界面配置 import 界面配置
    
    # 1. 初始化主题提供者
    配置 = 界面配置()
    ThemeProvider.initialize(配置)
    
    # 2. 测试创建文本控件
    print("=== 测试创建文本控件 ===")
    text = ControlBuilder.create_text("测试文本", size="lg", color="text_primary", weight="bold")
    print(f"创建的文本控件: {text}")
    
    # 3. 测试创建按钮控件
    print("\n=== 测试创建按钮控件 ===")
    def on_click(e):
        print("按钮被点击")
    
    button = ControlBuilder.create_button("测试按钮", on_click=on_click)
    print(f"创建的按钮控件: {button}")
    
    # 4. 测试创建输入框控件
    print("\n=== 测试创建输入框控件 ===")
    input_field = ControlBuilder.create_input("测试输入", value="默认值")
    print(f"创建的输入框控件: {input_field}")
    
    # 5. 测试创建容器控件
    print("\n=== 测试创建容器控件 ===")
    container = ControlBuilder.create_container(
        content=ControlBuilder.create_text("容器内容"),
        padding=ft.Padding.all(16),
        margin=ft.Margin.all(8)
    )
    print(f"创建的容器控件: {container}")
    
    # 6. 测试创建卡片控件
    print("\n=== 测试创建卡片控件 ===")
    card = ControlBuilder.create_card(
        content=ControlBuilder.create_text("卡片内容")
    )
    print(f"创建的卡片控件: {card}")
    
    # 7. 测试创建行容器控件
    print("\n=== 测试创建行容器控件 ===")
    row = ControlBuilder.create_row(
        controls=[
            ControlBuilder.create_text("文本1"),
            ControlBuilder.create_button("按钮1")
        ]
    )
    print(f"创建的行容器控件: {row}")
    
    # 8. 测试创建列容器控件
    print("\n=== 测试创建列容器控件 ===")
    column = ControlBuilder.create_column(
        controls=[
            ControlBuilder.create_text("文本1"),
            ControlBuilder.create_text("文本2")
        ]
    )
    print(f"创建的列容器控件: {column}")
    
    # 9. 测试创建图标控件
    print("\n=== 测试创建图标控件 ===")
    icon = ControlBuilder.create_icon("settings", size=24, color="primary")
    print(f"创建的图标控件: {icon}")