# -*- coding: utf-8 -*-

"""
模块名称：卡片开关.py
模块功能：卡片开关组件（左侧垂直布局）

职责：
- 卡片开关显示（左侧垂直布局：图标+标题+分割线）
- 开关状态管理

不负责：
- 点击处理（由功能卡片处理）
- 控件区
"""

import flet as ft
from typing import Callable, Dict, Any, List

from 设置界面.层级0_数据管理.配置管理 import ConfigManager
from 设置界面.层级5_基础模块.图标 import Icon
from 设置界面.层级5_基础模块.标签 import Label
from 设置界面.层级5_基础模块.分割线 import Divider


class CardSwitch:
    """
    卡片开关 - V3版本
    
    职责：
    - 卡片开关显示（左侧垂直布局：图标+标题+分割线）
    - 开关状态管理
    
    不负责：
    - 点击处理（由功能卡片处理）
    - 控件区
    """
    
    _config_manager: ConfigManager = None
    
    @classmethod
    def set_config_manager(cls, config_manager: ConfigManager):
        """设置配置管理实例"""
        cls._config_manager = config_manager
        Icon.set_config_manager(config_manager)
        Label.set_config_manager(config_manager)
        Divider.set_config_manager(config_manager)
    
    @staticmethod
    def _check_config_manager():
        """检查配置管理是否已设置"""
        if CardSwitch._config_manager is None:
            raise RuntimeError(
                "CardSwitch模块未设置config_manager，"
                "请先调用 CardSwitch.set_config_manager(config_manager)"
            )
    
    @staticmethod
    def get_left_width() -> int:
        """获取左侧宽度"""
        CardSwitch._check_config_manager()
        value = CardSwitch._config_manager.get_ui_config("卡片开关", "左侧宽度")
        return value if value else 100
    
    @staticmethod
    def get_padding() -> int:
        """获取内边距"""
        CardSwitch._check_config_manager()
        value = CardSwitch._config_manager.get_ui_config("卡片开关", "内边距")
        return value if value else 16
    
    @staticmethod
    def get_icon_size() -> int:
        """获取图标尺寸"""
        CardSwitch._check_config_manager()
        base_size = Icon.get_base_size()
        return int(base_size * 1.375)
    
    @staticmethod
    def get_title_size() -> int:
        """获取标题尺寸"""
        CardSwitch._check_config_manager()
        return Label.get_base_size()
    
    @staticmethod
    def get_subtitle_size() -> int:
        """获取副标题尺寸"""
        CardSwitch._check_config_manager()
        base_size = Label.get_base_size()
        return int(base_size * 0.71)
    
    @staticmethod
    def get_icon_title_spacing() -> int:
        """获取图标与标题间距"""
        CardSwitch._check_config_manager()
        spacing = CardSwitch._config_manager.get_ui_size("边距", "控件间距")
        if spacing is None:
            spacing = 6
        return spacing
    
    def __init__(self, page: ft.Page, config_manager: ConfigManager = None):
        self._page = page
        self._config_manager = config_manager or CardSwitch._config_manager
        self._enabled: bool = True
        self._controls_ref: Any = None
        self._icon_control: ft.Icon = None
        self._title_text: ft.Text = None
        self._subtitle_text: ft.Text = None
        self._switch_row: ft.Row = None
        self._container: ft.Container = None
        self._interface: str = ""
        self._card: str = ""
        self._theme_colors: Dict[str, str] = None
        self._on_toggle: Callable = None
        self._subtitle_enabled: str = ""
        self._subtitle_disabled: str = ""
        self._has_dynamic_subtitle: bool = False
    
    def create(
        self,
        interface: str,
        card: str,
        card_info: Dict = None,
        on_toggle: Callable[[str, str, bool], None] = None,
        theme_colors: Dict[str, str] = None,
        enabled: bool = None,
    ) -> ft.Container:
        """
        创建卡片开关
        
        参数：
        - interface: 界面名称
        - card: 卡片名称
        - card_info: 卡片信息
        - on_toggle: 开关状态变更回调
        - theme_colors: 主题颜色
        - enabled: 开关状态（None时从配置读取）
        
        返回：
        - ft.Container: 完整的卡片开关组件
        """
        if card_info is None:
            card_info = {}
        
        if theme_colors is None:
            theme_colors = self._get_theme_colors()
        
        self._interface = interface
        self._card = card
        self._theme_colors = theme_colors
        self._enabled = enabled if enabled is not None else self._get_enabled(interface, card)
        self._on_toggle = on_toggle
        
        title = card_info.get("title", card)
        icon_name = card_info.get("icon", "HOME")
        subtitle = card_info.get("subtitle", "")
        subtitle_enabled = card_info.get("subtitle_enabled", "")
        subtitle_disabled = card_info.get("subtitle_disabled", "")
        no_switch = card_info.get("no_switch", False)
        
        self._subtitle_enabled = subtitle_enabled
        self._subtitle_disabled = subtitle_disabled
        self._has_dynamic_subtitle = bool(subtitle_enabled and subtitle_disabled)
        
        if self._has_dynamic_subtitle:
            display_subtitle = subtitle_enabled if self._enabled else subtitle_disabled
        else:
            display_subtitle = subtitle
        
        icon_size = self.get_icon_size()
        title_size = self.get_title_size()
        subtitle_size = self.get_subtitle_size()
        left_width = self.get_left_width()
        padding = self.get_padding()
        icon_title_spacing = self.get_icon_title_spacing()
        card_height = self._config_manager.get_card_height(interface, card)
        
        accent_color = theme_colors.get("accent", "#0078D4")
        text_primary = theme_colors.get("text_primary", "#FFFFFF")
        text_secondary = theme_colors.get("text_secondary", "#B0B0B0")
        
        self._icon_control = ft.Icon(
            getattr(ft.Icons, icon_name.upper(), ft.Icons.HOME),
            size=icon_size,
            color=accent_color,
            opacity=1.0 if self._enabled else 0.4,
        )
        
        self._title_text = ft.Text(
            title,
            size=title_size,
            weight=ft.FontWeight.BOLD,
            color=text_primary,
            opacity=1.0 if self._enabled else 0.4,
            text_align=ft.TextAlign.CENTER,
        )
        
        left_content = ft.Column([
            self._icon_control,
            ft.Container(height=icon_title_spacing),
            self._title_text,
        ], spacing=0, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        def handle_toggle_click(e):
            if no_switch:
                return
            if self._on_toggle:
                self._on_toggle(interface, card, not self._enabled)
        
        left_container = ft.Container(
            content=left_content,
            width=left_width - 2,
            padding=ft.Padding(padding, 0, padding, 0),
            alignment=ft.alignment.Alignment(0, 0.5),
            on_click=None if no_switch else handle_toggle_click,
        )
        
        divider_height = card_height - padding
        divider_width = self._config_manager.get_ui_config("卡片开关", "分割线宽度") or 2
        
        divider_container = ft.Container(
            content=Divider.create_vertical(
                width=divider_width,
                color_type="accent",
                theme_colors=theme_colors,
            ),
            height=divider_height,
            alignment=ft.alignment.Alignment(0, 0.5),
            on_click=None if no_switch else handle_toggle_click,
        )
        
        self._subtitle_text = ft.Text(
            display_subtitle.replace(" | ", "\n").replace("|", "\n"),
            size=subtitle_size,
            color=text_secondary,
            opacity=0.8 if self._enabled else 0.4,
            max_lines=4,
            overflow=ft.TextOverflow.ELLIPSIS,
            no_wrap=False,
        ) if display_subtitle else None
        
        right_content = ft.Column([
            self._subtitle_text if self._subtitle_text else ft.Container(),
        ], spacing=0, alignment=ft.MainAxisAlignment.END, tight=True) if self._subtitle_text else ft.Container()
        
        right_container = ft.Container(
            content=right_content,
            expand=True if self._subtitle_text else False,
            padding=ft.Padding(8, 0, padding, 0),
            alignment=ft.alignment.Alignment(-1, 1),
        )
        
        self._switch_row = ft.Row([
            left_container,
            divider_container,
            right_container,
        ], spacing=0, vertical_alignment=ft.CrossAxisAlignment.CENTER, height=card_height)
        
        self._container = ft.Container(content=self._switch_row)
        
        return self._container
    
    def is_enabled(self) -> bool:
        """获取当前开关状态"""
        return self._enabled
    
    def set_enabled_state(self, enabled: bool):
        """设置开关状态（由功能卡片调用）"""
        self._enabled = enabled
        
        self._icon_control.opacity = 1.0 if enabled else 0.4
        self._title_text.opacity = 1.0 if enabled else 0.4
        
        if self._subtitle_text:
            self._subtitle_text.opacity = 0.8 if enabled else 0.4
            
            if self._has_dynamic_subtitle:
                new_subtitle = self._subtitle_enabled if enabled else self._subtitle_disabled
                self._subtitle_text.value = new_subtitle.replace(" | ", "\n").replace("|", "\n")
        
        try:
            self._icon_control.update()
            self._title_text.update()
            if self._subtitle_text:
                self._subtitle_text.update()
        except:
            pass
    
    def set_controls_ref(self, controls_ref: Any):
        """设置控件区引用"""
        self._controls_ref = controls_ref
    
    def set_subtitle(self, subtitle: str, update_now: bool = True):
        """更新副标题
        
        参数：
        - subtitle: 副标题文本
        - update_now: 是否立即更新UI（批量操作时设为False）
        """
        formatted_subtitle = subtitle.replace(" | ", "\n").replace("|", "\n") if subtitle else ""
        
        if self._subtitle_text:
            self._subtitle_text.value = formatted_subtitle
            if update_now:
                try:
                    self._subtitle_text.update()
                except:
                    pass
        else:
            subtitle_size = self.get_subtitle_size()
            text_secondary = self._theme_colors.get("text_secondary", "#B0B0B0") if self._theme_colors else "#B0B0B0"
            self._subtitle_text = ft.Text(
                formatted_subtitle,
                size=subtitle_size,
                color=text_secondary,
                opacity=0.8 if self._enabled else 0.4,
                max_lines=4,
                overflow=ft.TextOverflow.ELLIPSIS,
            )
            if self._switch_row and len(self._switch_row.controls) >= 3:
                right_container = self._switch_row.controls[2]
                right_container.expand = True
                right_content = ft.Column([
                    ft.Container(expand=True),
                    self._subtitle_text,
                ], spacing=0, alignment=ft.MainAxisAlignment.END)
                right_container.content = right_content
                
                if update_now and self._container:
                    try:
                        self._container.update()
                    except:
                        pass
    
    def _get_theme_colors(self) -> Dict[str, str]:
        """获取主题颜色"""
        if self._config_manager is None:
            raise RuntimeError("CardSwitch模块未设置config_manager")
        return self._config_manager.get_theme_colors()
    
    def _get_enabled(self, interface: str, card: str) -> bool:
        """获取卡片开关状态"""
        if self._config_manager:
            return self._config_manager.get_enabled(interface, card)
        return True
