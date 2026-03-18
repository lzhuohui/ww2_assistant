# -*- coding: utf-8 -*-
"""
最终验证：绝对可靠的圆形头像
"""

import flet as ft
from 前端.用户设置界面.单元模块.最终可靠头像 import FinalReliableAvatar

def main(page: ft.Page):
    page.title = "最终验证：绝对可靠的圆形头像"
    page.window.width = 900
    page.window.height = 700
    page.bgcolor = "#1E1E1E"
    
    # 创建测试场景
    tests = []
    
    # 场景1：基本测试
    avatar1 = FinalReliableAvatar.create(size=70, text="终", show_glow=True)
    tests.append(("基本测试", "直径70，文字'终'", avatar1))
    
    # 场景2：Row布局 - 最容易出问题的场景
    row_avatar = FinalReliableAvatar.create(size=70, text="R", bg_color="#2196F3")
    row_test = ft.Row(
        [
            row_avatar,
            ft.Container(width=20),
            ft.Column([
                ft.Text("Row布局测试", color="white", size=16, weight=ft.FontWeight.BOLD),
                ft.Text("这是最容易导致椭圆形的场景", color="#AAAAAA", size=12),
            ], spacing=4)
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )
    tests.append(("Row布局", "最容易导致椭圆形的场景", row_test))
    
    # 场景3：Column布局
    col_avatar = FinalReliableAvatar.create(size=70, text="C", bg_color="#4CAF50")
    col_test = ft.Column(
        [
            col_avatar,
            ft.Container(height=10),
            ft.Text("Column布局测试", color="white", size=16, weight=ft.FontWeight.BOLD),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
    tests.append(("Column布局", "垂直布局测试", col_test))
    
    # 场景4：模拟真实用户界面
    ui_avatar = FinalReliableAvatar.create(
        size=70,
        text="UI",
        show_glow=True,
        bg_color="#9C27B0"
    )
    simulated_ui = ft.Container(
        content=ft.Row(
            [
                ui_avatar,
                ft.Container(width=12),
                ft.Column([
                    ft.Text("最终可靠用户", color="white", size=14, weight=ft.FontWeight.BOLD),
                    ft.Text("✅ 完美圆形", color="#4CAF50", size=11),
                    ft.Text("✅ 无变形", color="#4CAF50", size=11),
                ], spacing=4)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        width=300,
        height=120,
        bgcolor="#1A1A1A",
        border_radius=12,
        padding=16,
        alignment=ft.Alignment(0, 0),
        clip_behavior=ft.ClipBehavior.NONE,
    )
    tests.append(("用户界面", "真实UI环境模拟", simulated_ui))
    
    # 场景5：极端测试 - 在尺寸异常的容器中
    extreme_avatar = FinalReliableAvatar.create(size=70, text="极", bg_color="#F44336")
    extreme_test = ft.Container(
        content=extreme_avatar,
        width=50,   # 容器宽度小于头像
        height=100, # 容器高度大于头像
        bgcolor="#333333",
        alignment=ft.Alignment(0, 0),
        border=ft.border.all(1, "#666666"),
    )
    tests.append(("极端容器", "容器尺寸异常", extreme_test))
    
    # 显示所有测试
    columns = []
    
    # 标题
    columns.append(ft.Text("最终验证：绝对可靠的圆形头像", 
                          color="white", size=28, weight=ft.FontWeight.BOLD))
    columns.append(ft.Text("解决所有椭圆问题的终极方案", 
                          color="#4ECDC4", size=16))
    
    columns.append(ft.Divider(height=20, color="#444"))
    
    # 技术原理
    columns.append(ft.Text("技术原理：", color="#FFD166", size=18, weight=ft.FontWeight.BOLD))
    columns.append(ft.Text("✅ 单一Container：无嵌套，无复杂结构", color="#AAAAAA"))
    columns.append(ft.Text("✅ 固定尺寸：width=size, height=size", color="#AAAAAA"))
    columns.append(ft.Text("✅ 数学正确：border_radius = size / 2", color="#AAAAAA"))
    columns.append(ft.Text("✅ 不使用**kwargs：避免参数冲突", color="#AAAAAA"))
    columns.append(ft.Text("✅ 不使用可能被覆盖的变量", color="#AAAAAA"))
    
    columns.append(ft.Divider(height=20, color="#444"))
    
    # 测试场景
    columns.append(ft.Text("测试场景：", color="#4ECDC4", size=18, weight=ft.FontWeight.BOLD))
    
    for title, description, content in tests:
        columns.append(ft.Text(f"🔍 {title}: {description}", color="#4ECDC4", size=14))
        columns.append(ft.Container(
            content=content,
            padding=12,
            bgcolor="#2D2D2D",
            border_radius=8,
            margin=ft.margin.only(bottom=20)
        ))
    
    # 验证结果
    columns.append(ft.Divider(height=20, color="#444"))
    columns.append(ft.Text("验证结果：", color="#4CAF50", size=18, weight=ft.FontWeight.BOLD))
    columns.append(ft.Text("✅ 所有场景都应该显示为完美圆形", color="#4CAF50"))
    columns.append(ft.Text("✅ 即使在Row布局中也不会变形", color="#4CAF50"))
    columns.append(ft.Text("✅ 光晕效果完整显示", color="#4CAF50"))
    columns.append(ft.Text("✅ 不受父容器尺寸影响", color="#4CAF50"))
    
    # 使用说明
    columns.append(ft.Divider(height=20, color="#444"))
    columns.append(ft.Text("使用方法：", color="#2196F3", size=18, weight=ft.FontWeight.BOLD))
    columns.append(ft.Text("from 前端.用户设置界面.单元模块.最终可靠头像 import FinalReliableAvatar", 
                          color="#AAAAAA", size=12, selectable=True))
    columns.append(ft.Text("avatar = FinalReliableAvatar.create(size=70, text='帅')", 
                          color="#AAAAAA", size=12, selectable=True))
    
    page.add(ft.Container(
        content=ft.Column(columns, spacing=12),
        padding=24
    ))

if __name__ == "__main__":
    ft.run(main)