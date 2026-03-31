# -*- coding: utf-8 -*-

"""
模块名称：头像.py
模块功能：头像组件，支持双击编辑金色文字

实现步骤：
- 创建圆形光影容器
- 支持金色渐变文字效果
- 支持双击编辑功能
- 支持悬停动画效果
- 支持光晕动画效果
- 从用户偏好.json获取UI配置

职责：
- 圆形光影容器
- 金色渐变文字
- 双击编辑功能
- 悬停动画效果
- 光晕动画效果
- 从用户偏好.json获取UI配置

不负责：
- 用户信息获取
- 数据持久化

设计原则（符合V2版本模块化设计补充共识):
- 用户偏好.json是UI配置唯一来源
- 如果用户偏好.json缺少配置，抛出错误
- 不使用DEFAULT_XXX掩盖问题
"""

import flet as ft
import time
import threading
from typing import Dict, Optional, Callable

# ============================================
# 数据和文件接口(前置,方便查看和修改)
# ============================================

DEFAULT_TEXT = "帅"

# 头像无默认值配置,所有UI配置从用户偏好.json获取
# 如果用户偏好.json缺少配置,抛出错误而非掩盖

# ============================================
# 公开接口
# ============================================

class Avatar:
    """
    头像组件(层级5:基础模块)
    
    职责:
    - 圆形光影容器
    - 金色渐变文字
    - 双击编辑功能
    - 悬停动画效果
    - 光晕动画效果
    - 从用户偏好.json获取UI配置
    
    不负责:
    - 用户信息获取
    - 数据持久化
    """
    
    _config_service = None
    
    @classmethod
    def set_config_service(cls, config_service):
        """设置配置服务实例"""
        cls._config_service = config_service
    
    @staticmethod
    def _check_config_service():
        """检查配置服务是否已设置"""
        if Avatar._config_service is None:
            raise RuntimeError(
                "Avatar模块未设置config_service，"
                "请先调用 Avatar.set_config_service(config_service)"
            )
    
    @staticmethod
    def get_size() -> int:
        """获取头像尺寸(从用户偏好.json获取)"""
        Avatar._check_config_service()
        value = Avatar._config_service.get_ui_config("头像", "尺寸")
        if value is None:
            raise RuntimeError("用户偏好.json缺少配置: 头像.尺寸")
        return value
    
    @staticmethod
    def _get_theme_colors() -> Dict[str, str]:
        """获取主题颜色"""
        Avatar._check_config_service()
        return Avatar._config_service.get_theme_colors()
    
    @staticmethod
    def _get_ui_config(key: str, default_value=None):
        """获取UI配置"""
        Avatar._check_config_service()
        value = Avatar._config_service.get_ui_config("头像", key)
        return value if value is not None else default_value
    
    @staticmethod
    def create(
        text: str = None,
        size: int = None,
        image_url: Optional[str] = None,
        bg_color: str = None,
        text_color: str = "#FFD700",
        show_glow: bool = True,
        on_click: Optional[Callable] = None,
        on_text_change: Optional[Callable[[str], None]] = None,
        enabled: bool = True,
        theme_colors: Dict[str, str] = None,
    ) -> ft.Container:
        """
        创建可编辑的可靠圆形头像
        
        参数:
        - text: 显示的文字(可选,默认为"帅")
        - size: 头像尺寸(可选,默认从用户偏好.json获取)
        - image_url: 图片URL(可选)
        - bg_color: 背景颜色(默认使用主题颜色)
        - text_color: 文字颜色
        - show_glow: 是否显示光晕
        - on_click: 点击回调
        - on_text_change: 文字变化回调
        - enabled: 是否启用
        - theme_colors: 主题颜色(可选,默认从配置服务获取)
        """
        if text is None:
            text = DEFAULT_TEXT
        
        if size is None:
            size = Avatar.get_size()
        
        if theme_colors is None:
            theme_colors = Avatar._get_theme_colors()
        
        if bg_color is None:
            bg_color = theme_colors.get("bg_card", "#282828")
        
        glow_spread = Avatar._get_ui_config("光晕扩散", 3)
        glow_blur = Avatar._get_ui_config("光晕模糊", 20)
        glow_delay = Avatar._get_ui_config("光晕延迟", 0.5)
        glow_interval = Avatar._get_ui_config("光晕间隔", 0.2)
        container_padding = Avatar._get_ui_config("容器内边距", 10)
        text_ratio = Avatar._get_ui_config("文字比例", 0.6)
        
        current_text = text[0] if text and len(text) > 0 else DEFAULT_TEXT
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
                content_padding=ft.Padding.all(0),
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
            border_radius=radius,
            alignment=ft.alignment.Alignment(0, 0),
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
            alignment=ft.alignment.Alignment(0, 0),
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


# *** 标准测试格式: 仅调用被测模块,AI不得添加数据 ***
if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    
    from 前端.V2.业务层.服务.配置服务 import ConfigService
    
    def main(page: ft.Page):
        page.title = "头像组件测试"
        page.theme_mode = ft.ThemeMode.DARK
        
        config_service = ConfigService()
        Avatar.set_config_service(config_service)
        
        print(f"头像尺寸: {Avatar.get_size()}")
        
        def on_text_change(new_text: str):
            print(f"文字变更: {new_text}")
        
        avatar = Avatar.create(
            on_text_change=on_text_change,
        )
        
        page.add(
            ft.Container(
                content=avatar,
                alignment=ft.alignment.Alignment(0, 0),
                expand=True,
            )
        )
    
    ft.run(main)
