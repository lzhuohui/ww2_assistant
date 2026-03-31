# -*- coding: utf-8 -*-

"""
模块名称：卡片开关.py
模块功能：卡片开关组件，完整的开关模块（左侧图标+标题 + 分割线 + 右侧副标题）

实现步骤：
- 从配置服务获取卡片信息
- 创建左侧区域（图标+标题）
- 创建分割线
- 创建右侧副标题
- 组合布局
- 开关状态逻辑

职责：
- 从配置服务获取卡片信息（模块自己获取）
- 从配置服务获取开关状态（模块自己获取）
- 完整的开关模块（左侧+分割线+右侧副标题）
- 开关状态逻辑
- 自动保存开关状态

不负责：
- 控件创建
- 控件布局
- 卡片容器

设计原则（符合V2版本模块化设计补充共识）：
- 不调用卡片容器，返回完整的开关模块
- 尺寸配置直接从用户偏好.json获取
- 卡片信息由模块自己获取，不依赖调用者传递
"""

import flet as ft
from typing import Callable, Dict, Optional

from 前端.V2.层级5_基础模块.图标 import Icon
from 前端.V2.层级5_基础模块.标签 import Label
from 前端.V2.层级5_基础模块.分割线 import Divider

# ============================================
# 数据和文件接口（前置，方便查看和修改）
# ============================================

# *** 用户指定变量: 变量值必须生效,AI不得更改数据 ***
USER_DIVIDER_HEIGHT = 90      # 分割线高度（像素）
USER_DIVIDER_WIDTH = 2         # 分割线粗细（像素）
# *********************************

# 卡片开关无默认值配置，其他UI配置从用户偏好.json获取

# ============================================
# 公开接口
# ============================================

