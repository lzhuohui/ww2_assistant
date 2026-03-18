import flet as ft
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from 前端.用户设置界面.零件.头像 import Avatar
from 前端.用户设置界面.配置.界面配置 import 界面配置
from 前端.用户设置界面.核心.主题提供者 import ThemeProvider

def main(page: ft.Page):
    # 初始化配置和主题
    配置 = 界面配置()
    ThemeProvider.initialize(配置)
    
    # 设置页面
    page.title = "头像调试"
    page.window.width = 600
    page.window.height = 600
    page.bgcolor = "#888888"  # 灰色背景便于观察
    
    # 创建头像
    avatar = Avatar.create(
        diameter=150,  # 大尺寸便于观察
        text="帅",
        show_glow=True,
        show_scan=True,
        enabled=True
    )
    
    # 添加调试信息显示
    debug_text = ft.Text("状态: 等待双击", color="white", size=16)
    color_info = ft.Text("", color="white", size=14)
    
    # 创建测试按钮
    def test_edit():
        # 模拟双击进入编辑状态
        print("=== 模拟编辑状态 ===")
        # 手动调用编辑逻辑
        avatar.on_click(None)  # 第一次点击
        import time
        time.sleep(0.1)
        avatar.on_click(None)  # 第二次点击（模拟双击）
        debug_text.value = "已模拟双击进入编辑状态"
        page.update()
    
    test_button = ft.ElevatedButton(
        "测试编辑状态",
        on_click=lambda e: test_edit()
    )
    
    # 布局
    page.add(
        ft.Column([
            ft.Text("头像编辑状态调试", color="white", size=20, weight=ft.FontWeight.BOLD),
            debug_text,
            color_info,
            test_button,
            ft.Divider(height=20, color="white"),
            ft.Container(
                content=avatar,
                alignment=ft.Alignment(0, 0),
                padding=50,
                bgcolor="#555555",  # 中等灰色背景
                border=ft.border.all(2, "white")
            ),
            ft.Text("说明: 1. 双击头像 2. 或点击上方测试按钮", color="white", size=12)
        ], expand=True, spacing=10)
    )

if __name__ == "__main__":
    ft.run(main)