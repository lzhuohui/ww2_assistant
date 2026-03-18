# -*- coding: utf-8 -*-
"""
完整编辑功能测试
测试头像编辑功能的所有交互场景
"""

import flet as ft
from 前端.用户设置界面.单元模块.可编辑可靠头像 import EditableReliableAvatar
from 前端.用户设置界面.配置.界面配置 import 界面配置
from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider

def main(page: ft.Page):
    # 初始化
    配置 = 界面配置()
    ThemeProvider.initialize(配置)
    
    page.title = "完整编辑功能测试"
    page.window.width = 900
    page.window.height = 700
    page.bgcolor = "#1E1E1E"
    
    # 状态显示
    status_text = ft.Text("状态: 等待交互", color="#4ECDC4", size=14)
    current_text_display = ft.Text("当前文字: 帅", color="#FFD700", size=14)
    
    # 文字变化回调
    def on_text_change(new_text):
        status_text.value = f"状态: 文字已修改为 '{new_text}'"
        current_text_display.value = f"当前文字: {new_text}"
        page.update()
        print(f"文字变化回调: {new_text}")
    
    # 创建可编辑头像
    avatar = EditableReliableAvatar.create(
        size=70,
        text="帅",
        show_glow=True,
        on_text_change=on_text_change,
    )
    
    # 测试场景
    test_scenarios = ft.Column([
        ft.Text("测试场景:", color="#FFD166", size=16, weight=ft.FontWeight.BOLD),
        ft.Text("1. 单击测试: 单击头像，应显示'双击可编辑'提示", color="#AAAAAA"),
        ft.Text("2. 长按测试: 长按头像，应显示'双击可编辑'提示", color="#AAAAAA"),
        ft.Text("3. 双击测试: 快速双击头像，应进入编辑状态", color="#AAAAAA"),
        ft.Text("4. 编辑测试: 输入单个汉字，按Enter保存", color="#AAAAAA"),
        ft.Text("5. 点击其他地方测试: 编辑时点击空白处，应保存", color="#AAAAAA"),
        ft.Text("6. 无效输入测试: 输入非汉字或超过1个字符，应不保存", color="#AAAAAA"),
    ], spacing=8)
    
    # 控制按钮
    def set_to_love():
        avatar.set_text("爱")
        status_text.value = "状态: 通过set_text()设置为'爱'"
        current_text_display.value = "当前文字: 爱"
        page.update()
    
    def set_to_beauty():
        avatar.set_text("美")
        status_text.value = "状态: 通过set_text()设置为'美'"
        current_text_display.value = "当前文字: 美"
        page.update()
    
    def get_text():
        text = avatar.get_text()
        status_text.value = f"状态: 通过get_text()获取到 '{text}'"
        page.update()
        print(f"获取文字: {text}")
    
    def get_editing():
        editing = avatar.get_editing()
        status_text.value = f"状态: 编辑状态为 {editing}"
        page.update()
        print(f"编辑状态: {editing}")
    
    def simulate_double_click():
        # 模拟双击（实际需要用户操作，这里只是提示）
        status_text.value = "状态: 请手动快速双击头像进行测试"
        page.update()
    
    controls = ft.Column([
        ft.Text("编程接口测试:", color="#2196F3", size=16, weight=ft.FontWeight.BOLD),
        ft.Row([
            ft.ElevatedButton("set_text('爱')", on_click=lambda e: set_to_love()),
            ft.ElevatedButton("set_text('美')", on_click=lambda e: set_to_beauty()),
            ft.ElevatedButton("get_text()", on_click=lambda e: get_text()),
            ft.ElevatedButton("get_editing()", on_click=lambda e: get_editing()),
        ], spacing=10),
        ft.Text("", color="#AAAAAA"),
        ft.Text("交互测试提示:", color="#4ECDC4", size=14),
        ft.Text("• 请手动测试单击、长按、双击等交互", color="#AAAAAA"),
        ft.Text("• 观察状态显示的变化", color="#AAAAAA"),
        ft.Text("• 查看控制台输出", color="#AAAAAA"),
    ], spacing=10)
    
    # 技术说明
    explanation = ft.Column([
        ft.Text("技术实现说明:", color="#9C27B0", size=16, weight=ft.FontWeight.BOLD),
        ft.Text("✅ 圆形可靠性: 使用固定尺寸 + border_radius = size/2", color="#AAAAAA"),
        ft.Text("✅ 双击检测: 使用time.time()检测0.3秒内的两次点击", color="#AAAAAA"),
        ft.Text("✅ 状态管理: editing变量控制编辑状态", color="#AAAAAA"),
        ft.Text("✅ 文字验证: 只允许单个汉字（\\u4e00-\\u9fff）", color="#AAAAAA"),
        ft.Text("✅ 事件处理: on_click, on_long_press, on_submit, on_blur", color="#AAAAAA"),
        ft.Text("✅ 线程安全: 使用threading处理光晕动画", color="#AAAAAA"),
        ft.Text("✅ 回调机制: on_text_change回调函数", color="#AAAAAA"),
    ], spacing=6)
    
    page.add(ft.Column([
        ft.Text("完整编辑功能测试", color="white", size=28, weight=ft.FontWeight.BOLD),
        ft.Text("测试头像编辑功能的所有交互场景", color="#4ECDC4", size=16),
        ft.Divider(height=20, color="#444"),
        
        # 头像展示区域
        ft.Container(
            content=ft.Column([
                ft.Text("可编辑头像:", color="white", size=18, weight=ft.FontWeight.BOLD),
                avatar,
                ft.Divider(height=10, color="#333"),
                status_text,
                current_text_display,
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15),
            padding=20,
            bgcolor="#2D2D2D",
            border_radius=12,
            alignment=ft.Alignment(0, 0),
        ),
        
        ft.Divider(height=20, color="#444"),
        test_scenarios,
        ft.Divider(height=20, color="#444"),
        controls,
        ft.Divider(height=20, color="#444"),
        explanation,
        
        # 使用说明
        ft.Container(
            content=ft.Column([
                ft.Text("使用说明:", color="#FFD166", size=16, weight=ft.FontWeight.BOLD),
                ft.Text("导入:", color="#4ECDC4", size=14),
                ft.Text("from 前端.用户设置界面.单元模块.可编辑可靠头像 import EditableReliableAvatar", 
                       color="#AAAAAA", size=12, selectable=True),
                ft.Text("", color="#AAAAAA"),
                ft.Text("创建头像:", color="#4ECDC4", size=14),
                ft.Text("avatar = EditableReliableAvatar.create(size=70, text='帅', on_text_change=callback)", 
                       color="#AAAAAA", size=12, selectable=True),
                ft.Text("", color="#AAAAAA"),
                ft.Text("控制方法:", color="#4ECDC4", size=14),
                ft.Text("avatar.set_text('新文字')  # 设置文字", color="#AAAAAA"),
                ft.Text("avatar.get_text()         # 获取文字", color="#AAAAAA"),
                ft.Text("avatar.set_image('url')   # 设置图片", color="#AAAAAA"),
                ft.Text("avatar.get_editing()      # 获取编辑状态", color="#AAAAAA"),
            ], spacing=8),
            padding=15,
            bgcolor="#1A1A1A",
            border_radius=8,
        ),
    ], spacing=15))

if __name__ == "__main__":
    ft.run(main)