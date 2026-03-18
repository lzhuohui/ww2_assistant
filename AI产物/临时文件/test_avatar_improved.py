#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
头像组件改进测试
基于网上最佳实践的改进方案验证
"""

import flet as ft
import sys
import os

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from 前端.用户设置界面.零件.头像 import 头像 as Avatar
from 前端.用户设置界面.核心.主题提供者 import ThemeProvider
from 前端.用户设置界面.配置.界面配置 import 界面配置

def main(page: ft.Page):
    """测试主函数"""
    # 初始化配置
    配置 = 界面配置()
    ThemeProvider.initialize(配置)
    
    # 设置页面
    page.title = "头像组件改进测试"
    page.padding = 20
    page.bgcolor = "#1E1E1E"  # 深色背景，便于观察
    
    # 创建测试说明
    title = ft.Text(
        "头像组件改进测试 - 基于网上最佳实践",
        size=24,
        weight=ft.FontWeight.BOLD,
        color="#FFFFFF"
    )
    
    description = ft.Text(
        "双击头像进入编辑状态，应显示深黑色背景和亮金色文字\n"
        "按Enter或点击其他地方退出编辑状态",
        size=14,
        color="#CCCCCC"
    )
    
    # 创建头像组件
    def on_text_change(new_text):
        print(f"文字已更改: {new_text}")
    
    avatar = Avatar.create(
        diameter=80,
        text="帅",
        on_text_change=on_text_change,
        show_glow=True,
        show_scan=True,
        enabled=True
    )
    
    # 创建状态显示
    status_text = ft.Text("状态: 正常", size=16, color="#FFFFFF")
    
    def update_status():
        """更新状态显示"""
        try:
            current_text = avatar.get_text()
            status_text.value = f"状态: 正常 | 当前文字: {current_text}"
        except:
            status_text.value = "状态: 正常"
        status_text.update()
    
    # 添加测试按钮
    def test_edit_mode(e):
        """手动测试编辑模式"""
        print("=== 手动触发编辑模式 ===")
        # 模拟双击事件
        avatar.on_click(None)
        page.update()
    
    test_button = ft.ElevatedButton(
        "手动测试编辑模式",
        on_click=test_edit_mode,
        bgcolor="#4CAF50",
        color="#FFFFFF"
    )
    
    # 创建布局
    content = ft.Column(
        [
            title,
            description,
            ft.Divider(height=20, color="transparent"),
            ft.Row([avatar], alignment=ft.MainAxisAlignment.CENTER),
            ft.Divider(height=20, color="transparent"),
            status_text,
            ft.Divider(height=10, color="transparent"),
            test_button,
            ft.Divider(height=20, color="transparent"),
            ft.Text("控制台输出:", size=14, color="#FFFFFF", weight=ft.FontWeight.BOLD),
            ft.Text(
                "请查看控制台输出，确认:\n"
                "1. 进入编辑状态时打印深黑色背景设置\n"
                "2. 退出编辑状态时打印透明背景恢复\n"
                "3. TextField焦点事件正常触发",
                size=12,
                color="#AAAAAA"
            )
        ],
        spacing=10,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
    
    page.add(content)
    
    # 添加定时更新状态
    def update_timer():
        import time
        while True:
            time.sleep(1)
            try:
                page.update()
                update_status()
            except:
                break
    
    import threading
    threading.Thread(target=update_timer, daemon=True).start()

if __name__ == "__main__":
    print("=== 头像组件改进测试启动 ===")
    print("基于网上最佳实践的改进方案:")
    print("1. 分离状态管理：明确区分编辑状态和正常状态")
    print("2. 统一背景色设置：确保所有层级背景色一致")
    print("3. 优化TextField配置：完全透明背景，显示容器背景色")
    print("4. 添加详细调试输出：验证颜色设置是否生效")
    print("=" * 50)
    
    ft.run(main)