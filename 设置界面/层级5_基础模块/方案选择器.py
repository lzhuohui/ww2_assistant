# -*- coding: utf-8 -*-

"""
模块名称：方案选择器.py
模块功能：方案选择下拉框，用于右上角方案切换

职责：
- 显示方案列表
- 处理方案切换
- 支持选项刷新

不负责：
- 懒加载（选项直接传入）
- 销毁管理（不需要）
"""

import flet as ft
from typing import Dict, List, Callable

from 设置界面.层级0_数据管理.配置管理 import ConfigManager


# ========== 常量定义 ==========
OPTION_ITEM_PADDING_V = 2       # 选项项垂直内边距
TEXT_HEIGHT_OFFSET = 4          # 文字高度补偿（避免文字被裁剪）
SCROLL_DURATION = 100           # 滚动动画时长（毫秒）


class SchemeSelector:
    """
    方案选择器 - 简化版下拉框
    
    与懒加载下拉框的区别：
    - 选项直接传入，不需要懒加载
    - 不需要销毁管理
    - 支持刷新选项
    """
    
    _config_manager: ConfigManager = None
    
    @classmethod
    def set_config_manager(cls, config_manager: ConfigManager):
        cls._config_manager = config_manager
    
    @staticmethod
    def _check_config_manager():
        if SchemeSelector._config_manager is None:
            raise RuntimeError("SchemeSelector模块未设置config_manager")
    
    @staticmethod
    def get_font_size() -> int:
        SchemeSelector._check_config_manager()
        return SchemeSelector._config_manager.get_ui_size("字体", "正文字体") or 16
    
    @staticmethod
    def get_icon_size() -> int:
        SchemeSelector._check_config_manager()
        return SchemeSelector._config_manager.get_ui_size("字体", "图标大小") or 18
    
    @staticmethod
    def get_border_radius() -> int:
        SchemeSelector._check_config_manager()
        return SchemeSelector._config_manager.get_radius("小") or 3
    
    @staticmethod
    def get_padding() -> int:
        SchemeSelector._check_config_manager()
        return SchemeSelector._config_manager.get_ui_size("边距", "控件区内边距") or 6
    
    @staticmethod
    def get_options_padding() -> int:
        SchemeSelector._check_config_manager()
        return SchemeSelector._config_manager.get_ui_size("边距", "控件区内边距") or 6
    
    @staticmethod
    def get_options_spacing() -> int:
        SchemeSelector._check_config_manager()
        return SchemeSelector._config_manager.get_ui_size("边距", "下拉框选项间距") or 4
    
    @staticmethod
    def get_max_options_height() -> int:
        SchemeSelector._check_config_manager()
        return SchemeSelector._config_manager.get_ui_config("控件", "下拉框最大高度") or 300
    
    @staticmethod
    def get_shadow_config() -> Dict:
        SchemeSelector._check_config_manager()
        return SchemeSelector._config_manager.get_shadow_config("菜单")
    
    def __init__(self, page: ft.Page, config_manager: ConfigManager = None):
        self._page = page
        self._config_manager = config_manager or SchemeSelector._config_manager
        self._container: ft.Container = None
        self._state: Dict = {}
        self._options_panel: ft.Container = None
        self._overlay_mask: ft.Container = None
        self._on_change: Callable = None
    
    def create(
        self,
        options: List[Dict[str, str]],
        current_value: str = None,
        on_change: Callable[[str], None] = None,
        width: int = None,
        height: int = None,
    ) -> ft.Container:
        """
        创建方案选择器
        
        Args:
            options: 选项列表，格式 [{"text": "显示文本", "value": "值"}, ...]
            current_value: 当前值
            on_change: 选择变更回调，参数为选中的值
            width: 宽度
            height: 高度
        
        Returns:
            选择器容器
        """
        if width is None:
            width = self._config_manager.get_ui_config("控件", "方案选择器宽度", 120)
        
        if height is None:
            height = self._config_manager.get_ui_config("控件", "下拉框高度", 30)
        
        self._on_change = on_change
        theme_colors = self._config_manager.get_theme_colors()
        
        font_size = SchemeSelector.get_font_size()
        icon_size = SchemeSelector.get_icon_size()
        border_radius = SchemeSelector.get_border_radius()
        padding = SchemeSelector.get_padding()
        options_padding = SchemeSelector.get_options_padding()
        options_spacing = SchemeSelector.get_options_spacing()
        max_options_height = SchemeSelector.get_max_options_height()
        shadow_config = SchemeSelector.get_shadow_config()
        
        text_color = theme_colors.get("text_primary", "#FFFFFF")
        text_secondary = theme_colors.get("text_secondary", "#B0B0B0")
        bg_card = theme_colors.get("bg_card", "#2D2D2D")
        border_color = theme_colors.get("border", "#3D3D3D")
        accent_color = theme_colors.get("accent", "#0078D4")
        hover_color = "#3A3A3A"
        
        current_option = None
        for opt in options:
            if opt.get("value") == current_value:
                current_option = opt
                break
        
        if current_option is None and options:
            current_option = options[0]
        
        self._state = {
            "current_value": current_option or {"text": "", "value": ""},
            "options": options,
            "is_open": False,
        }
        
        display_text = ft.Text(
            value=current_option.get("text", "") if current_option else "",
            size=font_size,
            color=text_color,
            overflow=ft.TextOverflow.ELLIPSIS,
        )
        
        dropdown_icon = ft.Icon(
            ft.Icons.ARROW_DROP_DOWN,
            size=icon_size,
            color=text_secondary,
        )
        
        options_list = ft.Column(
            [],
            spacing=options_spacing,
            scroll=ft.ScrollMode.HIDDEN,
            tight=True,
        )
        
        self._options_panel = ft.Container(
            content=options_list,
            visible=False,
            bgcolor=bg_card,
            border=ft.Border.all(1, border_color),
            border_radius=border_radius,
            padding=ft.Padding.symmetric(horizontal=0, vertical=options_padding),
            top=0,
            left=0,
            opacity=1.0,
            shadow=ft.BoxShadow(
                spread_radius=shadow_config["spread_radius"],
                blur_radius=shadow_config["blur_radius"],
                color=ft.Colors.with_opacity(shadow_config["opacity"], ft.Colors.BLACK),
                offset=ft.Offset(shadow_config["offset_x"], shadow_config["offset_y"]),
            ),
        )
        
        button_container = ft.Container(
            content=ft.Row(
                [display_text, dropdown_icon],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=padding,
            ),
            width=width,
            height=height,
            bgcolor=bg_card,
            border=ft.Border.all(1, border_color),
            border_radius=border_radius,
            padding=ft.Padding.symmetric(horizontal=padding, vertical=0),
        )
        
        self._overlay_mask = ft.Container(
            visible=False,
            bgcolor="transparent",
            expand=True,
        )
        
        button_position = {"top": 0, "left": 0}
        
        def close_selector():
            self._options_panel.visible = False
            self._overlay_mask.visible = False
            self._state["is_open"] = False
            if self._page:
                self._page.update()
        
        def select_option(option: Dict):
            self._state["current_value"] = option
            display_text.value = option.get("text", "")
            display_text.color = text_color
            close_selector()
            if self._on_change:
                self._on_change(option.get("value", ""))
        
        def build_options_list():
            opts = self._state["options"]
            options_list.controls.clear()
            current_val = self._state["current_value"].get("value", "")
            
            for opt in opts:
                is_selected = (opt.get("value", "") == current_val)
                
                option_btn = ft.Container(
                    content=ft.Text(opt.get("text", ""), size=font_size, color=text_color),
                    padding=ft.Padding.symmetric(horizontal=padding, vertical=OPTION_ITEM_PADDING_V),
                    height=font_size + TEXT_HEIGHT_OFFSET + 2 * OPTION_ITEM_PADDING_V,
                    width=float('inf'),
                    bgcolor=hover_color if is_selected else "transparent",
                    border_radius=border_radius,
                    on_click=lambda e, o=opt: select_option(o),
                )
                
                def on_hover(e, btn=option_btn, is_sel=is_selected):
                    if e.data == "true":
                        btn.bgcolor = hover_color
                    else:
                        btn.bgcolor = hover_color if is_sel else "transparent"
                    btn.update()
                
                option_btn.on_hover = on_hover
                options_list.controls.append(option_btn)
        
        def toggle_selector(e):
            page = None
            ctrl = e.control
            while ctrl:
                if hasattr(ctrl, 'page') and ctrl.page:
                    page = ctrl.page
                    break
                if hasattr(ctrl, 'content'):
                    ctrl = ctrl.content
                else:
                    break
            
            if page is None:
                return
            
            if not self._state["is_open"]:
                build_options_list()
                
                item_height = font_size + TEXT_HEIGHT_OFFSET + 2 * OPTION_ITEM_PADDING_V
                opts = self._state["options"]
                opts_count = len(opts)
                
                total_options_height = opts_count * item_height
                total_spacing_height = max(0, opts_count - 1) * options_spacing
                estimated_content_height = total_options_height + total_spacing_height + 2 * options_padding
                
                button_top = button_position["top"]
                button_left = button_position["left"]
                
                space_down = page.height - (button_top + height)
                space_up = button_top
                
                expand_down = None
                panel_height = None
                
                if estimated_content_height <= space_down:
                    expand_down = True
                elif estimated_content_height <= space_up:
                    expand_down = False
                else:
                    expand_down = space_down >= space_up
                
                if expand_down:
                    panel_top = button_top + height
                    available_height = space_down
                else:
                    available_height = space_up
                    panel_top = max(0, button_top - estimated_content_height)
                
                if estimated_content_height > available_height:
                    panel_height = min(available_height, max_options_height)
                
                if panel_height is not None and panel_height < item_height + 2 * options_padding:
                    panel_height = item_height + 2 * options_padding
                
                self._options_panel.top = panel_top
                if panel_height is not None:
                    self._options_panel.height = panel_height
                else:
                    self._options_panel.height = None
                self._options_panel.left = button_left
                self._options_panel.width = width - icon_size - padding
                
                self._options_panel.visible = True
                self._overlay_mask.visible = True
                self._state["is_open"] = True
                
                if self._overlay_mask not in page.overlay:
                    page.overlay.append(self._overlay_mask)
                if self._options_panel not in page.overlay:
                    page.overlay.append(self._options_panel)
                
                page.update()
            else:
                close_selector()
        
        def on_tap_down(e):
            if e.global_position and e.local_position:
                button_position["top"] = e.global_position.y - e.local_position.y
                button_position["left"] = e.global_position.x - e.local_position.x
        
        gesture_detector = ft.GestureDetector(
            content=button_container,
            on_tap_down=on_tap_down,
            on_tap=toggle_selector,
        )
        
        self._overlay_mask.on_click = lambda e: close_selector()
        
        last_hover_state = [False]
        
        def handle_hover(e):
            is_hovering = e.data == "true"
            if last_hover_state[0] != is_hovering:
                last_hover_state[0] = is_hovering
                if is_hovering:
                    button_container.border = ft.Border.all(1, accent_color)
                else:
                    button_container.border = ft.Border.all(1, border_color)
                button_container.update()
        
        button_container.on_hover = handle_hover
        
        self._container = ft.Container(content=gesture_detector, width=width, height=height)
        self._container._button_container = button_container
        self._container._display_text = display_text
        
        return self._container
    
    def refresh_options(self, options: List[Dict[str, str]], current_value: str = None):
        """
        刷新选项列表
        
        Args:
            options: 新的选项列表
            current_value: 当前值（可选，不传则保持当前值）
        """
        self._state["options"] = options
        
        if current_value is not None:
            for opt in options:
                if opt.get("value") == current_value:
                    self._state["current_value"] = opt
                    if hasattr(self._container, '_display_text'):
                        self._container._display_text.value = opt.get("text", "")
                    break
