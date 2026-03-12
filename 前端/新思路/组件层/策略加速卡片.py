# -*- coding: utf-8 -*-
"""
策略加速卡片 - 组件层（新思路）

设计思路:
    组装零件，构建策略加速卡片。
    采用装配模式，协调各零件交互。
    三级控制：左侧总开关 + 右侧速建/速产/保留独立开关

功能:
    1. 左侧：图标+标题+总开关
    2. 右侧第1行：圆形开关 + 速建限级下拉框 + 建筑类型下拉框
    3. 右侧第2行：圆形开关 + 速产限级下拉框 + 策略类型下拉框
    4. 右侧第3行：圆形开关 + 保留点数下拉框

数据来源:
    所有配置数据从配置目录获取。

使用场景:
    被页面层模块调用。

可独立运行调试: python 策略加速卡片.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft
from typing import Callable, Dict, Any
from 配置.界面配置 import 界面配置
from 新思路.组件层.通用卡片 import UniversalCard
from 新思路.零件层.圆形开关 import CircleSwitch
from 新思路.零件层.标签下拉框 import LabelDropdown


class StrategyCard:
    """策略加速卡片 - 组件层"""
    
    # 默认值定义
    默认值 = {
        "速建开关": True,
        "速建限级": "08",
        "速建类型": "城资建筑",
        "速产开关": True,
        "速产限级": "07",
        "速产类型": "平衡资源",
        "保留开关": True,
        "保留点数": "60",
    }
    
    @staticmethod
    def create(
        config: 界面配置,
        title: str = "策略加速",
        icon: str = "ROCKET_LAUNCH",
        enabled: bool = True,
        on_state_change: Callable[[bool], None] = None,
        help_text: str = None,
        speed_build_enabled: bool = True,
        speed_build_level: str = "08",
        speed_build_type: str = "城资建筑",
        speed_prod_enabled: bool = True,
        speed_prod_level: str = "07",
        speed_prod_type: str = "平衡资源",
        keep_points_enabled: bool = True,
        keep_points: str = "60",
        **kwargs
    ) -> ft.Container:
        """
        创建策略加速卡片
        
        参数:
            config: 界面配置对象
            title: 卡片标题
            icon: 图标名称
            enabled: 初始启用状态（左侧总开关）
            on_state_change: 状态变化回调
            help_text: 帮助提示文字
            speed_build_enabled: 建筑速建开关状态
            speed_build_level: 速建限级值
            speed_build_type: 速建类型值
            speed_prod_enabled: 资源速产开关状态
            speed_prod_level: 速产限级值
            speed_prod_type: 速产类型值
            keep_points_enabled: 策点保留开关状态
            keep_points: 保留点数值
        
        返回:
            ft.Container: 策略加速卡片容器
        """
        theme_colors = config.当前主题颜色
        
        # 内部状态
        current_enabled = enabled
        current_speed_build_enabled = speed_build_enabled
        current_speed_prod_enabled = speed_prod_enabled
        current_keep_points_enabled = keep_points_enabled
        
        # 等级选项 (05-15)
        level_options = [f"{i:02d}" for i in range(5, 16)]
        # 保留点数选项
        points_options = ["30", "60", "90", "120", "150", "180", "210", "240"]
        # 建筑类型选项
        build_type_options = ["城资建筑", "城市建筑", "资源建筑"]
        # 策略类型选项
        prod_type_options = ["平衡资源", "战时经济", "钢铁熔炉", "橡胶采集", "石油开采"]
        
        # ========== 第1行：建筑速建 ==========
        speed_build_switch = CircleSwitch.create(
            config=config,
            value=speed_build_enabled,
            on_change=lambda v: handle_speed_build_switch_change(v),
        )
        
        speed_build_level_dropdown = LabelDropdown.create(
            config=config,
            label="速建限级",
            options=level_options,
            value=speed_build_level,
            width=120,
            enabled=current_enabled and current_speed_build_enabled,
        )
        
        speed_build_type_dropdown = LabelDropdown.create(
            config=config,
            label="建筑类型",
            options=build_type_options,
            value=speed_build_type,
            width=120,
            enabled=current_enabled and current_speed_build_enabled,
        )
        
        row1 = ft.Row(
            [
                speed_build_switch,
                speed_build_level_dropdown,
                speed_build_type_dropdown,
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        
        # ========== 第2行：资源速产 ==========
        speed_prod_switch = CircleSwitch.create(
            config=config,
            value=speed_prod_enabled,
            on_change=lambda v: handle_speed_prod_switch_change(v),
        )
        
        speed_prod_level_dropdown = LabelDropdown.create(
            config=config,
            label="速产限级",
            options=level_options,
            value=speed_prod_level,
            width=120,
            enabled=current_enabled and current_speed_prod_enabled,
        )
        
        speed_prod_type_dropdown = LabelDropdown.create(
            config=config,
            label="策略类型",
            options=prod_type_options,
            value=speed_prod_type,
            width=120,
            enabled=current_enabled and current_speed_prod_enabled,
        )
        
        row2 = ft.Row(
            [
                speed_prod_switch,
                speed_prod_level_dropdown,
                speed_prod_type_dropdown,
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        
        # ========== 第3行：策点保留 ==========
        keep_points_switch = CircleSwitch.create(
            config=config,
            value=keep_points_enabled,
            on_change=lambda v: handle_keep_points_switch_change(v),
        )
        
        keep_points_dropdown = LabelDropdown.create(
            config=config,
            label="保留点数",
            options=points_options,
            value=keep_points,
            width=120,
            enabled=current_enabled and current_keep_points_enabled,
        )
        
        row3 = ft.Row(
            [
                keep_points_switch,
                keep_points_dropdown,
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        
        # ========== 右侧内容（每行作为单独控件传入）==========
        right_controls = [row1, row2, row3]
        
        # ========== 事件处理 ==========
        def handle_speed_build_switch_change(new_value: bool):
            nonlocal current_speed_build_enabled
            current_speed_build_enabled = new_value
            update_dropdowns_state("speed_build", current_enabled and current_speed_build_enabled)
            if on_state_change:
                on_state_change(current_enabled)
        
        def handle_speed_prod_switch_change(new_value: bool):
            nonlocal current_speed_prod_enabled
            current_speed_prod_enabled = new_value
            update_dropdowns_state("speed_prod", current_enabled and current_speed_prod_enabled)
            if on_state_change:
                on_state_change(current_enabled)
        
        def handle_keep_points_switch_change(new_value: bool):
            nonlocal current_keep_points_enabled
            current_keep_points_enabled = new_value
            update_dropdowns_state("keep_points", current_enabled and current_keep_points_enabled)
            if on_state_change:
                on_state_change(current_enabled)
        
        def update_dropdowns_state(group: str, enabled: bool):
            if group == "speed_build":
                speed_build_level_dropdown.disabled = not enabled
                speed_build_level_dropdown.opacity = 1.0 if enabled else 0.4
                speed_build_level_dropdown.update()
                speed_build_type_dropdown.disabled = not enabled
                speed_build_type_dropdown.opacity = 1.0 if enabled else 0.4
                speed_build_type_dropdown.update()
            elif group == "speed_prod":
                speed_prod_level_dropdown.disabled = not enabled
                speed_prod_level_dropdown.opacity = 1.0 if enabled else 0.4
                speed_prod_level_dropdown.update()
                speed_prod_type_dropdown.disabled = not enabled
                speed_prod_type_dropdown.opacity = 1.0 if enabled else 0.4
                speed_prod_type_dropdown.update()
            elif group == "keep_points":
                keep_points_dropdown.disabled = not enabled
                keep_points_dropdown.opacity = 1.0 if enabled else 0.4
                keep_points_dropdown.update()
        
        def update_all_children_state(new_enabled: bool):
            speed_build_switch.set_enabled(new_enabled)
            speed_prod_switch.set_enabled(new_enabled)
            keep_points_switch.set_enabled(new_enabled)
            update_dropdowns_state("speed_build", new_enabled and current_speed_build_enabled)
            update_dropdowns_state("speed_prod", new_enabled and current_speed_prod_enabled)
            update_dropdowns_state("keep_points", new_enabled and current_keep_points_enabled)
        
        def handle_total_state_change(new_enabled: bool):
            nonlocal current_enabled
            current_enabled = new_enabled
            update_all_children_state(new_enabled)
            if on_state_change:
                on_state_change(new_enabled)
        
        # ========== 创建卡片 ==========
        card = UniversalCard.create(
            config=config,
            title=title,
            icon=icon,
            enabled=enabled,
            on_state_change=handle_total_state_change,
            help_text=help_text,
            controls=right_controls,
        )
        
        # ========== 暴露控制接口 ==========
        def get_speed_build_enabled() -> bool:
            return current_speed_build_enabled
        
        def get_speed_prod_enabled() -> bool:
            return current_speed_prod_enabled
        
        def get_keep_points_enabled() -> bool:
            return current_keep_points_enabled
        
        def get_speed_build_level() -> str:
            return speed_build_level_dropdown.get_value()
        
        def get_speed_build_type() -> str:
            return speed_build_type_dropdown.get_value()
        
        def get_speed_prod_level() -> str:
            return speed_prod_level_dropdown.get_value()
        
        def get_speed_prod_type() -> str:
            return speed_prod_type_dropdown.get_value()
        
        def get_keep_points() -> str:
            return keep_points_dropdown.get_value()
        
        def get_all_values() -> Dict[str, Any]:
            return {
                "速建开关": current_speed_build_enabled,
                "速建限级": speed_build_level_dropdown.get_value(),
                "速建类型": speed_build_type_dropdown.get_value(),
                "速产开关": current_speed_prod_enabled,
                "速产限级": speed_prod_level_dropdown.get_value(),
                "速产类型": speed_prod_type_dropdown.get_value(),
                "保留开关": current_keep_points_enabled,
                "保留点数": keep_points_dropdown.get_value(),
            }
        
        def get_effective_values() -> Dict[str, Any]:
            """获取有效值（总开关开启时返回当前值，关闭时返回默认值）"""
            if card.get_state():
                return get_all_values()
            else:
                return StrategyCard.默认值.copy()
        
        card.get_speed_build_enabled = get_speed_build_enabled
        card.get_speed_prod_enabled = get_speed_prod_enabled
        card.get_keep_points_enabled = get_keep_points_enabled
        card.get_speed_build_level = get_speed_build_level
        card.get_speed_build_type = get_speed_build_type
        card.get_speed_prod_level = get_speed_prod_level
        card.get_speed_prod_type = get_speed_prod_type
        card.get_keep_points = get_keep_points
        card.get_all_values = get_all_values
        card.get_effective_values = get_effective_values
        
        return card


# 兼容别名
策略加速卡片 = StrategyCard


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    # 1. 界面配置初始化
    配置 = 界面配置()
    
    # 2. 自动加载用户数据覆盖默认值（在界面配置.__init__中自动完成）
    
    # 3. 正常启动被测模块
    def main(page: ft.Page):
        page.padding = 20
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        
        page.add(StrategyCard.create(
            配置,
            title="策略加速",
            icon="ROCKET_LAUNCH",
            enabled=True,
            speed_build_enabled=True,
            speed_build_level="08",
            speed_build_type="城资建筑",
            speed_prod_enabled=True,
            speed_prod_level="07",
            speed_prod_type="平衡资源",
            keep_points_enabled=True,
            keep_points="60",
        ))
    
    ft.run(main)
