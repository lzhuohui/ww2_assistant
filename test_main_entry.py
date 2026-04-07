#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
全面测试脚本 - 测试主入口及其相关模块
"""

import sys
import os
import traceback
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """测试所有模块导入"""
    print("\n" + "="*60)
    print("测试1: 模块导入测试")
    print("="*60)
    
    modules = [
        "设置界面.层级0_数据管理.配置管理",
        "设置界面.层级0_数据管理.配置数据",
        "设置界面.层级0_数据管理.授权管理.设备识别",
        "设置界面.层级0_数据管理.授权管理.加密工具",
        "设置界面.层级0_数据管理.授权管理.授权管理器",
        "设置界面.层级2_功能界面.注册界面",
        "设置界面.层级2_功能界面.策略界面",
        "设置界面.层级2_功能界面.系统界面",
        "设置界面.层级2_功能界面.账号界面",
        "设置界面.层级2_功能界面.建筑界面",
        "设置界面.层级2_功能界面.任务界面",
        "设置界面.层级2_功能界面.集资界面",
        "设置界面.层级2_功能界面.打野界面",
        "设置界面.层级2_功能界面.打扫界面",
        "设置界面.层级2_功能界面.个性化界面",
        "设置界面.层级2_功能界面.关于界面",
        "设置界面.层级3_功能卡片.功能卡片",
        "设置界面.层级3_功能卡片.界面容器",
        "设置界面.层级4_复合模块.信息卡片",
        "设置界面.层级4_复合模块.卡片控件",
        "设置界面.层级4_复合模块.卡片开关",
        "设置界面.层级4_复合模块.标签下拉框",
        "设置界面.层级4_复合模块.用户信息",
        "设置界面.层级5_基础模块.方案选择器",
        "设置界面.层级5_基础模块.标签",
        "设置界面.层级5_基础模块.下拉框",
        "设置界面.层级5_基础模块.输入框",
        "设置界面.层级5_基础模块.图标",
        "设置界面.层级5_基础模块.头像",
        "设置界面.层级5_基础模块.分割线",
        "设置界面.层级5_基础模块.主题色块",
        "设置界面.层级1_主入口.主入口",
    ]
    
    failed = []
    for module in modules:
        try:
            __import__(module)
            print(f"✓ {module}")
        except Exception as e:
            print(f"✗ {module}: {e}")
            failed.append((module, str(e)))
    
    if failed:
        print(f"\n❌ 导入失败: {len(failed)} 个模块")
        for module, error in failed:
            print(f"  - {module}: {error}")
        return False
    else:
        print(f"\n✓ 所有 {len(modules)} 个模块导入成功")
        return True

def test_config_files():
    """测试配置文件"""
    print("\n" + "="*60)
    print("测试2: 配置文件测试")
    print("="*60)
    
    import yaml
    import glob
    
    yaml_files = glob.glob(str(project_root / "设置界面" / "**" / "*.yaml"), recursive=True)
    
    failed = []
    for file in yaml_files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                yaml.safe_load(f)
            print(f"✓ {Path(file).relative_to(project_root)}")
        except Exception as e:
            print(f"✗ {Path(file).relative_to(project_root)}: {e}")
            failed.append((file, str(e)))
    
    if failed:
        print(f"\n❌ 配置文件错误: {len(failed)} 个")
        for file, error in failed:
            print(f"  - {file}: {error}")
        return False
    else:
        print(f"\n✓ 所有 {len(yaml_files)} 个配置文件检查通过")
        return True

def test_bom_characters():
    """测试BOM字符"""
    print("\n" + "="*60)
    print("测试3: BOM字符测试")
    print("="*60)
    
    import glob
    
    py_files = glob.glob(str(project_root / "设置界面" / "**" / "*.py"), recursive=True)
    
    bom_files = []
    for file in py_files:
        with open(file, 'rb') as f:
            first_bytes = f.read(3)
            if first_bytes == b'\xef\xbb\xbf':
                bom_files.append(file)
    
    if bom_files:
        print(f"❌ 发现 {len(bom_files)} 个文件有BOM字符:")
        for file in bom_files:
            print(f"  - {Path(file).relative_to(project_root)}")
        return False
    else:
        print(f"✓ 所有 {len(py_files)} 个Python文件都没有BOM字符")
        return True

def test_syntax():
    """测试语法"""
    print("\n" + "="*60)
    print("测试4: 语法测试")
    print("="*60)
    
    import py_compile
    import glob
    
    py_files = glob.glob(str(project_root / "设置界面" / "**" / "*.py"), recursive=True)
    
    failed = []
    for file in py_files:
        try:
            py_compile.compile(file, doraise=True)
            print(f"✓ {Path(file).relative_to(project_root)}")
        except py_compile.PyCompileError as e:
            print(f"✗ {Path(file).relative_to(project_root)}: {e}")
            failed.append((file, str(e)))
    
    if failed:
        print(f"\n❌ 语法错误: {len(failed)} 个文件")
        for file, error in failed:
            print(f"  - {file}: {error}")
        return False
    else:
        print(f"\n✓ 所有 {len(py_files)} 个Python文件语法检查通过")
        return True

def test_main_entry():
    """测试主入口"""
    print("\n" + "="*60)
    print("测试5: 主入口测试")
    print("="*60)
    
    try:
        from 设置界面.层级0_数据管理.配置管理 import ConfigManager
        from 设置界面.层级1_主入口.主入口 import MainEntry
        
        config_manager = ConfigManager()
        print("✓ ConfigManager 初始化成功")
        
        print("✓ MainEntry 导入成功（需要Flet Page对象才能完全初始化）")
        
        return True
    except Exception as e:
        print(f"✗ 主入口测试失败: {e}")
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("\n" + "="*60)
    print("开始全面测试主入口及其相关模块")
    print("="*60)
    
    results = {
        "模块导入": test_imports(),
        "配置文件": test_config_files(),
        "BOM字符": test_bom_characters(),
        "语法检查": test_syntax(),
        "主入口": test_main_entry(),
    }
    
    print("\n" + "="*60)
    print("测试结果汇总")
    print("="*60)
    
    for name, result in results.items():
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{name}: {status}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n✓ 所有测试通过！")
        return 0
    else:
        print("\n❌ 部分测试失败！")
        return 1

if __name__ == "__main__":
    sys.exit(main())
