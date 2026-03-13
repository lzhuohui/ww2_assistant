# -*- coding: utf-8 -*-
"""
图标标题v2 - 零件层（新思路）

设计思路:
    调用标签文本模块实现图标标题布局。
    以分割线为基准的布局模式。
    分割线高度可外部传入，与卡片高度联动。
    除分割线外，所有控件自适应。

功能:
    1. 图标：上方
    2. 主标题：下方（调用标签文本模块）
    3. 分割线：垂直分割线（可选，调用分割线模块）
    4. 副标题：分割线左侧（可选，调用标签文本模块）
    5. 状态切换：内置切换逻辑

布局规则:
    0. 全部控件边距为0
    1. 除分割线外，所有控件自适应
    2. 以分割线为基准
    3. 图标/主标题上下布置且中间对齐，交线与分割线中点水平对齐
    4. 副标题右侧和分割线左侧重合
    5. 副标题下部和主标题下部水平对齐

数据来源:
    所有配置数据从配置目录获取。

使用场景:
    被组件层模块调用，也可独立使用。

可独立运行调试: python 图标标题v2.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft
from typing import Callable, Optional
from 配置.界面配置 import 界面配置
from 新思路.零件层.标签文本 import LabelText
from 新思路.零件层.分割线 import Divider, CONTAINER_WIDTH, CONTAINER_HEIGHT, LINE_WIDTH


# *** 用户指定变量 - AI不得修改 ***
# 图标和标题尺寸（固定，不随分割线高度变化）
DEFAULT_ICON_SIZE = 24
DEFAULT_TITLE_SIZE = 14
DEFAULT_SUBTITLE_SIZE = 12
# 控件间距
ICON_TITLE_SPACING = 4
# 图标区域宽度（自适应：图标 + 间距 + 5个汉字）
ICON_AREA_WIDTH = DEFAULT_ICON_SIZE + ICON_TITLE_SPACING + 5 * DEFAULT_TITLE_SIZE  # 24 + 4 + 70 = 98
# *********************************


class IconTitleV2:
    """图标标题v2 - 调用标签文本模块实现布局"""
    
    def __init__(self, config):
        """初始化图标标题（支持调试逻辑）"""
        self.config = config
    
    def render(self):
        """渲染图标标题（支持调试逻辑）"""
        return IconTitleV2.create(
            config=self.config,
            title="测试标题",
            icon="HOME",
            enabled=True,
            subtitle="这是副标题",
        )
    
    @staticmethod
    def create(
        config: 界面配置,
        title: str,
        icon: str = None,
        enabled: bool = True,
        on_state_change: Callable[[bool], None] = None,
        on_click: Callable = None,
        subtitle: str = None,
        divider_height: int = None,
        divider_left: int = None,
        **kwargs
    ) -> ft.Container:
        """
        创建图标标题组件
        
        参数:
            config: 界面配置对象
            title: 标题文字
            icon: 图标名称（字符串）
            enabled: 初始启用状态
            on_state_change: 状态变化回调函数
            on_click: 点击回调函数（可选）
            subtitle: 副标题（可选）
            divider_height: 分割线高度（可选，默认CONTAINER_HEIGHT）
            divider_left: 分割线左侧位置（可选，默认CONTAINER_WIDTH）
        
        返回:
            ft.Container: 包含图标标题的容器
        """
        theme_colors = config.当前主题颜色
        weight_config = config.定义尺寸.get("字重", {})
        
        line_height = divider_height if divider_height is not None else CONTAINER_HEIGHT
        
        # ========== 创建图标控件 ==========
        icon_control = None
        if icon:
            if isinstance(icon, str):
                icon_name = icon.upper()
                icon_value = getattr(ft.Icons, icon_name, ft.Icons.SETTINGS)
            else:
                icon_value = icon
            icon_control = ft.Icon(
                icon_value,
                size=DEFAULT_ICON_SIZE,
                color=theme_colors.get("accent"),
                opacity=1.0 if enabled else 0.4,
            )
        
        # ========== 创建主标题（调用标签文本模块）==========
        title_control = LabelText.create(
            config=config,
            text=title,
            role="primary",
            enabled=enabled,
        )
        
        # ========== 创建副标题（调用标签文本模块）==========
        subtitle_control = None
        if subtitle:
            subtitle_control = LabelText.create(
                config=config,
                text=subtitle,
                role="secondary",
                enabled=enabled,
            )
        
        # ========== 创建分割线（调用分割线模块）==========
        divider = Divider.create(
            config=config,
            height=line_height,
            enabled=enabled,
        )
        
        # ========== 计算布局（自适应）==========
        icon_height = DEFAULT_ICON_SIZE if icon_control else 0
        title_height = DEFAULT_TITLE_SIZE
        subtitle_height = DEFAULT_SUBTITLE_SIZE if subtitle else 0
        
        # 分割线容器宽度
        divider_width = CONTAINER_WIDTH
        
        # 图标+标题总高度（用于计算垂直中点）
        icon_title_total_height = icon_height + (ICON_TITLE_SPACING if icon_control else 0) + title_height
        
        # 图标+标题垂直中点位置
        icon_title_center_y = line_height / 2
        
        # 图标+标题顶部位置（使其中点与分割线中点对齐）
        icon_title_top = icon_title_center_y - icon_title_total_height / 2
        
        # 标题顶部位置（如果有图标，标题在图标下方）
        title_top = icon_title_top + icon_height + (ICON_TITLE_SPACING if icon_control else 0)
        
        # 副标题顶部位置（底部与分割线底部往上一个卡片边距）
        ui_config = config.定义尺寸.get("界面", {})
        card_padding = ui_config.get("card_padding", 16)
        subtitle_top = line_height - subtitle_height - card_padding
        
        # ========== 构建Stack布局 ==========
        stack_children = []
        
        # 1. 分割线（固定位置）
        if divider:
            divider_container = ft.Container(
                content=divider,
                left=ICON_AREA_WIDTH,  # 分割线位置
                top=0,
            )
            stack_children.append(divider_container)
        
        # 2. 标题（保持自适应宽度，水平中线到分割线的距离50）
        icon_title_items = [title_control]
        icon_title_column = ft.Column(
            icon_title_items,
            spacing=ICON_TITLE_SPACING,
            horizontal_alignment=ft.CrossAxisAlignment.END,  # 右对齐，保持自适应宽度
            alignment=ft.MainAxisAlignment.START,
            tight=True,
        )
        
        # 主标题文字水平中线到分割线的距离50
        title_center_to_divider = 50
        # 计算标题容器的左边缘位置：分割线位置 - 标题文字宽度/2 - 距离
        title_text_width = len(title) * DEFAULT_TITLE_SIZE
        title_container_left = ICON_AREA_WIDTH - title_text_width / 2 - title_center_to_divider
        
        icon_title_container = ft.Container(
            content=icon_title_column,
            left=title_container_left,
            top=title_top,  # 使用标题顶部位置
            # 不设置宽度，保持自适应
        )
        stack_children.append(icon_title_container)
        
        # 2.1 图标（单独放置，中线到分割线的距离50）
        if icon_control:
            # 图标的中线到分割线的距离50
            icon_center_to_divider = 50
            # 计算图标左边缘位置：分割线位置 - 图标宽度/2 - 距离
            icon_left = ICON_AREA_WIDTH - DEFAULT_ICON_SIZE / 2 - icon_center_to_divider
            # 图标垂直位置：标题顶部位置 - 图标高度 - 间距
            icon_top = title_top - DEFAULT_ICON_SIZE - ICON_TITLE_SPACING
            icon_container = ft.Container(
                content=icon_control,
                left=icon_left,
                top=icon_top,
            )
            stack_children.append(icon_container)
        
        # 3. 副标题（左侧距离分割线一个分割线容器宽度）
        if subtitle_control:
            subtitle_container = ft.Container(
                content=subtitle_control,
                left=ICON_AREA_WIDTH + divider_width + divider_width,  # 分割线右侧+一个分割线容器宽度
                top=subtitle_top,
            )
            stack_children.append(subtitle_container)
        
        # ========== 计算整体尺寸 ==========
        # 宽度 = 图标区域 + 分割线 + 副标题区域
        subtitle_width = 100 if subtitle else 0  # 副标题预留宽度
        overall_width = ICON_AREA_WIDTH + divider_width + divider_width + subtitle_width
        
        # 4. 透明点击区域（只在分割线左侧）
        click_area = ft.Container(
            width=ICON_AREA_WIDTH,
            height=line_height,
            # 透明背景，只用于捕获点击事件
        )
        stack_children.append(click_area)
        
        # ========== 构建Stack ==========
        content_stack = ft.Stack(
            stack_children,
            width=overall_width,
            height=line_height,
            clip_behavior=ft.ClipBehavior.NONE,
        )
        
        # ========== 创建主容器 ==========
        container = ft.Container(
            content=content_stack,
            height=line_height,
            width=overall_width,
            alignment=ft.Alignment(-1, -1),
        )
        
        container._enabled = enabled
        
        def set_state(new_enabled: bool, notify: bool = True):
            container._enabled = new_enabled
            
            if icon_control:
                icon_control.opacity = 1.0 if new_enabled else 0.4
                icon_control.update()
            
            if title_control:
                title_control.set_state(new_enabled)
            
            if divider:
                divider.opacity = 0.7 if new_enabled else 0.2
                divider.update()
            
            if subtitle_control:
                subtitle_control.set_state(new_enabled)
            
            if notify and on_state_change:
                on_state_change(new_enabled)
        
        def toggle_state(e=None):
            set_state(not container._enabled)
        
        def handle_click(e):
            toggle_state()
            if on_click:
                on_click(e)
        
        # 只在透明点击区域添加点击事件，副标题区域不会触发
        click_area.on_click = handle_click
        container.set_state = set_state
        container.toggle_state = toggle_state
        container.get_state = lambda: container._enabled
        
        def set_subtitle(new_text: str):
            if subtitle_control:
                subtitle_control.set_text(new_text)
        
        container.set_subtitle = set_subtitle
        
        return container


# 兼容别名
图标标题v2 = IconTitleV2


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    # 1. 界面配置初始化
    配置 = 界面配置()
    
    # 2. 自动加载用户数据覆盖默认值（在界面配置.__init__中自动完成）
    
    # 3. 正常启动被测模块
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        page.add(IconTitleV2(配置).render())  # 只能更改此处**被测调用模块名称**
    
    ft.run(main)
