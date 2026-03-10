# -*- coding: utf-8 -*-
"""
主题设置卡片 - 组件层（新思路）

设计思路:
    组装零件，构建主题设置卡片。
    采用装配模式，协调各零件交互。
    使用通用卡片组件，保持统一风格。

功能:
    1. 调用通用卡片组件
    2. 显示主题预览效果
    3. 点击切换主题

数据来源:
    所有配置数据从配置目录获取。

使用场景:
    被页面层模块调用。

可独立运行调试: python 主题设置卡片.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft
from typing import Callable, List, Dict, Any
from 配置.界面配置 import 界面配置
from 新思路.组件层.通用卡片 import UniversalCard


# *** 用户指定变量 - AI不得修改 ***
# (用户指定的变量放在这里，用户没有指定之前就空着)
# *********************************


class ThemeSettingsCard:
    """主题设置卡片 - 组件层"""
    
    @staticmethod
    def create(
        config: 界面配置,
        title: str = "主题设置",
        icon: str = "PALETTE",
        enabled: bool = True,
        on_state_change: Callable[[bool], None] = None,
        help_text: str = None,
        on_theme_change: Callable[[str], None] = None,
        **kwargs
    ) -> ft.Container:
        """
        创建主题设置卡片
        
        参数:
            config: 界面配置对象
            title: 卡片标题
            icon: 图标名称
            enabled: 初始启用状态
            on_state_change: 状态变化回调
            help_text: 帮助提示文字
            on_theme_change: 主题变化回调
        
        返回:
            ft.Container: 主题设置卡片容器
        """
        theme_colors = config.当前主题颜色
        current_theme = config.主题名称
        
        # 主题颜色定义
        themes = {
            "浅色": {
                "bg": "#FFFFFF",
                "panel": "#F3F3F3",
                "text": "#1A1A1A",
                "accent": "#0078D4",
            },
            "深色": {
                "bg": "#202020",
                "panel": "#2D2D2D",
                "text": "#FFFFFF",
                "accent": "#60CDFF",
            },
        }
        
        # 存储主题卡片引用
        theme_cards_refs = {}
        
        def create_theme_preview(theme_name: str, is_selected: bool) -> ft.Container:
            """创建单个主题预览卡片"""
            theme = themes.get(theme_name, themes["浅色"])
            
            # 创建预览内容
            preview_content = ft.Column(
                [
                    # 模拟标题栏
                    ft.Container(
                        content=ft.Text(
                            "标题",
                            size=8,
                            color=theme["text"],
                        ),
                        bgcolor=theme["panel"],
                        padding=2,
                    ),
                    # 模拟内容区
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Container(
                                    content=ft.Text("内容行", size=6, color=theme["text"]),
                                    bgcolor=theme["panel"],
                                    padding=1,
                                ),
                                ft.Container(
                                    content=ft.Text("内容行", size=6, color=theme["text"]),
                                    bgcolor=theme["panel"],
                                    padding=1,
                                ),
                            ],
                            spacing=2,
                        ),
                        padding=2,
                    ),
                ],
                spacing=0,
            )
            
            # 创建预览卡片
            preview_card = ft.Container(
                content=preview_content,
                width=80,
                height=60,
                bgcolor=theme["bg"],
                border_radius=4,
                border=ft.Border.all(2, theme["accent"] if is_selected else "transparent"),
            )
            
            # 主题名称
            theme_label = ft.Text(
                theme_name,
                size=12,
                color=theme_colors.get("text_primary"),
            )
            
            # 选中标记
            check_icon = ft.Icon(
                ft.Icons.CHECK_CIRCLE,
                size=16,
                color=theme["accent"],
                visible=is_selected,
            )
            
            # 完整卡片
            card = ft.Container(
                content=ft.Column(
                    [
                        preview_card,
                        ft.Container(height=4),
                        ft.Row(
                            [theme_label, check_icon],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=4,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=0,
                ),
                on_click=lambda e: handle_theme_click(theme_name),
                ink=True,
                border_radius=8,
            )
            
            # 存储引用
            theme_cards_refs[theme_name] = {
                "card": card,
                "preview": preview_card,
                "check": check_icon,
            }
            
            return card
        
        def handle_theme_click(theme_name: str):
            """处理主题点击"""
            if on_theme_change:
                on_theme_change(theme_name)
        
        def update_selection(selected_theme: str):
            """更新选中状态"""
            for name, refs in theme_cards_refs.items():
                is_selected = (name == selected_theme)
                theme = themes.get(name, themes["浅色"])
                refs["preview"].border = ft.Border.all(2, theme["accent"] if is_selected else "transparent")
                refs["check"].visible = is_selected
            
            # 更新显示
            if card.page:
                card.update()
        
        # 创建主题卡片列表
        theme_names = ["浅色", "深色"]
        theme_cards = [
            create_theme_preview(name, name == current_theme)
            for name in theme_names
        ]
        
        # 创建主题选择器行
        theme_selector = ft.Row(
            theme_cards,
            alignment=ft.MainAxisAlignment.START,
            spacing=20,
        )
        
        # 调用通用卡片组件
        card = UniversalCard.create(
            config=config,
            title=title,
            icon=icon,
            enabled=enabled,
            on_state_change=on_state_change,
            help_text=help_text,
            controls=[theme_selector],
        )
        
        # 暴露控制接口
        card.update_selection = update_selection
        
        return card


# 兼容别名
主题设置卡片 = ThemeSettingsCard


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    # 1. 界面配置初始化
    配置 = 界面配置()
    
    # 2. 自动加载用户数据覆盖默认值（在界面配置.__init__中自动完成）
    
    # 3. 正常启动被测模块
    def main(page: ft.Page):
        page.padding = 20
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        
        def on_theme_change(theme_name: str):
            print(f"主题切换: {theme_name}")
        
        page.add(ThemeSettingsCard.create(配置, on_theme_change=on_theme_change))  # 只能更改此处**被测调用模块名称**
    
    ft.run(main)
