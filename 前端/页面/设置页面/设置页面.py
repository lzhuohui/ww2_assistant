import flet as ft

class SettingsPage(ft.BaseControl):
    """设置页面"""
    def __init__(self):
        super().__init__()
        self.settings = {
            "游戏路径": "",
            "设备ID": "",
            "脚本延迟": 1.0,
            "自动运行": False,
        }
    
    def build(self):
        # 游戏设置
        game_settings = ft.Column(
            [
                ft.Text("游戏设置", size=18, weight=ft.FontWeight.BOLD),
                ft.Row(
                    [
                        ft.Text("游戏路径:"),
                        ft.TextField(
                            value=self.settings["游戏路径"],
                            expand=True,
                            on_change=lambda e: setattr(self, "游戏路径", e.control.value)
                        ),
                        ft.ElevatedButton("浏览", on_click=self.browse_game_path)
                    ]
                ),
                ft.Row(
                    [
                        ft.Text("设备ID:"),
                        ft.TextField(
                            value=self.settings["设备ID"],
                            expand=True,
                            on_change=lambda e: setattr(self, "设备ID", e.control.value)
                        )
                    ]
                ),
            ],
            spacing=10,
            padding=20,
            bgcolor=ft.colors.SURFACE,
            border_radius=10
        )
        
        # 脚本设置
        script_settings = ft.Column(
            [
                ft.Text("脚本设置", size=18, weight=ft.FontWeight.BOLD),
                ft.Row(
                    [
                        ft.Text("脚本延迟:"),
                        ft.TextField(
                            value=str(self.settings["脚本延迟"]),
                            width=100,
                            on_change=lambda e: setattr(self, "脚本延迟", float(e.control.value))
                        ),
                        ft.Text("秒")
                    ]
                ),
                ft.Row(
                    [
                        ft.Checkbox(
                            label="自动运行",
                            value=self.settings["自动运行"],
                            on_change=lambda e: setattr(self, "自动运行", e.control.value)
                        )
                    ]
                ),
            ],
            spacing=10,
            padding=20,
            bgcolor=ft.colors.SURFACE,
            border_radius=10
        )
        
        # 操作按钮
        buttons = ft.Row(
            [
                ft.ElevatedButton("保存设置", on_click=self.save_settings),
                ft.ElevatedButton("加载默认", on_click=self.load_defaults),
                ft.ElevatedButton("开始运行", on_click=self.start_running)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20
        )
        
        return ft.Column(
            [
                game_settings,
                ft.Divider(),
                script_settings,
                ft.Divider(),
                buttons
            ],
            spacing=20,
            padding=20
        )
    
    def browse_game_path(self, e):
        """浏览游戏路径"""
        # 这里可以实现文件选择对话框
        pass
    
    def save_settings(self, e):
        """保存设置"""
        # 保存设置到文件
        pass
    
    def load_defaults(self, e):
        """加载默认设置"""
        # 加载默认设置
        pass
    
    def start_running(self, e):
        """开始运行"""
        # 跳转到监控页面
        self.page.go("/monitor")
