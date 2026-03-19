# -*- coding: utf-8 -*-
"""
模块名称：可展开卡片 | 层级：组件模块层
设计思路：
    基于ExpansionPanel的可展开卡片组件。
    点击卡片头部展开/收起详细内容。
    支持开关状态和详细内容区域。

功能：
    1. 点击展开/收起
    2. 支持开关状态（可选）
    3. 支持详细内容区域
    4. 支持操作按钮

对外接口：
    - create(): 创建可展开卡片
"""

import flet as ft
from typing import Callable, List, Optional
from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider
from 前端.配置.界面配置 import 界面配置


class ExpansionCard:
    """可展开卡片 - 组件模块层"""
    
    @staticmethod
    def create(
        config: 界面配置,
        title: str,
        icon: str = "INFO",
        subtitle: str = "",
        content_items: List[tuple] = None,
        enabled: bool = True,
        on_state_change: Callable[[bool], None] = None,
        expanded: bool = False,
        on_expand_change: Callable[[bool], None] = None,
        action_buttons: List[ft.Control] = None,
        **kwargs
    ) -> ft.Container:
        """
        创建可展开卡片
        
        参数:
            config: 界面配置对象
            title: 卡片标题
            icon: 图标名称
            subtitle: 副标题（可选）
            content_items: 内容项列表，每项为 (标签, 值, 点击回调)
            enabled: 开关状态
            on_state_change: 开关状态变化回调
            expanded: 是否展开
            on_expand_change: 展开状态变化回调
            action_buttons: 操作按钮列表
            **kwargs: 其他参数
        
        返回:
            ft.Container: 可展开卡片容器
        """
        theme_colors = config.当前主题颜色
        
        is_expanded = [expanded]
        
        icon_control = ft.Icon(
            getattr(ft.Icons, icon, ft.Icons.INFO),
            size=20,
            color=theme_colors.get("accent"),
        )
        
        title_control = ft.Text(
            title,
            size=16,
            weight=ft.FontWeight.BOLD,
            color=theme_colors.get("text_primary"),
        )
        
        subtitle_control = ft.Text(
            subtitle,
            size=12,
            color=theme_colors.get("text_secondary"),
        ) if subtitle else None
        
        expand_icon = ft.Icon(
            ft.Icons.EXPAND_MORE,
            size=24,
            color=theme_colors.get("text_secondary"),
        )
        
        switch_control = ft.Switch(
            value=enabled,
            on_change=lambda e: on_state_change(e.control.value) if on_state_change else None,
            active_color=theme_colors.get("accent"),
        ) if on_state_change else None
        
        header_left = ft.Row(
            [icon_control, ft.Container(width=8), title_control] + 
            ([ft.Container(width=8), subtitle_control] if subtitle_control else []),
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )
        
        header_right = ft.Row(
            ([switch_control] if switch_control else []) + [expand_icon],
            alignment=ft.MainAxisAlignment.END,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        
        header = ft.Row(
            [header_left, header_right],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        
        content_controls = []
        if content_items:
            for item in content_items:
                if len(item) == 3:
                    label, value, on_click = item
                else:
                    label, value = item[0], item[1]
                    on_click = None
                
                if label == "" and value in ["授权价格", "授权流程", ""]:
                    content_controls.append(
                        ft.Container(
                            content=ft.Text(
                                value,
                                size=14,
                                weight=ft.FontWeight.BOLD,
                                color=theme_colors.get("text_primary"),
                            ),
                            margin=ft.Margin(top=8, bottom=4, left=0, right=0),
                        )
                    )
                elif label == "":
                    content_controls.append(
                        ft.Container(
                            content=ft.Text(
                                value,
                                size=13,
                                color=theme_colors.get("text_secondary"),
                            ),
                            margin=ft.Margin(top=2, bottom=2, left=16, right=0),
                        )
                    )
                else:
                    value_control = ft.Text(
                        value,
                        size=14,
                        color=theme_colors.get("accent") if on_click else theme_colors.get("text_primary"),
                    )
                    
                    if on_click:
                        value_control = ft.GestureDetector(
                            content=value_control,
                            on_tap=on_click,
                        )
                    
                    row = ft.Row(
                        [
                            ft.Text(
                                label,
                                size=14,
                                color=theme_colors.get("text_secondary"),
                                width=80,
                            ),
                            value_control,
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    )
                    content_controls.append(row)
        
        if action_buttons:
            button_row = ft.Row(
                action_buttons,
                alignment=ft.MainAxisAlignment.END,
            )
            content_controls.append(ft.Container(height=8))
            content_controls.append(button_row)
        
        content_column = ft.Column(
            content_controls,
            spacing=4,
        )
        
        content_container = ft.Container(
            content=content_column,
            padding=ft.Padding(left=36, right=16, top=0, bottom=16),
            visible=is_expanded[0],
        )
        
        card_container = [None]
        
        def toggle_expand(e):
            is_expanded[0] = not is_expanded[0]
            content_container.visible = is_expanded[0]
            expand_icon.name = ft.Icons.EXPAND_LESS if is_expanded[0] else ft.Icons.EXPAND_MORE
            if card_container[0] and card_container[0].page:
                card_container[0].update()
            if on_expand_change:
                on_expand_change(is_expanded[0])
        
        header_container = ft.Container(
            content=header,
            padding=16,
            on_click=toggle_expand,
        )
        
        card = ft.Container(
            content=ft.Column(
                [header_container, content_container],
                spacing=0,
            ),
            bgcolor=theme_colors.get("bg_card"),
            border_radius=8,
            border=ft.border.all(1, theme_colors.get("border")),
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        )
        
        card_container[0] = card
        return card


# 兼容别名
可展开卡片 = ExpansionCard


# *** 调试逻辑 ***
if __name__ == "__main__":
    配置 = 界面配置()
    ThemeProvider.initialize(配置)
    
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        
        def on_copy(e):
            page.set_clipboard("123456")
            page.snack_bar = ft.SnackBar(content=ft.Text("已复制"))
            page.snack_bar.open = True
            page.update()
        
        page.add(ExpansionCard.create(
            config=配置,
            title="版本信息",
            icon="INFO",
            subtitle="点击查看详情",
            content_items=[
                ("软件名称", "二战风云辅助工具", None),
                ("当前版本", "v1.0.0", None),
                ("QQ群", "123456", on_copy),
            ],
            expanded=True,
        ))
    
    ft.run(main)
