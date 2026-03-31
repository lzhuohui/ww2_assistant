# -*- coding: utf-8 -*-

"""
模块名称：卡片开关.py
模块功能：卡片开关组件，左侧图标+标题+开关

实现步骤：
- 创建时自动从配置服务加载开关状态
- 创建左侧图标
- 创建标题
- 创建开关状态逻辑
- 创建分隔线
- 自动保存开关状态到配置

职责：
- 从配置服务获取开关状态（模块自己获取）
- 开关控件
- 左侧布局
- 开关状态逻辑
- 自动保存开关状态

不负责：
- 控件创建
- 控件布局

尺寸传递：
- 从卡片容器（层级5）继承基础尺寸
- 本模块定义特殊尺寸（图标、标题等）
"""

import flet as ft
from typing import Callable, Dict, Optional

from 前端.V2.层级5_基础模块.卡片容器 import CardContainer

# ============================================
# 数据和文件接口（前置，方便查看和修改）
# ============================================

DEFAULT_ICON_SIZE = 22
DEFAULT_TITLE_SIZE = 14
DEFAULT_SUBTITLE_SIZE = 10
DEFAULT_LEFT_WIDTH = 76

# ============================================
# 公开接口
# ============================================

class CardSwitch:
    """
    卡片开关（层级4：复合模块）
    
    职责：
    - 从配置服务获取开关状态（模块自己获取）
    - 开关控件
    - 左侧布局
    - 开关状态逻辑
    - 自动保存开关状态
    
    不负责：
    - 控件创建
    - 控件布局
    
    尺寸传递：
    - 从卡片容器（层级5）继承基础尺寸
    - 本模块定义特殊尺寸（图标、标题等）
    """
    
    @staticmethod
    def get_height():
        """获取卡片基础高度（从卡片容器继承，供单行控件卡片使用）"""
        return CardContainer.get_height()
    
    @staticmethod
    def calculate_height(control_rows: int = 1) -> int:
        """计算卡片高度（委托给卡片容器）"""
        return CardContainer.calculate_height(control_rows)
    
    @staticmethod
    def get_padding():
        """获取内边距（从卡片容器继承）"""
        return CardContainer.get_padding()
    
    @staticmethod
    def get_left_width():
        """获取左侧宽度（本模块定义）"""
        return DEFAULT_LEFT_WIDTH
    
    @staticmethod
    def get_icon_size():
        """获取图标尺寸（本模块定义）"""
        return DEFAULT_ICON_SIZE
    
    @staticmethod
    def get_title_size():
        """获取标题尺寸（本模块定义）"""
        return DEFAULT_TITLE_SIZE
    
    @staticmethod
    def get_subtitle_size():
        """获取副标题尺寸（本模块定义）"""
        return DEFAULT_SUBTITLE_SIZE
    
    def __init__(self, page: ft.Page = None, config_service=None):
        self._page = page
        self._config_service = config_service
        self._switches: Dict[str, ft.Container] = {}
    
    def create(
        self,
        section: str = "",
        title: str = "卡片标题",
        icon: str = "HOME",
        subtitle: str = "",
        on_toggle: Callable[[bool], None] = None,
        theme_colors: Dict[str, str] = None,
    ) -> ft.Container:
        """
        创建卡片开关（模块自己从配置服务获取开关状态）
        
        参数：
        - section: 配置节
        - title: 卡片标题
        - icon: 图标名称
        - subtitle: 卡片副标题（说明文字）
        - on_toggle: 开关切换回调
        - theme_colors: 主题颜色
        
        注意：开关状态由模块自己从config_service获取
        """
        if theme_colors is None:
            theme_colors = {
                "text_primary": "#000000",
                "text_secondary": "#666666",
                "text_disabled": "#999999",
                "accent": "#0078D4",
            }
        
        enabled = self._get_enabled(section)
        switch_state = [enabled]
        
        icon_control = ft.Icon(
            getattr(ft.Icons, icon.upper(), ft.Icons.HOME),
            size=DEFAULT_ICON_SIZE,
            color=theme_colors.get("accent"),
            opacity=1.0 if enabled else 0.4,
        )
        
        title_text = ft.Text(
            title,
            size=DEFAULT_TITLE_SIZE,
            weight=ft.FontWeight.BOLD,
            color=theme_colors.get("text_primary"),
            opacity=1.0 if enabled else 0.4,
        )
        
        subtitle_text = ft.Text(
            subtitle,
            size=DEFAULT_SUBTITLE_SIZE,
            color=theme_colors.get("text_secondary"),
            opacity=0.8 if enabled else 0.4,
            max_lines=2,
            overflow=ft.TextOverflow.ELLIPSIS,
        ) if subtitle else None
        
        left_content = ft.Column([
            icon_control,
            ft.Container(height=2),
            title_text,
        ], spacing=0, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        divider = ft.Container(
            width=2,
            bgcolor=theme_colors.get("accent"),
            height=70 - CardContainer.get_padding(),
        )
        
        right_content = ft.Column([
            ft.Container(expand=True),
            subtitle_text if subtitle_text else ft.Container(),
            ft.Container(height=4),
        ], spacing=0, alignment=ft.MainAxisAlignment.END) if subtitle_text else None
        
        def handle_click(e):
            new_state = not switch_state[0]
            switch_state[0] = new_state
            icon_control.opacity = 1.0 if new_state else 0.4
            title_text.opacity = 1.0 if new_state else 0.4
            if subtitle_text:
                subtitle_text.opacity = 0.8 if new_state else 0.4
            
            self._save_enabled(section, new_state)
            
            if on_toggle:
                on_toggle(new_state)
            
            if self._page:
                try:
                    container.update()
                except:
                    pass
        
        row_content = [
            ft.Container(
                content=left_content,
                width=DEFAULT_LEFT_WIDTH - 2,
                padding=ft.Padding(CardContainer.get_padding(), 0, CardContainer.get_padding(), 0),
            ),
            divider,
        ]
        
        if right_content:
            row_content.append(ft.Container(
                content=right_content,
                expand=True,
                padding=ft.Padding(8, 0, CardContainer.get_padding(), 0),
            ))
        
        container = ft.Container(
            content=ft.Row(row_content, spacing=0),
            on_click=handle_click,
        )
        
        def get_state() -> bool:
            return switch_state[0]
        
        def set_state(state: bool):
            switch_state[0] = state
            icon_control.opacity = 1.0 if state else 0.4
            title_text.opacity = 1.0 if state else 0.4
        
        container.get_state = get_state
        container.set_state = set_state
        
        key = section if section else f"switch_{len(self._switches)}"
        self._switches[key] = container
        
        return container
    
    def _get_enabled(self, section: str) -> bool:
        """从配置服务获取开关状态（模块内部逻辑）"""
        if self._config_service:
            return self._config_service.get_enabled(section, True)
        return True
    
    def _save_enabled(self, section: str, enabled: bool):
        """保存开关状态到配置（模块内部逻辑）"""
        if self._config_service:
            self._config_service.set_enabled(section, enabled)
    
    def get_state(self, section: str) -> bool:
        """获取指定section的开关状态"""
        if section in self._switches:
            return self._switches[section].get_state()
        return True
    
    def set_state(self, section: str, enabled: bool):
        """设置指定section的开关状态"""
        if section in self._switches:
            self._switches[section].set_state(enabled)

# *** 标准测试格式: 仅调用被测模块,AI不得添加数据 ***
if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    
    from 前端.V2.数据层.仓库.配置仓库 import ConfigRepository
    from 前端.V2.业务层.服务.配置服务 import ConfigService
    
    def main(page: ft.Page):
        page.title = "卡片开关测试"
        
        print("=" * 50)
        print("测试: 使用真实配置服务")
        print("=" * 50)
        
        repository = ConfigRepository()
        config_service = ConfigService(repository)
        
        card_switch = CardSwitch(page, config_service)
        
        print(f"开关状态(建筑设置.主帅主城): {card_switch._get_enabled('建筑设置.主帅主城')}")
        
        theme_colors = config_service.get_theme_colors()
        
        switch = card_switch.create(
            section="建筑设置.主帅主城",
            title="主帅主城",
            icon="DOMAIN",
            subtitle="设置主帅主城建筑等级",
            theme_colors=theme_colors,
        )
        
        page.add(ft.Column([
            ft.Text("卡片开关测试", size=20, weight=ft.FontWeight.BOLD),
            switch,
        ]))
    
    ft.app(target=main)
