# -*- coding: utf-8 -*-
"""
退出时间测试脚本（用户视角）

测试场景：
1. 启动应用
2. 点击"建筑"导航按钮
3. 在建筑页面操作下拉框
4. 点击"系统"导航按钮退出建筑页面
5. 测量从点击到页面完全切换的实际时间
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import time
import flet as ft
from 配置.界面配置 import 界面配置
from 新思路.页面层.主界面 import MainPage


timer_events = []


def record_event(event_name):
    """记录事件时间"""
    global timer_events
    current_time = time.time()
    timer_events.append((event_name, current_time))
    print(f"[{time.strftime('%H:%M:%S', time.localtime(current_time))}] {event_name}")


def main(page: ft.Page):
    global timer_events
    配置 = 界面配置()
    
    page.padding = 0
    page.bgcolor = 配置.当前主题颜色["bg_primary"]
    
    # 创建主界面
    main_page = MainPage(配置)
    main_page.page = page
    
    # 记录启动时间
    record_event("应用启动")
    
    # 创建界面
    page.add(main_page.create())
    record_event("界面创建完成")
    
    # 创建测试面板
    status_text = ft.Text("请手动测试：点击'建筑' -> 操作下拉框 -> 点击'系统'", size=14, color="yellow")
    
    # 添加计时按钮
    start_btn = ft.ElevatedButton(
        "开始计时（点击后立即点击'建筑'导航）",
        on_click=lambda e: start_test(),
        bgcolor="green",
        color="white",
    )
    
    end_btn = ft.ElevatedButton(
        "结束计时（点击后立即点击'系统'导航）",
        on_click=lambda e: end_test(),
        bgcolor="red",
        color="white",
    )
    
    test_panel = ft.Container(
        content=ft.Column([
            ft.Text("退出时间测试工具", size=18, weight=ft.FontWeight.BOLD, color="white"),
            ft.Container(height=10),
            status_text,
            ft.Container(height=10),
            ft.Row([start_btn, end_btn], spacing=10),
        ]),
        padding=15,
        bgcolor="black",
        border_radius=10,
    )
    
    page.add(test_panel)
    
    def start_test():
        timer_events = []
        record_event("开始计时（用户即将点击'建筑'）")
        status_text.value = "计时中... 请点击'建筑'导航按钮"
        page.update()
    
    def end_test():
        record_event("结束计时（用户已点击'系统'）")
        
        # 计算时间
        if len(timer_events) >= 2:
            total_time = timer_events[-1][1] - timer_events[0][1]
            status_text.value = f"测试完成！总耗时: {total_time:.3f}秒"
            
            # 打印详细报告
            print("\n" + "="*60)
            print("退出时间测试报告")
            print("="*60)
            for i in range(1, len(timer_events)):
                prev_name, prev_time = timer_events[i-1]
                curr_name, curr_time = timer_events[i]
                elapsed = curr_time - prev_time
                print(f"{prev_name} -> {curr_name}: {elapsed:.3f}秒")
            print(f"\n总耗时: {total_time:.3f}秒")
            print("="*60)
        
        page.update()


if __name__ == "__main__":
    ft.run(main)
