# -*- coding: utf-8 -*-
"""
帮助标签 - 零件层（新思路）

设计思路:
    独立功能模块，轻量级设计。
    点击显示简短提示文字，符合现代设计趋势。

功能:
    1. 图标：问号图标
    2. 提示：点击在图标右上角显示简短文字
    3. 状态切换：内置切换逻辑
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
from 新思路.零件层.标签文本 import LabelText


# *** 用户指定变量 - AI不得修改 ***
# (用户指定的变量放在这里，用户没有指定之前就空着)
# *********************************


class HelpTag:
    """帮助标签 - 轻量级独立功能模块"""
    
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
            help_text: 帮助提示文字（用户编辑）
            enabled: 初始启用状态
            icon_size: 图标大小
            on_state_change: 状态变化回调函数
            on_click: 点击回调函数（可选）
        
        返回:
            ft.Container: 包含帮助标签的容器
            如果help_text为空，返回None
        """
        if not help_text:
            return None
        
        theme_colors = config.当前主题颜色
        
        # 图标容器尺寸
        box_size = icon_size + 4
        
        # 创建图标控件
        icon_control = ft.Icon(
            ft.Icons.HELP_OUTLINE,
            size=icon_size,
            color=theme_colors.get("text_secondary"),
        )
        
        # 创建提示文字（调用标签文本模块）
        tip_label = LabelText.create(
            config=config,
            text=help_text,
            role="help",
            enabled=enabled,
        )
        
        tip_text = ft.Container(
            content=tip_label,
            padding=ft.Padding(left=8, top=4, right=8, bottom=4),
            bgcolor=theme_colors.get("bg_card"),
            border_radius=4,
            border=ft.Border.all(0.5, theme_colors.get("border")),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=4,
                color=theme_colors.get("shadow", "#00000020"),
                offset=ft.Offset(0, 1),
            ),
            visible=False,
            opacity=0.95,
        )
        
        # 内部状态
        current_enabled = enabled
        tip_visible = False
        
        def hide_tip():
            """隐藏提示"""
            nonlocal tip_visible
            tip_visible = False
            tip_text.visible = False
            tip_text.update()
        
        def show_tip():
            """显示提示"""
            nonlocal tip_visible
            tip_visible = True
            tip_text.visible = True
            tip_text.update()
        
        def toggle_tip():
            """切换提示显示状态"""
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
        
        # 创建主容器（Stack布局：图标 + 右上角提示）
        container = ft.Container(
            content=ft.Stack(
                [
                    icon_container,
                    ft.Container(
                        content=tip_text,
                        left=box_size + 4,  # 图标右侧
                        top=-box_size + 2,  # 右上角，与图标顶部对齐
                    ),
                ],
                width=box_size,
                height=box_size,
                clip_behavior=ft.ClipBehavior.NONE,
            ),
            width=box_size,
            height=box_size,
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
    # 1. 界面配置初始化
    配置 = 界面配置()
    
    # 2. 自动加载用户数据覆盖默认值（在界面配置.__init__中自动完成）
    
    # 3. 正常启动被测模块
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        page.add(HelpTag.create(配置, help_text="帮助提示内容", enabled=True))  # 只能更改此处**被测调用模块名称**
    
    ft.run(main)
