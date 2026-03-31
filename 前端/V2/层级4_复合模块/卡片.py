# -*- coding: utf-8 -*-

"""
模块名称：卡片.py
模块功能：卡片组件，左侧开关+右侧控件区

实现步骤：
- 创建左侧区域（图标+标题+开关）
- 创建右侧控件区
- 创建分隔线
- 组合布局

职责：
- 卡片容器
- 开关控制
- 控件区布局

不负责：
- 控件创建（由卡片组负责）
- 销毁（不需要销毁）

尺寸传递：
- 从卡片容器（层级5）继承基础尺寸
- 本模块定义特殊尺寸（图标、标题等）
"""

import flet as ft
from typing import Callable, Dict, List, Optional, Any

from 前端.V2.层级5_基础模块.卡片容器 import CardContainer
from 前端.V2.层级5_基础模块.图标 import Icon
from 前端.V2.层级5_基础模块.标签 import Label
from 前端.V2.层级5_基础模块.分割线 import Divider

# ============================================
# 数据和文件接口（前置，方便查看和修改）
# ============================================

DEFAULT_ICON_SIZE = 22
DEFAULT_TITLE_SIZE = 14
DEFAULT_SUBTITLE_SIZE = 11
DEFAULT_DIVIDER_LEFT = 76
DEFAULT_CONTROL_RIGHT_MARGIN = 16

# ============================================
# 公开接口
# ============================================

