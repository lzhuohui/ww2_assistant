# -*- coding: utf-8 -*-
"""
调色板设置卡片 - 组件层（新思路）

设计思路:
    复刻基础设置卡片的结构，使用主题色块作为控件。
    采用装配模式，协调各零件交互。
    使用通用卡片组件，保持统一风格。

功能:
    1. 调用通用卡片组件
    2. 在右侧放置主题色块（高对比度调色板预览）
    3. 支持调色板切换

数据来源:
    所有配置数据从配置目录获取。

使用场景:
    被页面层模块调用。

可独立运行调试: python 调色板设置卡片.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft
from typing import Callable, List, Dict, Any
from 配置.界面配置 import 界面配置
from 新思路.组件层.通用卡片 import UniversalCard
from 新思路.零件层.主题色块 import ThemeColorBlock


class PaletteSettingsCard:
    """调色板设置卡片 - 组件层"""
    
    默认调色板 = None  # None表示不使用高对比度调色板
    
    @staticmethod
    def create(
        config: 界面配置,
        title: str = "调色板设置",
        icon: str = "CONTRAST",
        enabled: bool = True,
        on_state_change: Callable[[bool], None] = None,
        help_text: str = None,
        palettes: List[str] = None,
        selected: str = None,
        on_palette_change: Callable[[str], None] = None,
        subtitle: str = None,
        **kwargs
    ) -> ft.Container:
        """
        创建调色板设置卡片
        
        参数:
            config: 界面配置对象
            title: 卡片标题
            icon: 图标名称
            enabled: 初始启用状态
            on_state_change: 状态变化回调
            help_text: 帮助提示文字
            palettes: 调色板列表
            selected: 当前选中的调色板
            on_palette_change: 调色板变化回调
            subtitle: 副标题
        
        返回:
            ft.Container: 调色板设置卡片容器
        """
        # 默认调色板列表
        default_palettes = ["水生", "沙漠", "黄昏", "夜空"]
        current_palettes = palettes if palettes else default_palettes
        current_selected = selected if selected else config.调色板名称
        
        # 调色板颜色映射
        palette_colors = {
            "水生": "#006994",
            "沙漠": "#C19A6B",
            "黄昏": "#FF6B6B",
            "夜空": "#2C3E50",
        }
        
        # 创建调色板色块容器
        palette_blocks_refs = {}
        
        def handle_palette_click(palette_name: str):
            """处理调色板点击"""
            # 只有启用时才允许切换调色板
            if not card.get_state():
                return
            
            # 更新选中状态
            for name, block in palette_blocks_refs.items():
                if hasattr(block, 'set_selected'):
                    block.set_selected(name == palette_name)
            
            # 切换调色板
            config.切换调色板(palette_name)
            
            # 调用外部回调
            if on_palette_change:
                on_palette_change(palette_name)
        
        # 创建调色板色块列表
        controls = []
        for palette_name in current_palettes:
            bg_color = palette_colors.get(palette_name, "#FFFFFF")
            is_selected = palette_name == current_selected
            
            block = ThemeColorBlock.create(
                config=config,
                theme_name=palette_name,
                bg_color=bg_color,
                is_selected=is_selected,
                on_click=handle_palette_click,
            )
            palette_blocks_refs[palette_name] = block
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
            subtitle=subtitle if subtitle else "高对比度调色板配置",
            controls_per_row=4,  # 调色板色块每行4个
        )
        
        # 暴露控制接口
        card.palette_blocks_refs = palette_blocks_refs
        
        return card


# 兼容别名
调色板设置卡片 = PaletteSettingsCard


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    # 1. 界面配置初始化
    配置 = 界面配置()
    
    # 2. 自动加载用户数据覆盖默认值（在界面配置.__init__中自动完成）
    
    # 3. 正常启动被测模块
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        page.add(PaletteSettingsCard.create(配置))
    
    ft.run(main)
