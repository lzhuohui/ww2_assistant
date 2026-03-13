# -*- coding: utf-8 -*-
"""
优化效果测试脚本

测试内容:
1. 启动时间对比
2. 页面切换时间对比
3. 退出时间对比
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
    
    start_time = time.time()
    
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        
        from 新思路.页面层.主界面 import MainPage
        main_page = MainPage(配置)
        main_page.page = page
        
        load_time = time.time() - start_time
        print(f"启动时间: {load_time:.3f}秒")
        
        page.add(main_page.create())
    
    ft.run(main)


def test_optimized():
    """测试优化版本"""
    print("\n" + "="*60)
    print("测试优化版本")
    print("="*60)
    
    配置 = 界面配置()
    
    start_time = time.time()
    
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        
        from 优化界面.页面层.主界面优化版 import MainPageOptimized
        main_page = MainPageOptimized(配置)
        main_page.page = page
        
        load_time = time.time() - start_time
        print(f"启动时间: {load_time:.3f}秒")
        
        page.add(main_page.create())
    
    ft.run(main)


if __name__ == "__main__":
    print("\n" + "="*60)
    print("界面性能优化测试")
    print("="*60)
    print("\n选择测试版本:")
    print("1. 原始版本")
    print("2. 优化版本")
    print("3. 对比测试")
    
    choice = input("\n请输入选择 (1/2/3): ").strip()
    
    if choice == "1":
        test_original()
    elif choice == "2":
        test_optimized()
    elif choice == "3":
        print("\n先测试原始版本...")
        test_original()
        print("\n再测试优化版本...")
        test_optimized()
    else:
        print("无效选择")
