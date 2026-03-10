# -*- coding: utf-8 -*-
"""
通用卡片 - 组件层

设计思路:
    统一的卡片组件，通过参数控制单行/多行模式。
    - 单行模式：左侧横向布局（图标+标题+描述），右侧单个控件
    - 多行模式：左侧纵向布局（图标+标题），中间分割线，右侧多行控件

功能:
    1. 自动适配：根据控件数量自动选择模式
    2. 统一风格：边距、阴影、圆角、边框统一
    3. 状态切换：单击左侧区域切换启用/禁用状态
    4. 悬停效果：统一的悬停视觉反馈
    5. 帮助提示：右上角"?"标签，点击显示帮助内容

数据来源:
    所有配置数据从界面配置获取。

使用场景:
    所有需要卡片布局的界面。

可独立运行调试: python 通用卡片.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import flet as ft
from typing import List, Callable, Optional, Any, Dict
from 原子层.界面配置 import 界面配置


# ==================== 用户指定变量区 ====================
# 所有数据从配置文件动态获取，此处仅保留模块级默认值（调试用）
# ========================================================


class UniversalCard:
    """通用卡片 - 统一的卡片组件"""
    
    @staticmethod
    def create(
        config: 界面配置,
        title: str,
        icon: str = None,
        description: str = None,
        controls: List[ft.Control] = None,
        items_per_row: int = None,
        enabled: bool = True,
        on_state_change: Callable[[bool], None] = None,
        help_text: str = None,
        height: int = None,
        width: int = None,
        **kwargs
    ) -> ft.Container:
        theme_colors = config.当前主题颜色
        
        font_config = config.定义尺寸.get("字体", {})
        weight_config = config.定义尺寸.get("字重", {})
        spacing_config = config.定义尺寸.get("间距", {})
        radius_config = config.定义尺寸.get("圆角", {})
        ui_config = config.定义尺寸.get("界面", {})
        card_config = config.定义尺寸.get("卡片", {})
        multirow_config = config.定义尺寸.get("多行卡片", {})
        shadow_config = config.定义尺寸.get("阴影", {})
        
        default_card_height = card_config.get("default_height", 70)
        default_card_spacing = card_config.get("default_spacing", 10)
        default_items_per_row = card_config.get("items_per_row", 6)
        default_row_height = card_config.get("row_height", 32)
        default_icon_size = card_config.get("icon_size", 24)
        default_title_size = card_config.get("title_size", 14)
        default_desc_size = card_config.get("desc_size", 12)
        
        divider_width = multirow_config.get("divider_width", 2)
        divider_height = multirow_config.get("divider_height", 60)
        divider_opacity = multirow_config.get("divider_opacity", 0.7)
        divider_blur = multirow_config.get("divider_blur", 6)
        left_width = multirow_config.get("left_width", 60)
        divider_left = multirow_config.get("divider_left", 90)
        content_left = multirow_config.get("content_left", 130)
        
        shadow_blur_default = shadow_config.get("blur_default", 4)
        shadow_blur_hover = shadow_config.get("blur_hover", 8)
        shadow_spread = shadow_config.get("spread", 0)
        shadow_offset_y = shadow_config.get("offset_y", 2)
        shadow_offset_y_hover = shadow_config.get("offset_y_hover", 3)
        
        card_border_radius = ui_config.get("card_radius", 8)
        card_border_width = ui_config.get("card_border_width", 1)
        card_padding = ui_config.get("card_padding", 16)
        item_padding = ui_config.get("item_padding", 12)
        
        actual_items_per_row = items_per_row if items_per_row is not None else default_items_per_row
        
        current_enabled = enabled
        control_list = controls or []
        
        is_single_row = len(control_list) == 1
        
        card_height = height or (default_card_height if is_single_row else None)
        card_width = width or 800
        
        icon_value = None
        if icon:
            if isinstance(icon, str):
                icon_name = icon.upper()
                icon_value = getattr(ft.Icons, icon_name, ft.Icons.SETTINGS)
            else:
                icon_value = icon
        
        icon_control = None
        if icon_value:
            icon_control = ft.Icon(
                icon_value,
                size=default_icon_size,
                color=theme_colors.get("accent"),
                opacity=1.0 if current_enabled else 0.4,
            )
        
        title_control = ft.Text(
            title,
            size=default_title_size,
            weight=weight_config.get("font_weight_medium", ft.FontWeight.W_500),
            color=theme_colors.get("text_primary"),
            opacity=1.0 if current_enabled else 0.4,
        )
        
        desc_control = None
        if description and is_single_row:
            desc_control = ft.Text(
                description,
                size=default_desc_size,
                color=theme_colors.get("text_secondary"),
                opacity=1.0 if current_enabled else 0.4,
            )
        
        help_icon = None
        if help_text:
            help_icon = ft.IconButton(
                icon=ft.Icons.HELP_OUTLINE,
                icon_size=14,
                icon_color=theme_colors.get("text_secondary"),
                tooltip=help_text,
                opacity=0.7 if current_enabled else 0.3,
                style=ft.ButtonStyle(
                    padding=0,
                ),
            )
        
        if is_single_row:
            left_row_items = [
                icon_control if icon_control else ft.Container(),
                ft.Column(
                    [
                        title_control,
                        desc_control if desc_control else ft.Container(),
                    ],
                    spacing=4,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ]
            
            if help_icon:
                left_row_items.append(help_icon)
            
            left_content = ft.Row(
                left_row_items,
                spacing=12,
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            )
            
            left_container = ft.Container(
                content=left_content,
                left=card_padding,
                top=0,
                bottom=0,
                alignment=ft.Alignment(-1, 0),
                on_click=lambda e: toggle_state(e) if not is_single_row else None,
            )
        else:
            left_column_items = [
                icon_control if icon_control else ft.Container(),
                title_control,
            ]
            
            if help_icon:
                left_column_items.insert(0, help_icon)
            
            left_content = ft.Column(
                left_column_items,
                spacing=spacing_config.get("spacing_xs", 4),
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
            )
            
            left_container = ft.Container(
                content=left_content,
                left=card_padding,
                top=0,
                bottom=0,
                width=left_width,
                alignment=ft.Alignment(0, 0),
                on_click=lambda e: toggle_state(e),
            )
        
        divider = None
        if not is_single_row:
            divider = ft.Container(
                width=divider_width,
                height=divider_height,
                bgcolor=theme_colors.get("accent"),
                opacity=divider_opacity if current_enabled else 0.2,
                shadow=ft.BoxShadow(
                    blur_radius=divider_blur,
                    color=theme_colors.get("accent"),
                    spread_radius=0,
                ) if current_enabled else None,
                left=divider_left,
                top=0,
                bottom=0,
            )
        
        right_content = None
        
        if is_single_row:
            single_control = control_list[0] if control_list else ft.Container()
            
            right_container = ft.Container(
                content=single_control,
                right=card_padding,
                top=0,
                bottom=0,
                alignment=ft.Alignment(1, 0),
            )
            
            stack_children = [
                left_container,
                right_container,
            ]
            
            stack_height = card_height
        else:
            rows = []
            for i in range(0, len(control_list), actual_items_per_row):
                row_items = control_list[i:i+actual_items_per_row]
                row = ft.Row(
                    row_items,
                    spacing=spacing_config.get("spacing_md", 12),
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                )
                rows.append(row)
            
            row_count = len(rows)
            row_spacing = spacing_config.get("spacing_sm", 8)
            padding_vertical = item_padding * 2
            content_height = row_count * default_row_height + (row_count - 1) * row_spacing if row_count > 0 else 0
            stack_height = content_height + padding_vertical
            
            right_content = ft.Column(
                rows,
                spacing=row_spacing,
                opacity=1.0 if current_enabled else 0.5,
            )
            
            right_container = ft.Container(
                content=right_content,
                left=content_left,
                right=card_padding,
                top=item_padding,
                height=content_height,
                alignment=ft.Alignment(-1, 0),
            )
            
            stack_children = [
                left_container,
                divider,
                right_container,
            ]
        
        main_stack = ft.Stack(
            stack_children,
            height=stack_height,
            width=card_width,
            clip_behavior=ft.ClipBehavior.NONE,
        )
        
        container = ft.Container(
            content=main_stack,
            bgcolor=theme_colors.get("bg_card"),
            border_radius=card_border_radius,
            border=ft.Border.all(card_border_width, theme_colors.get("border_light")),
            shadow=ft.BoxShadow(
                spread_radius=shadow_spread,
                blur_radius=shadow_blur_default,
                color=theme_colors.get("shadow"),
                offset=ft.Offset(0, shadow_offset_y),
            ),
            animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
            clip_behavior=ft.ClipBehavior.NONE,
        )
        
        def toggle_state(e):
            nonlocal current_enabled
            current_enabled = not current_enabled
            
            if icon_control:
                icon_control.opacity = 1.0 if current_enabled else 0.4
                icon_control.update()
            title_control.opacity = 1.0 if current_enabled else 0.4
            title_control.update()
            
            if help_icon:
                help_icon.opacity = 0.7 if current_enabled else 0.3
                help_icon.update()
            
            if divider:
                divider.opacity = divider_opacity if current_enabled else 0.2
                divider.update()
            
            if not is_single_row and right_content:
                right_content.opacity = 1.0 if current_enabled else 0.5
                right_content.update()
            
            if on_state_change:
                on_state_change(current_enabled)
        
        def on_hover(e):
            if e.data == "true":
                container.bgcolor = theme_colors.get("bg_hover")
                container.border = ft.Border.all(card_border_width, theme_colors.get("border"))
                container.shadow = ft.BoxShadow(
                    spread_radius=shadow_spread,
                    blur_radius=shadow_blur_hover,
                    color=theme_colors.get("shadow"),
                    offset=ft.Offset(0, shadow_offset_y_hover),
                )
            else:
                container.bgcolor = theme_colors.get("bg_card")
                container.border = ft.Border.all(card_border_width, theme_colors.get("border_light"))
                container.shadow = ft.BoxShadow(
                    spread_radius=shadow_spread,
                    blur_radius=shadow_blur_default,
                    color=theme_colors.get("shadow"),
                    offset=ft.Offset(0, shadow_offset_y),
                )
            container.update()
        
        container.on_hover = on_hover
        
        return container
    
    @staticmethod
    def create_list(
        config: 界面配置,
        card_configs: List[dict],
    ) -> ft.Column:
        card_config = config.定义尺寸.get("卡片", {})
        default_card_spacing = card_config.get("default_spacing", 10)
        
        controls = []
        
        for i, card_config_item in enumerate(card_configs):
            card = UniversalCard.create(
                config=config,
                title=card_config_item.get("title"),
                icon=card_config_item.get("icon"),
                description=card_config_item.get("description"),
                controls=card_config_item.get("controls"),
                items_per_row=card_config_item.get("items_per_row"),
                enabled=card_config_item.get("enabled", True),
                on_state_change=card_config_item.get("on_state_change"),
                help_text=card_config_item.get("help_text"),
                height=card_config_item.get("height"),
                width=card_config_item.get("width"),
            )
            controls.append(card)
            
            if i < len(card_configs) - 1:
                controls.append(ft.Divider(height=default_card_spacing, color="transparent"))
        
        return ft.Column(controls, spacing=0)


# 兼容别名
通用卡片 = UniversalCard


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    config = 界面配置()
    
    def main(page: ft.Page):
        page.padding = 20
        page.bgcolor = config.获取颜色("bg_primary")
        
        from 组件层.自定义下拉框 import CustomDropDown
        from 组件层.椭圆开关 import EllipseSwitch
        
        dropdown = CustomDropDown(config=config, options=["01", "02", "03"], value="01")
        switch = EllipseSwitch(config=config, value=False)
        
        page.add(ft.Text("单行卡片（下拉框）:", color=config.获取颜色("text_secondary")))
        page.add(UniversalCard.create(
            config=config,
            title="功能设置",
            description="请选择一个选项",
            icon="SETTINGS",
            controls=[dropdown.create()],
            help_text="点击切换启用/禁用状态",
        ))
        
        page.add(ft.Divider(height=20, color="transparent"))
        page.add(ft.Text("单行卡片（开关）:", color=config.获取颜色("text_secondary")))
        page.add(UniversalCard.create(
            config=config,
            title="功能开关",
            description="开启或关闭此功能",
            icon="POWER_SETTINGS_NEW",
            controls=[switch.create()],
            help_text="点击切换启用/禁用状态",
        ))
        
        page.add(ft.Divider(height=20, color="transparent"))
        page.add(ft.Text("多行卡片:", color=config.获取颜色("text_secondary")))
        
        level_options = [f"{i:02d}" for i in range(1, 13)]
        controls = [
            CustomDropDown(config=config, width=70, options=level_options, value="01").create(),
            CustomDropDown(config=config, width=70, options=level_options, value="02").create(),
            CustomDropDown(config=config, width=70, options=level_options, value="03").create(),
            CustomDropDown(config=config, width=70, options=level_options, value="04").create(),
            CustomDropDown(config=config, width=70, options=level_options, value="05").create(),
            CustomDropDown(config=config, width=70, options=level_options, value="06").create(),
            CustomDropDown(config=config, width=70, options=level_options, value="07").create(),
            CustomDropDown(config=config, width=70, options=level_options, value="08").create(),
        ]
        
        def on_state_change(enabled):
            print(f"状态变化: {'启用' if enabled else '禁用'}")
        
        page.add(UniversalCard.create(
            config=config,
            title="多行测试",
            icon="HOME",
            controls=controls,
            enabled=True,
            on_state_change=on_state_change,
            help_text="点击切换启用/禁用状态，禁用后该配置不会生效",
        ))
    
    ft.run(main)
