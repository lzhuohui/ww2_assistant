# -*- coding: utf-8 -*-
"""
模块名称：可编辑可靠圆形头像 | 层级：零件层
设计思路：
    在最终可靠头像基础上添加完整的编辑功能。
    保持圆形显示的可靠性，同时支持文字编辑。

功能：
    1. 绝对可靠的圆形显示
    2. 支持文字头像
    3. 支持图片URL
    4. 光晕效果
    5. 完整的编辑功能：
       - 单击/长按：提示"双击可编辑"
       - 双击：进入编辑状态
       - 编辑状态：自动选中文字
       - 保存方式：按Enter或点击其他地方
       - 文字验证：只允许单个汉字

对外接口：
    - create(): 创建可编辑的圆形头像
    - set_text(): 设置文字
    - get_text(): 获取文字
    - set_image(): 设置图片
"""

import flet as ft
import time
import threading
from typing import Optional, Callable
from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider
from 前端.配置.界面配置 import 界面配置


def create_editable_reliable_avatar(
    size: int = 70,
    text: str = "帅",
    image_url: Optional[str] = None,
    bg_color: str = None,
    text_color: str = "#FFD700",
    show_glow: bool = True,
    on_click: Optional[Callable] = None,
    on_text_change: Optional[Callable[[str], None]] = None,
    enabled: bool = True,
) -> ft.Container:
    """
    创建可编辑的可靠圆形头像
    
    参数:
        size: 头像尺寸（直径）
        text: 显示的文字
        image_url: 图片URL（可选）
        bg_color: 背景颜色（默认使用主题颜色）
        text_color: 文字颜色
        show_glow: 是否显示光晕
        on_click: 点击回调
        on_text_change: 文字变化回调
        enabled: 是否启用
    
    返回:
        ft.Container: 可编辑的圆形头像
    """
    配置 = 界面配置()
    
    if size is None:
        size = 配置.获取尺寸("头像", "default_size") or 70
    if bg_color is None:
        bg_color = ThemeProvider.get_color("bg_card")
    
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
    
    radius = size / 2
    
    def create_text_content():
        """创建文字显示内容"""
        if image_url:
            return ft.Image(
                src=image_url,
                width=size,
                height=size,
                fit=ft.ImageFit.COVER,
            )
        else:
            return ft.Text(
                current_text,
                size=int(size * text_ratio),
                color=text_color,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
            )
    
    def create_edit_content():
        """创建编辑状态内容"""
        return ft.TextField(
            value=current_text,
            text_align=ft.TextAlign.CENTER,
            border=ft.InputBorder.NONE,
            text_size=int(size * text_ratio),
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
        """完成编辑"""
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
        """显示提示"""
        if avatar_container.page:
            avatar_container.tooltip = "双击可编辑"
            try:
                avatar_container.update()
            except:
                pass
    
    def hide_tooltip():
        """隐藏提示"""
        time.sleep(2)
        try:
            if avatar_container.page and avatar_container.tooltip == "双击可编辑":
                avatar_container.tooltip = None
                avatar_container.update()
        except:
            pass
    
    def handle_click(e):
        """处理点击事件"""
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
        """处理长按事件"""
        if not editing and enabled:
            show_tooltip_hint()
            threading.Thread(target=hide_tooltip, daemon=True).start()
    
    avatar_container = ft.Container(
        content=create_text_content(),
        width=size,
        height=size,
        bgcolor=bg_color,
        border_radius=ft.border_radius.all(radius),
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
        """运行光晕动画"""
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
        width=size + container_padding * 2,
        height=size + container_padding * 2,
        alignment=ft.Alignment(0, 0),
    )
    
    container.on_click = handle_click
    container.on_long_press = handle_long_press
    
    def set_text(new_text: str):
        """设置文字"""
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
        """设置图片"""
        nonlocal image_url
        image_url = url
        avatar_container.content = create_text_content()
        try:
            avatar_container.update()
        except:
            pass
    
    def get_text() -> str:
        """获取当前文字"""
        return current_text
    
    def get_editing() -> bool:
        """获取编辑状态"""
        return editing
    
    container.set_text = set_text
    container.set_image = set_image
    container.get_text = get_text
    container.get_editing = get_editing
    
    return container


class Avatar:
    """
    可编辑可靠圆形头像类
    """
    
    @staticmethod
    def create(
        size: int = 70,
        text: str = "帅",
        image_url: Optional[str] = None,
        bg_color: str = None,
        text_color: str = "#FFD700",
        show_glow: bool = True,
        on_click: Optional[Callable] = None,
        on_text_change: Optional[Callable[[str], None]] = None,
        enabled: bool = True,
    ) -> ft.Container:
        """
        创建可编辑的可靠圆形头像
        """
        return create_editable_reliable_avatar(
            size=size,
            text=text,
            image_url=image_url,
            bg_color=bg_color,
            text_color=text_color,
            show_glow=show_glow,
            on_click=on_click,
            on_text_change=on_text_change,
            enabled=enabled,
        )


# *** 调试逻辑 ***
if __name__ == "__main__":
    配置 = 界面配置()
    ThemeProvider.initialize(配置)
    def main(page: ft.Page):
        page.add(Avatar.create())
    ft.run(main)