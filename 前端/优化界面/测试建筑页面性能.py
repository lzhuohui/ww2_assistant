# -*- coding: utf-8 -*-
"""
建筑页面性能对比测试

测试内容:
1. 原始版本：进入建筑页面时间、退出时间
2. 懒加载版本：进入建筑页面时间、退出时间
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import time
import flet as ft
from 配置.界面配置 import 界面配置


def test_original():
    """测试原始版本"""
    print("\n" + "="*60)
    print("测试原始版本")
    print("="*60)
    
    配置 = 界面配置()
    
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        
        start_time = time.time()
        
        from 新思路.页面层.建筑设置页面 import BuildingSettingsPage
        content = BuildingSettingsPage.create(配置)
        
        load_time = time.time() - start_time
        print(f"创建页面耗时: {load_time:.3f}秒")
        
        page.add(content)
    
    ft.run(main)


def test_lazy():
    """测试懒加载版本"""
    print("\n" + "="*60)
    print("测试懒加载版本")
    print("="*60)
    
    配置 = 界面配置()
    
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        
        start_time = time.time()
        
        from 优化界面.页面层.建筑设置页面懒加载 import BuildingSettingsPageLazy
        content = BuildingSettingsPageLazy.create(配置)
        
        load_time = time.time() - start_time
        print(f"创建页面耗时: {load_time:.3f}秒")
        
        page.add(content)
    
    ft.run(main)


if __name__ == "__main__":
    print("\n" + "="*60)
    print("建筑页面性能对比测试")
    print("="*60)
    print("\n选择测试版本:")
    print("1. 原始版本")
    print("2. 懒加载版本")
    print("3. 对比测试")
    
    choice = input("\n请输入选择 (1/2/3): ").strip()
    
    if choice == "1":
        test_original()
    elif choice == "2":
        test_lazy()
    elif choice == "3":
        print("\n先测试原始版本...")
        test_original()
        print("\n再测试懒加载版本...")
        test_lazy()
    else:
        print("无效选择")
