# -*- coding: utf-8 -*-
"""
控件工厂 - 零件层

设计思路:
    根据配置动态创建控件，支持多种控件类型。
    使用工厂模式，统一控件创建接口。

功能:
    1. 创建标准控件（下拉框、输入框、开关等）
    2. 创建色块控件（主题色块、调色板色块）
    3. 支持配置驱动创建
    4. 支持控件缓存和复用

数据来源:
    卡片配置文件。

使用场景:
    被通用卡片组件调用。
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft
from typing import Callable, List, Dict, Any
from 配置.界面配置 import 界面配置
from 新思路.零件层.标签下拉框 import LabelDropdown
from 新思路.零件层.标签输入框 import LabelInput
from 新思路.零件层.主题色块 import ThemeColorBlock


class ControlFactory:
    """控件工厂 - 根据配置创建控件"""
    
    @staticmethod
    def create_controls(
        config: 界面配置,
        card_config: Dict[str, Any],
        config_manager: Any,
        on_value_change: Callable[[str, Any], None] = None,
    ) -> List[ft.Control]:
        """
        根据配置创建控件列表
        
        参数:
            config: 界面配置对象
            card_config: 卡片配置字典
            config_manager: 配置管理器
            on_value_change: 值变化回调函数
        
        返回:
            控件列表
        """
        card_type = card_config.get("card_type", "standard")
        
        if card_type == "standard":
            return ControlFactory._create_standard_controls(
                config, card_config, config_manager, on_value_change
            )
        elif card_type == "color_blocks":
            return ControlFactory._create_color_blocks(
                config, card_config, config_manager, on_value_change
            )
        elif card_type == "switch_dropdown":
            return ControlFactory._create_switch_dropdown_controls(
                config, card_config, config_manager, on_value_change
            )
        else:
            return []
    
    @staticmethod
    def _create_standard_controls(
        config: 界面配置,
        card_config: Dict[str, Any],
        config_manager: Any,
        on_value_change: Callable[[str, Any], None] = None,
    ) -> List[ft.Control]:
        """创建标准控件（下拉框、输入框、开关等）"""
        controls = []
        card_name = card_config.get("title", "")
        
        for control_config in card_config.get("controls", []):
            control_type = control_config.get("type")
            config_key = control_config.get("config_key")
            
            # 获取当前值
            current_value = config_manager.get_value(card_name, config_key)
            
            # 根据类型创建控件
            if control_type == "dropdown":
                control = ControlFactory._create_dropdown(
                    config=config,
                    control_config=control_config,
                    current_value=current_value,
                    on_change=lambda value, key=config_key: ControlFactory._handle_value_change(
                        card_name, key, value, config_manager, on_value_change
                    ),
                )
            elif control_type == "input":
                control = ControlFactory._create_input(
                    config=config,
                    control_config=control_config,
                    current_value=current_value,
                    on_change=lambda value, key=config_key: ControlFactory._handle_value_change(
                        card_name, key, value, config_manager, on_value_change
                    ),
                )
            else:
                continue
            
            controls.append(control)
        
        return controls
    
    @staticmethod
    def _create_color_blocks(
        config: 界面配置,
        card_config: Dict[str, Any],
        config_manager: Any,
        on_value_change: Callable[[str, Any], None] = None,
    ) -> List[ft.Control]:
        """创建色块控件"""
        blocks_config = card_config.get("blocks_config", {})
        card_name = card_config.get("title", "")
        config_key = blocks_config.get("config_key")
        
        # 获取当前选中的值
        current_selected = config_manager.get_value(card_name, config_key)
        
        # 创建色块引用字典（用于更新选中状态）
        blocks_refs = {}
        
        # 创建色块列表
        blocks = []
        for item in blocks_config.get("items", []):
            name = item.get("name")
            color = item.get("color")
            is_selected = name == current_selected
            
            block = ThemeColorBlock.create(
                config=config,
                theme_name=name,
                bg_color=color,
                is_selected=is_selected,
                accent_color=config.当前主题颜色.get("accent"),  # 添加accent_color参数，使用主题的强调色
                on_click=lambda clicked_name: ControlFactory._handle_block_click(
                    clicked_name=clicked_name,
                    card_name=card_name,
                    blocks_config=blocks_config,
                    config_manager=config_manager,
                    on_value_change=on_value_change,
                    blocks_refs=blocks_refs,
                ),
            )
            blocks_refs[name] = block
            blocks.append(block)
        
        return blocks
    
    @staticmethod
    def _create_dropdown(
        config: 界面配置,
        control_config: Dict[str, Any],
        current_value: Any,
        on_change: Callable[[Any], None] = None,
    ) -> ft.Control:
        """创建下拉框控件"""
        return LabelDropdown.create(
            config=config,
            label=control_config.get("label", ""),
            options=control_config.get("options", []),
            value=current_value or control_config.get("value"),
            width=control_config.get("width"),
            on_change=on_change,
        )
    
    @staticmethod
    def _create_input(
        config: 界面配置,
        control_config: Dict[str, Any],
        current_value: Any,
        on_change: Callable[[Any], None] = None,
    ) -> ft.Control:
        """创建输入框控件"""
        return LabelInput.create(
            config=config,
            label=control_config.get("label", ""),
            value=current_value or control_config.get("value", ""),
            width=control_config.get("width"),
            on_change=on_change,
        )
    
    @staticmethod
    def _create_switch_dropdown_controls(
        config: 界面配置,
        card_config: Dict[str, Any],
        config_manager: Any,
        on_value_change: Callable[[str, Any], None] = None,
    ) -> List[ft.Control]:
        """创建开关下拉控件"""
        from 新思路.组件层.开关下拉卡片 import SwitchDropdownCard
        
        card_name = card_config.get("title", "")
        enabled = card_config.get("enabled", True)
        
        # 获取开关配置
        switch_config = card_config.get("switch_config", {})
        switch_key = switch_config.get("config_key")
        switch_value = config_manager.get_value(card_name, switch_key)
        if switch_value is None:
            switch_value = switch_config.get("default_value", True)
        
        # 创建设置项列表
        settings = []
        for dropdown_config in card_config.get("dropdown_configs", []):
            dropdown_key = dropdown_config.get("config_key")
            dropdown_value = config_manager.get_value(card_name, dropdown_key)
            if dropdown_value is None:
                dropdown_value = dropdown_config.get("default_value", "")
            
            settings.append({
                "type": "dropdown",
                "label": dropdown_config.get("label", ""),
                "options": dropdown_config.get("options", []),
                "value": dropdown_value,
                "width": dropdown_config.get("width"),  # 不设置默认值，让被调模块使用自己的默认值
                "on_change": lambda value, key=dropdown_key: ControlFactory._handle_value_change(
                    card_name, key, value, config_manager, on_value_change
                ),
            })
        
        # 创建开关下拉卡片
        card = SwitchDropdownCard.create(
            config=config,
            title=card_config.get("title", ""),
            icon=card_config.get("icon", "TOGGLE_ON"),
            subtitle=card_config.get("subtitle", ""),
            enabled=switch_value if isinstance(switch_value, bool) else enabled,
            on_state_change=lambda new_enabled: ControlFactory._handle_value_change(
                card_name, switch_key, new_enabled, config_manager, on_value_change
            ),
            settings=settings,
        )
        
        return [card]
    
    @staticmethod
    def _handle_value_change(
        card_name: str,
        config_key: str,
        value: Any,
        config_manager: Any,
        on_value_change: Callable[[str, Any], None] = None,
    ):
        """处理值变化"""
        # 保存到配置管理器
        config_manager.set_value(card_name, config_key, value)
        
        # 调用外部回调
        if on_value_change:
            on_value_change(config_key, value)
    
    @staticmethod
    def _handle_block_click(
        clicked_name: str,
        card_name: str,
        blocks_config: Dict[str, Any],
        config_manager: Any,
        on_value_change: Callable[[str, Any], None] = None,
        blocks_refs: Dict[str, Any] = None,
    ):
        """处理色块点击"""
        config_key = blocks_config.get("config_key")
        supports_deselect = blocks_config.get("supports_deselect", False)
        current_selected = config_manager.get_value(card_name, config_key)
        
        # 支持取消选择
        if supports_deselect and clicked_name == current_selected:
            new_value = None
        else:
            new_value = clicked_name
        
        # 保存到配置管理器
        config_manager.set_value(card_name, config_key, new_value)
        
        # 更新所有色块的选中状态
        if blocks_refs:
            for name, block in blocks_refs.items():
                if hasattr(block, 'set_selected'):
                    block.set_selected(name == new_value)
        
        # 调用外部回调
        if on_value_change:
            on_value_change(config_key, new_value)


# 兼容别名
控件工厂 = ControlFactory


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    from 配置.配置管理器 import ConfigManager
    
    # 1. 界面配置初始化
    配置 = 界面配置()
    config_manager = ConfigManager()
    
    # 2. 测试创建标准控件
    print("测试创建标准控件:")
    basic_config = config_manager.get_card_config("基础设置")
    controls = ControlFactory.create_controls(配置, basic_config, config_manager)
    print(f"创建了 {len(controls)} 个控件")
    
    # 3. 测试创建色块控件
    print("\n测试创建色块控件:")
    theme_config = config_manager.get_card_config("主题设置")
    blocks = ControlFactory.create_controls(配置, theme_config, config_manager)
    print(f"创建了 {len(blocks)} 个色块")
    
    print("\n测试完成")
