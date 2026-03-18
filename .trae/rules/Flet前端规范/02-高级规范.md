---
name: 05-Flet前端规范-高级
description: Flet框架高级规范
globs: ["gui/**/*.py", "ui/**/*.py", "**/*view*.py", "**/*page*.py"]
---

# Flet前端开发规范（高级）

## 异步处理
- 长时间运行的任务（如游戏循环）应放在线程中运行
- 使用`ft.Page`的`run_task`或`asyncio`处理异步
- 更新UI时使用`page.add()`或直接修改控件属性后调用`update()`

## 示例代码
```python
import flet as ft

class MonitorPage(ft.Column):
    def __init__(self):
        super().__init__()
        self.status_text = ft.Text("等待连接...")
        self.log_view = ft.ListView(expand=True, spacing=5)
        self.controls = [
            ft.Text("游戏监控", size=20),
            self.status_text,
            ft.Container(content=self.log_view, height=200),
        ]
    
    def update_status(self, status):
        self.status_text.value = status
        self.update()
```
