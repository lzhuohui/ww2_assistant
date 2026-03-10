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
    3. 状态切换：双击左侧区域切换启用/禁用状态
    4. 悬停效果：统一的悬停视觉反馈

数据来源:
    主题颜色从界面配置获取。

使用场景:
    替代下拉卡片、开关卡片、多行卡片。

可独立运行调试: python 通用卡片.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import flet as ft
from typing import List, Callable, Optional, Any, Dict
from 原子层.界面配置 import 界面配置


# ==================== 用户指定变量区 ====================
# 单行模式
DEFAULT_CARD_HEIGHT = 70          # 单行卡片默认高度
DEFAULT_CARD_SPACING = 10         # 卡片之间的间距

# 多行模式
ITEMS_PER_ROW = 6                 # 每行控件数量
ROW_HEIGHT = 32                   # 每行高度
DIVIDER_WIDTH = 2                 # 分割线宽度
DIVIDER_HEIGHT = 60               # 分割线高度
DIVIDER_OPACITY = 0.7             # 分割线透明度
DIVIDER_BLUR = 6                  # 分割线模糊
LEFT_WIDTH = 60                   # 左侧区域宽度
DIVIDER_LEFT = 90                 # 分割线左边距
CONTENT_LEFT = 130                # 内容区域左边距

# 通用
DEFAULT_ICON_SIZE = 24            # 图标大小
DEFAULT_TITLE_SIZE = 14           # 标题字体大小
DEFAULT_DESC_SIZE = 12            # 描述字体大小

# Win11 Fluent Design 阴影配置
SHADOW_BLUR_DEFAULT = 4           # 默认阴影模糊半径（Win11风格：轻微深度）
SHADOW_BLUR_HOVER = 8             # 悬停阴影模糊半径（Win11风格：增强深度）
SHADOW_SPREAD = 0                 # 阴影扩散半径
SHADOW_OFFSET_Y = 2               # 阴影Y轴偏移（模拟光源从上方照射）
CARD_BORDER_RADIUS = 8            # 卡片圆角（Win11风格：8px）
CARD_BORDER_WIDTH = 1             # 卡片边框宽度
# ========================================================


