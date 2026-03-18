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
    page.title = "头像测试"
    page.window.width = 400
    page.window.height = 400
    page.bgcolor = "#333333"  # 深色背景便于观察
    
    # 创建头像
    avatar = Avatar.create(
        diameter=100,
        text="帅",
        show_glow=True,
        show_scan=True,
        enabled=True
    )
    
    # 添加调试信息显示
    debug_text = ft.Text("双击头像测试编辑状态", color="white", size=16)
    
    # 布局
    page.add(
        ft.Column([
            debug_text,
            ft.Container(
                content=avatar,
                alignment=ft.Alignment(0, 0),
                expand=True
            )
        ], expand=True)
    )
    
    # 添加回调来显示状态
    def on_text_change(new_text):
        debug_text.value = f"文字已改为: {new_text}"
        page.update()
    
    # 设置文字变化回调
    avatar.get_text = lambda: "帅"  # 临时修复
    avatar.set_text = lambda x: None  # 临时修复

if __name__ == "__main__":
    ft.run(main)