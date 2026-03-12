# -*- coding: utf-8 -*-
"""
主题设置卡片 - 组件层（新思路）

设计思路:
    复刻基础设置卡片的结构，使用主题色块作为控件。
    采用装配模式，协调各零件交互。
    使用通用卡片组件，保持统一风格。

功能:
    1. 调用通用卡片组件
    2. 在右侧放置主题色块
    3. 支持主题切换

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


class ThemeSettingsCard:
    """主题设置卡片 - 组件层"""
    
    默认主题 = "深色"
    
    @staticmethod
    def create(
        config: 界面配置,
        title: str = "主题设置",
        icon: str = "PALETTE",
        enabled: bool = True,
        on_state_change: Callable[[bool], None] = None,
        help_text: str = None,
        themes: List[str] = None,
        selected: str = None,
        on_theme_change: Callable[[str], None] = None,
        subtitle: str = None,
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
            themes: 主题列表
            selected: 当前选中的主题
            on_theme_change: 主题变化回调
            subtitle: 副标题
        
        返回:
            ft.Container: 主题设置卡片容器
        """
        # 默认主题列表
        default_themes = ["浅色", "深色", "日出", "捕捉", "聚焦", "流畅"]
        current_themes = themes if themes else default_themes
        current_selected = selected if selected else ThemeSettingsCard.默认主题
        
        # 主题颜色映射
        theme_colors = {
            "浅色": "#FFFFFF",
            "深色": "#1A1A2E",
            "日出": "#FFE4B5",
            "捕捉": "#98FB98",
            "聚焦": "#87CEEB",
            "流畅": "#E6E6FA",
        }
        
        # 创建主题色块容器
        theme_blocks_refs = {}
        
        def handle_theme_click(theme_name: str):
            """处理主题点击"""
            # 只有启用时才允许切换主题
            if not card.get_state():
                return
            
            # 更新选中状态
            for name, block in theme_blocks_refs.items():
                if hasattr(block, 'set_selected'):
                    block.set_selected(name == theme_name)
            
            # 切换主题
            config.切换主题(theme_name)
            
            # 调用外部回调
            if on_theme_change:
                on_theme_change(theme_name)
        
        # 创建主题色块列表
        controls = []
        for theme_name in current_themes:
            bg_color = theme_colors.get(theme_name, "#FFFFFF")
            is_selected = theme_name == current_selected
            
            block = ThemeColorBlock.create(
                config=config,
                theme_name=theme_name,
                bg_color=bg_color,
                is_selected=is_selected,
                on_click=handle_theme_click,
            )
            theme_blocks_refs[theme_name] = block
            controls.append(block)
        
        # 调用通用卡片组件
        card = UniversalCard.create(
            config=config,
            title=title,
            icon=icon,
            enabled=enabled,
            on_state_change=on_state_change,
            help_text=help_text,
            controls=controls,
            subtitle=subtitle if subtitle else "主题配置描述",
            controls_per_row=6,  # 主题色块每行6个
        )
        
        # 暴露控制接口
        card.theme_blocks_refs = theme_blocks_refs
        
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
        page.add(ThemeSettingsCard.create(配置))
    
    ft.run(main)
