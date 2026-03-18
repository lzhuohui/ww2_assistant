# -*- coding: utf-8 -*-
"""
头像 - 零件层（新思路）

设计思路:
    独立功能模块，轻量级设计。
    圆形光影效果，支持扫描动画。

功能:
    1. 圆形背景
    2. 金色大字，默认"帅"
    3. 圆形光晕效果
    4. 扫描动画效果
    5. 点击/长按提示可编辑
    6. 双击进入编辑状态
    7. 支持主题联动

数据来源:
    所有配置数据从配置目录获取。

使用场景:
    被组件层模块调用，也可独立使用。

可独立运行调试: python 头像.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft
import time
import asyncio
from typing import Callable, Optional
from 配置.界面配置 import 界面配置


# *** 用户指定变量 - AI不得修改 ***
# (用户指定的变量放在这里，用户没有指定之前就空着)
# *********************************


class Avatar:
    """头像 - 独立功能模块"""
    
    @staticmethod
    def create(
        config: 界面配置,
        diameter: int = 60,
        text: str = "帅",
        on_text_change: Callable[[str], None] = None,
        show_glow: bool = True,
        show_scan: bool = True,
        **kwargs
    ) -> ft.Container:
        """
        创建头像组件
        
        参数:
            config: 界面配置对象
            diameter: 头像直径
            text: 初始文字，默认"帅"
            on_text_change: 文字变化回调
            show_glow: 是否显示光晕
            show_scan: 是否显示扫描效果
        
        返回:
            ft.Container: 头像容器
        """
        theme_colors = config.当前主题颜色
        
        # 内部状态
        current_text = text if text else "帅"
        editing = False
        last_click_time = 0
        show_tooltip = False
        
        radius = diameter / 2
        
        # 从主题获取颜色（支持主题联动）
        text_color = theme_colors.get("avatar_text", "#FFD700")
        glow_color = theme_colors.get("avatar_glow", "#FFD70080")
        scan_color = theme_colors.get("avatar_scan", "#FFFFFF40")
        bg_color = theme_colors.get("avatar_bg", "#1A1A1A")
        
        # 创建文字控件
        def create_text() -> ft.Text:
            return ft.Text(
                current_text,
                size=int(radius * 1.5),
                color=text_color,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
            )
        
        # 创建文本框控件
        def create_textfield() -> ft.TextField:
            def on_focus_handler(e):
                e.control.selection = (0, len(current_text))
            
            return ft.TextField(
                value=current_text,
                text_align=ft.TextAlign.CENTER,
                border=ft.InputBorder.NONE,
                text_size=int(radius * 1.5),
                color=text_color,
                dense=True,
                content_padding=0,
                max_length=1,
                autofocus=True,
                on_focus=on_focus_handler,
                on_submit=lambda e: finish_edit(e.control.value),
                on_blur=lambda e: finish_edit(e.control.value),
            )
        
        # 创建提示文字
        tooltip_text = ft.Text(
            "双击可编辑",
            size=10,
            color=theme_colors.get("text_secondary", "#888888"),
            visible=False,
        )
        
        # 完成编辑
        def finish_edit(new_text: str):
            nonlocal current_text, editing
            
            if new_text and len(new_text) == 1 and '\u4e00' <= new_text <= '\u9fff':
                old_text = current_text
                current_text = new_text
                if on_text_change and old_text != new_text:
                    on_text_change(new_text)
            
            editing = False
            text_container.content = create_text()
            text_container.update()
        
        # 显示提示
        def show_tooltip_hint():
            nonlocal show_tooltip
            show_tooltip = True
            tooltip_text.visible = True
            tooltip_text.update()
            
            # 2秒后隐藏
            def hide_tooltip():
                nonlocal show_tooltip
                time.sleep(2)
                show_tooltip = False
                tooltip_text.visible = False
                tooltip_text.update()
            
            import threading
            threading.Thread(target=hide_tooltip, daemon=True).start()
        
        # 处理点击
        def handle_click(e):
            nonlocal editing, last_click_time, current_text
            
            current_time = time.time()
            
            if editing:
                if isinstance(e.control, ft.TextField):
                    return
                if text_container and isinstance(text_container.content, ft.TextField):
                    finish_edit(text_container.content.value)
            else:
                if current_time - last_click_time < 0.3:
                    # 双击进入编辑
                    editing = True
                    if text_container:
                        text_container.content = create_textfield()
                        text_container.update()
                else:
                    # 单击显示提示
                    show_tooltip_hint()
                last_click_time = current_time
        
        # 处理长按
        def handle_long_press(e):
            if not editing:
                show_tooltip_hint()
        
        # 创建文字容器
        text_container = ft.Container(
            content=create_text(),
            alignment=ft.Alignment(0, 0),
        )
        
        # 创建圆形背景（透明，用光影整体处理）
        circle_bg = ft.Container(
            width=diameter,
            height=diameter,
            border_radius=ft.BorderRadius.all(radius),
            bgcolor="transparent",
        )
        
        # 创建扫描线
        scan_line = ft.Container(
            width=diameter,
            height=2,
            bgcolor=scan_color,
            visible=False,
            animate=ft.Animation(2000, ft.AnimationCurve.LINEAR),
        )
        
        # 创建主容器（圆形背景 + 文字）
        main_stack = ft.Stack(
            [
                circle_bg,
                text_container,
                scan_line,
            ],
            width=diameter,
            height=diameter,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        )
        
        # 创建主容器
        main_content = ft.Container(
            content=main_stack,
            width=diameter,
            height=diameter,
            border_radius=ft.BorderRadius.all(radius),
        )
        
        # 添加光晕效果
        if show_glow:
            main_content.shadow = ft.BoxShadow(
                spread_radius=2,
                blur_radius=8,
                color=glow_color,
                offset=ft.Offset(0, 0),
            )
        
        # 光影渐变动画控制
        glow_running = False
        glow_colors = [
            "#FFD70080",  # 金色
            "#FFA50080",  # 橙色
            "#FF634780",  # 番茄色
            "#FF450080",  # 橙红色
            "#FFD70080",  # 金色
        ]
        glow_index = 0
        
        async def run_glow_animation():
            nonlocal glow_running, glow_index
            if not show_glow or editing:
                return
            
            # 等待控件添加到页面
            retry_count = 0
            while retry_count < 50:  # 最多等待5秒
                try:
                    if main_content.page:
                        break
                except RuntimeError:
                    pass
                await asyncio.sleep(0.1)
                retry_count += 1
            
            try:
                if not main_content.page:
                    glow_running = False
                    return
            except RuntimeError:
                glow_running = False
                return
            
            glow_running = True
            
            while glow_running and not editing:
                for i, color in enumerate(glow_colors):
                    if not glow_running or editing:
                        break
                    # 检查控件是否仍在页面中
                    try:
                        if not main_content.page:
                            glow_running = False
                            return
                    except RuntimeError:
                        glow_running = False
                        return
                    main_content.shadow = ft.BoxShadow(
                        spread_radius=2,
                        blur_radius=8,
                        color=color,
                        offset=ft.Offset(0, 0),
                    )
                    main_content.update()
                    await asyncio.sleep(0.5)  # 每0.5秒切换一次颜色
            
            glow_running = False
        
        def start_glow():
            if show_glow and not editing and not glow_running:
                import threading
                import asyncio
                
                async def delayed_run_glow():
                    await asyncio.sleep(0.5)  # 额外等待0.5秒
                    await run_glow_animation()
                
                loop = asyncio.new_event_loop()
                threading.Thread(
                    target=lambda: loop.run_until_complete(delayed_run_glow()),
                    daemon=True
                ).start()
        
        # 启动光影渐变动画（延迟启动，等待控件添加到页面）
        if show_glow:
            def delayed_start_glow():
                time.sleep(3)  # 等待3秒确保控件已添加到页面
                start_glow()
            
            import threading
            threading.Thread(target=delayed_start_glow, daemon=True).start()
        
        # 扫描动画控制
        scan_running = False
        
        async def run_scan_animation():
            nonlocal scan_running
            if not show_scan or editing:
                return
            
            scan_running = True
            scan_line.visible = True
            
            # 从上到下扫描
            for i in range(0, int(diameter), 2):
                if not scan_running or editing:
                    break
                # 检查控件是否仍在页面中
                if not main_stack.page:
                    scan_running = False
                    return
                scan_line.top = i
                main_stack.update()
                await asyncio.sleep(0.02)
            
            # 检查控件是否仍在页面中
            if not main_stack.page:
                scan_running = False
                return
            scan_line.visible = False
            main_stack.update()
            scan_running = False
        
        def start_scan():
            if show_scan and not editing and not scan_running:
                import threading
                loop = asyncio.new_event_loop()
                threading.Thread(
                    target=lambda: loop.run_until_complete(run_scan_animation()),
                    daemon=True
                ).start()
        
        # 定时启动扫描动画（延迟启动，等待控件添加到页面）
        def scan_timer():
            time.sleep(2)  # 等待2秒确保控件已添加到页面
            while True:
                time.sleep(3)  # 每3秒扫描一次
                if not editing:
                    start_scan()
        
        import threading
        # 延迟启动扫描动画，等待控件添加到页面
        def delayed_start_scan():
            time.sleep(3)  # 等待3秒确保控件已添加到页面
            if show_scan:
                threading.Thread(target=scan_timer, daemon=True).start()
        
        if show_scan:
            threading.Thread(target=delayed_start_scan, daemon=True).start()
        
        # 创建完整容器
        container = ft.Container(
            content=ft.Column(
                [
                    main_content,
                    ft.Container(height=5),
                    tooltip_text,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
            ),
            on_click=handle_click,
            on_long_press=handle_long_press,
        )
        
        # 暴露控制接口
        def set_text(new_text: str):
            nonlocal current_text
            if new_text and len(new_text) == 1 and '\u4e00' <= new_text <= '\u9fff':
                current_text = new_text
                if text_container and not editing:
                    text_container.content = create_text()
                    text_container.update()
        
        container.set_text = set_text
        container.get_text = lambda: current_text
        
        return container


# 兼容别名
头像 = Avatar


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    # 1. 界面配置初始化
    配置 = 界面配置()
    
    # 2. 自动加载用户数据覆盖默认值（在界面配置.__init__中自动完成）
    
    # 3. 正常启动被测模块
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        page.add(Avatar.create(配置, diameter=60, text="帅", show_glow=True, show_scan=True))  # 只能更改此处**被测调用模块名称**
    
    ft.run(main)
# *** 调试逻辑 ***
if __name__ == "__main__":
    配置 = 界面配置()
    def main(page: ft.Page):
        # 不设置任何页面属性，让被测模块自己决定
        page.add(Avatar(配置).render())
    ft.run(main)