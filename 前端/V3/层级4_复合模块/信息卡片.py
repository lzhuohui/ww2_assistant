# -*- coding: utf-8 -*-

"""
模块名称：信息卡片.py
模块功能：纯信息展示卡片（无开关，布局：图标+标题 | 分割线 | 信息内容分行显示）

职责：
- 图标+标题+分割线+信息内容（分行显示）
- 用于关于界面等纯信息展示场景

不负责：
- 开关切换
- 数据存储
"""

from typing import Dict
import flet as ft

from 前端.V3.层级0_数据管理.配置管理 import ConfigManager
from 前端.V3.层级5_基础模块.图标 import Icon
from 前端.V3.层级5_基础模块.标签 import Label
from 前端.V3.层级5_基础模块.分割线 import Divider


class InfoCard:
    """信息卡片 - V3版本"""
    
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
        if InfoCard._config_manager is None:
            raise RuntimeError(
                "InfoCard模块未设置config_manager，"
                "请先调用 InfoCard.set_config_manager(config_manager)"
            )
    
    @staticmethod
    def get_left_width() -> int:
        """获取左侧宽度"""
        InfoCard._check_config_manager()
        value = InfoCard._config_manager.get_ui_config("卡片开关", "左侧宽度")
        return value if value else 100
    
    @staticmethod
    def get_icon_size() -> int:
        """获取图标尺寸"""
        InfoCard._check_config_manager()
        base_size = Icon.get_base_size()
        return int(base_size * 1.375)
    
    @staticmethod
    def get_title_size() -> int:
        """获取标题尺寸"""
        InfoCard._check_config_manager()
        return Label.get_base_size()
    
    @staticmethod
    def get_info_size() -> int:
        """获取信息文字尺寸"""
        InfoCard._check_config_manager()
        base_size = Label.get_base_size()
        return int(base_size * 0.875)
    
    @staticmethod
    def get_icon_title_spacing() -> int:
        """获取图标与标题间距"""
        InfoCard._check_config_manager()
        spacing = InfoCard._config_manager.get_ui_size("边距", "控件间距")
        return spacing if spacing is not None else 6
    
    def __init__(self, page: ft.Page, config_manager: ConfigManager = None):
        self._page = page
        if config_manager and config_manager != InfoCard._config_manager:
            InfoCard.set_config_manager(config_manager)
        self._config_manager = config_manager or InfoCard._config_manager
        self._container: ft.Container = None
    
    def create(
        self,
        interface: str,
        card: str,
        card_info: Dict = None,
        theme_colors: Dict[str, str] = None,
    ) -> ft.Container:
        """创建信息卡片
        
        参数:
        - interface: 界面名称
        - card: 卡片名称
        - card_info: 卡片信息（包含title, icon, 控件列表）
        - theme_colors: 主题颜色
        """
        if card_info is None:
            card_info = {}
        
        if theme_colors is None:
            theme_colors = self._get_theme_colors()
        
        title = card_info.get("title", card)
        icon_name = card_info.get("icon", "INFO")
        controls_config = card_info.get("控件列表", [])
        
        icon_size = self.get_icon_size()
        title_size = self.get_title_size()
        info_size = self.get_info_size()
        icon_title_spacing = self.get_icon_title_spacing()
        left_width = self.get_left_width()
        padding = self._config_manager.get_ui_config("卡片开关", "内边距") or 16
        
        card_height = self._config_manager.get_card_height(interface, card)
        
        accent_color = theme_colors.get("accent", "#0078D4")
        text_primary = theme_colors.get("text_primary", "#FFFFFF")
        text_secondary = theme_colors.get("text_secondary", "#B0B0B0")
        bg_card = theme_colors.get("bg_card", "#2D2D2D")
        border_color = theme_colors.get("border", "#3D3D3D")
        
        icon_control = ft.Icon(
            getattr(ft.Icons, icon_name.upper(), ft.Icons.INFO),
            size=icon_size,
            color=accent_color,
        )
        
        title_text = ft.Text(
            title,
            size=title_size,
            weight=ft.FontWeight.BOLD,
            color=text_primary,
        )
        
        info_rows = []
        for item in controls_config:
            label = item.get("label", "")
            value = item.get("value", "")
            copyable = item.get("copyable", False)
            
            if label:
                if copyable:
                    value_control = self._create_copyable_text(
                        value, info_size, text_primary, theme_colors
                    )
                else:
                    value_control = ft.Text(value, size=info_size, color=text_primary)
                info_rows.append(ft.Row([
                    ft.Text(label, size=info_size, color=text_secondary, width=80),
                    value_control,
                ], spacing=8, vertical_alignment=ft.CrossAxisAlignment.CENTER))
            else:
                if copyable:
                    info_rows.append(self._create_copyable_text(
                        value, info_size, text_primary, theme_colors
                    ))
                else:
                    info_rows.append(ft.Text(value, size=info_size, color=text_primary))
        
        left_content = ft.Column([
            icon_control,
            ft.Container(height=icon_title_spacing),
            title_text,
        ], spacing=0, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        left_container = ft.Container(
            content=left_content,
            width=left_width - 2,
            padding=ft.Padding(padding, 0, padding, 0),
            alignment=ft.alignment.Alignment(0, 0.5),
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
        )
        
        right_content = ft.Column(
            info_rows,
            spacing=4,
            alignment=ft.MainAxisAlignment.CENTER,
        ) if info_rows else ft.Container()
        
        right_container = ft.Container(
            content=right_content,
            expand=True,
            padding=ft.Padding(8, 0, padding, 0),
            alignment=ft.alignment.Alignment(-1, 0.5),
        )
        
        card_row = ft.Row([
            left_container,
            divider_container,
            right_container,
        ], spacing=0, vertical_alignment=ft.CrossAxisAlignment.CENTER, height=card_height)
        
        self._container = ft.Container(
            content=card_row,
            bgcolor=bg_card,
            border=ft.Border.all(1, border_color),
            border_radius=self._config_manager.get_radius("中") or 8,
        )
        
        return self._container
    
    def _get_theme_colors(self) -> Dict[str, str]:
        """获取主题颜色"""
        if self._config_manager is None:
            raise RuntimeError("InfoCard模块未设置config_manager")
        return self._config_manager.get_theme_colors()
    
    def _create_copyable_text(
        self,
        text: str,
        font_size: int,
        text_color: str,
        theme_colors: Dict[str, str],
    ) -> ft.Container:
        """创建可点击复制的文本控件
        
        功能：
        - 悬停时显示背景色变化
        - 点击时复制到剪贴板
        - 复制成功显示提示
        """
        hover_bg = theme_colors.get("bg_hover", "#3D3D3D")
        
        async def on_click(e):
            await ft.Clipboard().set(str(text))
            self._show_copy_snackbar(f"已复制: {text}")
        
        def on_hover(e):
            e.control.bgcolor = hover_bg if e.data == "true" else None
            e.control.update()
        
        return ft.Container(
            content=ft.Text(text, size=font_size, color=text_color),
            on_click=on_click,
            on_hover=on_hover,
            border_radius=4,
            padding=ft.Padding(4, 2, 4, 2),
        )
    
    def _show_copy_snackbar(self, message: str):
        """显示复制成功提示（SnackBar）"""
        self._page.show_dialog(ft.SnackBar(ft.Text(message), duration=1500))
    
    def destroy(self):
        """销毁卡片"""
        self._container = None
