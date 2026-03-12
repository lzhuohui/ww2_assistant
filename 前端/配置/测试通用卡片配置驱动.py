# -*- coding: utf-8 -*-
"""
测试通用卡片配置驱动功能

测试目标:
    验证通用卡片是否能够根据配置创建卡片。

测试步骤:
    1. 创建配置管理器
    2. 获取卡片配置
    3. 根据配置创建控件
    4. 验证控件功能
"""

import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import flet as ft
from 前端.配置.配置管理器 import ConfigManager
from 前端.配置.界面配置 import 界面配置
from 前端.新思路.零件层.标签下拉框 import LabelDropdown


def test_config_driven_card():
    """测试通用卡片配置驱动功能"""
    print("=" * 60)
    print("测试通用卡片配置驱动功能")
    print("=" * 60)
    
    # 1. 创建配置管理器
    print("\n1. 创建配置管理器")
    config_manager = ConfigManager()
    print("   ✅ 配置管理器创建成功")
    
    # 2. 获取基础设置卡片配置
    print("\n2. 获取基础设置卡片配置")
    basic_config = config_manager.get_card_config("基础设置")
    if basic_config:
        print(f"   ✅ 基础设置配置获取成功: {basic_config.get('title')}")
        print(f"   控件数量: {len(basic_config.get('controls', []))}")
    else:
        print("   ❌ 基础设置配置获取失败")
        return
    
    # 3. 根据配置创建控件
    print("\n3. 根据配置创建控件")
    ui_config = 界面配置()
    controls = []
    
    for control_config in basic_config.get('controls', []):
        control_type = control_config.get('type')
        
        if control_type == 'dropdown':
            control = LabelDropdown.create(
                config=ui_config,
                label=control_config.get('label'),
                options=control_config.get('options'),
                value=config_manager.get_value("基础设置", control_config.get('config_key')),
            )
            controls.append(control)
            print(f"   ✅ 创建下拉框: {control_config.get('label')}")
    
    print(f"   总共创建控件: {len(controls)} 个")
    
    # 4. 验证控件功能
    print("\n4. 验证控件功能")
    for i, control in enumerate(controls, 1):
        has_set_state = hasattr(control, 'set_state')
        print(f"   控件{i}: set_state方法={'✅ 存在' if has_set_state else '❌ 不存在'}")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)


if __name__ == "__main__":
    test_config_driven_card()
