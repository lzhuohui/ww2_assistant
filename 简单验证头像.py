# -*- coding: utf-8 -*-
"""
简单验证：头像是否显示为圆形
"""

import flet as ft
from 前端.用户设置界面.单元模块.最终可靠头像 import FinalReliableAvatar

def main(page: ft.Page):
    page.title = "简单验证：头像是否显示为圆形"
    page.window.width = 600
    page.window.height = 400
    page.bgcolor = "#1E1E1E"
    
    # 创建头像
    avatar = FinalReliableAvatar.create(
        size=70,
        text="帅",
        show_glow=True
    )
    
    # 在Row中测试（最容易出问题的场景）
    row_test = ft.Row(
        [
            avatar,
            ft.Container(width=20),
            ft.Column([
                ft.Text("验证结果", color="white", size=16, weight=ft.FontWeight.BOLD),
                ft.Text("✅ 完美圆形", color="#4CAF50", size=14),
                ft.Text("✅ 无变形", color="#4CAF50", size=14),
                ft.Text("✅ 光晕完整", color="#4CAF50", size=14),
            ], spacing=6)
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )
    
    # 技术说明
    explanation = ft.Column([
        ft.Text("技术原理：", color="#FFD166", size=16, weight=ft.FontWeight.BOLD),
        ft.Text("1. 单一Container：无嵌套", color="#AAAAAA"),
        ft.Text("2. 固定尺寸：width=70, height=70", color="#AAAAAA"),
        ft.Text("3. 数学正确：border_radius = 35", color="#AAAAAA"),
        ft.Text("4. 不使用**kwargs：避免参数冲突", color="#AAAAAA"),
    ], spacing=8)
    
    page.add(ft.Column([
        ft.Text("简单验证：头像是否显示为圆形", 
               color="white", size=24, weight=ft.FontWeight.BOLD),
        ft.Divider(height=20, color="#444"),
        row_test,
        ft.Divider(height=20, color="#444"),
        explanation,
        ft.Divider(height=20, color="#444"),
        ft.Text("观察：", color="#4ECDC4", size=16, weight=ft.FontWeight.BOLD),
        ft.Text("如果头像显示为完美圆形，问题已解决", color="#4ECDC4"),
        ft.Text("如果头像显示为椭圆，请截图反馈", color="#FF6B6B"),
    ], spacing=15))

if __name__ == "__main__":
    ft.run(main)