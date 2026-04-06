# -*- coding: utf-8 -*-

"""
模块名称：界面容器.py
模块功能：功能界面容器，统一管理标题栏和内容区

职责：
- 创建标题栏（左侧标题+副标题，右侧方案选择器+默认按钮+保存按钮）
- 管理内容区域
- 处理方案切换和保存

不负责：
- 具体功能卡片内容
"""

import flet as ft
from typing import Dict, List, Callable, Any

from 设置界面.层级0_数据管理.配置管理 import ConfigManager
from 设置界面.层级5_基础模块.方案选择器 import SchemeSelector


class InterfaceContainer:
    """
    界面容器 - 统一管理功能界面的布局
    
    结构：
    ┌─────────────────────────────────────────────────────┐
    │ [标题] | [副标题]         [方案选择器] [默认] [保存] │  ← 标题栏
    ├─────────────────────────────────────────────────────┤
    │                                                     │
    │                   功能卡片区域                       │  ← 内容区
    │                                                     │
    └─────────────────────────────────────────────────────┘
    """
    
    def __init__(self, page: ft.Page, config_manager: ConfigManager):
        self._page = page
        self._config_manager = config_manager
        self._scheme_selector: SchemeSelector = None
        self._save_dlg: ft.AlertDialog = None
        self._on_scheme_change: Callable = None
        self._on_load_defaults: Callable = None
        self._on_start: Callable = None
    
    def create(
        self,
        title: str,
        hint: str,
        cards: List[ft.Control],
        on_scheme_change: Callable[[str], None] = None,
        on_load_defaults: Callable[[], None] = None,
        on_start: Callable[[], None] = None,
    ) -> ft.Container:
        """
        创建界面容器
        
        Args:
            title: 界面标题
            hint: 界面副标题/提示
            cards: 功能卡片列表
            on_scheme_change: 方案切换回调，参数为新方案名
            on_load_defaults: 加载默认值回调
        
        Returns:
            界面容器
        """
        self._on_scheme_change = on_scheme_change
        self._on_load_defaults = on_load_defaults
        self._on_start = on_start
        theme_colors = self._config_manager.get_theme_colors()
        
        title_bar = self._create_title_bar(title, hint, theme_colors)
        
        card_spacing = self._config_manager.get_ui_size("边距", "卡片间距")
        
        cards_column = ft.Column(
            controls=cards,
            spacing=card_spacing,
            scroll=ft.ScrollMode.HIDDEN,
            expand=True,
        )
        
        title_spacing = self._config_manager.get_ui_size("边距", "卡片间距")
        
        main_column = ft.Column(
            controls=[title_bar, cards_column],
            spacing=title_spacing,
            expand=True,
        )
        
        bg_primary = theme_colors.get("bg_primary", "#202020")
        padding = self._config_manager.get_ui_size("边距", "界面内边距")
        
        return ft.Container(
            content=main_column,
            bgcolor=bg_primary,
            padding=padding,
            expand=True,
            alignment=ft.Alignment(-1, -1),
            clip_behavior=ft.ClipBehavior.NONE,
        )
    
    def _create_title_bar(self, title: str, hint: str, theme_colors: Dict[str, str]) -> ft.Row:
        """创建标题栏"""
        text_primary = theme_colors.get("text_primary", "#FFFFFF")
        text_secondary = theme_colors.get("text_secondary", "#B0B0B0")
        
        title_control = ft.Text(
            value=title,
            size=24,
            weight=ft.FontWeight.BOLD,
            color=text_primary,
        )
        
        hint_control = ft.Text(
            value=hint,
            size=12,
            color=text_secondary,
        )
        
        left_section = ft.Row(
            controls=[title_control, ft.VerticalDivider(width=1, color=text_secondary), hint_control],
            vertical_alignment=ft.CrossAxisAlignment.END,
            spacing=12,
            expand=True,
        )
        
        right_section = self._build_scheme_selector(theme_colors)
        
        return ft.Row(
            controls=[left_section, right_section],
            vertical_alignment=ft.CrossAxisAlignment.END,
        )
    
    def _build_scheme_selector(self, theme_colors: Dict[str, str]) -> ft.Row:
        """构建方案选择器、默认按钮和保存按钮"""
        scheme_names = self._config_manager.get_scheme_names()
        current_scheme = self._config_manager.get_current_scheme()
        
        scheme_options = [{"text": name, "value": name} for name in scheme_names]
        
        self._scheme_selector = SchemeSelector(self._page, self._config_manager)
        
        selector_container = self._scheme_selector.create(
            options=scheme_options,
            current_value=current_scheme,
            on_change=self._on_scheme_change_callback,
            width=120,
        )
        
        accent = theme_colors.get("accent", "#0078D4")
        text_secondary = theme_colors.get("text_secondary", "#B0B0B0")
        
        default_btn = ft.IconButton(
            icon=ft.Icons.RESTORE,
            icon_color=text_secondary,
            tooltip="加载默认值",
            on_click=self._on_default_click,
        )
        
        save_btn = ft.IconButton(
            icon=ft.Icons.SAVE,
            icon_color=accent,
            tooltip="重命名方案",
            on_click=self._show_save_dialog,
        )
        
        start_btn = ft.IconButton(
            icon=ft.Icons.PLAY_ARROW,
            icon_color=accent,
            tooltip="启动游戏",
            on_click=self._on_start_click,
        )
        
        return ft.Row([
            selector_container,
            default_btn,
            save_btn,
            start_btn,
        ], spacing=4, vertical_alignment=ft.CrossAxisAlignment.CENTER)
    
    def _on_scheme_change_callback(self, scheme_name: str):
        """方案选择变更回调"""
        self._config_manager.switch_scheme(scheme_name)
        
        if self._on_scheme_change:
            self._on_scheme_change(scheme_name)
    
    def _on_default_click(self, e):
        """默认按钮点击回调"""
        if self._on_load_defaults:
            self._on_load_defaults()
    
    def _on_start_click(self, e):
        """启动按钮点击回调"""
        if self._on_start:
            self._on_start()
    
    def _show_save_dialog(self, e):
        """显示保存方案对话框 - Win11风格"""
        theme_colors = self._config_manager.get_theme_colors()
        text_primary = theme_colors.get("text_primary", "#FFFFFF")
        text_secondary = theme_colors.get("text_secondary", "#B0B0B0")
        accent = theme_colors.get("accent", "#0078D4")
        bg_card = theme_colors.get("bg_card", "#2A2A2A")
        
        font_size = self._config_manager.get_ui_size("字体", "中") or 16
        title_font_size = self._config_manager.get_ui_size("字体", "大") or 18
        input_width = self._config_manager.get_ui_config("控件", "输入框宽度") or 120
        border_radius = self._config_manager.get_radius("中") or 8
        
        current_scheme = self._config_manager.get_current_scheme()
        
        name_input = ft.TextField(
            value=current_scheme,
            border_color=accent,
            focused_border_color=accent,
            cursor_color=accent,
            text_style=ft.TextStyle(color=text_primary, size=font_size),
            hint_style=ft.TextStyle(color=text_secondary, size=font_size),
            width=input_width,
            text_align=ft.TextAlign.CENTER,
            dense=True,
            content_padding=ft.Padding.symmetric(horizontal=8, vertical=4),
        )
        
        error_text = ft.Text(
            value="",
            color=ft.Colors.RED,
            size=11,
            visible=False,
            height=16,
        )
        
        def close_dlg(e):
            self._save_dlg.open = False
            self._page.update()
        
        def do_save(e):
            new_name = name_input.value.strip()
            if not new_name:
                return
            
            if len(new_name) > 4:
                error_text.value = "方案名称不能超过4个字"
                error_text.visible = True
                self._page.update()
                return
            
            old_name = current_scheme
            
            if self._config_manager.save_and_rename_scheme(old_name, new_name):
                self._refresh_scheme_selector(new_name)
            
            self._save_dlg.open = False
            self._page.update()
        
        def on_input_change(e):
            if error_text.visible:
                error_text.visible = False
            if len(name_input.value) > 4:
                error_text.value = "不能超过4个字"
                error_text.visible = True
            self._page.update()
        
        name_input.on_change = on_input_change
        
        self._save_dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("重命名方案", color=text_primary, size=title_font_size, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
            content=ft.Column(
                controls=[
                    name_input,
                    error_text,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=4,
                tight=True,
            ),
            actions=[
                ft.TextButton("取消", on_click=close_dlg, style=ft.ButtonStyle(color=text_secondary)),
                ft.TextButton("确定", on_click=do_save, style=ft.ButtonStyle(color=accent)),
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
            bgcolor=bg_card,
            on_dismiss=close_dlg,
            shape=ft.RoundedRectangleBorder(radius=border_radius),
        )
        
        self._page.overlay.append(self._save_dlg)
        self._save_dlg.open = True
        self._page.update()
    
    def _refresh_scheme_selector(self, current_value: str = None):
        """刷新方案选择器选项"""
        if self._scheme_selector:
            scheme_names = self._config_manager.get_scheme_names()
            scheme_options = [{"text": name, "value": name} for name in scheme_names]
            self._scheme_selector.refresh_options(scheme_options, current_value)
