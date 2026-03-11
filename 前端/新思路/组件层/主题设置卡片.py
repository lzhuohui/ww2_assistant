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
from 新思路.零件层.主题色块 import ThemeColorBlock


# *** 用户指定变量 - AI不得修改 ***
# (用户指定的变量放在这里，用户没有指定之前就空着)
# *********************************


class ThemeSettingsCard:
    """主题设置卡片 - 组件层"""
    
    @staticmethod
    def create(
        config: 界面配置,
        page: ft.Page = None,
        on_refresh: Callable[[], None] = None,
        title: str = "主题设置",
        icon: str = "PALETTE",
        enabled: bool = True,
        on_state_change: Callable[[bool], None] = None,
        help_text: str = None,
        **kwargs
    ) -> ft.Container:
        """
        创建主题设置卡片
        
        参数:
            config: 界面配置对象
            page: 页面对象（可选，用于更新页面显示）
            on_refresh: 刷新回调（主题切换后调用）
            title: 卡片标题
            icon: 图标名称
            enabled: 初始启用状态
            on_state_change: 状态变化回调
            help_text: 帮助提示文字
        
        返回:
            ft.Container: 主题设置卡片容器
        """
        theme_colors = config.当前主题颜色
        current_theme = config.主题名称
        
        # 从配置文件获取所有主题颜色
        from 配置.主题配置 import 主题配置
        all_themes = 主题配置.主题颜色
        
        # 构建预览用的简化主题数据
        themes = {}
        for theme_name, theme_data in all_themes.items():
            themes[theme_name] = {
                "bg": theme_data.get("bg_primary", "#FFFFFF"),
                "panel": theme_data.get("bg_secondary", "#F3F3F3"),
                "text": theme_data.get("text_primary", "#1A1A1A"),
                "accent": theme_data.get("accent", "#0078D4"),
            }
        
        # 存储主题卡片引用
        theme_cards_refs = {}
        
        def create_theme_preview(theme_name: str, is_selected: bool) -> ft.Container:
            """创建单个主题预览卡片"""
            theme = themes.get(theme_name, themes["浅色"])
            
            # 使用主题色块零件
            block = ThemeColorBlock.create(
                config=config,
                theme_name=theme_name,
                bg_color=theme["bg"],
                accent_color=theme["accent"],
                is_selected=is_selected,
                on_click=lambda tn=theme_name: handle_theme_click(tn),
            )
            
            # 存储引用
            theme_cards_refs[theme_name] = block
            
            return block
        
        def handle_theme_click(theme_name: str):
            """处理主题点击"""
            # 切换主题
            config.切换主题(theme_name)
            print(f"主题切换: {theme_name}")
            
            # 更新选中状态
            update_selection(theme_name)
            
            # 调用刷新回调
            if on_refresh:
                on_refresh()
        
        def update_selection(selected_theme: str):
            """更新选中状态"""
            for name, block in theme_cards_refs.items():
                is_selected = (name == selected_theme)
                block.set_selected(is_selected)
        
        # 创建主题卡片列表
        theme_names = ["浅色", "深色", "日出", "捕捉", "聚焦", "流畅"]
        theme_cards = [
            create_theme_preview(name, name == current_theme)
            for name in theme_names
        ]
        
        # 创建主题选择器行
        content = ft.Row(
            theme_cards,
            alignment=ft.MainAxisAlignment.START,
            spacing=20,
            wrap=True,
        )
        
        # 调用通用卡片组件
        card = UniversalCard.create(
            config=config,
            title=title,
            icon=icon,
            enabled=enabled,
            on_state_change=on_state_change,
            help_text=help_text,
            controls=[content],
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
        page.padding = 0
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        page.add(ThemeSettingsCard.create(配置))  # 只能更改此处**被测调用模块名称**
    
    ft.run(main)
