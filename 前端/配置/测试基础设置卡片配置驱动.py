# -*- coding: utf-8 -*-
"""
测试基础设置卡片配置驱动创建

测试目标:
    验证基础设置卡片是否可以通过配置驱动方式创建。

测试步骤:
    1. 创建配置管理器
    2. 使用配置驱动创建基础设置卡片
    3. 验证卡片功能
    4. 测试值变化回调
"""

import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import flet as ft
from 前端.配置.配置管理器 import ConfigManager
from 前端.配置.界面配置 import 界面配置


def test_basic_settings_card():
    """测试基础设置卡片配置驱动创建"""
    print("=" * 60)
    print("测试基础设置卡片配置驱动创建")
    print("=" * 60)
    
    # 1. 创建配置管理器
    print("\n1. 创建配置管理器")
    config_manager = ConfigManager()
    print("   ✅ 配置管理器创建成功")
    
    # 2. 创建界面配置
    print("\n2. 创建界面配置")
    ui_config = 界面配置()
    print("   ✅ 界面配置创建成功")
    
    # 3. 导入通用卡片配置驱动扩展
    print("\n3. 导入通用卡片配置驱动扩展")
    try:
        from 前端.新思路.组件层.通用卡片配置驱动扩展 import UniversalCard
        print("   ✅ 导入成功")
    except Exception as e:
        print(f"   ❌ 导入失败: {e}")
        return
    
    # 4. 测试创建基础设置卡片
    print("\n4. 测试创建基础设置卡片")
    
    def on_value_change(config_key: str, value: any):
        """值变化回调"""
        print(f"   配置变化: {config_key} = {value}")
    
    try:
        basic_card = UniversalCard.create_from_config(
            config=ui_config,
            card_name="基础设置",
            config_manager=config_manager,
            on_value_change=on_value_change,
        )
        print("   ✅ 基础设置卡片创建成功")
        print(f"   卡片类型: {type(basic_card)}")
        print(f"   卡片标题: 基础设置")
        
        # 验证卡片功能
        if hasattr(basic_card, 'set_state'):
            print("   ✅ 卡片支持set_state方法")
        else:
            print("   ❌ 卡片不支持set_state方法")
        
        if hasattr(basic_card, 'get_state'):
            print("   ✅ 卡片支持get_state方法")
        else:
            print("   ❌ 卡片不支持get_state方法")
        
    except Exception as e:
        print(f"   ❌ 基础设置卡片创建失败: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # 5. 测试配置值
    print("\n5. 测试配置值")
    挂机模式 = config_manager.get_value("基础设置", "挂机模式")
    print(f"   挂机模式: {挂机模式}")
    
    指令速度 = config_manager.get_value("基础设置", "指令速度")
    print(f"   指令速度: {指令速度}")
    
    # 6. 测试设置配置值
    print("\n6. 测试设置配置值")
    config_manager.set_value("基础设置", "挂机模式", "手动挂机")
    新挂机模式 = config_manager.get_value("基础设置", "挂机模式")
    print(f"   设置挂机模式为'手动挂机': {新挂机模式}")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)


if __name__ == "__main__":
    test_basic_settings_card()
