# -*- coding: utf-8 -*-

"""
模块名称：下拉框.py
模块功能：下拉框组件，使用PopupMenuButton实现，支持text/value格式和懒加载

实现步骤：
- 创建时自动从配置服务加载选项列表
- 创建时自动从配置服务获取当前值
- 支持text/value格式
- 支持懒加载（option_loader）
- 选择后自动保存到配置
- 支持销毁管理减少内存占用
- Win11风格深色主题

职责：
- 从配置服务获取选项列表
- 从配置服务获取当前值
- 从用户偏好.json获取UI配置
- 自动保存到配置

不负责：
- 布局
- 开关状态

设计原则（符合V2版本模块化设计补充共识）：
- 用户偏好.json是UI配置唯一来源
- 如果用户偏好.json缺少配置，抛出错误
- 不使用DEFAULT_XXX掩盖问题
"""

import flet as ft
from typing import List, Dict, Callable, Any, Optional

# ============================================
# 数据和文件接口（前置，方便查看和修改）
# ============================================

# *** 用户指定变量: 变量值必须生效,AI不得更改数据 ***
USER_WIDTH = 120      # 下拉框宽度（None表示从用户偏好.json获取）
USER_HEIGHT = 30     # 下拉框高度（None表示从用户偏好.json获取）
# *********************************

# 下拉框无默认值配置，所有UI配置从用户偏好.json获取
# 如果用户偏好.json缺少配置，抛出错误而非掩盖

# ============================================
# 公开接口
# ============================================

