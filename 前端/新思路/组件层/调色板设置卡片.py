# -*- coding: utf-8 -*-
"""
调色板设置卡片 - 组件层（新思路）

设计思路:
    组装零件，构建调色板设置卡片。
    采用装配模式，协调各零件交互。
    使用通用卡片组件，保持统一风格。

功能:
    1. 调用通用卡片组件
    2. 显示高对比度调色板预览效果
    3. 点击切换调色板

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


# *** 用户指定变量 - AI不得修改 ***
# (用户指定的变量放在这里，用户没有指定之前就空着)
# *********************************


class PaletteSettingsCard:
    """调色板设置卡片 - 组件层"""
    
    @staticmethod
    def create(
        config: 界面配置,
        page: ft.Page = None,
        on_refresh: Callable[[], None] = None,
        title: str = "高对比度调色板",
        icon: str = "CONTRAST",
        enabled: bool = True,
        on_state_change: Callable[[bool], None] = None,
        help_text: str = None,
        **kwargs
    ) -> ft.Container:
        """
        创建调色板设置卡片
        
        参数:
            config: 界面配置对象
            page: 页面对象（可选，用于更新页面显示）
            on_refresh: 刷新回调（调色板切换后调用）
            title: 卡片标题
            icon: 图标名称
            enabled: 初始启用状态
            on_state_change: 状态变化回调
            help_text: 帮助提示文字
        
        返回:
            ft.Container: 调色板设置卡片容器
        """
        theme_colors = config.当前主题颜色
        current_palette = config.调色板名称
        
        # 从配置文件获取所有调色板颜色
        from 配置.主题配置 import 主题配置
        all_palettes = 主题配置.高对比度调色板
        
        # 构建预览用的简化调色板数据
        palettes = {}
        for palette_name, palette_data in all_palettes.items():
            palettes[palette_name] = {
                "bg": palette_data.get("bg_primary", "#000000"),
                "panel": palette_data.get("bg_secondary", "#000000"),
                "text": palette_data.get("text_primary", "#FFFFFF"),
                "accent": palette_data.get("accent", "#00BCFF"),
            }
        
        # 存储调色板卡片引用
        palette_cards_refs = {}
        
        def create_palette_preview(palette_name: str, is_selected: bool) -> ft.Container:
            """创建单个调色板预览卡片"""
            palette = palettes.get(palette_name, palettes["水生"])
            
            # 使用主题色块零件
            block = ThemeColorBlock.create(
                config=config,
                theme_name=palette_name,
                bg_color=palette["bg"],
                accent_color=palette["accent"],
                is_selected=is_selected,
                on_click=lambda pn=palette_name: handle_palette_click(pn),
            )
            
            # 存储引用
            palette_cards_refs[palette_name] = block
            
            return block
        
        def handle_palette_click(palette_name: str):
            """处理调色板点击"""
            # 切换调色板
            config.切换调色板(palette_name)
            print(f"调色板切换: {palette_name}")
            
            # 更新选中状态
            update_selection(palette_name)
            
            # 调用刷新回调
            if on_refresh:
                on_refresh()
        
        def update_selection(selected_palette: str):
            """更新选中状态"""
            for name, block in palette_cards_refs.items():
                is_selected = (name == selected_palette)
                block.set_selected(is_selected)
        
        # 创建调色板卡片列表
        palette_names = ["水生", "沙漠", "黄昏", "夜空"]
        palette_cards = [
            create_palette_preview(name, name == current_palette)
            for name in palette_names
        ]
        
        # 创建调色板选择器行
        content = ft.Row(
            palette_cards,
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
        page.add(PaletteSettingsCard.create(配置))  # 只能更改此处**被测调用模块名称**
    
    ft.run(main)
