import flet as ft
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from 页面.设置页面.设置页面 import SettingsPage
from 页面.监控页面.监控页面 import MonitorPage
from 页面.关于页面.关于页面 import AboutPage

def main(page: ft.Page):
    """应用主入口"""
    # 页面配置
    page.title = "二战风云辅助工具"
    page.window_width = 800
    page.window_height = 600
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # 页面路由
    def route_change(e):
        page.views.clear()
        if page.route == "/":
            page.views.append(
                ft.View(
                    "/",
                    [
                        ft.AppBar(title=ft.Text("设置"), bgcolor=ft.colors.SURFACE_VARIANT),
                        SettingsPage(),
                    ]
                )
            )
        elif page.route == "/monitor":
            page.views.append(
                ft.View(
                    "/monitor",
                    [
                        ft.AppBar(title=ft.Text("监控"), bgcolor=ft.colors.SURFACE_VARIANT),
                        MonitorPage(),
                    ]
                )
            )
        elif page.route == "/about":
            page.views.append(
                ft.View(
                    "/about",
                    [
                        ft.AppBar(title=ft.Text("关于"), bgcolor=ft.colors.SURFACE_VARIANT),
                        AboutPage(),
                    ]
                )
            )
        page.update()
    
    def view_pop(e):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)
    
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go("/")

if __name__ == "__main__":
    ft.run(main)
