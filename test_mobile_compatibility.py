# -*- coding: utf-8 -*-
"""
测试移动设备兼容性修改
"""

import flet as ft
from 设置界面.层级1_主入口.主入口 import MainEntry

def test_mobile_detection():
    """测试移动设备检测逻辑"""
    print("测试移动设备检测逻辑...")
    
    # 创建一个模拟类来测试_is_mobile_device方法
    class MockPage:
        def __init__(self, window_width=None):
            self.window = MockWindow(window_width)
            
    class MockWindow:
        def __init__(self, width=None):
            self.width = width
    
    # 测试主入口的_is_mobile_device方法
    test_cases = [
        {"width": 390, "expected": True, "name": "移动设备(390px)"},
        {"width": 599, "expected": True, "name": "移动设备边界(599px)"},
        {"width": 600, "expected": False, "name": "桌面设备边界(600px)"},
        {"width": 1200, "expected": False, "name": "桌面设备(1200px)"},
        {"width": None, "expected": False, "name": "未设置宽度"},
    ]
    
    for case in test_cases:
        mock_page = MockPage(case["width"])
        
        # 创建MainEntry实例并注入模拟页面
        main_entry = MainEntry.__new__(MainEntry)
        main_entry._page = mock_page
        
        # 直接调用_is_mobile_device方法
        result = main_entry._is_mobile_device()
        
        status = "✅" if result == case["expected"] else "❌"
        print(f"  {status} {case['name']}: 期望={case['expected']}, 实际={result}")
    
    print("\n=== 移动设备检测测试完成 ===")

def test_main_entry_structure():
    """测试主入口结构"""
    print("\n测试主入口结构...")
    
    try:
        # 导入所有必要的模块
        import flet as ft
        from typing import Dict, Any, Optional
        
        # 检查类定义
        print("1. 检查MainEntry类定义...")
        if hasattr(MainEntry, '__init__'):
            print("   ✅ MainEntry有__init__方法")
        else:
            print("   ❌ MainEntry缺少__init__方法")
            
        # 检查移动设备检测方法
        print("2. 检查移动设备检测方法...")
        if hasattr(MainEntry, '_is_mobile_device'):
            print("   ✅ MainEntry有_is_mobile_device方法")
        else:
            print("   ❌ MainEntry缺少_is_mobile_device方法")
            
        # 检查_setup_page方法
        print("3. 检查_setup_page方法...")
        if hasattr(MainEntry, '_setup_page'):
            print("   ✅ MainEntry有_setup_page方法")
        else:
            print("   ❌ MainEntry缺少_setup_page方法")
            
        # 导入配置管理器
        print("4. 检查依赖导入...")
        try:
            from 设置界面.层级0_数据管理.配置管理 import ConfigManager
            print("   ✅ ConfigManager导入成功")
        except ImportError as e:
            print(f"   ❌ ConfigManager导入失败: {e}")
            
        print("\n=== 主入口结构测试完成 ===")
        
    except Exception as e:
        print(f"测试失败: {e}")

if __name__ == "__main__":
    print("="*60)
    print("移动设备兼容性测试")
    print("="*60)
    
    test_mobile_detection()
    test_main_entry_structure()
    
    print("\n" + "="*60)
    print("APK打包准备检查:")
    print("="*60)
    
    # 检查requirements.txt是否存在
    import os
    if os.path.exists("requirements.txt"):
        print("✅ requirements.txt 文件存在")
        with open("requirements.txt", "r", encoding="utf-8") as f:
            content = f.read()
            if "flet==" in content:
                print("✅ requirements.txt 包含flet依赖")
            if "PyYAML>=" in content:
                print("✅ requirements.txt 包含PyYAML依赖")
            if "cryptography>=" in content:
                print("✅ requirements.txt 包含cryptography依赖")
            if "pypinyin>=" in content:
                print("✅ requirements.txt 包含pypinyin依赖")
    else:
        print("❌ requirements.txt 文件不存在")
    
    # 检查flet.yaml
    if os.path.exists("flet.yaml"):
        print("✅ flet.yaml 文件存在")
    else:
        print("❌ flet.yaml 文件不存在")
    
    # 检查main.py入口点
    if os.path.exists("main.py"):
        print("✅ main.py 文件存在")
    else:
        print("❌ main.py 文件不存在")
    
    # 检查Flutter配置
    if os.path.exists("build/flutter"):
        print("✅ build/flutter 目录存在")
    else:
        print("❌ build/flutter 目录不存在")
    
    print("\n" + "="*60)
    print("建议下一步:")
    print("1. 运行: flet build apk")
    print("2. 或在本地测试: flet run")
    print("="*60)