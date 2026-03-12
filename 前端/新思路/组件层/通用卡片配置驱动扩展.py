# -*- coding: utf-8 -*-
"""
通用卡片配置驱动扩展 - 组件层

设计思路:
    为通用卡片添加配置驱动创建方法，实现"调用通用卡片后通过简单路径处理即可实现各种卡片效果"的目标。

功能:
    1. 配置驱动创建卡片
    2. 自动创建控件
    3. 统一接口

数据来源:
    卡片配置文件。

使用场景:
    被页面层模块调用。
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft
from typing import Callable, Optional, List, Dict, Any
from 配置.界面配置 import 界面配置
from 新思路.组件层.通用卡片 import UniversalCard
from 新思路.零件层.控件工厂 import ControlFactory


class UniversalCardConfigDriven:
    """通用卡片配置驱动扩展"""
    
    @staticmethod
    def create_from_config(
        config: 界面配置,
        card_name: str,
        config_manager: Any,
        on_value_change: Callable[[str, Any], None] = None,
        **kwargs
    ) -> ft.Container:
        """
        根据配置创建卡片
        
        参数:
            config: 界面配置对象
            card_name: 卡片名称
            config_manager: 配置管理器
            on_value_change: 值变化回调函数
        
        返回:
            ft.Container: 完整的卡片容器
        """
        # 获取卡片配置
        card_config = config_manager.get_card_config(card_name)
        
        if not card_config:
            raise ValueError(f"未找到卡片配置: {card_name}")
        
        # 使用控件工厂创建控件
        controls = ControlFactory.create_controls(
            config=config,
            card_config=card_config,
            config_manager=config_manager,
            on_value_change=on_value_change,
        )
        
        # 调用原有的create方法
        return UniversalCard.create(
            config=config,
            title=card_config.get("title"),
            icon=card_config.get("icon"),
            subtitle=card_config.get("subtitle"),
            controls=controls,
            controls_per_row=card_config.get("controls_per_row", 1),
            **kwargs
        )


# 为UniversalCard类添加配置驱动创建方法
def create_from_config(
    config: 界面配置,
    card_name: str,
    config_manager: Any,
    on_value_change: Callable[[str, Any], None] = None,
    **kwargs
) -> ft.Container:
    """
    根据配置创建卡片
    
    参数:
        config: 界面配置对象
        card_name: 卡片名称
        config_manager: 配置管理器
        on_value_change: 值变化回调函数
    
    返回:
        ft.Container: 完整的卡片容器
    """
    return UniversalCardConfigDriven.create_from_config(
        config=config,
        card_name=card_name,
        config_manager=config_manager,
        on_value_change=on_value_change,
        **kwargs
    )


# 将方法添加到UniversalCard类
UniversalCard.create_from_config = staticmethod(create_from_config)


# 兼容别名
通用卡片配置驱动 = UniversalCardConfigDriven


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    from 配置.配置管理器 import ConfigManager
    
    # 1. 界面配置初始化
    配置 = 界面配置()
    config_manager = ConfigManager()
    
    # 2. 测试配置驱动创建
    print("测试配置驱动创建:")
    
    # 测试创建基础设置卡片
    try:
        basic_card = UniversalCard.create_from_config(
            config=配置,
            card_name="基础设置",
            config_manager=config_manager,
        )
        print("   ✅ 基础设置卡片创建成功")
    except Exception as e:
        print(f"   ❌ 基础设置卡片创建失败: {e}")
    
    # 测试创建主题设置卡片
    try:
        theme_card = UniversalCard.create_from_config(
            config=配置,
            card_name="主题设置",
            config_manager=config_manager,
        )
        print("   ✅ 主题设置卡片创建成功")
    except Exception as e:
        print(f"   ❌ 主题设置卡片创建失败: {e}")
    
    # 测试创建调色板设置卡片
    try:
        palette_card = UniversalCard.create_from_config(
            config=配置,
            card_name="调色板设置",
            config_manager=config_manager,
        )
        print("   ✅ 调色板设置卡片创建成功")
    except Exception as e:
        print(f"   ❌ 调色板设置卡片创建失败: {e}")
    
    print("\n测试完成")
