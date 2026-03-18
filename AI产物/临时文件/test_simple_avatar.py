import flet as ft
import time

class SimpleAvatar:
    """简化的头像组件，专门测试编辑状态背景色"""
    
    @staticmethod
    def create(diameter=100, text="帅"):
        current_text = text
        editing = False
        last_click_time = 0
        radius = diameter / 2
        
        # 创建圆形背景容器
        circle_bg = ft.Container(
            width=diameter,
            height=diameter,
            border_radius=ft.BorderRadius.all(radius),
            bgcolor="transparent",
        )
        
        # 创建文字
        def create_text():
            return ft.Text(
                current_text,
                size=int(radius * 1.5),
                color="#FFD700",  # 金色
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
            )
        
        # 创建文字容器
        text_container = ft.Container(
            content=create_text(),
            alignment=ft.Alignment(0, 0),
            width=diameter,
            height=diameter,
            bgcolor="transparent",
        )
        
        # 创建 TextField
        def create_textfield():
            return ft.TextField(
                value=current_text,
                text_align=ft.TextAlign.CENTER,
                border=ft.InputBorder.NONE,
                text_size=int(radius * 1.5),
                color="#FFE44D",  # 亮金色
                text_style=ft.TextStyle(color="#FFE44D", weight=ft.FontWeight.BOLD),
                cursor_color="#FFE44D",
                bgcolor="transparent",
                focused_bgcolor="transparent",
                dense=True,
                content_padding=0,
                max_length=1,
                autofocus=True,
            )
        
        # 创建 Stack
        stack = ft.Stack(
            [
                circle_bg,      # 底层：背景
                text_container, # 上层：文字
            ],
            width=diameter,
            height=diameter,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        )
        
        # 主容器
        main_container = ft.Container(
            content=stack,
            width=diameter,
            height=diameter,
            border_radius=ft.BorderRadius.all(radius),
            bgcolor="transparent",
        )
        
        # 最外层容器
        container = ft.Container(
            content=main_container,
            border_radius=ft.BorderRadius.all(radius),
            bgcolor="transparent",
        )
        
        def handle_click(e):
            nonlocal editing, last_click_time
            
            current_time = time.time()
            
            if editing:
                # 退出编辑
                editing = False
                circle_bg.bgcolor = "transparent"
                main_container.bgcolor = "transparent"
                container.bgcolor = "transparent"
                text_container.bgcolor = "transparent"
                text_container.content = create_text()
                print("退出编辑状态")
            else:
                if current_time - last_click_time < 0.3:
                    # 双击进入编辑
                    editing = True
                    circle_bg.bgcolor = "#FF0000"  # 红色
                    main_container.bgcolor = "#FF0000"  # 红色
                    container.bgcolor = "#FF0000"  # 红色
                    text_container.bgcolor = "#FF0000"  # 红色
                    text_container.content = create_textfield()
                    print("进入编辑状态 - 背景色应为红色")
                else:
                    print("单击")
                last_click_time = current_time
            
            # 更新所有容器
            circle_bg.update()
            main_container.update()
            container.update()
            text_container.update()
        
        container.on_click = handle_click
        
        return container

def main(page: ft.Page):
    page.title = "简化头像测试"
    page.window.width = 400
    page.window.height = 400
    page.bgcolor = "#CCCCCC"  # 浅灰色背景
    
    # 创建简化头像
    avatar = SimpleAvatar.create(diameter=150, text="帅")
    
    # 添加说明
    instructions = ft.Text(
        "双击头像测试编辑状态背景色\n应该变成红色",
        color="black",
        size=16,
        text_align=ft.TextAlign.CENTER
    )
    
    page.add(
        ft.Column([
            instructions,
            ft.Container(
                content=avatar,
                alignment=ft.Alignment(0, 0),
                padding=50,
                bgcolor="#888888",  # 中灰色
                border=ft.border.all(2, "black")
            )
        ], expand=True, spacing=20, alignment=ft.MainAxisAlignment.CENTER)
    )

if __name__ == "__main__":
    ft.run(main)