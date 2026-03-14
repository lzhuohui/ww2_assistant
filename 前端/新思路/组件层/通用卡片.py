# -*- coding: utf-8 -*-
"""
通用卡片 - 组件层（新思路）

设计思路:
    装配模式：组合零件模块，协调交互。
    - 不直接操作零件内部控件
    - 通过零件暴露的接口进行控制
    - 负责布局和协调
    - 支持多行控件布局

功能:
    1. 组合零件模块
    2. 协调状态切换
    3. 布局排列
    4. 支持多行控件
    5. 支持副标题（与主标题底部对齐）

数据来源:
    所有配置数据从配置目录获取。

使用场景:
    被扩展卡片模块调用，也可直接使用。

可独立运行调试: python 通用卡片.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft
from typing import Callable, Optional, List, Dict, Any
from 配置.界面配置 import 界面配置
from 新思路.零件层.卡片容器 import CardContainer
from 新思路.零件层.图标标题 import IconTitle
from 新思路.零件层.标签下拉框 import LabelDropdown
from 新思路.零件层.控件工厂 import ControlFactory

# *** 用户指定变量 - AI不得修改 ***
# 布局参数
DEFAULT_CARD_WIDTH = 800 # 卡片宽度（像素）
DEFAULT_CONTROL_MARGIN_RIGHT = 20 # 控件右边距
DEFAULT_CONTROL_H_SPACING = 16 # 控件水平间距
DEFAULT_CONTROL_V_SPACING = 8 # 控件垂直间距
DEFAULT_CONTROLS_PER_ROW = 1 # 每行控件数量
# *********************************


class UniversalCard:
    """通用卡片 - 装配模式，组合零件模块，支持多行控件"""
    
    def __init__(self, config):
        """初始化通用卡片（支持调试逻辑）"""
        self.config = config
    
    def render(self):
        """渲染通用卡片（支持调试逻辑）"""
        return UniversalCard.create(
            config=self.config,
            title="测试卡片",
            icon="HOME",
            enabled=True,
            help_text="点击切换状态",
            controls=[
                LabelDropdown.create(
                    config=self.config,
                    label="模式",
                    options=["自动挂机", "手动挂机", "半自动挂机"],
                    value="自动挂机",
                ),
                LabelDropdown.create(
                    config=self.config,
                    label="策略",
                    options=["策略A", "策略B", "策略C"],
                    value="策略A",
                ),
            ],
            subtitle="这是副标题",
        )
    
    @staticmethod
    def create(
        config: 界面配置,
        title: str,
        icon: str = None,
        enabled: bool = True,
        on_state_change: Callable[[bool], None] = None,
        help_text: str = None,
        height: int = None,
        width: int = None,
        controls: List[ft.Control] = None,
        subtitle: str = None,
        controls_per_row: int = None,
        **kwargs
    ) -> ft.Container:
        """
        创建通用卡片
        
        参数:
            config: 界面配置对象
            title: 标题文字
            icon: 图标名称
            enabled: 初始启用状态
            on_state_change: 状态变化回调
            help_text: 帮助提示文字
            height: 卡片高度
            width: 卡片宽度
            controls: 右侧控件列表（支持多行）
            subtitle: 副标题（与主标题底部对齐）
            controls_per_row: 每行控件数量（默认使用 DEFAULT_CONTROLS_PER_ROW）
        
        返回:
            ft.Container: 完整的卡片容器
        """
        ui_config = config.定义尺寸.get("界面", {})
        card_config = config.定义尺寸.get("卡片", {})
        
        card_padding = ui_config.get("card_padding", 16)
        
        card_width = width or DEFAULT_CARD_WIDTH
        
        current_enabled = enabled
        current_controls_per_row = controls_per_row if controls_per_row is not None else DEFAULT_CONTROLS_PER_ROW
        parts: List = []
        
        # ========== 第一步：计算所有布局参数 ==========
        num_rows = 0
        total_controls_height = 0
        
        # 计算最小卡片高度（一个控件的高度 + padding）
        min_control_height = 35  # 单个控件默认高度
        min_card_height = min_control_height + card_padding * 2  # 最小卡片高度 = 控件高度 + 上下padding
        
        card_height = min_card_height  # 卡片高度默认值（最小高度）
        
        if controls:
            control_v_spacing = DEFAULT_CONTROL_V_SPACING
            
            # 计算每行控件的最大高度
            num_controls = len(controls)
            num_rows = (num_controls + current_controls_per_row - 1) // current_controls_per_row
            
            # 获取每个控件的实际高度
            for i, control in enumerate(controls):
                control_height = getattr(control, 'height', 35) or 35
                # 累加每行的高度
                if i % current_controls_per_row == 0:
                    total_controls_height += control_height
            
            calculated_height = total_controls_height + card_padding * (num_rows + 1)
            card_height = max(calculated_height, min_card_height)  # 确保不小于最小高度
        
        def on_icon_title_state_change(new_enabled: bool):
            nonlocal current_enabled
            current_enabled = new_enabled
            sync_parts_state(new_enabled)
            if on_state_change:
                on_state_change(new_enabled)
        
        # ========== 第二步：创建图标标题 ==========
        icon_title = IconTitle.create(
            config=config,
            title=title,
            icon=icon,
            enabled=current_enabled,
            on_state_change=on_icon_title_state_change,
            subtitle=subtitle,
            divider_height=card_height,
        )
        parts.append(icon_title)
        
        def sync_parts_state(new_enabled: bool):
            for part in parts:
                if hasattr(part, 'set_state'):
                    part.set_state(new_enabled, notify=False)
            # 同步控件的启用状态
            if controls:
                for control in controls:
                    # 设置透明度
                    control.opacity = 1.0 if new_enabled else 0.4
                    # 调用控件的set_state方法（如果存在）
                    if hasattr(control, 'set_state'):
                        control.set_state(new_enabled)
                    if control.page:
                        control.update()
        
        # ========== 第三步：创建左侧区域 ==========
        left_container = ft.Container(
            content=icon_title,
        )
        
        # ========== 第四步：创建右侧控件 ==========
        stack_children = [left_container]
        
        if controls:
            control_margin_right = DEFAULT_CONTROL_MARGIN_RIGHT
            control_h_spacing = DEFAULT_CONTROL_H_SPACING
            
            rows = []
            
            for row_idx in range(num_rows):
                start_idx = row_idx * current_controls_per_row
                end_idx = min(start_idx + current_controls_per_row, len(controls))
                row_controls = controls[start_idx:end_idx]
                
                row = ft.Row(
                    row_controls,
                    spacing=control_h_spacing,
                    alignment=ft.MainAxisAlignment.END,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                )
                rows.append(row)
            
            content_column = ft.Column(
                rows,
                spacing=card_padding,  # 行间距 = 标准卡片边距
                scroll=ft.ScrollMode.AUTO,
            )
            
            content_container = ft.Container(
                content=content_column,
                right=control_margin_right,
                top=card_padding,  # 上边距 = 标准卡片边距
            )
            stack_children.append(content_container)
        
        # ========== 创建主布局 ==========
        main_stack = ft.Stack(
            stack_children,
            height=card_height,
            width=card_width,
            clip_behavior=ft.ClipBehavior.NONE,
        )
        
        # ========== 创建卡片容器 ==========
        container = CardContainer.create(
            config=config,
            content=main_stack,
            height=card_height,
            width=card_width,
        )
        
        # ========== 暴露控制接口 ==========
        def set_state(new_enabled: bool):
            nonlocal current_enabled
            current_enabled = new_enabled
            icon_title.set_state(new_enabled, notify=False)
            sync_parts_state(new_enabled)
            if on_state_change:
                on_state_change(new_enabled)
        
        def toggle_state():
            set_state(not current_enabled)
        
        def get_state() -> bool:
            return current_enabled
        
        container.set_state = set_state
        container.toggle_state = toggle_state
        container.get_state = get_state
        
        def set_subtitle(new_text: str):
            if hasattr(icon_title, 'set_subtitle'):
                icon_title.set_subtitle(new_text)
        
        container.set_subtitle = set_subtitle
        
        return container
    
    @staticmethod
    def create_from_config(
        config: 界面配置,
        card_name: str,
        config_manager: Any,
        on_value_change: Callable[[str, Any], None] = None,
        dynamic_options: Dict[str, List[str]] = None,
        **kwargs
    ) -> ft.Container:
        """
        根据配置创建卡片
        
        参数:
            config: 界面配置对象
            card_name: 卡片名称
            config_manager: 配置管理器
            on_value_change: 值变化回调函数
            dynamic_options: 动态选项字典 {config_key: [options]}
        
        返回:
            ft.Container: 完整的卡片容器
        """
        card_config = config_manager.get_card_config(card_name)
        
        if not card_config:
            raise ValueError(f"未找到卡片配置: {card_name}")
        
        card_type = card_config.get("card_type", "standard")
        
        controls = ControlFactory.create_controls(
            config=config,
            card_config=card_config,
            config_manager=config_manager,
            on_value_change=on_value_change,
            dynamic_options=dynamic_options,
        )
        
        if card_type == "switch_dropdown":
            return controls[0] if controls else None
        
        return UniversalCard.create(
            config=config,
            title=card_config.get("title"),
            icon=card_config.get("icon"),
            subtitle=card_config.get("subtitle"),
            controls=controls,
            controls_per_row=card_config.get("controls_per_row", 1),
            **kwargs
        )


# 兼容别名
通用卡片 = UniversalCard


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    # 1. 界面配置初始化
    配置 = 界面配置()
    
    # 2. 自动加载用户数据覆盖默认值（在界面配置.__init__中自动完成）
    
    # 3. 正常启动被测模块
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        page.add(UniversalCard(配置).render())
    
    ft.run(main)
