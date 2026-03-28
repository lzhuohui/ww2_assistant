#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模块名称：Dropdown
模块功能：下拉框组件，使用PopupMenuButton实现懒加载
实现步骤：
- 创建时只显示当前值，不加载选项列表
- 第一次点击时加载选项列表并显示菜单
- 支持销毁管理减少内存占用
- Win11风格
"""

from typing import Callable, List, Optional
import flet as ft


USER_WIDTH = 120
USER_HEIGHT = 30


class DropdownManager:
    """下拉框管理器 - 控件级懒加载管理"""
    
    _instance = None
    _initialized = False
    
    def __new__(cls, page: ft.Page = None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, page: ft.Page = None):
        if DropdownManager._initialized:
            if page and not hasattr(self, 'page'):
                self.page = page
                self._init_overlay()
            return
        
        self.page = page
        self.dropdowns = {}
        self.loaded_states = {}
        self.open_dropdown_id = None
        self.overlay_container = None
        self.backdrop = None
        
        if page:
            self._init_overlay()
        
        DropdownManager._initialized = True
    
    def _init_overlay(self):
        """初始化overlay容器"""
        if self.overlay_container is not None:
            return
        
        self.backdrop = ft.Container(
            content=None,
            bgcolor="transparent",
            visible=False,
            on_click=lambda e: self.close_all(),
        )
        self.page.overlay.append(self.backdrop)
        
        self.overlay_container = ft.Container(
            content=ft.Column(scroll=ft.ScrollMode.AUTO),
            visible=False,
            bgcolor="#FFFFFF",
            border=ft.border.all(1, "#E0E0E0"),
            border_radius=6,
            top=0,
            left=0,
            padding=0,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=8,
                color="#33000000",
            ),
        )
        self.page.overlay.append(self.overlay_container)
    
    def register_dropdown(self, dropdown_id: str, dropdown_info: dict):
        """注册下拉框"""
        self.dropdowns[dropdown_id] = dropdown_info
        self.loaded_states[dropdown_id] = False
    
    def close_all(self):
        """关闭所有下拉菜单"""
        if self.overlay_container:
            self.overlay_container.visible = False
            self._destroy_options()
        if self.backdrop:
            self.backdrop.visible = False
        self.open_dropdown_id = None
        if self.page:
            self.page.update()
    
    def _destroy_options(self):
        """销毁当前选项列表"""
        if self.overlay_container and self.overlay_container.content:
            self.overlay_container.content.controls = []
    
    def toggle_dropdown(self, dropdown_id: str, button: ft.Container):
        """切换下拉菜单显示"""
        drop_info = self.dropdowns.get(dropdown_id)
        if not drop_info or drop_info.get("disabled", False):
            return
        
        if self.open_dropdown_id == dropdown_id:
            self.close_all()
            return
        
        self.close_all()
        
        option_loader = drop_info.get("option_loader")
        on_change = drop_info.get("on_change")
        current_value = drop_info.get("current_value")
        selected_text = drop_info.get("selected_text")
        
        options = []
        if option_loader:
            options = option_loader()
        
        if not options:
            return
        
        button_top = button.top if hasattr(button, 'top') and button.top else 0
        button_left = button.left if hasattr(button, 'left') and button.left else 0
        
        if self.page:
            try:
                button_top = self._calculate_button_top(button)
                button_left = self._calculate_button_left(button)
            except:
                pass
        
        self._position_popup(button_top, button_left, len(options))
        
        def select_item(value: str):
            drop_info["current_value"] = value
            if selected_text:
                selected_text.value = value
            self.close_all()
            if on_change:
                on_change(value)
        
        options_controls = []
        for option in options:
            is_selected = option == current_value
            option_container = ft.Container(
                content=ft.Text(
                    option,
                    size=14,
                    color="#0078D4" if is_selected else "#333333",
                ),
                padding=ft.padding.symmetric(horizontal=12, vertical=8),
                bgcolor="#F0F0F0" if is_selected else "transparent",
                on_click=lambda e, v=option: select_item(v),
                on_hover=lambda e, sel=is_selected: setattr(
                    e.control, 
                    "bgcolor", 
                    "#E5E5E5" if e.data == "true" else ("#F0F0F0" if sel else "transparent")
                ) or e.control.update(),
            )
            options_controls.append(option_container)
        
        self.overlay_container.content.controls = [
            ft.Column(
                controls=options_controls,
                spacing=0,
            )
        ]
        
        self._show_backdrop()
        self._show_popup(dropdown_id)
        
        self.page.update()
    
    def _calculate_button_top(self, button: ft.Container) -> float:
        return 0
    
    def _calculate_button_left(self, button: ft.Container) -> float:
        return 0
    
    def _position_popup(self, button_top: float, button_left: float, option_count: int):
        if not self.page:
            return
        
        window_height = self.page.height
        window_width = self.page.width
        
        item_height = 36
        menu_content_height = option_count * item_height + 16
        
        self.overlay_container.width = USER_WIDTH + 40
        
        space_below = window_height - button_top - USER_HEIGHT - 20
        space_above = button_top - 20
        
        if space_below >= menu_content_height:
            self.overlay_container.top = button_top + USER_HEIGHT
            self.overlay_container.height = menu_content_height
        elif space_above >= menu_content_height:
            self.overlay_container.height = menu_content_height
            self.overlay_container.top = button_top - menu_content_height
        else:
            self.overlay_container.top = 20
            self.overlay_container.height = window_height - 40
        
        popup_width = self.overlay_container.width
        if button_left + popup_width > window_width - 20:
            self.overlay_container.left = window_width - popup_width - 20
        else:
            self.overlay_container.left = button_left
    
    def _show_backdrop(self):
        if self.backdrop:
            self.backdrop.top = 0
            self.backdrop.left = 0
            self.backdrop.width = self.page.width if self.page else 1000
            self.backdrop.height = self.page.height if self.page else 800
            self.backdrop.visible = True
    
    def _show_popup(self, dropdown_id: str):
        if self.overlay_container:
            self.overlay_container.visible = True
        self.open_dropdown_id = dropdown_id


_manager_instance = None


def get_manager(page: ft.Page = None) -> DropdownManager:
    global _manager_instance
    if _manager_instance is None:
        _manager_instance = DropdownManager(page)
    elif page and not hasattr(_manager_instance, 'page'):
        _manager_instance.page = page
        _manager_instance._init_overlay()
    return _manager_instance


def create_dropdown(
    current_value: str = "",
    on_change: Optional[Callable[[str], None]] = None,
    option_loader: Optional[Callable[[], List[str]]] = None,
    dropdown_id: Optional[str] = None,
    width: int = USER_WIDTH,
    enabled: bool = True,
    config: any = None,
) -> ft.Container:
    """
    创建下拉框
    
    参数:
        current_value: 当前选中的值
        on_change: 值改变时的回调函数
        option_loader: 懒加载选项的函数
        dropdown_id: 下拉框的唯一ID
        width: 下拉框宽度
        enabled: 是否启用
        config: 配置对象
    
    返回:
        Container: 包含下拉框的容器
    """
    import uuid
    
    if dropdown_id is None:
        dropdown_id = f"dropdown_{uuid.uuid4().hex[:8]}"
    
    if config is None:
        theme_colors = {
            "text_primary": "#000000",
            "text_secondary": "#666666",
            "text_disabled": "#999999",
            "bg_primary": "#FFFFFF",
            "bg_secondary": "#F5F5F5",
            "border": "#CCCCCC",
            "accent": "#0078D4"
        }
    else:
        theme_colors = config.当前主题颜色
    
    text_color = theme_colors.get("text_primary") if enabled else theme_colors.get("text_disabled")
    icon_color = theme_colors.get("text_secondary") if enabled else theme_colors.get("text_disabled")
    bg_color = theme_colors.get("bg_secondary") if enabled else theme_colors.get("bg_primary")
    border_color = theme_colors.get("border") if enabled else "transparent"
    
    selected_text = ft.Text(
        current_value if current_value else "请选择...",
        size=14,
        color=text_color,
        overflow=ft.TextOverflow.ELLIPSIS,
    )
    
    dropdown_icon = ft.Icon(
        ft.Icons.KEYBOARD_ARROW_DOWN,
        size=18,
        color=icon_color,
    )
    
    button_container = ft.Container(
        content=ft.Row(
            controls=[
                selected_text,
                dropdown_icon,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        width=width,
        height=USER_HEIGHT,
        padding=ft.padding.symmetric(horizontal=12),
        border=ft.border.all(1, border_color),
        border_radius=6,
        bgcolor=bg_color,
    )
    
    container = ft.Container(
        content=button_container,
        width=width,
    )
    
    dropdown_info = {
        "option_loader": option_loader,
        "on_change": on_change,
        "current_value": current_value,
        "selected_text": selected_text,
        "disabled": not enabled,
        "button": button_container,
    }
    
    def on_button_click(e):
        manager = get_manager()
        if manager.page is None and container.page:
            manager.page = container.page
            manager._init_overlay()
        
        manager.register_dropdown(dropdown_id, dropdown_info)
        manager.toggle_dropdown(dropdown_id, button_container)
    
    button_container.on_click = on_button_click
    
    def get_value() -> str:
        return dropdown_info.get("current_value", "")
    
    def set_value(new_value: str):
        dropdown_info["current_value"] = new_value
        selected_text.value = new_value
        try:
            if container.page:
                container.update()
        except:
            pass
    
    def set_enabled(state: bool):
        dropdown_info["disabled"] = not state
        text_col = theme_colors.get("text_primary") if state else theme_colors.get("text_disabled")
        icon_col = theme_colors.get("text_secondary") if state else theme_colors.get("text_disabled")
        bg_col = theme_colors.get("bg_secondary") if state else theme_colors.get("bg_primary")
        border_col = theme_colors.get("border") if state else "transparent"
        
        selected_text.color = text_col
        dropdown_icon.color = icon_col
        button_container.bgcolor = bg_col
        button_container.border = ft.border.all(1, border_col)
        
        try:
            if container.page:
                container.update()
        except:
            pass
    
    def unload_options():
        pass
    
    def set_options(options: List[str]):
        original_loader = dropdown_info.get("option_loader")
        dropdown_info["option_loader"] = lambda: options
    
    container.get_value = get_value
    container.set_value = set_value
    container.set_enabled = set_enabled
    container.unload_options = unload_options
    container.set_options = set_options
    
    return container


if __name__ == "__main__":
    def test_main(page: ft.Page):
        page.title = "下拉框测试"
        page.window.width = 400
        page.window.height = 300
        page.padding = 20
        
        manager = get_manager(page)
        
        dropdown = create_dropdown(
            current_value="选项1",
            on_change=lambda v: print(f"选择了: {v}"),
            option_loader=lambda: [f"选项{i}" for i in range(1, 11)],
            dropdown_id="test_dropdown",
        )
        
        page.add(dropdown)
    
    ft.app(target=test_main)
