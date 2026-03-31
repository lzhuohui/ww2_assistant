#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
实际测试建筑配置区下拉框显示
"""

import flet as ft
from 核心层.配置.界面配置 import UIConfig
from 表示层.组件.基础.下拉框 import create_dropdown

def main(page: ft.Page):
    config = UIConfig()
    page.title = '测试建筑配置区下拉框显示'
    page.window_width = 400
    page.window_height = 300
    page.padding = 20
    
    # 测试1：模拟建筑配置区的下拉框（懒加载，有current_value）
    print("测试1：建筑配置区下拉框（懒加载，current_value='17'）")
    dropdown1 = create_dropdown(
        current_value='17',
        width=70,
        config=config,
        option_loader=lambda: ['01', '02', '03', '04', '05', '10', '15', '17', '20']
    )
    
    display_value1 = dropdown1.get_value()
    print(f"  显示值: {display_value1}")
    
    if display_value1 == '17':
        print("  ✅ 测试通过：显示正确的默认值17")
    elif display_value1 == '请选择':
        print("  ❌ 测试失败：显示'请选择'而不是17")
    else:
        print(f"  ⚠️  测试异常：显示值异常 {display_value1}")
    
    # 测试2：模拟其他界面的下拉框（直接提供options）
    print("\n测试2：其他界面下拉框（直接提供options，current_value='选项2'）")
    dropdown2 = create_dropdown(
        options=['选项1', '选项2', '选项3'],
        current_value='选项2',
        width=100,
        config=config,
    )
    
    display_value2 = dropdown2.get_value()
    print(f"  显示值: {display_value2}")
    
    if display_value2 == '选项2':
        print("  ✅ 测试通过：显示正确的值'选项2'")
    else:
        print(f"  ⚠️  测试异常：显示值异常 {display_value2}")
    
    # 测试3：无current_value的情况
    print("\n测试3：无current_value的下拉框（options不为空）")
    dropdown3 = create_dropdown(
        options=['A', 'B', 'C'],
        current_value='',
        width=100,
        config=config,
    )
    
    display_value3 = dropdown3.get_value()
    print(f"  显示值: {display_value3}")
    
    if display_value3 == 'A':
        print("  ✅ 测试通过：显示第一个选项'A'")
    else:
        print(f"  ⚠️  测试异常：显示值异常 {display_value3}")
    
    # 测试4：既无options也无current_value
    print("\n测试4：既无options也无current_value")
    dropdown4 = create_dropdown(
        current_value='',
        width=100,
        config=config,
    )
    
    display_value4 = dropdown4.get_value()
    print(f"  显示值: {display_value4}")
    
    if display_value4 == '请选择':
        print("  ✅ 测试通过：显示'请选择'")
    else:
        print(f"  ⚠️  测试异常：显示值异常 {display_value4}")
    
    # 在页面上显示结果
    page.add(ft.Column([
        ft.Text("下拉框显示测试结果", size=20, weight=ft.FontWeight.BOLD),
        ft.Divider(height=10),
        ft.Text(f"测试1（建筑配置区）: {display_value1}", size=14),
        ft.Text(f"测试2（其他界面）: {display_value2}", size=14),
        ft.Text(f"测试3（无current_value）: {display_value3}", size=14),
        ft.Text(f"测试4（无options）: {display_value4}", size=14),
        ft.Divider(height=20),
        ft.Text("结论:", size=16, weight=ft.FontWeight.BOLD),
        ft.Text("建筑配置区下拉框现在应该显示默认值（如17）", size=12),
        ft.Text("而不是'请选择'，与其他界面保持一致", size=12),
    ], spacing=10))

if __name__ == "__main__":
    ft.run(main)