# -*- coding: utf-8 -*-
"""
帮助标签 - 零件层（新思路）

设计思路:
    独立功能模块，自带状态切换能力。
    符合"装配"模式，即插即用。

功能:
    1. 图标：问号图标
    2. 提示：点击显示帮助内容（兼容模拟器和手机）
    3. 状态切换：内置切换逻辑，通过回调通知外部
    4. 外部控制：支持外部设置状态

数据来源:
    所有配置数据从配置目录获取。

使用场景:
    被组件层模块调用，也可独立使用。

可独立运行调试: python 帮助标签.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft
from typing import Callable, Optional
from 配置.界面配置 import 界面配置


class HelpTag:
    """帮助标签 - 独立功能模块，自带状态切换"""
    
    @staticmethod
    def create(
        config: 界面配置,
        help_text: str,
        enabled: bool = True,
        icon_size: int = 14,
        on_state_change: Callable[[bool], None] = None,
        on_click: Callable = None,
        **kwargs
    ) -> Optional[ft.Container]:
        """
        创建帮助标签组件
        
        参数:
            config: 界面配置对象
            help_text: 帮助提示文字
            enabled: 初始启用状态
            icon_size: 图标大小
            on_state_change: 状态变化回调函数，参数为新状态
            on_click: 点击回调函数（可选，用于扩展）
        
        返回:
            ft.Container: 包含帮助标签的容器，具备状态切换能力
            如果help_text为空，返回None
        """
        if not help_text:
            return None
        
        theme_colors = config.当前主题颜色
        
        # 计算外框尺寸，刚好包裹问号文字
        box_size = icon_size + 4
        
        # 提示框尺寸
        tip_width = 200
        tip_padding = 12
        
        # 创建图标控件
        icon_control = ft.Icon(
            ft.Icons.HELP_OUTLINE,
            size=icon_size,
            color=theme_colors.get("text_secondary"),
        )
        
        # 创建提示框内容
        tip_content = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text(
                                "帮助",
                                size=12,
                                weight=ft.FontWeight.BOLD,
                                color=theme_colors.get("text_primary"),
                            ),
                            ft.IconButton(
                                icon=ft.Icons.CLOSE,
                                icon_size=14,
                                icon_color=theme_colors.get("text_secondary"),
                                style=ft.ButtonStyle(padding=0),
                                on_click=lambda e: hide_tip(),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Divider(height=8, color="transparent"),
                    ft.Text(
                        help_text,
                        size=12,
                        color=theme_colors.get("text_secondary"),
                    ),
                ],
                spacing=0,
            ),
            width=tip_width,
            padding=tip_padding,
            bgcolor=theme_colors.get("bg_card"),
            border_radius=8,
            border=ft.Border.all(1, theme_colors.get("border")),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=8,
                color=theme_colors.get("shadow"),
                offset=ft.Offset(0, 2),
            ),
            visible=False,
        )
        
        # 内部状态
        current_enabled = enabled
        tip_visible = False
        
        def hide_tip():
            """隐藏提示框"""
            nonlocal tip_visible
            tip_visible = False
            tip_content.visible = False
            tip_content.update()
        
        def show_tip():
            """显示提示框"""
            nonlocal tip_visible
            tip_visible = True
            tip_content.visible = True
            tip_content.update()
        
        def toggle_tip():
            """切换提示框显示状态"""
            if tip_visible:
                hide_tip()
            else:
                show_tip()
        
        def set_state(new_enabled: bool, notify: bool = True):
            """设置状态"""
            nonlocal current_enabled
            current_enabled = new_enabled
            
            container.opacity = 0.7 if current_enabled else 0.3
            container.update()
            
            if notify and on_state_change:
                on_state_change(current_enabled)
        
        def toggle_state():
            """切换状态"""
            set_state(not current_enabled)
        
        def handle_click(e):
            """处理点击事件"""
            toggle_tip()
            if on_click:
                on_click(e)
        
        # 创建图标容器
        icon_container = ft.Container(
            content=icon_control,
            width=box_size,
            height=box_size,
            on_click=handle_click,
        )
        
        # 创建主容器（包含图标和提示框）
        container = ft.Container(
            content=ft.Stack(
                [
                    icon_container,
                    ft.Container(
                        content=tip_content,
                        left=box_size + 8,
                        top=0,
                    ),
                ],
                width=box_size,
                height=box_size,
            ),
            opacity=0.7 if enabled else 0.3,
        )
        
        # 暴露控制接口
        container.set_state = set_state
        container.toggle_state = toggle_state
        container.get_state = lambda: current_enabled
        container.show_tip = show_tip
        container.hide_tip = hide_tip
        container.toggle_tip = toggle_tip
        
        return container


# 兼容别名
帮助标签 = HelpTag


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    config = 界面配置()
    
    def main(page: ft.Page):
        page.padding = 20
        page.bgcolor = config.获取颜色("bg_primary")
        
        page.add(ft.Text("帮助标签测试（点击显示/隐藏提示框）:", color=config.获取颜色("text_secondary")))
        page.add(ft.Divider(height=20, color="transparent"))
        
        def on_state_change(enabled):
            print(f"状态变化: {'启用' if enabled else '禁用'}")
        
        help_tag = HelpTag.create(
            config=config,
            help_text="这是帮助提示内容，可以显示多行文字。\n点击问号图标显示/隐藏提示框。\n点击关闭按钮或再次点击问号图标关闭提示框。",
            enabled=True,
            on_state_change=on_state_change,
        )
        
        page.add(ft.Container(
            content=help_tag,
            padding=20,
            bgcolor=config.获取颜色("bg_card"),
            border_radius=8,
        ))
        
        page.add(ft.Divider(height=20, color="transparent"))
        
        # 测试外部控制
        def external_toggle(e):
            help_tag.toggle_tip()
        
        page.add(ft.ElevatedButton("外部切换提示框", on_click=external_toggle))
    
    ft.run(main)
