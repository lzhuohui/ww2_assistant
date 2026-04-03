# -*- coding: utf-8 -*-

"""
模块名称：下拉框.py
模块功能：下拉框组件，使用自定义组件实现真正的懒加载

实现步骤：
- 调用时只加载当前值（不加载选项列表）
- 点击时才加载选项列表并显示
- 点击另一个下拉框时，销毁上一个下拉框的选项列表
- 切换界面时，销毁所有下拉框的选项数据和实例引用

销毁说明：
- options: 选项列表数据（内存）
- options_loaded: 是否已加载标志
- _all_dropdowns: 类变量，存储所有实例引用
- 不销毁：控件本身（Flet管理）、配置数据（持久化）
"""

import flet as ft
from typing import List, Dict, Callable

from 前端.V3.层级0_数据管理.配置管理 import ConfigManager


class Dropdown:
    """
    下拉框组件 - 使用自定义组件实现真正的懒加载
    
    实现步骤：
    1. 调用时只加载当前值（不加载选项列表）
    2. 点击时才加载选项列表并显示
    3. 销毁时清理选项数据
    """
    
    _config_manager: ConfigManager = None
    _current_open_key: str = None
    _all_dropdowns: Dict[str, 'Dropdown'] = {}
    
    @classmethod
    def set_config_manager(cls, config_manager: ConfigManager):
        cls._config_manager = config_manager
    
    @staticmethod
    def _check_config_manager():
        if Dropdown._config_manager is None:
            raise RuntimeError("Dropdown模块未设置config_manager")
    
    @staticmethod
    def get_font_size() -> int:
        Dropdown._check_config_manager()
        return Dropdown._config_manager.get_ui_size("字体", "正文字体") or 16
    
    @staticmethod
    def get_icon_size() -> int:
        Dropdown._check_config_manager()
        return Dropdown._config_manager.get_ui_size("字体", "图标大小") or 18
    
    @staticmethod
    def get_border_radius() -> int:
        Dropdown._check_config_manager()
        return Dropdown._config_manager.get_radius("小") or 3
    
    @staticmethod
    def get_padding() -> int:
        Dropdown._check_config_manager()
        return Dropdown._config_manager.get_ui_size("边距", "中") or 8
    
    @staticmethod
    def get_placeholder_text() -> str:
        Dropdown._check_config_manager()
        return Dropdown._config_manager.get_text_config("下拉框", "占位符") or "点击加载选项..."
    
    @staticmethod
    def get_options_padding() -> int:
        Dropdown._check_config_manager()
        return Dropdown._config_manager.get_ui_size("边距", "中") or 8
    
    @staticmethod
    def get_options_spacing() -> int:
        Dropdown._check_config_manager()
        return Dropdown._config_manager.get_ui_size("边距", "小") or 2
    
    @staticmethod
    def get_option_item_padding() -> int:
        Dropdown._check_config_manager()
        return Dropdown._config_manager.get_ui_size("边距", "中") or 6
    
    @staticmethod
    def get_max_options_height() -> int:
        Dropdown._check_config_manager()
        return Dropdown._config_manager.get_ui_config("控件", "下拉框最大高度") or 300
    
    @classmethod
    def destroy_all_instances(cls):
        """销毁所有下拉框实例的选项数据（类方法，供层级1调用）"""
        for key in list(cls._all_dropdowns.keys()):
            dropdown_instance = cls._all_dropdowns[key]
            dropdown_instance.destroy_all()
        cls._all_dropdowns.clear()
        cls._current_open_key = None
    
    def __init__(self, page: ft.Page = None, config_manager: ConfigManager = None):
        self._page = page
        self._config_manager = config_manager or Dropdown._config_manager
        self._dropdowns: Dict[str, ft.Container] = {}
        self._dropdown_states: Dict[str, Dict] = {}
        self._options_panels: Dict[str, ft.Container] = {}
    
    def create(
        self,
        interface: str = "",
        card: str = "",
        control_id: str = "",
        enabled: bool = True,
        on_change: Callable[[str, str, str, Dict[str, str]], None] = None,
        theme_colors: Dict[str, str] = None,
        width: int = None,
        height: int = None,
    ) -> ft.Container:
        if width is None:
            width = self._config_manager.get_layout_value(interface, card, "dropdown_width", control_id)
            if width is None:
                width = self._config_manager.get_ui_config("控件", "下拉框宽度", 100)
        
        if height is None:
            height = self._config_manager.get_ui_config("控件", "下拉框高度", 30)
        
        border_radius = Dropdown.get_border_radius()
        
        if theme_colors is None:
            theme_colors = self._config_manager.get_theme_colors()
        
        current_value = self._get_current_value(interface, card, control_id)
        
        container = self._build_dropdown(
            current_value, enabled,
            width, height, border_radius, theme_colors,
            interface, card, control_id, on_change,
        )
        
        key = f"{interface}.{card}.{control_id}" if interface and card and control_id else f"dropdown_{len(self._dropdowns)}"
        self._dropdowns[key] = container
        Dropdown._all_dropdowns[key] = self
        
        return container
    
    def _get_current_value(self, interface: str, card: str, control_id: str) -> Dict[str, str]:
        if self._config_manager:
            raw_value = self._config_manager.get_raw_value(interface, card, control_id)
            if raw_value:
                return {"text": raw_value, "value": raw_value}
        return {"text": Dropdown.get_placeholder_text(), "value": ""}
    
    def _load_options(self, interface: str, card: str, control_id: str) -> List[Dict[str, str]]:
        if self._config_manager is None:
            return []
        return self._config_manager.get_options(interface, card, control_id)
    
    def _save_value(self, interface: str, card: str, control_id: str, value: Dict[str, str]):
        if self._config_manager:
            self._config_manager.set_value(interface, card, control_id, value)
    
    def _close_all_dropdowns(self, current_key: str = None):
        for key, dropdown_instance in Dropdown._all_dropdowns.items():
            if key != current_key and key in dropdown_instance._dropdown_states:
                state = dropdown_instance._dropdown_states[key]
                if state.get("is_open", False):
                    state["is_open"] = False
                    state["options"] = []
                    state["options_loaded"] = False
                    if key in dropdown_instance._options_panels:
                        options_panel = dropdown_instance._options_panels[key]
                        options_panel.visible = False
                    if key in dropdown_instance._dropdowns:
                        container = dropdown_instance._dropdowns[key]
                        if hasattr(container, '_overlay_mask'):
                            container._overlay_mask.visible = False
                    if dropdown_instance._page:
                        dropdown_instance._page.update()
        
        Dropdown._current_open_key = current_key
    
    def _build_dropdown(
        self,
        current_value: Dict,
        enabled: bool,
        width: int,
        height: int,
        border_radius: int,
        theme_colors: Dict,
        interface: str,
        card: str,
        control_id: str,
        on_change: Callable,
    ) -> ft.Container:
        text_color = theme_colors.get("text_primary", "#FFFFFF")
        text_secondary = theme_colors.get("text_secondary", "#B0B0B0")
        disabled_color = theme_colors.get("text_disabled", "#666666")
        bg_card = theme_colors.get("bg_card", "#2D2D2D")
        border_color = theme_colors.get("border", "#3D3D3D")
        accent_color = theme_colors.get("accent", "#0078D4")
        
        font_size = Dropdown.get_font_size()
        icon_size = Dropdown.get_icon_size()
        padding = Dropdown.get_padding()
        options_padding = Dropdown.get_options_padding()
        options_spacing = Dropdown.get_options_spacing()
        option_item_padding = Dropdown.get_option_item_padding()
        max_options_height = Dropdown.get_max_options_height()
        
        key = f"{interface}.{card}.{control_id}"
        
        state = {
            "current_value": current_value,
            "enabled": enabled,
            "options": [],
            "options_loaded": False,
            "is_open": False,
            "interface": interface,
            "card": card,
            "control_id": control_id,
        }
        self._dropdown_states[key] = state
        
        display_text = ft.Text(
            value=current_value.get("text", ""),
            size=font_size,
            color=text_color if enabled else disabled_color,
            overflow=ft.TextOverflow.ELLIPSIS,
        )
        
        dropdown_icon = ft.Icon(
            ft.Icons.ARROW_DROP_DOWN,
            size=icon_size,
            color=text_secondary if enabled else disabled_color,
        )
        
        options_list = ft.Column(
            [],
            spacing=options_spacing,
            scroll=ft.ScrollMode.HIDDEN,
            tight=True,
        )
        
        options_panel = ft.Container(
            content=options_list,
            visible=False,
            bgcolor=bg_card,
            border_radius=border_radius,
            padding=options_padding,
            top=height + 2,
            left=0,
            opacity=1.0,
        )
        self._options_panels[key] = options_panel
        
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
        
        button_position = {"top": 0, "left": 0}
        
        current_page = [self._page]
        
        overlay_mask = ft.Container(
            visible=False,
            bgcolor="transparent",
            expand=True,
        )
        
        def close_dropdown():
            options_panel.visible = False
            overlay_mask.visible = False
            state["is_open"] = False
            if current_page[0]:
                current_page[0].update()
        
        def select_option(option: Dict):
            state["current_value"] = option
            display_text.value = option.get("text", "")
            display_text.color = text_color
            self._save_value(interface, card, control_id, option)
            if on_change:
                on_change(interface, card, control_id, option)
            close_dropdown()
        
        def build_options_list():
            opts = state["options"]
            options_list.controls.clear()
            current_val = state["current_value"].get("value", "")
            selected_index = -1
            
            for i, opt in enumerate(opts):
                if opt.get("value", "") == current_val:
                    selected_index = i
                
                is_selected = (opt.get("value", "") == current_val)
                option_btn = ft.Container(
                    content=ft.Text(opt.get("text", ""), size=font_size, color=text_color),
                    padding=ft.Padding.symmetric(horizontal=padding, vertical=2),
                    bgcolor=accent_color if is_selected else bg_card,
                    border_radius=border_radius,
                    on_click=lambda e, o=opt: select_option(o),
                )
                
                def on_hover(e, btn=option_btn, is_sel=is_selected):
                    if e.data == "true":
                        btn.bgcolor = accent_color
                    else:
                        btn.bgcolor = accent_color if is_sel else bg_card
                    btn.update()
                
                option_btn.on_hover = on_hover
                options_list.controls.append(option_btn)
            
            return selected_index
        
        def on_tap_down(e):
            if e.global_position and e.local_position:
                button_position["top"] = e.global_position.y - e.local_position.y
                button_position["left"] = e.global_position.x - e.local_position.x
        
        def toggle_dropdown(e):
            if not state["enabled"]:
                return
            
            page = None
            if e.control and hasattr(e.control, 'page') and e.control.page:
                page = e.control.page
            elif e.control and hasattr(e.control, 'content') and e.control.content:
                content = e.control.content
                if hasattr(content, 'page') and content.page:
                    page = content.page
            
            if page is None:
                return
            
            current_page[0] = page
            
            if not state["is_open"]:
                self._close_all_dropdowns(key)
                
                if not state["options_loaded"]:
                    options = self._load_options(interface, card, control_id)
                    state["options"] = options
                    state["options_loaded"] = True
                
                selected_index = build_options_list()
                
                opts = state["options"]
                item_height = font_size + 4 + options_spacing
                content_height = len(opts) * item_height + options_padding * 2
                
                button_top = button_position["top"]
                button_left = button_position["left"]
                
                space_below = page.height - button_top - height - 20
                space_above = button_top - 20
                
                if selected_index >= 0:
                    selected_offset = selected_index * item_height + options_padding
                else:
                    selected_offset = 0
                
                panel_top = button_top - selected_offset
                panel_height = min(content_height, page.height - 40)
                
                if panel_top < 20:
                    panel_top = 20
                elif panel_top + panel_height > page.height - 20:
                    panel_top = page.height - panel_height - 20
                
                options_panel.top = panel_top
                options_panel.height = panel_height
                options_panel.left = button_left
                
                options_panel.visible = True
                overlay_mask.visible = True
                state["is_open"] = True
                
                if overlay_mask not in page.overlay:
                    page.overlay.append(overlay_mask)
                if options_panel not in page.overlay:
                    page.overlay.append(options_panel)
                
                page.update()
                
                if selected_index >= 0 and content_height > panel_height:
                    scroll_offset = selected_index * item_height
                    try:
                        page.run_task(options_list.scroll_to, offset=scroll_offset, duration=100)
                    except Exception:
                        pass
            else:
                close_dropdown()
            
            page.update()
        
        gesture_detector = ft.GestureDetector(
            content=button_container,
            on_tap_down=on_tap_down,
            on_tap=toggle_dropdown,
        )
        
        def on_mask_click(e):
            close_dropdown()
        
        overlay_mask.on_click = on_mask_click
        
        last_hover_state = [False]
        
        def handle_hover(e):
            if not state["enabled"]:
                return
            is_hovering = e.data == "true"
            if last_hover_state[0] != is_hovering:
                last_hover_state[0] = is_hovering
                if is_hovering:
                    button_container.border = ft.Border.all(1, accent_color)
                else:
                    button_container.border = ft.Border.all(1, border_color if state["enabled"] else "transparent")
                button_container.update()
        
        button_container.on_hover = handle_hover
        
        container = ft.Container(content=gesture_detector, width=width, height=height)
        container._button_container = button_container
        container._options_panel = options_panel
        container._overlay_mask = overlay_mask
        
        def get_value() -> Dict[str, str]:
            return state["current_value"]
        
        def set_value(value: Dict[str, str]):
            state["current_value"] = value
            display_text.value = value.get("text", "")
            if self._page:
                self._page.update()
        
        def set_enabled(is_enabled: bool):
            state["enabled"] = is_enabled
            display_text.color = text_color if is_enabled else disabled_color
            dropdown_icon.color = text_secondary if is_enabled else disabled_color
            button_container.border = ft.Border.all(1, border_color if is_enabled else "transparent")
            try:
                if self._page:
                    self._page.update()
            except RuntimeError:
                pass
        
        def set_options(new_options: List[Dict]):
            state["options"] = new_options
            state["options_loaded"] = True
        
        container.get_value = get_value
        container.set_value = set_value
        container.set_enabled = set_enabled
        container.set_options = set_options
        
        return container
    
    def get_value(self, interface: str, card: str, control_id: str) -> Dict[str, str]:
        key = f"{interface}.{card}.{control_id}"
        if key in self._dropdowns:
            container = self._dropdowns[key]
            if hasattr(container, 'get_value'):
                return container.get_value()
        return {"text": "", "value": ""}
    
    def destroy_all(self):
        for key in list(self._dropdown_states.keys()):
            self._dropdown_states[key]["options"] = []
            self._dropdown_states[key]["options_loaded"] = False
            self._dropdown_states[key]["is_open"] = False
            if key in self._options_panels:
                self._options_panels[key].visible = False
            if key in self._dropdowns:
                container = self._dropdowns[key]
                if hasattr(container, '_overlay_mask'):
                    container._overlay_mask.visible = False
        
        self._dropdowns.clear()
        self._dropdown_states.clear()
        self._options_panels.clear()
        Dropdown._current_open_key = None