class Dropdown:
    """
    下拉框组件 - 使用PopupMenuButton实现
    
    职责：
    - 从配置服务获取选项列表
    - 从配置服务获取当前值
    - 从用户偏好.json获取UI配置
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
    def _check_config_service():
        """检查配置服务是否已设置"""
        if Dropdown._config_service is None:
            raise RuntimeError(
                "Dropdown模块未设置config_service，"
                "请先调用 Dropdown.set_config_service(config_service)"
            )
    
    @staticmethod
    def get_width() -> int:
        """获取下拉框宽度（从用户偏好.json获取）"""
        Dropdown._check_config_service()
        width = Dropdown._config_service.get_ui_config("下拉框", "宽度")
        if width is None:
            raise RuntimeError("用户偏好.json缺少配置: 下拉框.宽度")
        return width
    
    @staticmethod
    def get_height() -> int:
        """获取下拉框高度（从用户偏好.json获取）"""
        Dropdown._check_config_service()
        height = Dropdown._config_service.get_ui_config("下拉框", "高度")
        if height is None:
            raise RuntimeError("用户偏好.json缺少配置: 下拉框.高度")
        return height
    
    @staticmethod
    def get_border_radius() -> int:
        """获取下拉框圆角（从用户偏好.json获取）"""
        Dropdown._check_config_service()
        radius = Dropdown._config_service.get_ui_config("下拉框", "圆角")
        if radius is None:
            radius = Dropdown._config_service.get_ui_config("圆角", "小")
        if radius is None:
            raise RuntimeError("用户偏好.json缺少配置: 下拉框.圆角")
        return radius
    
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
        width: int = None,
        height: int = None,
        option_loader: Callable[[], List[Dict[str, str]]] = None,
    ) -> ft.Container:
        """
        创建下拉框
        
        参数：
        - section: 配置节
        - control_id: 控件ID
        - enabled: 是否启用
        - on_change: 值变更回调
        - theme_colors: 主题颜色
        - width: 宽度（可选，优先级：USER_WIDTH > 参数 > 用户偏好.json）
        - height: 高度（可选，优先级：USER_HEIGHT > 参数 > 用户偏好.json）
        - option_loader: 懒加载函数，点击时才加载选项
        """
        width = width if width is not None else (USER_WIDTH if USER_WIDTH is not None else Dropdown.get_width())
        height = height if height is not None else (USER_HEIGHT if USER_HEIGHT is not None else Dropdown.get_height())
        border_radius = Dropdown.get_border_radius()
        
        if theme_colors is None:
            theme_colors = self._get_theme_colors()
        
        options = self._get_options(section, control_id)
        current_value = self._get_current_value(section, control_id, options)
        
        container = self._build_dropdown(
            options, current_value, enabled,
            width, height, border_radius, theme_colors,
            section, control_id, on_change,
            option_loader
        )
        
        key = f"{section}.{control_id}" if section and control_id else f"dropdown_{len(self._dropdowns)}"
        self._dropdowns[key] = container
        
        return container
    
    def _get_theme_colors(self) -> Dict[str, str]:
        """获取主题颜色"""
        if self._config_service is None:
            raise RuntimeError("Dropdown模块未设置config_service")
        return self._config_service.get_theme_colors()
    
    def _get_options(self, section: str, control_id: str) -> List[Dict[str, str]]:
        """从配置服务获取选项列表"""
        if self._config_service is None:
            return [{"text": "选项A", "value": "a"}, {"text": "选项B", "value": "b"}]
        return self._config_service.get_options(section, control_id)
    
    def _get_current_value(self, section: str, control_id: str, options: List[Dict]) -> Dict[str, str]:
        """从配置服务获取当前值"""
        if self._config_service:
            value = self._config_service.get_text_value(section, control_id)
            if value and value.get("text") and value.get("text") != "":
                return value
        
        return {"text": "请选定数据...", "value": ""}
    
    def _save_value(self, section: str, control_id: str, value: Dict[str, str]):
        """保存值到配置"""
        if self._config_service:
            self._config_service.set_value(section, control_id, value)
    
    def _build_dropdown(
        self,
        options: List[Dict],
        current_value: Dict,
        enabled: bool,
        width: int,
        height: int,
        border_radius: int,
        theme_colors: Dict,
        section: str,
        control_id: str,
        on_change: Callable,
        option_loader: Callable,
    ) -> ft.Container:
        """构建下拉框"""
        
        text_color = theme_colors.get("text_primary", "#FFFFFF")
        text_secondary = theme_colors.get("text_secondary", "#B0B0B0")
        disabled_color = theme_colors.get("text_disabled", "#666666")
        bg_primary = theme_colors.get("bg_primary", "#1A1A2E")
        bg_card = theme_colors.get("bg_card", "#2D2D4A")
        border_color = theme_colors.get("border", "#3D3D5C")
        accent_color = theme_colors.get("accent", "#0078D4")
        
        state = {
            "current_value": current_value,
            "enabled": enabled,
            "options": options or [],
            "option_loader": option_loader,
            "has_loaded": option_loader is None,
        }
        
        display_text = ft.Text(
            value=current_value.get("text", ""),
            size=14,
            color=text_color if enabled else disabled_color,
            overflow=ft.TextOverflow.ELLIPSIS,
        )
        
        dropdown_icon = ft.Icon(
            ft.Icons.ARROW_DROP_DOWN,
            size=20,
            color=text_secondary if enabled else disabled_color,
        )
        
        button_container = ft.Container(
            content=ft.Row(
                [display_text, dropdown_icon],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8,
            ),
            width=width,
            height=height,
            bgcolor=bg_card,
            border=ft.Border.all(1, border_color),
            border_radius=border_radius,
            padding=ft.Padding.symmetric(horizontal=12, vertical=0),
        )
        
        def create_option_callback(option: Dict):
            def callback(e):
                state["current_value"] = option
                display_text.value = option.get("text", "")
                display_text.color = text_color
                self._save_value(section, control_id, option)
                if on_change:
                    on_change(section, control_id, option)
                if button_container.page:
                    button_container.page.update()
            return callback
        
        def load_options() -> List[Dict]:
            if not state["has_loaded"] and state["option_loader"]:
                print(f"[懒加载] 执行option_loader函数")
                state["options"] = state["option_loader"]()
                state["has_loaded"] = True
                print(f"[懒加载] 加载了 {len(state['options'])} 个选项")
            return state["options"]
        
        def create_menu_items() -> List[ft.PopupMenuItem]:
            opts = load_options()
            menu_items = []
            
            for opt in opts:
                menu_content = ft.Container(
                    content=ft.Text(opt.get("text", ""), size=14, color=text_color),
                    padding=ft.Padding.symmetric(horizontal=12, vertical=8),
                    bgcolor=bg_card,
                    border_radius=4,
                )
                
                menu_item = ft.PopupMenuItem(
                    content=menu_content,
                    on_click=create_option_callback(opt),
                )
                menu_items.append(menu_item)
            
            if not menu_items:
                menu_content = ft.Container(
                    content=ft.Text("无可用选项", size=14, color=disabled_color, italic=True),
                    padding=ft.Padding.symmetric(horizontal=12, vertical=8),
                )
                menu_item = ft.PopupMenuItem(
                    content=menu_content,
                    disabled=True,
                )
                menu_items.append(menu_item)
            
            return menu_items
        
        initial_menu_items = create_menu_items()
        
        popup_menu_button = ft.PopupMenuButton(
            content=button_container,
            items=initial_menu_items,
            menu_padding=0,
            enable_feedback=True,
            tooltip="",
            disabled=not enabled,
            bgcolor=bg_card,
        )
        
        container = ft.Container(
            content=popup_menu_button,
            width=width,
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
                
                if container.page:
                    container.page.update()
        
        button_container.on_hover = handle_hover
        
        def get_value() -> Dict[str, str]:
            return state["current_value"]
        
        def set_value(value: Dict[str, str]):
            opts = load_options()
            value_text = value.get("text", "")
            for opt in opts:
                if opt.get("text") == value_text:
                    state["current_value"] = opt
                    display_text.value = opt.get("text", "")
                    if container.page:
                        container.page.update()
                    break
        
        def set_enabled(is_enabled: bool):
            state["enabled"] = is_enabled
            popup_menu_button.disabled = not is_enabled
            
            text_col = text_color if is_enabled else disabled_color
            icon_col = text_secondary if is_enabled else disabled_color
            border_col = border_color if is_enabled else "transparent"
            
            display_text.color = text_col
            dropdown_icon.color = icon_col
            button_container.border = ft.Border.all(1, border_col)
            
            try:
                if container.page:
                    container.page.update()
            except RuntimeError:
                pass
        
        def set_options(new_options: List[Dict]):
            state["options"] = new_options
            popup_menu_button.items = create_menu_items()
            if container.page:
                container.page.update()
        
        container.get_value = get_value
        container.set_value = set_value
        container.set_enabled = set_enabled
        container.set_options = set_options
        
        return container
    
    def get_value(self, section: str, control_id: str) -> Dict[str, str]:
        """获取下拉框当前值"""
        key = f"{section}.{control_id}"
        if key in self._dropdowns:
            container = self._dropdowns[key]
            if hasattr(container, 'get_value'):
                return container.get_value()
        return {"text": "", "value": ""}
    
    def destroy_all(self):
        """销毁所有下拉框"""
        self._dropdowns.clear()

# *** 标准测试格式: 仅调用被测模块,AI不得添加数据 ***
if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
    
    from 前端.V2.业务层.服务.配置服务 import ConfigService
    
    def main(page: ft.Page):
        page.title = "下拉框测试"
        page.bgcolor = "#1A1A2E"
        
        config_service = ConfigService()
        Dropdown.set_config_service(config_service)
        
        print(f"下拉框宽度: {Dropdown.get_width()}")
        print(f"下拉框高度: {Dropdown.get_height()}")
        
        dropdown = Dropdown(page, config_service)
        
        def on_change(section, control_id, value):
            print(f"选择变更: section={section}, control_id={control_id}, value={value}")
        
        container = dropdown.create(
            section="建筑设置.主帅主城",
            control_id="城市等级",
            enabled=True,
            on_change=on_change,
        )
        
        page.add(ft.Column([
            ft.Text("下拉框测试", size=20, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
            ft.Container(height=20),
            container,
        ], alignment=ft.MainAxisAlignment.CENTER))
    
    ft.run(main)
