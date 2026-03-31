# -*- coding: utf-8 -*-

"""
模块名称：下拉框.py
模块功能：下拉框组件，使用PopupMenuButton实现，支持text/value格式

实现步骤：
- 创建时自动从配置服务加载选项列表
- 创建时自动从配置服务加载当前值
- 支持text/value格式
- 选择后自动保存到配置
- 支持销毁管理减少内存占用
- Win11风格

职责：
- 从配置服务获取选项列表
- 从配置服务获取当前值
- 懒加载菜单（点击时加载，关闭时销毁）
- 自动保存到配置
- 销毁菜单

不负责：
- 布局
- 开关状态

设计原则（符合V2版本模块化设计补充共识）：
- 从配置服务获取UI配置（宽度、高度）
- 定义DEFAULT_XXX作为fallback
"""

import flet as ft
from typing import List, Dict, Callable, Any, Optional

# ============================================
# 默认配置（fallback，用于模块独立测试）
# ============================================

DEFAULT_WIDTH = 120
DEFAULT_HEIGHT = 30

# ============================================
# 公开接口
# ============================================

class Dropdown:
    """
    下拉框组件 - 使用PopupMenuButton实现
    
    职责：
    - 从配置服务获取选项列表
    - 从配置服务获取当前值
    - 从配置服务获取UI配置
    - 自动保存到配置
    
    不负责：
    - 布局
    - 开关状态
    """
    
    _config_service = None
    
    @classmethod
    def set_config_service(cls, config_service):
        """设置配置服务实例"""
        cls._config_service = config_service
    
    @staticmethod
    def get_width() -> int:
        """获取下拉框宽度（从配置服务获取）"""
        if Dropdown._config_service:
            return Dropdown._config_service.get_ui_config("下拉框", "宽度", DEFAULT_WIDTH)
        return DEFAULT_WIDTH
    
    @staticmethod
    def get_height() -> int:
        """获取下拉框高度（从配置服务获取）"""
        if Dropdown._config_service:
            return Dropdown._config_service.get_ui_config("下拉框", "高度", DEFAULT_HEIGHT)
        return DEFAULT_HEIGHT
    
    def __init__(self, page: ft.Page = None, config_service=None):
        self._page = page
        self._config_service = config_service
        self._dropdowns: Dict[str, ft.Container] = {}
    
    def create(
        self,
        section: str = "",
        control_id: str = "",
        enabled: bool = True,
        on_change: Callable[[str, str, Dict[str, str]], None] = None,
        theme_colors: Dict[str, str] = None,
    ) -> ft.Container:
        """
        创建下拉框
        
        参数：
        - section: 配置节
        - control_id: 控件ID
        - enabled: 是否启用
        - on_change: 值变更回调
        - theme_colors: 主题颜色
        
        注意：宽度、高度从配置服务获取，调用者不应传递
        """
        width = Dropdown.get_width()
        height = Dropdown.get_height()
        
        if theme_colors is None:
            theme_colors = {
                "text_primary": "#FFFFFF",
                "text_secondary": "#C5C5C5",
                "text_disabled": "#656565",
                "bg_primary": "#202020",
                "bg_secondary": "#282828",
                "border": "#3D3D3D",
                "accent": "#0078D4"
            }
        
        options = self._get_options(section, control_id)
        current_value = self._get_current_value(section, control_id, options)
        
        current_selected = [current_value.copy()]
        enabled_state = [enabled]
        
        text_color = theme_colors.get("text_primary") if enabled else theme_colors.get("text_disabled")
        icon_color = theme_colors.get("text_secondary") if enabled else theme_colors.get("text_disabled")
        bg_color = theme_colors.get("bg_secondary") if enabled else theme_colors.get("bg_primary")
        border_color = theme_colors.get("border") if enabled else "transparent"
        
        selected_text = ft.Text(
            current_selected[0].get("text", ""),
            size=14,
            color=text_color,
            overflow=ft.TextOverflow.ELLIPSIS,
        )
        
        dropdown_icon = ft.Icon(
            ft.Icons.KEYBOARD_ARROW_DOWN,
            size=18,
            color=icon_color,
        )
        
        def create_menu_items():
            """创建菜单项列表"""
            menu_items = []
            for option in options:
                def create_callback(opt=option):
                    def callback(e):
                        current_selected[0] = opt.copy()
                        selected_text.value = opt.get("text", "")
                        
                        self._save_value(section, control_id, opt)
                        
                        if on_change:
                            on_change(section, control_id, opt)
                        
                        if self._page:
                            try:
                                container.update()
                            except:
                                pass
                    return callback
                
                menu_item = ft.PopupMenuItem(
                    content=option.get("text", ""),
                    on_click=create_callback(),
                )
                menu_items.append(menu_item)
            return menu_items
        
        popup_menu_button = ft.PopupMenuButton(
            content=ft.Container(
                content=ft.Row(
                    [selected_text, dropdown_icon],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                width=width,
                height=height,
                border_radius=6,
                bgcolor=bg_color,
                border=ft.border.all(1, border_color),
                padding=ft.padding.symmetric(horizontal=12, vertical=0),
            ),
            items=create_menu_items(),
            menu_padding=0,
            enable_feedback=True,
            tooltip="",
        )
        
        container = ft.Container(
            content=popup_menu_button,
            width=width,
        )
        
        def handle_hover(e):
            if not enabled_state[0]:
                return
            button_content = popup_menu_button.content
            if e.data == "true":
                button_content.border = ft.border.all(1, theme_colors.get("accent"))
            else:
                button_content.border = ft.border.all(1, theme_colors.get("border"))
            try:
                if self._page:
                    container.update()
            except:
                pass
        
        popup_menu_button.content.on_hover = handle_hover
        
        def get_value() -> Dict[str, str]:
            return current_selected[0].copy()
        
        def set_value(new_value: Dict[str, str]):
            if isinstance(new_value, dict):
                current_selected[0] = new_value.copy()
                selected_text.value = new_value.get("text", "")
                if self._page:
                    try:
                        container.update()
                    except:
                        pass
        
        def set_enabled(state: bool):
            enabled_state[0] = state
            text_col = theme_colors.get("text_primary") if state else theme_colors.get("text_disabled")
            icon_col = theme_colors.get("text_secondary") if state else theme_colors.get("text_disabled")
            bg_col = theme_colors.get("bg_secondary") if state else theme_colors.get("bg_primary")
            border_col = theme_colors.get("border") if state else "transparent"
            
            selected_text.color = text_col
            dropdown_icon.color = icon_col
            popup_menu_button.content.bgcolor = bg_col
            popup_menu_button.content.border = ft.border.all(1, border_col)
            
            try:
                if self._page:
                    container.update()
            except:
                pass
        
        container.get_value = get_value
        container.set_value = set_value
        container.set_enabled = set_enabled
        
        key = f"{section}.{control_id}" if section and control_id else f"dropdown_{len(self._dropdowns)}"
        self._dropdowns[key] = container
        
        return container
    
    def _get_options(self, section: str, control_id: str) -> List[Dict[str, str]]:
        """从配置服务获取选项列表"""
        if self._config_service is None:
            return [{"text": "选项A", "value": "a"}, {"text": "选项B", "value": "b"}]
        return self._config_service.get_options(section, control_id)
    
    def _get_current_value(self, section: str, control_id: str, options: List[Dict]) -> Dict[str, str]:
        """
        从配置服务获取当前值
        
        加载逻辑：
        1. 有用户配置值 → 显示用户配置的值
        2. 无用户配置值（APK第一次安装或文件损坏）→ 显示"请选定数据..."
        
        注意：保留原有懒加载功能（PopupMenuButton行为不变）
        """
        if self._config_service:
            value = self._config_service.get_text_value(section, control_id)
            if value and value.get("text") and value.get("text") != "":
                return value
        
        return {"text": "请选定数据...", "value": ""}
    
    def _save_value(self, section: str, control_id: str, value: Dict[str, str]):
        """保存值到配置"""
        if self._config_service:
            self._config_service.set_value(section, control_id, value)
    
    def get_default_value(self, section: str, control_id: str) -> str:
        """
        公开接口：获取默认值
        
        用途：
        - "重置为默认值"功能
        - "一键填充默认值"功能
        - 新用户快速配置参考
        """
        if self._config_service:
            return self._config_service.get_control_default(section, control_id)
        return ""
    
    def reset_to_default(self, section: str, control_id: str) -> bool:
        """
        公开接口：重置为默认值
        
        返回：
        - True: 重置成功
        - False: 没有默认值或重置失败
        """
        default_value = self.get_default_value(section, control_id)
        if default_value:
            options = self._get_options(section, control_id)
            for opt in options:
                if opt.get("value") == default_value or opt.get("text") == default_value:
                    self._save_value(section, control_id, opt)
                    return True
        return False
    
    def destroy_all(self):
        """销毁所有下拉框菜单"""
        self._dropdowns.clear()

# *** 标准测试格式: 仅调用被测模块,AI不得添加数据 ***
if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
    
    from 前端.V2.数据层.仓库.配置仓库 import ConfigRepository
    from 前端.V2.业务层.服务.配置服务 import ConfigService
    
    def main(page: ft.Page):
        page.title = "下拉框测试"
        
        print("=" * 50)
        print("测试1: 使用真实配置服务")
        print("=" * 50)
        
        repository = ConfigRepository()
        config_service = ConfigService(repository)
        
        Dropdown.set_config_service(config_service)
        
        print(f"从配置服务获取下拉框宽度: {Dropdown.get_width()}")
        print(f"从配置服务获取下拉框高度: {Dropdown.get_height()}")
        print(f"配置文件中的值应为: 宽度=120, 高度=30")
        
        print("\n" + "=" * 50)
        print("测试2: 验证选项列表获取")
        print("=" * 50)
        
        dropdown = Dropdown(page, config_service)
        
        options = dropdown._get_options("建筑设置.主帅主城", "城市等级")
        print(f"获取选项列表(建筑设置.主帅主城.城市等级): {len(options)}个选项")
        if options:
            print(f"第一个选项: {options[0]}")
        
        print("\n" + "=" * 50)
        print("测试3: 创建下拉框并验证")
        print("=" * 50)
        
        theme_colors = config_service.get_theme_colors()
        print(f"从配置服务获取主题颜色: {theme_colors}")
        
        container = dropdown.create(
            section="建筑设置.主帅主城",
            control_id="城市等级",
            enabled=True,
            theme_colors=theme_colors,
        )
        
        print(f"下拉框容器宽度: {container.width}")
        print(f"验证: 宽度应等于配置服务返回值({Dropdown.get_width()})")
        
        page.add(ft.Column([
            ft.Text("下拉框测试", size=20, weight=ft.FontWeight.BOLD),
            container,
        ]))
    
    ft.app(target=main)
