#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flet界面实例测试

创建日期: 2026-03-08
作者: AI
版本: v1.0.0

说明：运行此文件可以看到实际的Flet界面
"""

import flet as ft
import random
import time


def main(page: ft.Page):
    """主函数 - 创建一个简单的测试界面"""
    
    # 设置页面标题
    page.title = "Flet界面实例测试"
    page.window_width = 800
    page.window_height = 600
    page.padding = 20
    
    # 创建标题
    title = ft.Text(
        "Flet界面测试示例",
        size=30,
        weight=ft.FontWeight.BOLD,
        color="blue"
    )
    
    # 创建状态文本
    status_text = ft.Text(
        "准备就绪 - 请点击下方按钮",
        size=16,
        color="green"
    )
    
    # 创建计数器显示
    counter_text = ft.Text(
        "点击次数: 0",
        size=20,
        weight=ft.FontWeight.BOLD
    )
    
    # 计数器
    click_count = 0
    
    def on_button_click(e):
        """按钮点击事件"""
        nonlocal click_count
        click_count += 1
        counter_text.value = f"点击次数: {click_count}"
        status_text.value = f"按钮被点击了！时间: {time.strftime('%H:%M:%S')}"
        status_text.color = "orange"
        page.update()
    
    def on_reset_click(e):
        """重置按钮点击事件"""
        nonlocal click_count
        click_count = 0
        counter_text.value = "点击次数: 0"
        status_text.value = "计数器已重置"
        status_text.color = "green"
        page.update()
    
    # 创建按钮
    test_button = ft.Button(
        "点击我测试",
        on_click=on_button_click,
        width=200,
        height=50
    )
    
    reset_button = ft.Button(
        "重置计数器",
        on_click=on_reset_click,
        width=200,
        height=50
    )
    
    # 创建输入框
    name_input = ft.TextField(
        label="请输入您的名字",
        hint_text="在这里输入...",
        width=400
    )
    
    def on_greet_click(e):
        """问候按钮点击事件"""
        name = name_input.value
        if name:
            greeting_text.value = f"你好，{name}！欢迎使用Flet测试界面！"
            greeting_text.color = "purple"
        else:
            greeting_text.value = "请输入名字后再点击问候按钮"
            greeting_text.color = "red"
        page.update()
    
    greet_button = ft.Button(
        "问候",
        on_click=on_greet_click,
        width=200,
        height=50
    )
    
    greeting_text = ft.Text(
        "",
        size=18,
        weight=ft.FontWeight.BOLD
    )
    
    # 创建进度条
    progress_bar = ft.ProgressBar(width=400, value=0)
    progress_text = ft.Text("进度: 0%")
    
    def on_progress_click(e):
        """进度条测试"""
        progress_button.disabled = True
        page.update()
        
        for i in range(101):
            progress_bar.value = i / 100
            progress_text.value = f"进度: {i}%"
            page.update()
            time.sleep(0.02)
        
        progress_text.value = "进度: 完成！"
        progress_button.disabled = False
        page.update()
    
    progress_button = ft.Button(
        "开始进度测试",
        on_click=on_progress_click,
        width=200,
        height=50
    )
    
    # 创建卡片布局
    card = ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text("测试信息卡片", size=20, weight=ft.FontWeight.BOLD),
                    ft.Text("这是一个Flet卡片组件示例"),
                    ft.Text(f"当前时间: {time.strftime('%Y-%m-%d %H:%M:%S')}"),
                    ft.Text(f"随机数: {random.randint(1, 100)}"),
                ],
                spacing=10
            ),
            padding=20
        ),
        width=400
    )
    
    # 创建主要内容区域（使用Column代替Tabs）
    content_area = ft.Column(
        [
            ft.Text("按钮交互测试", size=18, weight=ft.FontWeight.BOLD),
            ft.Row([test_button, reset_button], spacing=20),
            counter_text,
            status_text,
            ft.Divider(),
            
            ft.Text("输入框测试", size=18, weight=ft.FontWeight.BOLD),
            name_input,
            greet_button,
            greeting_text,
            ft.Divider(),
            
            ft.Text("进度条测试", size=18, weight=ft.FontWeight.BOLD),
            progress_button,
            progress_bar,
            progress_text,
            ft.Divider(),
            
            ft.Text("卡片组件展示", size=18, weight=ft.FontWeight.BOLD),
            card,
        ],
        spacing=20,
        alignment=ft.MainAxisAlignment.START,
        scroll=ft.ScrollMode.AUTO
    )
    
    # 布局
    page.add(
        ft.Column(
            [
                ft.Row([title], alignment=ft.MainAxisAlignment.CENTER),
                ft.Divider(),
                content_area,
            ],
            spacing=10,
            expand=True
        )
    )


if __name__ == "__main__":
    print("="*60)
    print("正在启动Flet界面测试...")
    print("="*60)
    print("请稍候，界面即将出现...")
    print("="*60)
    ft.app(target=main)
