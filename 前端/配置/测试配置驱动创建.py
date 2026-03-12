# -*- coding: utf-8 -*-
"""
测试配置驱动创建方法

测试目标:
    验证通用卡片的配置驱动创建方法是否正常工作。

测试步骤:
    1. 创建配置管理器
    2. 使用配置驱动创建基础设置卡片
    3. 使用配置驱动创建主题设置卡片
    4. 验证卡片功能
"""

import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import flet as ft
from 前端.配置.配置管理器 import ConfigManager
from 前端.配置.界面配置 import 界面配置
from 前端.新思路.组件层.通用卡片 import UniversalCard


def test_config_driven_creation():
    """测试配置驱动创建方法"""
    print("=" * 60)
    print("测试配置驱动创建方法")
    print("=" * 60)
    
    # 1. 创建配置管理器
    print("\n1. 创建配置管理器")
    config_manager = ConfigManager()
    print("   ✅ 配置管理器创建成功")
    
    # 2. 创建界面配置
    print("\n2. 创建界面配置")
    ui_config = 界面配置()
    print("   ✅ 界面配置创建成功")
    
    # 3. 测试创建基础设置卡片
    print("\n3. 测试创建基础设置卡片")
    try:
        basic_card = UniversalCard.create_from_config(
            config=ui_config,
            card_name="基础设置",
            config_manager=config_manager,
        )
        print("   ✅ 基础设置卡片创建成功")
        print(f"   卡片类型: {type(basic_card)}")
    except Exception as e:
        print(f"   ❌ 基础设置卡片创建失败: {e}")
    
    # 4. 测试创建主题设置卡片
    print("\n4. 测试创建主题设置卡片")
    try:
        theme_card = UniversalCard.create_from_config(
            config=ui_config,
            card_name="主题设置",
            config_manager=config_manager,
        )
        print("   ✅ 主题设置卡片创建成功")
        print(f"   卡片类型: {type(theme_card)}")
    except Exception as e:
        print(f"   ❌ 主题设置卡片创建失败: {e}")
    
    # 5. 测试创建调色板设置卡片
    print("\n5. 测试创建调色板设置卡片")
    try:
        palette_card = UniversalCard.create_from_config(
            config=ui_config,
            card_name="调色板设置",
            config_manager=config_manager,
        )
        print("   ✅ 调色板设置卡片创建成功")
        print(f"   卡片类型: {type(palette_card)}")
    except Exception as e:
        print(f"   ❌ 调色板设置卡片创建失败: {e}")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)


if __name__ == "__main__":
    test_config_driven_creation()
