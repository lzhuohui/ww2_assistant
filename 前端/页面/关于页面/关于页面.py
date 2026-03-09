import flet as ft

class AboutPage(ft.BaseControl):
    """关于页面"""
    def build(self):
        return ft.Column(
            [
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("二战风云辅助工具", size=24, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                            ft.Text("版本: 1.0.0", size=16, text_align=ft.TextAlign.CENTER),
                            ft.Divider(),
                            ft.Text("功能介绍", size=18, weight=ft.FontWeight.BOLD),
                            ft.Text("- 游戏设置管理", size=14),
                            ft.Text("- 脚本运行监控", size=14),
                            ft.Text("- 运行日志查看", size=14),
                            ft.Divider(),
                            ft.Text("技术架构", size=18, weight=ft.FontWeight.BOLD),
                            ft.Text("- 前端: Flet (Python)", size=14),
                            ft.Text("- 后端: Python", size=14),
                            ft.Text("- 设备控制: ADB", size=14),
                            ft.Divider(),
                            ft.Text("使用说明", size=18, weight=ft.FontWeight.BOLD),
                            ft.Text("1. 在设置页面配置游戏路径和设备ID", size=14),
                            ft.Text("2. 调整脚本参数", size=14),
                            ft.Text("3. 点击开始运行", size=14),
                            ft.Text("4. 在监控页面查看运行状态", size=14),
                            ft.Divider(),
                            ft.Text("版权信息", size=18, weight=ft.FontWeight.BOLD),
                            ft.Text("© 2026 二战风云辅助工具", size=14, text_align=ft.TextAlign.CENTER),
                            ft.Text("本工具仅供学习使用", size=14, text_align=ft.TextAlign.CENTER)
                        ],
                        spacing=10,
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    padding=30,
                    bgcolor=ft.colors.SURFACE,
                    border_radius=10,
                    alignment=ft.alignment.center
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        )
