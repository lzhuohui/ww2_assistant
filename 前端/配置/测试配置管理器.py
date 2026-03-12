# -*- coding: utf-8 -*-
"""
测试配置管理器

测试目标:
    验证配置管理器的功能是否正常。

测试步骤:
    1. 创建配置管理器
    2. 测试获取卡片配置
    3. 测试获取/设置配置值
    4. 测试配置持久化
"""

import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from 前端.配置.配置管理器 import ConfigManager


def test_config_manager():
    """测试配置管理器"""
    print("=" * 60)
    print("测试配置管理器")
    print("=" * 60)
    
    # 1. 创建配置管理器
    print("\n1. 创建配置管理器")
    config_manager = ConfigManager()
    print("   ✅ 配置管理器创建成功")
    
    # 2. 测试获取卡片配置
    print("\n2. 测试获取卡片配置")
    basic_config = config_manager.get_card_config("基础设置")
    if basic_config:
        print(f"   ✅ 基础设置配置获取成功: {basic_config.get('title')}")
    else:
        print("   ❌ 基础设置配置获取失败")
    
    theme_config = config_manager.get_card_config("主题设置")
    if theme_config:
        print(f"   ✅ 主题设置配置获取成功: {theme_config.get('title')}")
    else:
        print("   ❌ 主题设置配置获取失败")
    
    # 3. 测试获取配置值
    print("\n3. 测试获取配置值")
    # 测试基础设置的配置值
    挂机模式 = config_manager.get_value("基础设置", "挂机模式")
    print(f"   挂机模式: {挂机模式}")
    
    指令速度 = config_manager.get_value("基础设置", "指令速度")
    print(f"   指令速度: {指令速度}")
    
    # 测试主题设置的配置值
    主题模式 = config_manager.get_value("主题设置", "主题模式")
    print(f"   主题模式: {主题模式}")
    
    # 4. 测试设置配置值
    print("\n4. 测试设置配置值")
    config_manager.set_value("基础设置", "挂机模式", "手动挂机")
    新挂机模式 = config_manager.get_value("基础设置", "挂机模式")
    print(f"   设置挂机模式为'手动挂机': {新挂机模式}")
    
    config_manager.set_value("主题设置", "主题模式", "浅色")
    新主题模式 = config_manager.get_value("主题设置", "主题模式")
    print(f"   设置主题模式为'浅色': {新主题模式}")
    
    # 5. 测试重置配置值
    print("\n5. 测试重置配置值")
    config_manager.reset_value("基础设置", "挂机模式")
    重置后挂机模式 = config_manager.get_value("基础设置", "挂机模式")
    print(f"   重置挂机模式: {重置后挂机模式}")
    
    config_manager.reset_value("主题设置", "主题模式")
    重置后主题模式 = config_manager.get_value("主题设置", "主题模式")
    print(f"   重置主题模式: {重置后主题模式}")
    
    # 6. 测试获取所有配置值
    print("\n6. 测试获取所有配置值")
    all_values = config_manager.get_all_values("基础设置")
    print(f"   基础设置所有配置值: {all_values}")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)


if __name__ == "__main__":
    test_config_manager()
