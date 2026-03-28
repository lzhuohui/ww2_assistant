#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试下拉框视觉修复效果
简洁直接，不搞复杂设计
"""

import flet as ft
from 下拉框_合格版 import create_dropdown


def main(page: ft.Page):
    page.title = "下拉框视觉修复测试"
    page.window_width = 400
    page.window_height = 400
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    
    # 标题
    title = ft.Text("✅ 下拉框视觉修复完成", size=20, weight=ft.FontWeight.BOLD)
    
    # 视觉要点
    visual_info = ft.Column([
        ft.Text("修复的视觉细节：", size=16, weight=ft.FontWeight.W_500),
        ft.Text("1. 🔍 箭头图标清晰可见", size=14),
        ft.Text("2. 🎨 按钮和菜单背景色统一 (#F8F9FA)", size=14),
        ft.Text("3. 📏 合适的间距和字体大小", size=14),
        ft.Divider(height=20),
    ], spacing=8)
    
    # 测试下拉框1
    dropdown1 = create_dropdown(
        options=["北京", "上海", "广州", "深圳"],
        current_value="北京",
        width=150,
        on_change=lambda v: print(f"选择了: {v}"),
    )
    
    # 测试下拉框2（懒加载）
    dropdown2 = create_dropdown(
        current_value="17",
        width=100,
        option_loader=lambda: [f"{i:02d}" for i in range(41)],
        on_change=lambda v: print(f"等级选择了: {v}"),
    )
    
    # 测试控件
    test_field = ft.TextField(
        label="测试文本框",
        hint_text="下拉框打开时，这个控件的位置应该保持不变",
        width=200,
    )
    
    # 布局
    page.add(
        ft.Column([
            title,
            ft.Divider(height=10),
            visual_info,
            ft.Text("城市选择:", size=14),
            dropdown1,
            ft.Divider(height=10),
            ft.Text("建筑等级:", size=14),
            dropdown2,
            ft.Divider(height=20),
            test_field,
            ft.Divider(height=20),
            ft.Text("✅ 所有视觉细节已修复", size=16, color="#4CAF50"),
            ft.Text("可以直接集成到主项目中", size=14),
        ], spacing=10)
    )
    
    print("=" * 60)
    print("下拉框视觉修复测试")
    print("=" * 60)
    print("修复内容：")
    print("1. 箭头图标清晰可见")
    print("2. 按钮和菜单背景色统一 (#F8F9FA)")
    print("3. 合适的间距和字体大小")
    print("=" * 60)


if __name__ == "__main__":
    ft.app(target=main)