class Card:
    """
    卡片组件 - 左侧开关+右侧控件区（层级4：复合模块）
    
    职责：
    - 卡片容器
    - 开关控制
    - 控件区布局
    
    不负责：
    - 控件创建（由卡片组负责）
    - 销毁（不需要销毁）
    
    尺寸传递：
    - 从卡片容器（层级5）继承基础尺寸
    - 本模块定义特殊尺寸（图标、标题等）
    """
    
    @staticmethod
    def get_height():
        """获取卡片高度（从卡片容器继承）"""
        return CardContainer.get_height()
    
    @staticmethod
    def get_padding():
        """获取内边距（从卡片容器继承）"""
        return CardContainer.get_padding()
    
    @staticmethod
    def get_icon_size():
        """获取图标尺寸（本模块定义）"""
        return DEFAULT_ICON_SIZE
    
    @staticmethod
    def get_title_size():
        """获取标题尺寸（本模块定义）"""
        return DEFAULT_TITLE_SIZE
    
    @staticmethod
    def get_subtitle_size():
        """获取副标题尺寸（本模块定义）"""
        return DEFAULT_SUBTITLE_SIZE
    
    @staticmethod
    def get_divider_left():
        """获取分隔线左边距（本模块定义）"""
        return DEFAULT_DIVIDER_LEFT
    
    @staticmethod
    def get_control_right_margin():
        """获取控件右边距（本模块定义）"""
        return DEFAULT_CONTROL_RIGHT_MARGIN
    
    @staticmethod
    def create(
        title: str = "卡片标题",
        icon: str = "HOME",
        subtitle: str = "",
        enabled: bool = True,
        controls: List[ft.Control] = None,
        controls_per_row: int = 6,
        width: int = None,
        on_switch_change: Callable[[bool], None] = None,
        theme_colors: Dict[str, str] = None,
    ) -> ft.Container:
        """
        创建卡片
        
        参数：
        - title: 卡片标题
        - icon: 图标名称
        - subtitle: 副标题
        - enabled: 是否启用
        - controls: 控件列表
        - controls_per_row: 每行控件数
        - width: 卡片宽度
        - on_switch_change: 开关变更回调
        - theme_colors: 主题颜色
        """
        if theme_colors is None:
            theme_colors = {
                "text_primary": "#000000",
                "text_secondary": "#666666",
                "text_disabled": "#999999",
                "bg_card": "#FFFFFF",
                "accent": "#0078D4",
            }
        
        is_enabled = [enabled]
        switch_state = [enabled]
        
        icon_control = Icon.create(
            icon_name=icon,
            size=DEFAULT_ICON_SIZE,
            color_type="accent",
            theme_colors=theme_colors,
            opacity=1.0 if enabled else 0.4,
        )
        
        title_text = Label.create(
            text=title,
            size=DEFAULT_TITLE_SIZE,
            weight=ft.FontWeight.BOLD,
            color_type="primary",
            theme_colors=theme_colors,
        )
        title_text.opacity = 1.0 if enabled else 0.4
        
        subtitle_text = Label.create(
            text=subtitle,
            size=DEFAULT_SUBTITLE_SIZE,
            color_type="secondary",
            theme_colors=theme_colors,
        )
        
        controls_column = ft.Column([], spacing=8, alignment=ft.MainAxisAlignment.CENTER)
        
        controls_container = ft.Container(
            content=controls_column,
            opacity=1.0,
            right=DEFAULT_CONTROL_RIGHT_MARGIN,
            top=0,
            bottom=0,
            alignment=ft.alignment.Alignment(1.0, 0.5),
            clip_behavior=ft.ClipBehavior.NONE,
        )
        
        subtitle_container = ft.Container(
            content=subtitle_text,
            left=8,
            top=0,
            bottom=0,
            right=0,
            opacity=0.0,
            alignment=ft.Alignment(-1.0, 0.0),
        )
        
        right_stack = ft.Stack([
            subtitle_container,
            controls_container,
        ], clip_behavior=ft.ClipBehavior.NONE)
        
        right_container = ft.Container(
            content=right_stack,
            expand=True,
            clip_behavior=ft.ClipBehavior.NONE,
        )
        
        left_width = DEFAULT_DIVIDER_LEFT - 2
        
        left_content = ft.Column([
            icon_control,
            ft.Container(height=4),
            title_text,
        ], spacing=0, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        divider = ft.Container(
            width=2,
            bgcolor=theme_colors.get("accent", "#0078d4"),
            height=DEFAULT_CARD_HEIGHT - DEFAULT_PADDING,
            margin=ft.Margin(0, DEFAULT_PADDING / 2, 0, DEFAULT_PADDING / 2)
        )
        
        left_container = ft.Container(
            content=left_content,
            padding=ft.Padding(left=DEFAULT_PADDING, top=0, right=DEFAULT_PADDING, bottom=0),
            width=left_width,
            expand=False,
            alignment=ft.Alignment(0, 0.5),
        )
        
        main_row = ft.Row([
            left_container,
            divider,
            right_container,
        ], height=DEFAULT_CARD_HEIGHT, spacing=0, vertical_alignment=ft.CrossAxisAlignment.CENTER, expand=True if width is None else False)
        
        container = CardContainer.create(
            content=main_row,
            height=DEFAULT_CARD_HEIGHT,
            width=width,
            padding=DEFAULT_PADDING,
            theme_colors=theme_colors,
        )
        container.clip_behavior = ft.ClipBehavior.NONE
        
        def handle_switch_toggle():
            """处理开关切换"""
            new_state = not switch_state[0]
            switch_state[0] = new_state
            is_enabled[0] = new_state
            
            if on_switch_change:
                on_switch_change(new_state)
            
            update_card_state()
        
        def update_card_state():
            """更新卡片状态"""
            if switch_state[0]:
                container.opacity = 1.0
                subtitle_text.color = theme_colors.get("text_secondary")
                icon_control.opacity = 1.0
                title_text.opacity = 1.0
                
                for ctrl in controls_column.controls[:]:
                    if hasattr(ctrl, 'controls'):
                        for c in ctrl.controls:
                            if hasattr(c, 'set_enabled'):
                                c.set_enabled(True)
            else:
                container.opacity = 0.5
                subtitle_text.color = theme_colors.get("text_disabled", "#888888")
                icon_control.opacity = 0.4
                title_text.opacity = 0.4
                
                for ctrl in controls_column.controls[:]:
                    if hasattr(ctrl, 'controls'):
                        for c in ctrl.controls:
                            if hasattr(c, 'set_enabled'):
                                c.set_enabled(False)
            
            try:
                if container.page:
                    container.page.update()
            except:
                pass
        
        left_container.on_click = lambda e: handle_switch_toggle()
        
        def layout_controls(control_list: List[ft.Control]):
            """布局控件"""
            row_list = []
            current_row_controls = []
            current_row_count = 0
            
            for single_control in control_list:
                if current_row_count >= controls_per_row and current_row_controls:
                    row_list.append(ft.Row(
                        current_row_controls,
                        spacing=12,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.END,
                    ))
                    current_row_controls = []
                    current_row_count = 0
                
                current_row_controls.append(single_control)
                current_row_count += 1
            
            if current_row_controls:
                row_list.append(ft.Row(
                    current_row_controls,
                    spacing=12,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.END,
                ))
            
            controls_column.controls = row_list
        
        def get_switch_state() -> bool:
            """获取开关状态"""
            return switch_state[0]
        
        def set_switch_state(state: bool):
            """设置开关状态"""
            switch_state[0] = state
            is_enabled[0] = state
            update_card_state()
        
        def set_subtitle(new_subtitle: str):
            """设置副标题"""
            subtitle_text.value = new_subtitle
            try:
                if container.page:
                    container.page.update()
            except:
                pass
        
        container.get_switch_state = get_switch_state
        container.set_switch_state = set_switch_state
        container.set_subtitle = set_subtitle
        container.layout_controls = layout_controls
        container._controls_column = controls_column
        
        if controls is not None:
            layout_controls(controls)
        
        update_card_state()
        
        return container

# *** 标准测试格式: 仅调用被测模块,AI不得添加数据 ***
if __name__ == "__main__":
    def main(page: ft.Page):
        page.title = "卡片测试"
        
        def on_switch(enabled):
            print(f"开关状态: {enabled}")
        
        card = Card.create(
            title="测试卡片",
            icon="SETTINGS",
            enabled=True,
            on_switch_change=on_switch,
        )
        page.add(card)
    
    ft.app(target=main)
