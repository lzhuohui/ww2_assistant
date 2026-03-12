# -*- coding: utf-8 -*-
"""
任务设置页面 - 页面层（新思路）

设计思路:
    组装组件，构建任务设置页面。

功能:
    1. 主线任务卡片
    2. 支线任务卡片

数据来源:
    所有配置数据从配置目录获取。

使用场景:
    被主界面调用。

可独立运行调试: python 任务设置页面.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft
from typing import Callable
from 配置.界面配置 import 界面配置
from 新思路.组件层.通用卡片 import UniversalCard
from 新思路.零件层.标签下拉框 import LabelDropdown


class TaskSettingsPage:
    """任务设置页面 - 页面层"""
    
    @staticmethod
    def create(config: 界面配置, page: ft.Page = None, on_refresh: Callable[[], None] = None) -> ft.Column:
        """
        创建任务设置页面
        
        参数:
            config: 界面配置对象
            page: 页面对象（可选，用于更新页面显示）
            on_refresh: 刷新回调（主题/调色板切换后调用）
        
        返回:
            ft.Column: 任务设置页面容器
        """
        theme_colors = config.当前主题颜色
        
        # 主城等级选项 (01-15)
        main_level_options = [f"{i:02d}" for i in range(1, 16)]
        # 支线主城等级选项 (05-15)
        side_level_options = [f"{i:02d}" for i in range(5, 16)]
        
        # ========== 主线任务卡片 ==========
        main_dropdown = LabelDropdown.create(
            config=config,
            label="主线限级",
            options=main_level_options,
            value="05",
        )
        
        main_card = UniversalCard.create(
            config=config,
            title="主线任务",
            icon="TASK",
            enabled=True,
            subtitle="达到设置主城等级后,允许执行主线任务",
            controls=[main_dropdown],
        )
        
        # ========== 支线任务卡片 ==========
        side_dropdown = LabelDropdown.create(
            config=config,
            label="支线限级",
            options=side_level_options,
            value="10",
        )
        
        side_card = UniversalCard.create(
            config=config,
            title="支线任务",
            icon="TASK_ALT",
            enabled=True,
            subtitle="达到设置主城等级后,允许执行支线任务",
            controls=[side_dropdown],
        )
        
        # ========== 页面容器 ==========
        page_content = ft.Column(
            [
                # 页面标题
                ft.Text(
                    "任务设置",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=theme_colors.get("text_primary"),
                ),
                ft.Container(height=20),
                # 主线任务卡片
                main_card,
                ft.Container(height=15),
                # 支线任务卡片
                side_card,
            ],
            spacing=0,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )
        
        # 页面容器
        page_container = ft.Container(
            content=page_content,
            padding=ft.Padding.all(20),
            expand=True,
        )
        
        # 暴露卡片引用
        page_container.main_card = main_card
        page_container.side_card = side_card
        
        return page_container


# 兼容别名
任务设置页面 = TaskSettingsPage


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    # 1. 界面配置初始化
    配置 = 界面配置()
    
    # 2. 自动加载用户数据覆盖默认值（在界面配置.__init__中自动完成）
    
    # 3. 正常启动被测模块
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        page.add(TaskSettingsPage.create(配置))
    
    ft.run(main)
