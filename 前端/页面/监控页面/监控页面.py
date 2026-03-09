import flet as ft
import time

class MonitorPage(ft.BaseControl):
    """监控页面"""
    def __init__(self):
        super().__init__()
        self.status = "就绪"
        self.logs = []
        self.start_time = None
    
    def build(self):
        # 状态卡片
        status_card = ft.Column(
            [
                ft.Text("运行状态", size=18, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=ft.Text(
                        self.status,
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=ft.colors.GREEN if self.status == "运行中" else ft.colors.BLUE
                    ),
                    padding=20,
                    bgcolor=ft.colors.SURFACE,
                    border_radius=10,
                    alignment=ft.alignment.center
                ),
                ft.Row(
                    [
                        ft.ElevatedButton("开始", on_click=self.start_monitoring),
                        ft.ElevatedButton("暂停", on_click=self.pause_monitoring),
                        ft.ElevatedButton("停止", on_click=self.stop_monitoring)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20
                )
            ],
            spacing=10,
            padding=20,
            bgcolor=ft.colors.SURFACE,
            border_radius=10
        )
        
        # 日志查看器
        self.log_list = ft.ListView(
            expand=True,
            spacing=10,
            padding=10
        )
        
        log_card = ft.Column(
            [
                ft.Text("运行日志", size=18, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=self.log_list,
                    height=300,
                    bgcolor=ft.colors.SURFACE,
                    border_radius=10,
                    padding=10
                ),
                ft.Row(
                    [
                        ft.ElevatedButton("清空日志", on_click=self.clear_logs),
                        ft.ElevatedButton("导出日志", on_click=self.export_logs)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20
                )
            ],
            spacing=10,
            padding=20,
            bgcolor=ft.colors.SURFACE,
            border_radius=10
        )
        
        return ft.Column(
            [
                status_card,
                ft.Divider(),
                log_card
            ],
            spacing=20,
            padding=20
        )
    
    def start_monitoring(self, e):
        """开始监控"""
        self.status = "运行中"
        self.start_time = time.time()
        self.add_log("开始监控")
        self.update()
    
    def pause_monitoring(self, e):
        """暂停监控"""
        self.status = "暂停"
        self.add_log("暂停监控")
        self.update()
    
    def stop_monitoring(self, e):
        """停止监控"""
        self.status = "停止"
        self.add_log("停止监控")
        self.update()
    
    def add_log(self, message):
        """添加日志"""
        timestamp = time.strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.logs.append(log_entry)
        self.log_list.controls.append(ft.Text(log_entry))
        if len(self.logs) > 50:
            self.logs.pop(0)
            self.log_list.controls.pop(0)
        self.update()
    
    def clear_logs(self, e):
        """清空日志"""
        self.logs.clear()
        self.log_list.controls.clear()
        self.update()
    
    def export_logs(self, e):
        """导出日志"""
        # 导出日志到文件
        pass
