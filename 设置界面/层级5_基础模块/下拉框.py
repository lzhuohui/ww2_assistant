# -*- coding: utf-8 -*-

"""
模块名称：下拉框.py
模块功能：高性能下拉框组件，针对大量选项场景优化

优化策略：
1. 界面级缓存 - 同界面内复用选项数据，切换界面时清空
2. 搜索功能 - 选项超过阈值时显示搜索框
3. 隐藏滚动条 - 使用ScrollMode.HIDDEN实现Win11风格
4. 聚焦功能 - 使用offset方式scroll_to，可靠稳定

使用方式：
- 通过 DropdownOptimized.set_config_manager() 初始化
- 通过 create() 方法创建下拉框
"""

from typing import List, Dict, Callable, Optional

import flet as ft

from 设置界面.层级0_数据管理.配置管理 import ConfigManager

try:
    from pypinyin import lazy_pinyin
    PINYIN_AVAILABLE = True
except ImportError:
    PINYIN_AVAILABLE = False

OPTION_ITEM_PADDING_V = 2
TEXT_HEIGHT_OFFSET = 4
SCROLL_DURATION = 100

SEARCH_THRESHOLD = 25
CACHE_ENABLED = True

SEARCH_BOX_HEIGHT = 32
DEFAULT_MAX_MENU_HEIGHT = 540


def _calculate_item_height(font_size: int) -> int:
    return font_size + TEXT_HEIGHT_OFFSET + 2 * OPTION_ITEM_PADDING_V


