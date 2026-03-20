# -*- coding: utf-8 -*-
"""
模块名称：用户头像
设计思路及联动逻辑:
    在可靠头像基础上添加完整的编辑功能。
    1. 支持圆形显示、文字头像、图片URL、光晕效果
    2. 双击进入编辑状态，按Enter或点击其他地方保存
模块隔离原则:
    1. 不直接创建被调用模块的内容
    2. 不覆盖被调用模块的计算结果
    3. 用户指定变量除外
"""

import threading
import time
from typing import Callable, Optional

import flet as ft

from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider
from 前端.用户设置界面.配置.界面配置 import 界面配置


# *** 用户指定变量 - AI不得修改, 变量值必须生效 ***
# （用户未指定变量）
# *********************************


class Avatar:
    """可编辑可靠圆形头像"""
    
    @staticmethod
    def create(
        size: int=70,
        text: str="帅",
        image_url: Optional[str]=None,
        bg_color: str="",
        text_color: str="#FFD700",
        show_glow: bool=True,
        on_click: Optional[Callable]=None,
        on_text_change: Optional[Callable[[str], None]]=None,
        enabled: bool=True,
    ) -> ft.Container:
        配置 = 界面配置()
        
        actual_size = size if size else 配置.获取尺寸("头像", "default_size") or 70
        actual_bg_color = bg_color if bg_color else ThemeProvider.get_color("bg_card")
        
        glow_spread = 配置.获取尺寸("阴影", "glow_spread") or 3
        glow_blur = 配置.获取尺寸("阴影", "glow_blur") or 20
        glow_delay = 配置.获取尺寸("头像", "glow_animation_delay") or 0.5
        glow_interval = 配置.获取尺寸("头像", "glow_animation_interval") or 0.2
        container_padding = 配置.获取尺寸("头像", "container_padding") or 10
        text_ratio = 配置.获取尺寸("头像", "text_ratio") or 0.6
        
        current_text = text[0] if text and len(text) > 0 else "帅"
        editing = False
        last_click_time = 0
        glow_running = False
        current_image_url = image_url
        
        radius = actual_size / 2
        
        def create_text_content():
            if current_image_url:
                return ft.Image(
                    src=current_image_url,
                    width=actual_size,
                    height=actual_size,
                    fit=ft.ImageFit.COVER,
                )
            else:
                return ft.Text(
                    current_text,
                    size=int(actual_size * text_ratio),
                    color=text_color,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                )
        
        def create_edit_content():
            return ft.TextField(
                value=current_text,
                text_align=ft.TextAlign.CENTER,
                border=ft.InputBorder.NONE,
                text_size=int(actual_size * text_ratio),
                color=text_color,
                bgcolor="transparent",
                dense=True,
                content_padding=ft.padding.all(0),
                max_length=1,
                autofocus=True,
                on_submit=lambda e: finish_edit(e.control.value),
                on_blur=lambda e: finish_edit(e.control.value),
            )
        
        def finish_edit(new_text: str):
            nonlocal current_text, editing
            
            if new_text and len(new_text) == 1 and '\u4e00' <= new_text <= '\u9fff':
                old_text = current_text
                current_text = new_text
                
                if on_text_change and old_text != new_text:
                    on_text_change(new_text)
            
            editing = False
            avatar_container.content = create_text_content()
            try:
                avatar_container.update()
            except:
                pass
        
        def show_tooltip_hint():
            if avatar_container.page:
                avatar_container.tooltip = "双击可编辑"
                try:
                    avatar_container.update()
                except:
                    pass
        
        def hide_tooltip():
            time.sleep(2)
            try:
                if avatar_container.page and avatar_container.tooltip == "双击可编辑":
                    avatar_container.tooltip = None
                    avatar_container.update()
            except:
                pass
        
        def handle_click(e):
            nonlocal editing, last_click_time
            
            if not enabled:
                return
            
            current_time = time.time()
            
            if editing:
                return
            
            if current_time - last_click_time < 0.3:
                editing = True
                avatar_container.content = create_edit_content()
                try:
                    avatar_container.update()
                except:
                    pass
            else:
                show_tooltip_hint()
                threading.Thread(target=hide_tooltip, daemon=True).start()
            
            last_click_time = current_time
            
            if on_click:
                on_click()
        
        def handle_long_press(e):
            if not editing and enabled:
                show_tooltip_hint()
                threading.Thread(target=hide_tooltip, daemon=True).start()
        
        avatar_container = ft.Container(
            content=create_text_content(),
            width=actual_size,
            height=actual_size,
            bgcolor=actual_bg_color,
            border_radius=ft.BorderRadius.all(radius),
            alignment=ft.Alignment(0, 0),
        )
        
        glow_color = text_color if text_color.startswith("#") else "#FFD700"
        
        if show_glow:
            avatar_container.shadow = ft.BoxShadow(
                spread_radius=glow_spread,
                blur_radius=glow_blur,
                color=f"{glow_color}80",
                offset=ft.Offset(0, 0),
            )
        
        glow_colors = [
            f"{glow_color}40",
            f"{glow_color}60",
            f"{glow_color}90",
            f"{glow_color}60",
            f"{glow_color}40",
        ]
        
        def run_glow_animation():
            nonlocal glow_running
            
            if not show_glow or editing or not enabled:
                return
            
            time.sleep(glow_delay)
            glow_running = True
            
            while glow_running and not editing and enabled:
                for color in glow_colors:
                    if not glow_running or editing or not enabled:
                        break
                    try:
                        avatar_container.shadow = ft.BoxShadow(
                            spread_radius=glow_spread,
                            blur_radius=glow_blur,
                            color=color,
                            offset=ft.Offset(0, 0),
                        )
                        avatar_container.update()
                        time.sleep(glow_interval)
                    except Exception:
                        break
            
            glow_running = False
        
        if show_glow and enabled:
            threading.Thread(target=run_glow_animation, daemon=True).start()
        
        container = ft.Container(
            content=avatar_container,
            width=actual_size + container_padding * 2,
            height=actual_size + container_padding * 2,
            alignment=ft.Alignment(0, 0),
        )
        
        container.on_click = handle_click
        container.on_long_press = handle_long_press
        
        def set_text(new_text: str):
            nonlocal current_text
            if new_text and len(new_text) == 1 and '\u4e00' <= new_text <= '\u9fff':
                current_text = new_text
                if not editing:
                    avatar_container.content = create_text_content()
                    try:
                        avatar_container.update()
                    except:
                        pass
        
        def set_image(url: str):
            nonlocal current_image_url
            current_image_url = url
            avatar_container.content = create_text_content()
            try:
                avatar_container.update()
            except:
                pass
        
        def get_text() -> str:
            return current_text
        
        def get_editing() -> bool:
            return editing
        
        container.set_text = set_text
        container.set_image = set_image
        container.get_text = get_text
        container.get_editing = get_editing
        
        return container


# *** 调试逻辑 ***
if __name__ == "__main__":
    ft.run(lambda page: page.add(Avatar.create()))
