#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试最终版架构 - 验证简化后的实现
"""

import flet as ft
from 核心层.配置.界面配置 import UIConfig
from 配置.简化选项管理器 import get_simple_option_manager
from 表示层.组件.基础.下拉框 import create_dropdown
from 表示层.界面.建筑配置区_最终版 import create_building_config_section

def main(page: ft.Page):
    config = UIConfig()
    page.title = '测试最终版架构'
    page.window_width = 500
    page.window_height = 600
    page.padding = 20
    
    print("=" * 70)
    print("测试最终版架构")
    print("=" * 70)
    
    # 测试1：简化选项管理器
    print("\n🔍 测试1：简化选项管理器")
    option_manager = get_simple_option_manager()
    
    # 测试建筑等级选项
    loader = option_manager.get_option_loader("building_level", max_level=40)
    options = loader()
    print(f"✅ 建筑等级选项: {len(options)} 个选项")
    print(f"  前5个选项: {options[:5]}")
    print(f"  是否包含'17': {'17' in options}")
    
    if len(options) == 0:
        print("❌ 问题：选项管理器返回空列表！")
    else:
        print("✅ 选项管理器正常")
    
    # 测试2：直接创建下拉框
    print("\n🔍 测试2：直接创建下拉框")
    dropdown = create_dropdown(
        current_value="17",
        width=70,
        config=config,
        option_loader=option_manager.get_option_loader("building_level", max_level=40),
    )
    
    display_value = dropdown.get_value()
    print(f"✅ 下拉框创建成功")
    print(f"  显示值: {display_value}")
    
    if display_value == "17":
        print("✅ 下拉框显示正确的默认值")
    else:
        print(f"❌ 下拉框显示异常: {display_value}")
    
    # 测试3：建筑配置区
    print("\n🔍 测试3：建筑配置区")
    section, manager = create_building_config_section(config=config)
    print(f"✅ 建筑配置区创建成功")
    print(f"  section类型: {type(section)}")
    print(f"  manager: {manager}")
    
    # 在页面上显示结果
    page.add(ft.Column([
        ft.Text("最终版架构测试", size=20, weight=ft.FontWeight.BOLD),
        ft.Divider(height=10),
        ft.Text(f"建筑等级选项数量: {len(options)}", size=14),
        ft.Text(f"下拉框显示值: {display_value}", size=14),
        ft.Text(f"建筑配置区创建: 成功", size=14),
        ft.Divider(height=20),
        ft.Text("架构说明:", size=16, weight=ft.FontWeight.BOLD),
        ft.Text("1. 所有选项集中管理", size=12),
        ft.Text("2. 下拉框直接使用选项管理器", size=12),
        ft.Text("3. 实现方式简单直接", size=12),
        ft.Text("4. 遵循下拉框测试目录的实现方式", size=12),
    ], spacing=10))

if __name__ == "__main__":
    ft.app(target=main)