class CardSwitch:
    """
    卡片开关（层级4：复合模块）
    
    职责：
    - 从配置服务获取卡片信息（模块自己获取）
    - 从配置服务获取开关状态（模块自己获取）
    - 完整的开关模块（左侧+分割线+右侧副标题）
    - 开关状态逻辑
    - 自动保存开关状态
    
    不负责：
    - 控件创建
    - 控件布局
    - 卡片容器
    """
    
    _config_service = None
    
    @classmethod
    def set_config_service(cls, config_service):
        """设置配置服务实例"""
        cls._config_service = config_service
        Icon.set_config_service(config_service)
        Label.set_config_service(config_service)
        Divider.set_config_service(config_service)
    
    @staticmethod
    def _check_config_service():
        """检查配置服务是否已设置"""
        if CardSwitch._config_service is None:
            raise RuntimeError(
                "CardSwitch模块未设置config_service，"
                "请先调用 CardSwitch.set_config_service(config_service)"
            )
    
    @staticmethod
    def get_divider_height() -> int:
        """获取分割线高度（用户指定变量）"""
        return USER_DIVIDER_HEIGHT

    @staticmethod
    def get_left_width() -> int:
        """获取左侧宽度（从用户偏好.json获取）"""
        CardSwitch._check_config_service()
        value = CardSwitch._config_service.get_ui_config("卡片开关", "左侧宽度")
        if value is None:
            raise RuntimeError("用户偏好.json缺少配置: 卡片开关.左侧宽度")
        return value
    
    @staticmethod
    def get_padding() -> int:
        """获取内边距（从用户偏好.json获取）"""
        CardSwitch._check_config_service()
        value = CardSwitch._config_service.get_ui_config("卡片开关", "内边距")
        if value is None:
            raise RuntimeError("用户偏好.json缺少配置: 卡片开关.内边距")
        return value
    
    @staticmethod
    def get_height() -> int:
        """获取高度（从用户偏好.json获取，默认使用卡片最小高度）"""
        CardSwitch._check_config_service()
        value = CardSwitch._config_service.get_ui_config("卡片", "最小高度")
        if value is None:
            value = 100
        return value
    
    @staticmethod
    def get_icon_size() -> int:
        """获取图标尺寸（从用户偏好.json获取基础大小*1.375）"""
        CardSwitch._check_config_service()
        base_size = Icon.get_base_size()
        return int(base_size * 1.375)
    
    @staticmethod
    def get_title_size() -> int:
        """获取标题尺寸（从用户偏好.json获取基础大小）"""
        CardSwitch._check_config_service()
        return Label.get_base_size()
    
    @staticmethod
    def get_subtitle_size() -> int:
        """获取副标题尺寸（从用户偏好.json获取基础大小*0.71）"""
        CardSwitch._check_config_service()
        base_size = Label.get_base_size()
        return int(base_size * 0.71)
    
    def __init__(self, page: ft.Page = None, config_service=None):
        self._page = page
        self._config_service = config_service
        self._switches: Dict[str, ft.Control] = {}
    
    def create(
        self,
        section: str = "",
        on_toggle: Callable[[bool], None] = None,
        theme_colors: Dict[str, str] = None,
    ) -> ft.Control:
        """
        创建完整的开关模块（左侧+分割线+右侧副标题）
        
        参数：
        - section: 配置节（用于获取卡片信息和开关状态）
        - on_toggle: 开关切换回调
        - theme_colors: 主题颜色
        
        返回：
        - ft.Control: 完整的开关模块（Row）
        
        注意：卡片信息、开关状态由模块自己从config_service获取
        """
        if self._config_service is None:
            raise RuntimeError("CardSwitch模块未设置config_service，请先传入config_service参数")
        
        if theme_colors is None:
            theme_colors = self._config_service.get_theme_colors()
        
        card_info = self._get_card_info(section)
        title = card_info.get("title", "卡片标题")
        icon = card_info.get("icon", "HOME")
        subtitle = card_info.get("subtitle", "")
        
        enabled = self._get_enabled(section)
        switch_state = [enabled]
        
        icon_size = CardSwitch.get_icon_size()
        title_size = CardSwitch.get_title_size()
        subtitle_size = CardSwitch.get_subtitle_size()
        left_width = CardSwitch.get_left_width()
        padding = CardSwitch.get_padding()
        card_height = CardSwitch.get_height()
        
        icon_control = ft.Icon(
            getattr(ft.Icons, icon.upper(), ft.Icons.HOME),
            size=icon_size,
            color=theme_colors.get("accent"),
            opacity=1.0 if enabled else 0.4,
        )
        
        title_text = ft.Text(
            title,
            size=title_size,
            weight=ft.FontWeight.BOLD,
            color=theme_colors.get("text_primary"),
            opacity=1.0 if enabled else 0.4,
        )
        
        left_content = ft.Column([
            icon_control,
            ft.Container(height=2),
            title_text,
        ], spacing=0, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        left_container = ft.Container(
            content=left_content,
            width=left_width - 2,
            padding=ft.Padding(padding, 0, padding, 0),
            alignment=ft.alignment.Alignment(0, 0.5),
        )
        
        divider_container = ft.Container(
            content=Divider.create_vertical(
                width=USER_DIVIDER_WIDTH,
                color_type="accent",
            ),
            height=USER_DIVIDER_HEIGHT,
            alignment=ft.alignment.Alignment(0, 0),
        )
        
        subtitle_text = ft.Text(
            subtitle,
            size=subtitle_size,
            color=theme_colors.get("text_secondary"),
            opacity=0.8 if enabled else 0.4,
            max_lines=2,
            overflow=ft.TextOverflow.ELLIPSIS,
        ) if subtitle else None
        
        right_content = ft.Column([
            ft.Container(expand=True),
            subtitle_text if subtitle_text else ft.Container(),
        ], spacing=0, alignment=ft.MainAxisAlignment.END) if subtitle_text else ft.Container(expand=True)
        
        right_container = ft.Container(
            content=right_content,
            expand=True,
            padding=ft.Padding(8, 0, padding, 0),
        )
        
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
                    switch_row.update()
                except:
                    pass
        
        switch_row = ft.Row([
            left_container,
            divider_container,
            right_container,
        ], spacing=0, vertical_alignment=ft.CrossAxisAlignment.CENTER, height=USER_DIVIDER_HEIGHT)
        
        switch_row.on_click = handle_click
        
        def get_state() -> bool:
            return switch_state[0]
        
        def set_state(state: bool):
            switch_state[0] = state
            icon_control.opacity = 1.0 if state else 0.4
            title_text.opacity = 1.0 if state else 0.4
            if subtitle_text:
                subtitle_text.opacity = 0.8 if state else 0.4
        
        switch_row.get_state = get_state
        switch_row.set_state = set_state
        switch_row._icon_control = icon_control
        switch_row._title_text = title_text
        switch_row._subtitle_text = subtitle_text
        
        key = section if section else f"switch_{len(self._switches)}"
        self._switches[key] = switch_row
        
        return switch_row
    
    def _get_card_info(self, section: str) -> Dict:
        """从配置服务获取卡片信息（模块内部逻辑）"""
        if self._config_service:
            return self._config_service.get_card_info(section)
        return {}
    
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
    
    from 前端.V2.业务层.服务.配置服务 import ConfigService
    
    def main(page: ft.Page):
        page.title = "卡片开关测试"
        
        print("=" * 50)
        print("测试: 使用真实配置服务")
        print("=" * 50)
        
        config_service = ConfigService()
        
        CardSwitch.set_config_service(config_service)
        
        card_switch = CardSwitch(page, config_service)
        
        print(f"开关状态(建筑设置.主帅主城): {card_switch._get_enabled('建筑设置.主帅主城')}")
        
        switch = card_switch.create(
            section="建筑设置.主帅主城",
        )
        
        page.add(ft.Column([
            ft.Text("卡片开关测试", size=20, weight=ft.FontWeight.BOLD),
            ft.Container(content=switch, height=CardSwitch.get_height()),
        ]))
    
    ft.run(main)