if __name__ == "__main__":
    from 前端.V3.层级0_数据管理.配置管理 import ConfigManager
    
    def main(page: ft.Page):
        page.title = "下拉框懒加载测试"
        
        config_manager = ConfigManager()
        Dropdown.set_config_manager(config_manager)
        dropdown = Dropdown(page, config_manager)
        
        theme_colors = config_manager.get_theme_colors()
        page.bgcolor = theme_colors.get("bg_primary", "#202020")
        
        def on_change(interface, card, control_id, value):
            print(f"选择变更: {value}")
        
        container1 = dropdown.create(
            interface="系统界面",
            card="挂机模式",
            control_id="挂机模式",
            enabled=True,
            on_change=on_change,
        )
        
        container2 = dropdown.create(
            interface="系统界面",
            card="指令速度",
            control_id="指令速度",
            enabled=True,
            on_change=on_change,
        )
        
        page.add(ft.Column([
            ft.Text("下拉框懒加载测试", size=20, weight=ft.FontWeight.BOLD, color=theme_colors.get("text_primary", "#FFFFFF")),
            ft.Container(height=20),
            ft.Row([ft.Text("挂机模式:", color=theme_colors.get("text_secondary", "#B0B0B0")), container1], spacing=8),
            ft.Container(height=10),
            ft.Row([ft.Text("指令速度:", color=theme_colors.get("text_secondary", "#B0B0B0")), container2], spacing=8),
            ft.Container(height=20),
            ft.Text("测试说明：", size=16, weight=ft.FontWeight.BOLD, color=theme_colors.get("text_primary", "#FFFFFF")),
            ft.Text("1. 进入界面时，下拉框只显示当前值，不加载选项", size=14, color=theme_colors.get("text_secondary", "#B0B0B0")),
            ft.Text("2. 点击下拉框时，才加载选项列表并直接显示", size=14, color=theme_colors.get("text_secondary", "#B0B0B0")),
            ft.Text("3. 点击另一个下拉框时，自动关闭上一个", size=14, color=theme_colors.get("text_secondary", "#B0B0B0")),
            ft.Text("4. 点击菜单外关闭菜单", size=14, color=theme_colors.get("text_secondary", "#B0B0B0")),
        ], alignment=ft.MainAxisAlignment.CENTER))
    
    ft.run(main)
