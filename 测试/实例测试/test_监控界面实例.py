#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
监控界面实例测试

创建日期: 2026-03-08
作者: AI
版本: v1.0.0

说明：模拟游戏辅助工具的监控界面
"""

import flet as ft
import random
import time
from datetime import datetime


def main(page: ft.Page):
    """主函数 - 创建监控界面"""
    
    page.title = "游戏辅助工具 - 实时监控"
    page.window_width = 1000
    page.window_height = 800
    page.padding = 20
    
    # ========== 状态变量 ==========
    is_running = False
    start_time = None
    total_clicks = 0
    
    # ========== 标题区域 ==========
    title = ft.Text(
        "实时监控面板",
        size=32,
        weight=ft.FontWeight.BOLD,
        color="#90CAF9"
    )
    
    # ========== 状态卡片 ==========
    status_indicator = ft.Container(
        content=ft.Row(
            [
                ft.Text("●", size=20, color="red"),
                ft.Text("停止", size=18, weight=ft.FontWeight.BOLD, color="red")
            ],
            spacing=10
        ),
        padding=15,
        bgcolor="#FFEBEE",
        border_radius=10
    )
    
    runtime_text = ft.Text(
        "运行时间: 00:00:00",
        size=20,
        weight=ft.FontWeight.BOLD
    )
    
    # ========== 数据指标 ==========
    clicks_text = ft.Text(
        "0",
        size=48,
        weight=ft.FontWeight.BOLD,
        color="blue"
    )
    clicks_label = ft.Text("总点击次数", size=14)
    
    cps_text = ft.Text(
        "0.0",
        size=48,
        weight=ft.FontWeight.BOLD,
        color="green"
    )
    cps_label = ft.Text("点击/秒", size=14)
    
    success_rate_text = ft.Text(
        "100%",
        size=48,
        weight=ft.FontWeight.BOLD,
        color="orange"
    )
    success_rate_label = ft.Text("成功率", size=14)
    
    # ========== 日志区域 ==========
    log_list = ft.ListView(
        expand=True,
        spacing=5,
        auto_scroll=True
    )
    
    def add_log(message, level="info"):
        """添加日志"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        color = "white"
        if level == "success":
            color = "green"
        elif level == "warning":
            color = "orange"
        elif level == "error":
            color = "red"
        
        log_entry = ft.Container(
            content=ft.Text(
                f"[{timestamp}] {message}",
                color=color,
                size=12
            ),
            padding=5,
            bgcolor="#1E1E1E",
            border_radius=3
        )
        
        log_list.controls.append(log_entry)
        
        # 限制日志数量
        if len(log_list.controls) > 100:
            log_list.controls.pop(0)
        
        page.update()
    
    # ========== 图表区域（模拟） ==========
    chart_data = []
    
    chart_container = ft.Container(
        content=ft.Column(
            [
                ft.Text("实时数据图表", size=16, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=ft.Text("图表区域 - 实时数据可视化", color="grey"),
                    bgcolor="#3A3A3A",
                    padding=50
                )
            ]
        ),
        padding=15,
        bgcolor="#1E1E1E",
        border_radius=10,
        height=200
    )
    
    # ========== 控制按钮 ==========
    def on_start(e):
        """开始按钮"""
        nonlocal is_running, start_time
        is_running = True
        start_time = time.time()
        
        status_indicator.content = ft.Row(
            [
                ft.Text("●", size=20, color="green"),
                ft.Text("运行中", size=18, weight=ft.FontWeight.BOLD, color="green")
            ],
            spacing=10
        )
        status_indicator.bgcolor = "#E8F5E9"
        
        start_btn.disabled = True
        stop_btn.disabled = False
        
        add_log("脚本已启动", "success")
        page.update()
        
        # 启动更新循环
        update_runtime()
    
    def on_stop(e):
        """停止按钮"""
        nonlocal is_running
        is_running = False
        
        status_indicator.content = ft.Row(
            [
                ft.Text("●", size=20, color="red"),
                ft.Text("停止", size=18, weight=ft.FontWeight.BOLD, color="red")
            ],
            spacing=10
        )
        status_indicator.bgcolor = "#FFEBEE"
        
        start_btn.disabled = False
        stop_btn.disabled = True
        
        add_log("脚本已停止", "warning")
        page.update()
    
    def on_clear_log(e):
        """清空日志"""
        log_list.controls.clear()
        add_log("日志已清空")
        page.update()
    
    def update_runtime():
        """更新运行时间"""
        if is_running and start_time:
            elapsed = int(time.time() - start_time)
            hours = elapsed // 3600
            minutes = (elapsed % 3600) // 60
            seconds = elapsed % 60
            runtime_text.value = f"运行时间: {hours:02d}:{minutes:02d}:{seconds:02d}"
            
            # 模拟数据更新
            if random.random() > 0.7:
                nonlocal total_clicks
                total_clicks += random.randint(1, 5)
                clicks_text.value = str(total_clicks)
                
                # 计算CPS
                if elapsed > 0:
                    cps = total_clicks / elapsed
                    cps_text.value = f"{cps:.1f}"
                
                # 随机添加日志
                if random.random() > 0.8:
                    messages = [
                        ("执行点击操作", "info"),
                        ("检测到游戏界面", "success"),
                        ("等待下一次操作", "info"),
                        ("坐标偏移计算完成", "info"),
                    ]
                    msg, level = random.choice(messages)
                    add_log(msg, level)
            
            page.update()
            
            # 继续更新（使用简单的延迟循环）
            if is_running:
                time.sleep(1)
                update_runtime()
    
    start_btn = ft.Button(
        "开始",
        on_click=on_start,
        style=ft.ButtonStyle(
            bgcolor="green",
            color="white"
        ),
        width=120,
        height=45
    )
    
    stop_btn = ft.Button(
        "停止",
        on_click=on_stop,
        disabled=True,
        style=ft.ButtonStyle(
            bgcolor="red",
            color="white"
        ),
        width=120,
        height=45
    )
    
    clear_btn = ft.Button(
        "清空日志",
        on_click=on_clear_log,
        width=120,
        height=45
    )
    
    # ========== 布局 ==========
    page.add(
        ft.Column(
            [
                # 标题
                ft.Row([title], alignment=ft.MainAxisAlignment.CENTER),
                
                ft.Divider(),
                
                # 状态和运行时间
                ft.Row(
                    [
                        status_indicator,
                        ft.Container(width=20),
                        runtime_text
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                
                ft.Divider(),
                
                # 数据指标
                ft.Row(
                    [
                        # 点击次数
                        ft.Card(
                            content=ft.Container(
                                content=ft.Column(
                                    [clicks_text, clicks_label],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                                ),
                                padding=20,
                                width=150
                            )
                        ),
                        # CPS
                        ft.Card(
                            content=ft.Container(
                                content=ft.Column(
                                    [cps_text, cps_label],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                                ),
                                padding=20,
                                width=150
                            )
                        ),
                        # 成功率
                        ft.Card(
                            content=ft.Container(
                                content=ft.Column(
                                    [success_rate_text, success_rate_label],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                                ),
                                padding=20,
                                width=150
                            )
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY
                ),
                
                ft.Divider(),
                
                # 图表
                chart_container,
                
                ft.Divider(),
                
                # 控制按钮
                ft.Row(
                    [start_btn, stop_btn, clear_btn],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20
                ),
                
                ft.Divider(),
                
                # 日志区域
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("运行日志", size=16, weight=ft.FontWeight.BOLD),
                            ft.Container(
                                content=log_list,
                                bgcolor="black",
                                padding=10,
                                border_radius=5,
                                height=200
                            )
                        ]
                    ),
                    padding=10,
                    bgcolor="#1E1E1E",
                    border_radius=10
                ),
            ],
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )
    )
    
    # 添加初始日志
    add_log("监控界面已启动")
    add_log("等待开始命令...")


if __name__ == "__main__":
    print("正在启动监控界面测试...")
    print("请稍候，界面即将出现...")
    ft.run(main)
