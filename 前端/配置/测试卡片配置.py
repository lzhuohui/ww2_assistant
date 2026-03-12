# -*- coding: utf-8 -*-
"""
测试卡片配置文件

测试目标:
    验证卡片配置文件的格式和内容是否正确。

测试步骤:
    1. 导入卡片配置
    2. 验证配置结构
    3. 打印配置内容
    4. 验证配置完整性
"""

import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# 使用绝对导入
from 前端.配置.卡片配置 import 卡片配置


def test_card_config():
    """测试卡片配置文件"""
    print("=" * 60)
    print("测试卡片配置文件")
    print("=" * 60)
    
    # 1. 验证配置结构
    print("\n1. 验证配置结构")
    print(f"   配置项数量: {len(卡片配置)}")
    print(f"   配置项名称: {list(卡片配置.keys())}")
    
    # 2. 验证基础设置配置
    print("\n2. 验证基础设置配置")
    basic_config = 卡片配置.get("基础设置")
    if basic_config:
        print(f"   标题: {basic_config.get('title')}")
        print(f"   图标: {basic_config.get('icon')}")
        print(f"   副标题: {basic_config.get('subtitle')}")
        print(f"   每行控件数: {basic_config.get('controls_per_row')}")
        print(f"   控件数量: {len(basic_config.get('controls', []))}")
        
        # 验证控件配置
        print("\n   控件配置:")
        for i, control in enumerate(basic_config.get('controls', []), 1):
            print(f"     控件{i}: type={control.get('type')}, label={control.get('label')}, value={control.get('value')}")
    else:
        print("   ❌ 未找到基础设置配置")
    
    # 3. 验证主题设置配置
    print("\n3. 验证主题设置配置")
    theme_config = 卡片配置.get("主题设置")
    if theme_config:
        print(f"   标题: {theme_config.get('title')}")
        print(f"   图标: {theme_config.get('icon')}")
        print(f"   副标题: {theme_config.get('subtitle')}")
        print(f"   控件类型: {theme_config.get('controls_type')}")
        print(f"   主题列表: {theme_config.get('themes')}")
        print(f"   当前选中: {theme_config.get('selected')}")
    else:
        print("   ❌ 未找到主题设置配置")
    
    # 4. 验证调色板设置配置
    print("\n4. 验证调色板设置配置")
    palette_config = 卡片配置.get("调色板设置")
    if palette_config:
        print(f"   标题: {palette_config.get('title')}")
        print(f"   图标: {palette_config.get('icon')}")
        print(f"   副标题: {palette_config.get('subtitle')}")
        print(f"   控件类型: {palette_config.get('controls_type')}")
        print(f"   调色板列表: {palette_config.get('palettes')}")
        print(f"   当前选中: {palette_config.get('selected')}")
    else:
        print("   ❌ 未找到调色板设置配置")
    
    # 5. 验证配置完整性
    print("\n5. 验证配置完整性")
    required_keys = ["基础设置", "主题设置", "调色板设置"]
    missing_keys = [key for key in required_keys if key not in 卡片配置]
    
    if not missing_keys:
        print("   ✅ 所有必需的配置项都存在")
    else:
        print(f"   ❌ 缺少配置项: {missing_keys}")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)


if __name__ == "__main__":
    test_card_config()