class DropdownOptimized:
    """
    高性能下拉框组件
    
    优化特性：
    1. 界面级缓存：同界面内复用选项数据
    2. 搜索功能：选项超过阈值时启用
    3. 隐藏滚动条：Win11风格
    4. 聚焦功能：offset方式scroll_to
    
    全局状态管理：
    - _config_manager: 配置管理实例（类级别）
    - _current_open_key: 当前打开的下拉框key，确保同时只有一个下拉框打开
    - _all_dropdowns: 所有下拉框实例字典，用于生命周期管理
    - _interface_cache: 界面级选项缓存，提高性能
    - _current_interface: 当前界面名称，用于缓存管理
    
    生命周期：
    1. 创建：通过create()方法创建实例，自动注册到_all_dropdowns
    2. 使用：用户交互，打开/关闭下拉框
    3. 销毁：通过destroy_all_instances()或destroy_interface_instances()销毁
    """
    
    _config_manager: ConfigManager = None
    _current_open_key: str = None
    _all_dropdowns: Dict[str, 'DropdownOptimized'] = {}
    
    _interface_cache: Dict[str, Dict[str, List[Dict]]] = {}
    _current_interface: str = None
    
    @classmethod
    def set_config_manager(cls, config_manager: ConfigManager):
        """
        设置配置管理实例（类级别）
        
        注意：此方法必须在创建任何Dropdown实例之前调用
        通常在MainEntry的_init_modules方法中调用
        
        参数:
            config_manager: 配置管理实例
        """
        cls._config_manager = config_manager
    
    @staticmethod
    def _check_config_manager():
        """检查配置管理是否已设置"""
        if DropdownOptimized._config_manager is None:
            raise RuntimeError(
                "DropdownOptimized模块未设置config_manager。\n"
                "解决方案：\n"
                "1. 确保在创建Dropdown实例之前调用 Dropdown.set_config_manager(config_manager)\n"
                "2. 通常在MainEntry的_init_modules方法中调用\n"
                "3. 检查初始化顺序是否正确"
            )
    
    @staticmethod
    def get_font_size() -> int:
        DropdownOptimized._check_config_manager()
        return DropdownOptimized._config_manager.get_ui_size("字体", "正文字体") or 16
    
    @staticmethod
    def get_icon_size() -> int:
        DropdownOptimized._check_config_manager()
        return DropdownOptimized._config_manager.get_ui_size("字体", "图标大小") or 18
    
    @staticmethod
    def get_border_radius() -> int:
        DropdownOptimized._check_config_manager()
        return DropdownOptimized._config_manager.get_radius("小") or 3
    
    @staticmethod
    def get_padding() -> int:
        DropdownOptimized._check_config_manager()
        return DropdownOptimized._config_manager.get_ui_size("边距", "下拉框内边距") or 8
    
    @staticmethod
    def get_options_padding() -> int:
        DropdownOptimized._check_config_manager()
        return DropdownOptimized._config_manager.get_ui_size("边距", "下拉框内边距") or 8
    
    @staticmethod
    def get_options_spacing() -> int:
        DropdownOptimized._check_config_manager()
        return DropdownOptimized._config_manager.get_ui_size("边距", "下拉框选项间距") or 4
    
    @staticmethod
    def get_max_options_height() -> int:
        DropdownOptimized._check_config_manager()
        return DropdownOptimized._config_manager.get_ui_config("控件", "下拉框最大菜单高度") or DEFAULT_MAX_MENU_HEIGHT
    
    @staticmethod
    def get_shadow_config() -> Dict:
        DropdownOptimized._check_config_manager()
        return DropdownOptimized._config_manager.get_shadow_config("菜单")
    
    @classmethod
    def set_current_interface(cls, interface: str):
        """
        设置当前界面（用于缓存管理）
        
        当切换界面时，会自动清理上一个界面的缓存
        
        参数:
            interface: 界面名称
        """
        if cls._current_interface and cls._current_interface != interface:
            cls._clear_interface_cache(cls._current_interface)
        cls._current_interface = interface
    
    @classmethod
    def _clear_interface_cache(cls, interface: str):
        """
        清理指定界面的缓存
        
        参数:
            interface: 界面名称
        """
        if interface in cls._interface_cache:
            cls._interface_cache[interface].clear()
            del cls._interface_cache[interface]
    
    @classmethod
    def get_cached_options(cls, interface: str, key: str) -> Optional[List[Dict]]:
        """
        获取缓存的选项列表
        
        参数:
            interface: 界面名称
            key: 下拉框key，格式为 "card.control_id"
        
        返回:
            缓存的选项列表，如果不存在则返回None
        """
        if not CACHE_ENABLED:
            return None
        if interface in cls._interface_cache:
            return cls._interface_cache[interface].get(key)
        return None
    
    @classmethod
    def cache_options(cls, interface: str, key: str, options: List[Dict]):
        """
        缓存选项列表
        
        参数:
            interface: 界面名称
            key: 下拉框key，格式为 "card.control_id"
            options: 选项列表
        """
        if not CACHE_ENABLED:
            return
        if interface not in cls._interface_cache:
            cls._interface_cache[interface] = {}
        cls._interface_cache[interface][key] = options
    
    @classmethod
    def clear_dropdown_cache(cls, interface: str, key: str):
        """
        清除特定下拉框的缓存
        
        参数:
            interface: 界面名称
            key: 下拉框key，格式为 "card.control_id"
        """
        if interface in cls._interface_cache:
            if key in cls._interface_cache[interface]:
                del cls._interface_cache[interface][key]
    
    @classmethod
    def destroy_all_instances(cls):
        """
        销毁所有下拉框实例
        
        使用场景：
        - 主题切换时，需要重建所有UI
        - 方案切换时，需要清空所有状态
        - 应用退出时，清理资源
        
        注意：此方法会清空_all_dropdowns字典和所有缓存
        """
        keys_to_process = list(cls._all_dropdowns.keys())
        for key in keys_to_process:
            if key in cls._all_dropdowns:
                instance = cls._all_dropdowns[key]
                instance._destroy_instance(key)
        cls._all_dropdowns.clear()
        cls._current_open_key = None
    
    @classmethod
    def destroy_interface_instances(cls, interface: str):
        """
        销毁指定界面的所有下拉框实例
        
        使用场景：
        - 切换界面时，销毁上一界面的下拉框
        - 释放内存，避免资源泄漏
        
        参数:
            interface: 界面名称
        """
        keys_to_remove = [k for k in list(cls._all_dropdowns.keys()) if k.startswith(f"{interface}.")]
        for key in keys_to_remove:
            if key in cls._all_dropdowns:
                instance = cls._all_dropdowns[key]
                instance._destroy_instance(key)
                del cls._all_dropdowns[key]
        cls._clear_interface_cache(interface)
    
    @classmethod
    def cleanup_page_overlay(cls, page: ft.Page):
        """
        清理页面overlay中的下拉框面板和遮罩
        
        使用场景：
        - 切换界面时，清理overlay中的残留元素
        - 重建UI前，确保overlay干净
        
        参数:
            page: Flet页面对象
        """
        panels_to_remove = []
        masks_to_remove = []
        for key in list(cls._all_dropdowns.keys()):
            if key not in cls._all_dropdowns:
                continue
            instance = cls._all_dropdowns[key]
            for panel_key, panel in list(instance._options_panels.items()):
                try:
                    if panel in page.overlay:
                        panels_to_remove.append(panel)
                except:
                    pass
            for container_key, container in instance._dropdowns.items():
                try:
                    if hasattr(container, '_overlay_mask') and container._overlay_mask in page.overlay:
                        masks_to_remove.append(container._overlay_mask)
                except:
                    pass
        
        for panel in panels_to_remove:
            try:
                page.overlay.remove(panel)
            except:
                pass
        for mask in masks_to_remove:
            try:
                page.overlay.remove(mask)
            except:
                pass
    
    def __init__(self, page: ft.Page = None, config_manager: ConfigManager = None):
        self._page = page
        self._config_manager = config_manager or DropdownOptimized._config_manager
        self._dropdowns: Dict[str, ft.Container] = {}
        self._dropdown_states: Dict[str, Dict] = {}
        self._options_panels: Dict[str, ft.Container] = {}
    
    def _destroy_instance(self, key: str):
        if key in self._dropdown_states:
            state = self._dropdown_states[key]
            state["options"] = []
            state["options_loaded"] = False
            state["is_open"] = False
        
        if key in self._options_panels:
            panel = self._options_panels[key]
            panel.visible = False
            if hasattr(panel.content, 'controls'):
                panel.content.controls.clear()
        
        if key in self._dropdowns:
            container = self._dropdowns[key]
            if hasattr(container, '_overlay_mask'):
                container._overlay_mask.visible = False
    
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
        use_defaults: bool = False,
    ) -> ft.Container:
        if width is None:
            width = self._config_manager.get_layout_value(interface, card, "dropdown_width", control_id)
            if width is None:
                width = self._config_manager.get_ui_config("控件", "下拉框宽度", 100)
        
        if height is None:
            height = self._config_manager.get_ui_config("控件", "下拉框高度", 30)
        
        border_radius = DropdownOptimized.get_border_radius()
        
        if theme_colors is None:
            theme_colors = self._config_manager.get_theme_colors()
        
        current_value = self._get_current_value(interface, card, control_id, use_defaults)
        
        container = self._build_dropdown(
            current_value, enabled,
            width, height, border_radius, theme_colors,
            interface, card, control_id, on_change,
        )
        
        key = f"{interface}.{card}.{control_id}" if interface and card and control_id else f"dropdown_{len(self._dropdowns)}"
        self._dropdowns[key] = container
        DropdownOptimized._all_dropdowns[key] = self
        
        return container
    
    def _get_current_value(self, interface: str, card: str, control_id: str, use_defaults: bool = False) -> Dict[str, str]:
        if self._config_manager:
            control_config = self._config_manager.get_control_config(interface, card, control_id)
            dynamic_options = control_config.get("dynamic_options", "")
            
            if dynamic_options in ("commanders", "commanders_exclude_primary"):
                if dynamic_options == "commanders":
                    state = self._config_manager.get_commander_dropdown_state(interface, card, control_id)
                else:
                    primary_control_id = control_id.replace("次要统帅", "主要统帅")
                    primary_commander = self._config_manager.get_raw_value(interface, card, primary_control_id)
                    state = self._config_manager.get_commander_dropdown_state(interface, card, control_id, primary_commander)
                
                return state["current_value"]
            
            if use_defaults:
                default_value = self._config_manager.get_default(interface, card, control_id)
                if default_value:
                    return {"text": default_value, "value": default_value}
            else:
                raw_value = self._config_manager.get_raw_value(interface, card, control_id)
                if raw_value:
                    return {"text": raw_value, "value": raw_value}
            
            default_value = self._config_manager.get_default(interface, card, control_id)
            if default_value:
                return {"text": default_value, "value": default_value}
        
        return {"text": "点击加载选项...", "value": ""}
    
    def _load_options(self, interface: str, card: str, control_id: str) -> List[Dict[str, str]]:
        key = f"{interface}.{card}.{control_id}"
        
        cached = DropdownOptimized.get_cached_options(interface, key)
        if cached is not None:
            return cached
        
        options = self._config_manager.get_options(interface, card, control_id)
        
        DropdownOptimized.cache_options(interface, key, options)
        
        return options
    
    def _save_value(self, interface: str, card: str, control_id: str, value: Dict[str, str]):
        if self._config_manager:
            self._config_manager.set_value(interface, card, control_id, value)
    
    def _close_all_dropdowns(self, current_key: str = None):
        open_key = DropdownOptimized._current_open_key
        if open_key and open_key != current_key:
            if open_key in DropdownOptimized._all_dropdowns:
                dropdown_instance = DropdownOptimized._all_dropdowns[open_key]
                if open_key in dropdown_instance._dropdown_states:
                    state = dropdown_instance._dropdown_states[open_key]
                    if state.get("is_open", False):
                        state["is_open"] = False
                        if open_key in dropdown_instance._options_panels:
                            panel = dropdown_instance._options_panels[open_key]
                            panel.visible = False
                            if hasattr(panel.content, 'controls'):
                                panel.content.controls.clear()
                        if open_key in dropdown_instance._dropdowns:
                            container = dropdown_instance._dropdowns[open_key]
                            if hasattr(container, '_overlay_mask'):
                                container._overlay_mask.visible = False
        
        DropdownOptimized._current_open_key = current_key
    
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
        hover_color = "#3A3A3A"
        
        font_size = DropdownOptimized.get_font_size()
        icon_size = DropdownOptimized.get_icon_size()
        padding = DropdownOptimized.get_padding()
        
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
            "panel_created": False,
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
        panel_ref = [None]
        mask_ref = [None]
        
        def create_panel_if_needed():
            if state["panel_created"]:
                return panel_ref[0], mask_ref[0]
            
            options_padding = DropdownOptimized.get_options_padding()
            options_spacing = DropdownOptimized.get_options_spacing()
            shadow_config = DropdownOptimized.get_shadow_config()
            
            search_box = ft.Container(
                content=ft.TextField(
                    hint_text="搜索...",
                    border=ft.InputBorder.NONE,
                    filled=True,
                    bgcolor="transparent",
                    text_size=font_size,
                    color=text_color,
                    hint_style=ft.TextStyle(color=text_secondary),
                    on_change=lambda e: self._on_search(e, key),
                ),
                padding=ft.Padding.symmetric(horizontal=padding, vertical=4),
                height=0,
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
            
            overlay_mask = ft.Container(
                visible=False,
                bgcolor="transparent",
                expand=True,
                on_click=lambda e: close_dropdown(),
            )
            
            panel_ref[0] = options_panel
            mask_ref[0] = overlay_mask
            self._options_panels[key] = options_panel
            
            state["panel_created"] = True
            state["search_box"] = search_box
            state["options_list"] = options_list
            
            return options_panel, overlay_mask
        
        def close_dropdown():
            if not state["is_open"]:
                return
            if panel_ref[0]:
                panel_ref[0].visible = False
            if mask_ref[0]:
                mask_ref[0].visible = False
            state["is_open"] = False
            if "options_list" in state:
                state["options_list"].controls.clear()
            if current_page[0]:
                current_page[0].update()
        
        def select_option(option: Dict, from_search: bool = False):
            state["current_value"] = option
            display_text.value = option.get("text", "")
            display_text.color = text_color
            self._save_value(interface, card, control_id, option)
            if on_change:
                on_change(interface, card, control_id, option)
            close_dropdown()
        
        def create_option_button(opt: Dict, is_selected: bool) -> ft.Container:
            item_height = _calculate_item_height(font_size)
            btn = ft.Container(
                content=ft.Text(opt.get("text", ""), size=font_size, color=text_color),
                padding=ft.Padding.symmetric(horizontal=padding, vertical=OPTION_ITEM_PADDING_V),
                height=item_height,
                width=float('inf'),
                bgcolor=hover_color if is_selected else "transparent",
                border_radius=border_radius,
                on_click=lambda e, o=opt: select_option(o),
            )
            
            def on_hover(e, button=btn, sel=is_selected):
                try:
                    if e.data == "true":
                        button.bgcolor = hover_color
                    else:
                        button.bgcolor = hover_color if sel else "transparent"
                    button.update()
                except RuntimeError:
                    pass
            
            btn.on_hover = on_hover
            return btn
        
        def build_options_list(opts: List[Dict], need_search: bool):
            """
            构建选项列表
            
            性能优化策略：
            1. 选项数据已缓存（通过get_cached_options）
            2. 选项按钮每次重新构建，原因：
               - 需要更新选中状态
               - 需要处理搜索过滤
               - Flet控件不支持复用
            3. 使用列表推导式优化性能
            
            参数:
                opts: 选项列表
                need_search: 是否需要搜索框
            
            返回:
                选中项的索引，如果没有选中项则返回-1
            """
            options_list = state.get("options_list")
            if not options_list:
                return -1
            
            options_list.controls.clear()
            
            if need_search and "search_box" in state:
                options_list.controls.append(state["search_box"])
            
            current_val = state["current_value"].get("value", "")
            selected_index = -1
            
            for i, opt in enumerate(opts):
                is_selected = (opt.get("value", "") == current_val)
                if is_selected:
                    selected_index = i
                btn = create_option_button(opt, is_selected)
                options_list.controls.append(btn)
            
            return selected_index
        
        def on_tap_down(e):
            try:
                if e.global_position and e.local_position:
                    button_position["top"] = e.global_position.y - e.local_position.y
                    button_position["left"] = e.global_position.x - e.local_position.x
            except Exception:
                pass
        
        def toggle_dropdown(e):
            if not state["enabled"]:
                return
            
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
            
            current_page[0] = page
            
            if not state["is_open"]:
                self._close_all_dropdowns(key)
                
                options_panel, overlay_mask = create_panel_if_needed()
                
                if not state["options_loaded"]:
                    options = self._load_options(interface, card, control_id)
                    state["options"] = options
                    state["options_loaded"] = True
                
                opts = state["options"]
                opts_count = len(opts)
                
                need_search = opts_count >= SEARCH_THRESHOLD
                
                if "search_box" in state:
                    state["search_box"].height = SEARCH_BOX_HEIGHT if need_search else 0
                
                selected_index = build_options_list(opts, need_search)
                
                options_padding = DropdownOptimized.get_options_padding()
                options_spacing = DropdownOptimized.get_options_spacing()
                max_options_height = DropdownOptimized.get_max_options_height()
                item_height = _calculate_item_height(font_size)
                
                total_options_height = opts_count * item_height
                total_spacing_height = max(0, opts_count - 1) * options_spacing
                search_height = SEARCH_BOX_HEIGHT if need_search else 0
                estimated_content_height = total_options_height + total_spacing_height + 2 * options_padding + search_height
                
                button_top = button_position["top"]
                button_left = button_position["left"]
                
                space_down = page.height - (button_top + height)
                space_up = button_top
                
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
                elif estimated_content_height > max_options_height:
                    panel_height = max_options_height
                else:
                    panel_height = estimated_content_height
                
                min_height = item_height + 2 * options_padding + search_height
                if panel_height is not None and panel_height < min_height:
                    panel_height = min_height
                
                dropdown_text_width = width - 3 * padding - icon_size
                
                max_text_width = 0
                for opt in opts:
                    text = opt.get("text", "")
                    chinese_count = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
                    other_count = len(text) - chinese_count
                    text_width = chinese_count * font_size + other_count * font_size * 0.6
                    if text_width > max_text_width:
                        max_text_width = text_width
                
                min_panel_width = max_text_width + 2 * padding + 4
                min_dropdown_panel = width - padding - icon_size
                panel_width = max(min_dropdown_panel, min_panel_width)
                
                options_panel.top = panel_top
                if panel_height is not None:
                    options_panel.height = panel_height
                else:
                    options_panel.height = None
                options_panel.left = button_left
                options_panel.width = panel_width
                
                options_panel.visible = True
                overlay_mask.visible = True
                state["is_open"] = True
                
                container._overlay_mask = overlay_mask
                
                if overlay_mask not in page.overlay:
                    page.overlay.append(overlay_mask)
                if options_panel not in page.overlay:
                    page.overlay.append(options_panel)
                
                page.update()
                
                if selected_index >= 0 and panel_height is not None:
                    search_offset = SEARCH_BOX_HEIGHT if need_search else 0
                    scroll_offset = search_offset + selected_index * (item_height + options_spacing)
                    options_list = state.get("options_list")
                    if options_list:
                        try:
                            import asyncio
                            loop = asyncio.get_event_loop()
                            if loop.is_running():
                                asyncio.create_task(options_list.scroll_to(offset=scroll_offset, duration=SCROLL_DURATION))
                            else:
                                loop.run_until_complete(options_list.scroll_to(offset=scroll_offset, duration=SCROLL_DURATION))
                        except:
                            pass
            else:
                close_dropdown()
                page.update()
        
        gesture_detector = ft.GestureDetector(
            content=button_container,
            on_tap_down=on_tap_down,
            on_tap=toggle_dropdown,
        )
        
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
        
        def get_value() -> Dict[str, str]:
            return state["current_value"]
        
        def set_value(value: Dict[str, str]):
            state["current_value"] = value
            display_text.value = value.get("text", "")
        
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
    
    def _on_search(self, e, key: str):
        if key not in self._dropdown_states:
            return
        
        state = self._dropdown_states[key]
        keyword = e.control.value.lower().strip()
        
        if not keyword:
            self._rebuild_options_list(key, state["options"])
            return
        
        filtered = [
            opt for opt in state["options"]
            if self._match_option(opt, keyword)
        ]
        
        self._rebuild_options_list(key, filtered)
    
    def _match_option(self, opt: Dict, keyword: str) -> bool:
        text = opt.get("text", "").lower()
        if keyword in text:
            return True
        
        if PINYIN_AVAILABLE:
            pinyin = ''.join(lazy_pinyin(text))
            return keyword in pinyin
        
        return False
    
    def _rebuild_options_list(self, key: str, options: List[Dict]):
        if key not in self._options_panels:
            return
        
        panel = self._options_panels[key]
        options_list = panel.content
        
        if options_list is None:
            return
        
        search_box = None
        if options_list.controls and hasattr(options_list.controls[0], 'content'):
            if isinstance(options_list.controls[0].content, ft.TextField):
                search_box = options_list.controls[0]
        
        options_list.controls.clear()
        
        if search_box:
            options_list.controls.append(search_box)
        
        current_val = self._dropdown_states[key]["current_value"].get("value", "")
        
        font_size = DropdownOptimized.get_font_size()
        padding = DropdownOptimized.get_padding()
        text_color = self._config_manager.get_theme_colors().get("text_primary", "#FFFFFF")
        hover_color = "#3A3A3A"
        border_radius = DropdownOptimized.get_border_radius()
        item_height = _calculate_item_height(font_size)
        
        for opt in options:
            is_selected = (opt.get("value", "") == current_val)
            btn = ft.Container(
                content=ft.Text(opt.get("text", ""), size=font_size, color=text_color),
                padding=ft.Padding.symmetric(horizontal=padding, vertical=OPTION_ITEM_PADDING_V),
                height=item_height,
                width=float('inf'),
                bgcolor=hover_color if is_selected else "transparent",
                border_radius=border_radius,
                on_click=lambda e, o=opt: self._select_option_from_search(key, o),
            )
            options_list.controls.append(btn)
        
        options_list.update()
    
    def _select_option_from_search(self, key: str, option: Dict):
        if key not in self._dropdown_states:
            return
        
        state = self._dropdown_states[key]
        interface = state["interface"]
        card = state["card"]
        control_id = state["control_id"]
        
        state["current_value"] = option
        
        if key in self._dropdowns:
            container = self._dropdowns[key]
            if hasattr(container, '_button_container'):
                display_text = container._button_container.content.controls[0]
                display_text.value = option.get("text", "")
        
        self._save_value(interface, card, control_id, option)
        
        self._close_all_dropdowns()
        
        if self._page:
            self._page.update()
    
    def get_value(self, interface: str, card: str, control_id: str) -> Dict[str, str]:
        key = f"{interface}.{card}.{control_id}"
        if key in self._dropdowns:
            container = self._dropdowns[key]
            if hasattr(container, 'get_value'):
                return container.get_value()
        return {"text": "", "value": ""}


Dropdown = DropdownOptimized
