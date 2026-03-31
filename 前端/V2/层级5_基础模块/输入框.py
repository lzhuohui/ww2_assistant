# -*- coding: utf-8 -*-

"""
模块名称：输入框.py
模块功能：输入框组件，支持文本输入和配置保存

实现步骤：
- 创建时自动从配置服务加载当前值
- 支持密码模式
- 支持值变更回调
- 支持最大长度限制
- 自动保存到配置

职责：
- 从配置服务获取当前值
- 从用户偏好.json获取UI配置
- 文本输入
- 自动保存到配置

不负责：
- 布局
- 销毁（不需要销毁）

设计原则（符合V2版本模块化设计补充共识）：
- 用户偏好.json是UI配置唯一来源
- 如果用户偏好.json缺少配置，抛出错误
- 不使用DEFAULT_XXX掩盖问题
"""

import flet as ft
from typing import Callable, Dict, Optional, Any

# ============================================
# 数据和文件接口（前置，方便查看和修改）
# ============================================

# *** 用户指定变量: 变量值必须生效,AI不得更改数据 ***
USER_WIDTH = 150      # 输入框宽度（None表示从用户偏好.json获取）
USER_HEIGHT = 30     # 输入框高度（None表示从用户偏好.json获取）
# *********************************

# 输入框无默认值配置，所有UI配置从用户偏好.json获取
# 如果用户偏好.json缺少配置，抛出错误而非掩盖

# ============================================
# 公开接口
# ============================================

