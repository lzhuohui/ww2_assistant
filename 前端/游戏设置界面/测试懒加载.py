# -*- coding: utf-8 -*-
"""
测试下拉框懒加载功能
"""

import flet as ft
import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入下拉框组件
from 表示层.组件.基础.下拉框 import Dropdown

def main(page: ft.Page):
    page.title = "下拉框懒加载测试"
    page.window_width = 400
    page.window_height = 300
    
    # 创建多个下拉框
    dropdowns = []
    
    # 创建10个下拉框，每个有10个选项
    for i in range(10):
        options = [f"选项{i}-{j}" for j in range(10)]
        
        def create_on_change(idx):
            def on_change(value):
                print(f"下拉框 {idx} 选择了: {value}")
            return on_change
        
        def create_on_open(idx):
            def on_open():
                print(f"下拉框 {idx} 打开，开始加载选项...")
            return on_open
        
        dropdown = Dropdown.create(
            options=options,
            current_value=options[0],
            on_change=create_on_change(i),
            on_open=create_on_open(i),
            width=200,
            height=35
        )
        dropdowns.append(dropdown)
    
    # 添加一个标签显示状态
    status_text = ft.Text("创建了10个下拉框，每个有10个选项。点击任意下拉框查看加载日志。", size=12)
    
    # 布局
    page.add(
        ft.Column([
            ft.Text("下拉框懒加载测试", size=20, weight=ft.FontWeight.BOLD),
            status_text,
            ft.Divider(),
            *dropdowns
        ], spacing=10)
    )
    
    print("界面已创建，等待点击下拉框...")
    print("注意：如果懒加载生效，应该在点击下拉框时才看到'开始加载选项...'的日志")

if __name__ == "__main__":
    ft.run(main)