class UniversalCard:  # 通用卡片组件
    """通用卡片 - 统一的单行/多行卡片组件"""
    
    @staticmethod
    def create(
        config: 界面配置,
        title: str,
        icon: str = None,
        description: str = None,
        controls: List[ft.Control] = None,
        items_per_row: int = ITEMS_PER_ROW,
        enabled: bool = True,
        on_state_change: Callable[[bool], None] = None,
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
        
        current_enabled = enabled
        control_list = controls or []
        
        is_single_row = len(control_list) == 1
        
        card_height = height or (DEFAULT_CARD_HEIGHT if is_single_row else None)
        card_width = width or ui_config.get("card_width", 800)
        
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
                size=DEFAULT_ICON_SIZE,
                color=theme_colors.get("accent"),
                opacity=1.0 if current_enabled else 0.4,
            )
        
        title_control = ft.Text(
            title,
            size=DEFAULT_TITLE_SIZE,
            weight=weight_config.get("font_weight_medium", ft.FontWeight.W_500),
            color=theme_colors.get("text_primary"),
            opacity=1.0 if current_enabled else 0.4,
        )
        
        desc_control = None
        if description and is_single_row:
            desc_control = ft.Text(
                description,
                size=DEFAULT_DESC_SIZE,
                color=theme_colors.get("text_secondary"),
                opacity=1.0 if current_enabled else 0.4,
            )
        
        if is_single_row:
            left_content = ft.Row(
                [
                    icon_control if icon_control else ft.Container(),
                    ft.Column(
                        [
                            title_control,
                            desc_control if desc_control else ft.Container(),
                        ],
                        spacing=4,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
                spacing=12,
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            )
            
            left_container = ft.Container(
                content=left_content,
                left=ui_config.get("card_padding", 16),
                top=0,
                bottom=0,
                alignment=ft.Alignment(-1, 0),
            )
        else:
            left_content = ft.Column(
                [
                    icon_control,
                    title_control,
                ],
                spacing=spacing_config.get("spacing_xs", 4),
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
            )
            
            left_gesture = ft.GestureDetector(
                content=left_content,
                on_double_tap=None,
            )
            
            left_container = ft.Container(
                content=left_gesture,
                left=ui_config.get("card_padding", 16),
                top=0,
                bottom=0,
                width=LEFT_WIDTH,
                alignment=ft.Alignment(0, 0),
            )
        
        divider = None
        if not is_single_row:
            divider = ft.Container(
                width=DIVIDER_WIDTH,
                height=DIVIDER_HEIGHT,
                bgcolor=theme_colors.get("accent"),
                opacity=DIVIDER_OPACITY if current_enabled else 0.2,
                shadow=ft.BoxShadow(
                    blur_radius=DIVIDER_BLUR,
                    color=theme_colors.get("accent"),
                    spread_radius=0,
                ) if current_enabled else None,
                left=DIVIDER_LEFT,
                top=0,
                bottom=0,
            )
        
        if is_single_row:
            single_control = control_list[0] if control_list else ft.Container()
            
            right_container = ft.Container(
                content=single_control,
                right=ui_config.get("card_padding", 16),
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
            for i in range(0, len(control_list), items_per_row):
                row_items = control_list[i:i+items_per_row]
                row = ft.Row(
                    row_items,
                    spacing=spacing_config.get("spacing_md", 12),
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                )
                rows.append(row)
            
            row_count = len(rows)
            row_spacing = spacing_config.get("spacing_sm", 8)
            padding_vertical = ui_config.get("item_padding", 12) * 2
            content_height = row_count * ROW_HEIGHT + (row_count - 1) * row_spacing if row_count > 0 else 0
            stack_height = content_height + padding_vertical
            
            right_content = ft.Column(
                rows,
                spacing=row_spacing,
                opacity=1.0 if current_enabled else 0.5,
            )
            
            right_container = ft.Container(
                content=right_content,
                left=CONTENT_LEFT,
                right=ui_config.get("card_padding", 16),
                top=ui_config.get("item_padding", 12),
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
            border_radius=CARD_BORDER_RADIUS,
            border=ft.Border.all(CARD_BORDER_WIDTH, theme_colors.get("border_light")),
            shadow=ft.BoxShadow(
                spread_radius=SHADOW_SPREAD,
                blur_radius=SHADOW_BLUR_DEFAULT,
                color=theme_colors.get("shadow"),
                offset=ft.Offset(0, SHADOW_OFFSET_Y),
            ),
            animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
            clip_behavior=ft.ClipBehavior.NONE,
        )
        
        def toggle_state(e):  # 切换启用/禁用状态
            nonlocal current_enabled
            current_enabled = not current_enabled
            
            if icon_control:
                icon_control.opacity = 1.0 if current_enabled else 0.4
                icon_control.update()
            title_control.opacity = 1.0 if current_enabled else 0.4
            title_control.update()
            
            if divider:
                divider.opacity = DIVIDER_OPACITY if current_enabled else 0.2
                divider.update()
            
            if not is_single_row and right_content:
                right_content.opacity = 1.0 if current_enabled else 0.5
                right_content.update()
            
            if on_state_change:
                on_state_change(current_enabled)
        
        if not is_single_row:
            left_gesture.on_double_tap = toggle_state
        
        def on_hover(e):  # 悬停效果
            if e.data == "true":
                container.bgcolor = theme_colors.get("bg_hover")
                container.border = ft.Border.all(CARD_BORDER_WIDTH, theme_colors.get("border"))
                container.shadow = ft.BoxShadow(
                    spread_radius=SHADOW_SPREAD,
                    blur_radius=SHADOW_BLUR_HOVER,
                    color=theme_colors.get("shadow"),
                    offset=ft.Offset(0, SHADOW_OFFSET_Y + 1),
                )
            else:
                container.bgcolor = theme_colors.get("bg_card")
                container.border = ft.Border.all(CARD_BORDER_WIDTH, theme_colors.get("border_light"))
                container.shadow = ft.BoxShadow(
                    spread_radius=SHADOW_SPREAD,
                    blur_radius=SHADOW_BLUR_DEFAULT,
                    color=theme_colors.get("shadow"),
                    offset=ft.Offset(0, SHADOW_OFFSET_Y),
                )
            container.update()
        
        container.on_hover = on_hover
        
        return container
    
    @staticmethod
    def create_list(
        config: 界面配置,
        card_configs: List[dict],
    ) -> ft.Column:
        controls = []
        
        for i, card_config in enumerate(card_configs):
            card = UniversalCard.create(
                config=config,
                title=card_config.get("title"),
                icon=card_config.get("icon"),
                description=card_config.get("description"),
                controls=card_config.get("controls"),
                items_per_row=card_config.get("items_per_row", ITEMS_PER_ROW),
                enabled=card_config.get("enabled", True),
                on_state_change=card_config.get("on_state_change"),
                height=card_config.get("height"),
                width=card_config.get("width"),
            )
            controls.append(card)
            
            if i < len(card_configs) - 1:
                controls.append(ft.Divider(height=DEFAULT_CARD_SPACING, color="transparent"))
        
        return ft.Column(controls, spacing=0)


# 兼容别名
通用卡片 = UniversalCard
下拉卡片 = UniversalCard
开关卡片 = UniversalCard
多行卡片 = UniversalCard


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
        ))
        
        page.add(ft.Divider(height=20, color="transparent"))
        page.add(ft.Text("单行卡片（开关）:", color=config.获取颜色("text_secondary")))
        page.add(UniversalCard.create(
            config=config,
            title="功能开关",
            description="开启或关闭此功能",
            icon="POWER_SETTINGS_NEW",
            controls=[switch.create()],
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
        ))
    
    ft.run(main)
