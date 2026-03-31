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
- 从配置服务获取UI配置
- 文本输入
- 自动保存到配置

不负责：
- 布局
- 销毁（不需要销毁）

设计原则（符合V2版本模块化设计补充共识）：
- 从配置服务获取UI配置（宽度、高度）
- 定义DEFAULT_XXX作为fallback
"""

import flet as ft
from typing import Callable, Dict, Optional, Any

# ============================================
# 默认配置（fallback，用于模块独立测试）
# ============================================

DEFAULT_WIDTH = 120
DEFAULT_HEIGHT = 30

# ============================================
# 公开接口
# ============================================

class InputBox:
    """
    输入框组件
    
    职责：
    - 从配置服务获取当前值
    - 从配置服务获取UI配置
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
    def get_width() -> int:
        """获取输入框宽度（从配置服务获取，fallback到默认值）"""
        if InputBox._config_service:
            return InputBox._config_service.get_ui_config("输入框", "宽度", DEFAULT_WIDTH)
        return DEFAULT_WIDTH
    
    @staticmethod
    def get_height() -> int:
        """获取输入框高度（从配置服务获取，fallback到默认值）"""
        if InputBox._config_service:
            return InputBox._config_service.get_ui_config("输入框", "高度", DEFAULT_HEIGHT)
        return DEFAULT_HEIGHT
    
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
    ) -> ft.TextField:
        """
        创建输入框
        
        参数：
        - section: 配置节
        - control_id: 控件ID
        - enabled: 是否启用
        - max_length: 最大长度限制
        - on_change: 值变更回调
        - theme_colors: 主题颜色
        
        注意：
        - 宽度、高度从配置服务获取，调用者不应传递
        - hint_text、password从配置服务获取，调用者不应传递
        """
        width = InputBox.get_width()
        height = InputBox.get_height()
        
        if theme_colors is None:
            theme_colors = self._get_theme_colors()
        
        current_value = self._get_current_value(section, control_id)
        hint_text = self._get_hint(section, control_id)
        password_mode = self._get_password(section, control_id)
        
        def handle_change(e):
            new_value = e.control.value
            if max_length and new_value and len(new_value) > max_length:
                e.control.value = new_value[:max_length]
                new_value = e.control.value
            
            self._save_value(section, control_id, new_value)
            
            if on_change and section and control_id:
                on_change(section, control_id, new_value)
        
        text_field = ft.TextField(
            value=current_value,
            hint_text=hint_text,
            width=width,
            height=height,
            disabled=not enabled,
            password=password_mode,
            can_reveal_password=password_mode,
            on_change=handle_change,
            border_color=theme_colors.get("border"),
            focused_border_color=theme_colors.get("accent"),
            text_style=ft.TextStyle(color=theme_colors.get("text_primary")),
            hint_style=ft.TextStyle(color=theme_colors.get("text_disabled")),
            text_align=ft.TextAlign.LEFT,
            content_padding=ft.padding.symmetric(horizontal=10, vertical=5),
        )
        
        key = f"{section}.{control_id}" if section and control_id else f"input_{len(self._inputs)}"
        self._inputs[key] = text_field
        
        return text_field
    
    def _get_current_value(self, section: str, control_id: str) -> str:
        """从配置服务获取当前值"""
        if self._config_service:
            return self._config_service.get_value(section, control_id, "")
        return ""
    
    def _save_value(self, section: str, control_id: str, value: str):
        """保存值到配置"""
        if self._config_service:
            self._config_service.set_value(section, control_id, value)
    
    def _get_hint(self, section: str, control_id: str) -> str:
        """从配置服务获取提示文本"""
        if self._config_service:
            config = self._config_service.get_control_config(section, control_id)
            return config.get("hint", "")
        return ""
    
    def _get_password(self, section: str, control_id: str) -> bool:
        """从配置服务获取密码模式"""
        if self._config_service:
            config = self._config_service.get_control_config(section, control_id)
            return config.get("password", False)
        return False
    
    def _get_theme_colors(self) -> Dict[str, str]:
        """获取主题颜色"""
        if self._config_service is None:
            raise RuntimeError("InputBox模块未设置config_service")
        return self._config_service.get_theme_colors()
    
    def get_value(self, section: str, control_id: str) -> str:
        """获取输入框当前值"""
        key = f"{section}.{control_id}"
        if key in self._inputs:
            return self._inputs[key].value or ""
        return ""
    
    def set_value(self, section: str, control_id: str, value: str) -> None:
        """设置输入框值"""
        key = f"{section}.{control_id}"
        if key in self._inputs:
            self._inputs[key].value = value
            if self._page:
                try:
                    self._inputs[key].update()
                except:
                    pass
    
    def set_enabled(self, section: str, control_id: str, enabled: bool) -> None:
        """设置启用状态"""
        key = f"{section}.{control_id}"
        if key in self._inputs:
            self._inputs[key].disabled = not enabled
            if self._page:
                try:
                    self._inputs[key].update()
                except:
                    pass

# *** 标准测试格式: 仅调用被测模块,AI不得添加数据 ***
if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
    
    from 前端.V2.业务层.服务.配置服务 import ConfigService
    
    def main(page: ft.Page):
        page.title = "输入框测试"
        
        print("=" * 50)
        print("测试: 使用真实配置服务")
        print("=" * 50)
        
        config_service = ConfigService()
        InputBox.set_config_service(config_service)
        
        print(f"从配置服务获取输入框宽度: {InputBox.get_width()}")
        print(f"从配置服务获取输入框高度: {InputBox.get_height()}")
        print(f"配置文件中的值应为: 宽度=120, 高度=30")
        
        input_box = InputBox(page, config_service)
        
        text_field = input_box.create(
            section="账号设置.账号01",
            control_id="名称",
            enabled=True,
        )
        
        print(f"输入框宽度: {text_field.width}")
        print(f"验证: 宽度应等于配置服务返回值({InputBox.get_width()})")
        
        page.add(ft.Column([
            ft.Text("输入框测试", size=20, weight=ft.FontWeight.BOLD),
            text_field,
        ]))
    
    ft.app(target=main)
