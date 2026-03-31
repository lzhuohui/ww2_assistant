#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试真正的懒加载实现
验证共识 #020 是否被正确实现：
1. 点击时才加载选项列表
2. 任何时候只有一个下拉框有完整选项列表
3. 销毁上一个下拉框的选项列表
"""

import flet as ft
import sys
import os

# 添加项目根目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from 表示层.组件.基础.下拉框 import create_dropdown
from 核心层.状态.下拉框状态管理器 import dropdown_state_manager


def test_true_lazy_loading(page: ft.Page):
    """测试真正的懒加载"""
    page.title = "真正的懒加载测试"
    page.window_width = 600  # type: ignore
    page.window_height = 500  # type: ignore
    page.padding = 20
    
    # 创建测试标题
    title = ft.Text("真正的懒加载测试 - 验证共识 #020", size=20, weight=ft.FontWeight.BOLD)
    
    # 状态显示
    status_text = ft.Text("状态: 等待测试", size=14)
    loaded_count_text = ft.Text("已加载下拉框: 0", size=14)
    active_dropdown_text = ft.Text("当前活动下拉框: 无", size=14)
    
    def update_status():
        """更新状态显示"""
        loaded_count = dropdown_state_manager.get_loaded_count()
        active_dropdown = dropdown_state_manager.get_current_active()
        
        loaded_count_text.value = f"已加载下拉框: {loaded_count}"
        active_dropdown_text.value = f"当前活动下拉框: {active_dropdown or '无'}"
        
        if loaded_count == 0:
            status_text.value = "状态: 所有下拉框都未加载选项 ✅"
            status_text.color = "green"
        elif loaded_count == 1:
            status_text.value = f"状态: 只有1个下拉框加载了选项 ✅ (ID: {active_dropdown})"
            status_text.color = "green"
        else:
            status_text.value = f"状态: 错误！有{loaded_count}个下拉框同时加载了选项 ❌"
            status_text.color = "red"
        
        page.update()
    
    # 创建多个测试下拉框
    test_dropdowns = []
    
    # 下拉框1
    dropdown1 = create_dropdown(
        current_value="选项1",
        on_change=lambda v: print(f"下拉框1选择了: {v}"),
        option_loader=lambda: [f"选项{i}" for i in range(1, 21)],
        dropdown_id="test_dropdown_1",
    )
    
    # 下拉框2
    dropdown2 = create_dropdown(
        current_value="选项A",
        on_change=lambda v: print(f"下拉框2选择了: {v}"),
        option_loader=lambda: [f"选项{chr(65+i)}" for i in range(20)],  # A-T
        dropdown_id="test_dropdown_2",
    )
    
    # 下拉框3
    dropdown3 = create_dropdown(
        current_value="数字1",
        on_change=lambda v: print(f"下拉框3选择了: {v}"),
        option_loader=lambda: [f"数字{i}" for i in range(1, 21)],
        dropdown_id="test_dropdown_3",
    )
    
    # 测试按钮
    def test_click_sequence():
        """测试点击序列"""
        status_text.value = "状态: 测试点击序列..."
        status_text.color = "blue"
        page.update()
        
        # 模拟点击下拉框1
        print("\n=== 测试1: 点击下拉框1 ===")
        if hasattr(dropdown1, 'needs_reopen') and dropdown1.needs_reopen():
            dropdown1.clear_reopen_flag()
        
        # 更新状态
        update_status()
        
        # 等待一下
        import time
        time.sleep(1)
        
        # 模拟点击下拉框2
        print("\n=== 测试2: 点击下拉框2 ===")
        if hasattr(dropdown2, 'needs_reopen') and dropdown2.needs_reopen():
            dropdown2.clear_reopen_flag()
        
        # 更新状态
        update_status()
        
        # 等待一下
        time.sleep(1)
        
        # 模拟点击下拉框3
        print("\n=== 测试3: 点击下拉框3 ===")
        if hasattr(dropdown3, 'needs_reopen') and dropdown3.needs_reopen():
            dropdown3.clear_reopen_flag()
        
        # 更新状态
        update_status()
        
        # 最终检查
        time.sleep(1)
        final_loaded = dropdown_state_manager.get_loaded_count()
        if final_loaded == 1:
            status_text.value = f"状态: 测试通过！任何时候只有一个下拉框有完整选项列表 ✅"
            status_text.color = "green"
        else:
            status_text.value = f"状态: 测试失败！有{final_loaded}个下拉框同时加载了选项 ❌"
            status_text.color = "red"
        
        page.update()
    
    test_button = ft.ElevatedButton(
        "运行懒加载测试",
        on_click=lambda e: test_click_sequence(),
        icon="PLAY_ARROW",
    )
    
    # 清空状态按钮
    def clear_state(e):
        dropdown_state_manager.clear_all()
        update_status()
    
    clear_button = ft.ElevatedButton(
        "清空所有状态",
        on_click=clear_state,
        icon="CLEAR_ALL",
    )
    
    # 布局
    page.add(
        title,
        ft.Divider(height=20),
        
        ft.Column([
            status_text,
            loaded_count_text,
            active_dropdown_text,
        ], spacing=10),
        
        ft.Divider(height=20),
        
        ft.Text("测试下拉框:", size=16, weight=ft.FontWeight.BOLD),
        ft.Column([
            ft.Row([ft.Text("下拉框1:"), dropdown1], spacing=10),
            ft.Row([ft.Text("下拉框2:"), dropdown2], spacing=10),
            ft.Row([ft.Text("下拉框3:"), dropdown3], spacing=10),
        ], spacing=15),
        
        ft.Divider(height=20),
        
        ft.Row([test_button, clear_button], spacing=20),
        
        ft.Divider(height=20),
        
        ft.Text("测试说明:", size=14, weight=ft.FontWeight.BOLD),
        ft.Column([
            ft.Text("1. 点击任意下拉框，观察控制台输出", size=12),
            ft.Text("2. 点击'运行懒加载测试'按钮进行自动化测试", size=12),
            ft.Text("3. 验证'任何时候只有一个下拉框有完整选项列表'", size=12),
            ft.Text("4. 观察'已加载下拉框'数量应该始终为0或1", size=12),
        ], spacing=5),
    )
    
    # 初始状态更新
    update_status()


if __name__ == "__main__":
    print("=" * 60)
    print("真正的懒加载测试 - 验证共识 #020")
    print("=" * 60)
    print("测试目标:")
    print("1. ✅ 点击时才加载选项列表")
    print("2. ✅ 任何时候只有一个下拉框有完整选项列表")
    print("3. ✅ 销毁上一个下拉框的选项列表")
    print("=" * 60)
    
    ft.run(test_true_lazy_loading)