class InputBox:
    """
    输入框组件
    
    职责：
    - 从配置服务获取当前值
    - 从用户偏好.json获取UI配置
    - 文本输入
    - 自动保存到配置
    
    不负责：
    - 布局
    - 销毁（不需要销毁）
    """
    
    _config_service = None
    
    @classmethod
    def set_config_service(cls, config_service):
        """设置配置服务实例"""
        cls._config_service = config_service
    
    @staticmethod
    def _check_config_service():
        """检查配置服务是否已设置"""
        if InputBox._config_service is None:
            raise RuntimeError(
                "InputBox模块未设置config_service，"
                "请先调用 InputBox.set_config_service(config_service)"
            )
    
    @staticmethod
    def get_width() -> int:
        """获取输入框宽度（从用户偏好.json获取）"""
        InputBox._check_config_service()
        width = InputBox._config_service.get_ui_config("输入框", "宽度")
        if width is None:
            raise RuntimeError("用户偏好.json缺少配置: 输入框.宽度")
        return width
    
    @staticmethod
    def get_height() -> int:
        """获取输入框高度（从用户偏好.json获取）"""
        InputBox._check_config_service()
        height = InputBox._config_service.get_ui_config("输入框", "高度")
        if height is None:
            raise RuntimeError("用户偏好.json缺少配置: 输入框.高度")
        return height
    
    @staticmethod
    def get_border_radius() -> int:
        """获取输入框圆角（从用户偏好.json获取）"""
        InputBox._check_config_service()
        radius = InputBox._config_service.get_ui_config("输入框", "圆角")
        if radius is None:
            radius = InputBox._config_service.get_ui_config("圆角", "小")
        if radius is None:
            raise RuntimeError("用户偏好.json缺少配置: 输入框.圆角")
        return radius
    
    def __init__(self, page: ft.Page = None, config_service=None):
        self._page = page
        self._config_service = config_service or InputBox._config_service
        self._inputs: Dict[str, ft.TextField] = {}
    
    def create(
        self,
        section: str = "",
        control_id: str = "",
        enabled: bool = True,
        max_length: int = None,
        on_change: Callable[[str, str, str], None] = None,
        theme_colors: Dict[str, str] = None,
        hint_text: str = None,
        password_mode: bool = False,
        width: int = None,
        height: int = None,
    ) -> ft.TextField:
        """
        创建输入框
        
        参数：
        - section: 配置节
        - control_id: 控件ID
        - enabled: 是否启用
        - max_length: 最大长度
        - on_change: 值变更回调
        - theme_colors: 主题颜色
        - hint_text: 提示文本
        - password_mode: 密码模式
        - width: 宽度（可选，优先级：USER_WIDTH > 参数 > 用户偏好.json）
        - height: 高度（可选，优先级：USER_HEIGHT > 参数 > 用户偏好.json）
        """
        width = USER_WIDTH if USER_WIDTH is not None else (width if width is not None else InputBox.get_width())
        height = USER_HEIGHT if USER_HEIGHT is not None else (height if height is not None else InputBox.get_height())
        border_radius = InputBox.get_border_radius()
        
        if theme_colors is None:
            theme_colors = self._get_theme_colors()
        
        current_value = self._get_current_value(section, control_id)
        
        if hint_text is None:
            hint_text = self._get_hint(section, control_id)
        
        if password_mode is None:
            password_mode = self._get_password_mode(section, control_id)
        
        text_field = self._build_text_field(
            current_value, enabled, width, height, border_radius,
            theme_colors, hint_text, password_mode,
            max_length, section, control_id, on_change
        )
        
        key = f"{section}.{control_id}" if section and control_id else f"input_{len(self._inputs)}"
        self._inputs[key] = text_field
        
        return text_field
    
    def _get_theme_colors(self) -> Dict[str, str]:
        """获取主题颜色"""
        if self._config_service is None:
            raise RuntimeError("InputBox模块未设置config_service")
        return self._config_service.get_theme_colors()
    
    def _get_current_value(self, section: str, control_id: str) -> str:
        """从配置服务获取当前值"""
        if self._config_service:
            return self._config_service.get_value(section, control_id, "")
        return ""
    
    def _get_hint(self, section: str, control_id: str) -> str:
        """从配置服务获取提示文本"""
        if self._config_service:
            config = self._config_service.get_control_config(section, control_id)
            return config.get("hint", "")
        return ""
    
    def _get_password_mode(self, section: str, control_id: str) -> bool:
        """从配置服务获取密码模式"""
        if self._config_service:
            config = self._config_service.get_control_config(section, control_id)
            return config.get("password", False)
        return False
    
    def _build_text_field(
        self,
        current_value: str,
        enabled: bool,
        width: int,
        height: int,
        border_radius: int,
        theme_colors: Dict,
        hint_text: str,
        password_mode: bool,
        max_length: int,
        section: str,
        control_id: str,
        on_change: Callable,
    ) -> ft.TextField:
        """构建文本输入框"""
        
        text_color = theme_colors.get("text_primary", "#FFFFFF")
        disabled_color = theme_colors.get("text_disabled", "#656565")
        bg_card = theme_colors.get("bg_card", "#2D2D4A")
        border_color = theme_colors.get("border", "#3D3D3D")
        
        def handle_change(e):
            self._save_value(section, control_id, e.control.value)
            if on_change:
                on_change(section, control_id, e.control.value)
        
        text_field = ft.TextField(
            value=current_value,
            width=width,
            height=height,
            text_size=12,
            color=text_color if enabled else disabled_color,
            bgcolor=bg_card,
            border_color=border_color,
            border_radius=border_radius,
            hint_text=hint_text,
            hint_style=ft.TextStyle(color=disabled_color),
            password=password_mode,
            can_reveal_password=password_mode,
            max_length=max_length,
            on_change=handle_change,
            disabled=not enabled,
            content_padding=ft.Padding.symmetric(horizontal=8, vertical=4),
        )
        
        return text_field
    
    def _save_value(self, section: str, control_id: str, value: str):
        """保存值到配置"""
        if self._config_service:
            self._config_service.set_value(section, control_id, value)
    
    def get_value(self, section: str, control_id: str) -> str:
        """获取输入框当前值"""
        key = f"{section}.{control_id}"
        if key in self._inputs:
            return self._inputs[key].value or ""
        return ""

# *** 标准测试格式: 仅调用被测模块,AI不得添加数据 ***
if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
    
    from 前端.V2.业务层.服务.配置服务 import ConfigService
    
    def main(page: ft.Page):
        page.title = "输入框测试"
        
        config_service = ConfigService()
        InputBox.set_config_service(config_service)
        
        print(f"输入框宽度: {InputBox.get_width()}")
        print(f"输入框高度: {InputBox.get_height()}")
        
        input_box = InputBox(page, config_service)
        
        text_field = input_box.create(
            section="账号设置.账号01",
            control_id="名称",
            enabled=True,
        )
        
        page.add(ft.Column([
            ft.Text("输入框测试", size=20, weight=ft.FontWeight.BOLD),
            text_field,
        ]))
    
    ft.run(main)
