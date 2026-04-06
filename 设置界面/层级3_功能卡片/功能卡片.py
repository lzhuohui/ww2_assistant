# -*- coding: utf-8 -*-

"""
模块名称：功能卡片.py
模块功能：功能卡片组件，Stack布局（三层结构）

职责：
- Stack布局：背景容器(下层) + 卡片开关(中层) + 卡片控件(上层)
- 卡片高度精确控制
- 开关状态联动容器透明度

不负责：
- 数据存储
- 销毁管理（由层级1主入口负责）
"""

import flet as ft
from typing import Callable, Dict, Any

from 设置界面.层级0_数据管理.配置管理 import ConfigManager
from 设置界面.层级4_复合模块.卡片开关 import CardSwitch
from 设置界面.层级4_复合模块.卡片控件 import CardControls


class FunctionCard:
    """
    功能卡片 - V3版本
    
    职责：
    - Stack布局：背景容器(下层) + 卡片开关(中层) + 卡片控件(上层)
    - 卡片高度精确控制
    - 开关状态联动容器透明度
    
    不负责：
    - 数据存储
    """
    
    _config_manager: ConfigManager = None
    
    @classmethod
    def set_config_manager(cls, config_manager: ConfigManager):
        """设置配置管理实例"""
        cls._config_manager = config_manager
        CardSwitch.set_config_manager(config_manager)
        CardControls.set_config_manager(config_manager)
    
    @staticmethod
    def _check_config_manager():
        """检查配置管理是否已设置"""
        if FunctionCard._config_manager is None:
            raise RuntimeError(
                "FunctionCard模块未设置config_manager，"
                "请先调用 FunctionCard.set_config_manager(config_manager)"
            )
    
    @staticmethod
    def get_min_height() -> int:
        """获取卡片最小高度"""
        FunctionCard._check_config_manager()
        value = FunctionCard._config_manager.get_ui_config("卡片", "最小高度")
        return value if value else 100
    
    @staticmethod
    def get_padding() -> int:
        """获取卡片内边距"""
        FunctionCard._check_config_manager()
        return FunctionCard._config_manager.get_ui_size("边距", "卡片内边距")
    
    @staticmethod
    def get_border_radius() -> int:
        """获取卡片圆角"""
        FunctionCard._check_config_manager()
        return FunctionCard._config_manager.get_ui_size("圆角", "卡片圆角")
    
    @staticmethod
    def get_spacing() -> int:
        """获取卡片间距"""
        FunctionCard._check_config_manager()
        return FunctionCard._config_manager.get_ui_size("边距", "卡片间距")
    
    def __init__(self, page: ft.Page, config_manager: ConfigManager = None):
        self._page = page
        if config_manager and config_manager != FunctionCard._config_manager:
            FunctionCard.set_config_manager(config_manager)
        self._config_manager = config_manager or FunctionCard._config_manager
        self._cards: Dict[str, ft.Stack] = {}
        self._card_switches: Dict[str, CardSwitch] = {}
        self._card_controls: Dict[str, CardControls] = {}
        self._containers: Dict[str, ft.Container] = {}
    
    def create(
        self,
        interface: str,
        card: str,
        on_change: Callable[[str, str, str, Any], None] = None,
        on_toggle: Callable[[str, str, bool], None] = None,
        theme_colors: Dict[str, str] = None,
        use_defaults: bool = False,
    ) -> ft.Stack:
        """
        创建功能卡片（Stack三层布局）
        
        参数：
        - interface: 界面名称
        - card: 卡片名称
        - on_change: 控件值变更回调
        - on_toggle: 开关状态变更回调
        - theme_colors: 主题颜色
        - use_defaults: 是否使用默认值（True时忽略方案值）
        
        返回：
        - ft.Stack: 完整的功能卡片
        """
        if theme_colors is None:
            theme_colors = self._get_theme_colors()
        
        card_info = self._get_card_info(interface, card)
        key = f"{interface}.{card}"
        
        card_height = self._config_manager.get_card_height(interface, card)
        
        no_switch = card_info.get("no_switch", False)
        
        if use_defaults:
            enabled = self._config_manager.get_enabled_default(interface, card)
        else:
            enabled = self._config_manager.get_enabled(interface, card)
        
        if no_switch:
            enabled = True
        
        card_switch = CardSwitch(self._page, self._config_manager)
        card_controls = CardControls(self._page, self._config_manager)
        
        controls_section = card_controls.create(
            interface=interface,
            card=card,
            on_change=on_change,
            theme_colors=theme_colors,
            use_defaults=use_defaults,
        )
        
        bg_card = theme_colors.get("bg_card", "#2D2D2D")
        border_color = theme_colors.get("border", "#3D3D3D")
        accent = theme_colors.get("accent", "#0078D4")
        
        animation_config = self._config_manager.get_animation_config()
        transition_duration = animation_config.get("transition_duration", 167)
        
        bg_container = ft.Container(
            bgcolor=bg_card,
            border=ft.Border.all(1, border_color),
            border_radius=self.get_border_radius(),
            padding=0,
            height=card_height,
            opacity=1.0 if enabled else 0.5,
            clip_behavior=ft.ClipBehavior.NONE,
            animate=transition_duration,
        )
        
        def on_card_hover(e):
            if e.data == "true":
                bg_container.border = ft.Border.all(1, accent)
            else:
                bg_container.border = ft.Border.all(1, border_color)
            bg_container.update()
        
        bg_container.on_hover = on_card_hover
        
        self._containers[key] = bg_container
        
        def handle_toggle(interface: str, card: str, new_enabled: bool):
            if no_switch:
                return
            card_switch.set_enabled_state(new_enabled)
            bg_container.opacity = 1.0 if new_enabled else 0.5
            card_controls.set_enabled(new_enabled)
            self._config_manager.set_enabled(interface, card, new_enabled)
            if on_toggle:
                on_toggle(interface, card, new_enabled)
            try:
                card_stack.update()
            except:
                pass
        
        switch_section = card_switch.create(
            interface=interface,
            card=card,
            card_info=card_info,
            on_toggle=handle_toggle,
            theme_colors=theme_colors,
            enabled=enabled,
        )
        
        left_width = CardSwitch.get_left_width()
        
        subtitle_max_width = 400
        switch_max_width = left_width + subtitle_max_width
        
        switch_container = ft.Container(
            content=switch_section,
            alignment=ft.alignment.Alignment(0, 0.5),
            top=0,
            left=0,
            width=switch_max_width,
        )
        
        controls_container = ft.Container(
            content=ft.Row([
                ft.Container(expand=True),
                controls_section,
            ], spacing=0, vertical_alignment=ft.CrossAxisAlignment.CENTER, expand=True),
            top=0,
            left=left_width,
            right=0,
            height=card_height,
        )
        
        card_stack = ft.Stack([
            bg_container,
            switch_container,
            controls_container,
        ], clip_behavior=ft.ClipBehavior.NONE, key=key)
        
        card_stack.height = card_height
        
        card_switch.set_controls_ref(card_controls)
        
        self._card_switches[key] = card_switch
        self._card_controls[key] = card_controls
        self._cards[key] = card_stack
        
        return card_stack
    
    def _get_theme_colors(self) -> Dict[str, str]:
        """获取主题颜色"""
        if self._config_manager is None:
            raise RuntimeError("FunctionCard模块未设置config_manager")
        return self._config_manager.get_theme_colors()
    
    def _get_card_info(self, interface: str, card: str) -> Dict[str, Any]:
        """获取卡片信息"""
        if self._config_manager:
            return self._config_manager.get_card_info(interface, card)
        return {}
    
    def set_subtitle(self, interface: str, card: str, subtitle: str, update_now: bool = True):
        """更新卡片副标题
        
        参数：
        - interface: 界面名称
        - card: 卡片名称
        - subtitle: 副标题文本
        - update_now: 是否立即更新UI（批量操作时设为False）
        """
        key = f"{interface}.{card}"
        if key in self._card_switches:
            self._card_switches[key].set_subtitle(subtitle, update_now)
    
    def destroy(self):
        """销毁所有卡片资源"""
        self._cards.clear()
        self._card_switches.clear()
        self._card_controls.clear()
        self._containers.clear()
