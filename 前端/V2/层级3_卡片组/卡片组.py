# -*- coding: utf-8 -*-

"""
模块名称：卡片组.py
模块功能：卡片组组件，组合卡片开关+卡片控件+卡片容器

实现步骤：
- 调用卡片开关创建完整的开关模块（浮动上层）
- 调用卡片控件创建控件区
- 调用卡片容器创建容器（底层）
- Stack布局（卡片开关浮动在卡片容器上层）

职责：
- 调用卡片开关获取完整的开关模块
- 调用卡片控件获取控件区
- 调用卡片容器创建容器
- Stack布局（卡片开关浮动在卡片容器上层）
- 销毁功能

不负责：
- 控件创建（由卡片控件负责）
- 开关逻辑（由卡片开关负责）
- 获取卡片信息（由卡片开关负责）
- 设置透明度（由卡片控件负责）

设计原则（符合V2版本模块化设计补充共识）：
- 卡片开关浮动在卡片容器上层，互不干扰
- 用户指定变量各自生效
- 只传递section，不传递具体数据
"""

import flet as ft
from typing import Callable, Dict, List, Optional, Any

from 前端.V2.层级5_基础模块.卡片容器 import CardContainer
from 前端.V2.层级4_复合模块.卡片开关 import CardSwitch
from 前端.V2.层级4_复合模块.卡片控件 import CardControls

class CardGroup:
    """
    卡片组（层级3：组合模块）
    
    职责：
    - 调用卡片开关获取完整的开关模块
    - 调用卡片控件获取控件区
    - 调用卡片容器创建容器
    - Stack布局（卡片开关浮动在卡片容器上层）
    - 销毁功能
    
    不负责：
    - 控件创建（由卡片控件负责）
    - 开关逻辑（由卡片开关负责）
    - 获取卡片信息（由卡片开关负责）
    - 设置透明度（由卡片控件负责）
    """
    
    _config_service = None
    
    @classmethod
    def set_config_service(cls, config_service):
        """设置配置服务实例"""
        cls._config_service = config_service
        CardContainer.set_config_service(config_service)
        CardSwitch.set_config_service(config_service)
        CardControls.set_config_service(config_service)
    
    @staticmethod
    def get_height():
        """获取卡片高度（从卡片容器继承）"""
        return CardContainer.get_height()
    
    @staticmethod
    def get_padding():
        """获取内边距（从卡片容器继承）"""
        return CardContainer.get_padding()
    
    @staticmethod
    def _check_config_service():
        """检查配置服务是否已设置"""
        if CardGroup._config_service is None:
            raise RuntimeError(
                "CardGroup模块未设置config_service，"
                "请先调用 CardGroup.set_config_service(config_service)"
            )
    
    def __init__(self, page: ft.Page = None, config_service=None):
        self._page = page
        self._config_service = config_service or CardGroup._config_service
        self._card_switch = CardSwitch(page, self._config_service)
        self._card_controls = CardControls(page, self._config_service)
        self._cards: Dict[str, ft.Container] = {}
    
    @property
    def dropdown(self):
        """提供下拉框实例访问（用于销毁）"""
        return self._card_controls.dropdown
    
    def create(
        self,
        section: str = "",
        page: ft.Page = None,
        on_switch_change: Callable[[bool], None] = None,
        on_control_change: Callable[[str, str, Any], None] = None,
        theme_colors: Dict[str, str] = None,
        width: int = None,
        height: int = None,
        controls_per_row: int = None,
    ) -> ft.Stack:
        """
        创建卡片组（卡片开关浮动在卡片容器上层）
        
        参数：
        - section: 配置节（卡片开关和卡片控件自己获取数据）
        - page: 页面实例
        - on_switch_change: 开关变更回调
        - on_control_change: 控件值变更回调
        - theme_colors: 主题颜色（可选，不传则从配置服务获取）
        - width: 卡片宽度
        - height: 卡片高度（可选，默认使用卡片容器高度）
        - controls_per_row: 每行控件数（可选，默认从配置服务获取）
        
        返回：
        - ft.Stack: 卡片开关浮动在卡片容器上层的堆叠
        """
        if self._config_service is None:
            raise RuntimeError("CardGroup模块未设置config_service，请先调用CardGroup.set_config_service()")
        
        if theme_colors is None:
            theme_colors = self._config_service.get_theme_colors()

        if height is None:
            height = CardContainer.get_height()
        
        def on_toggle(new_enabled: bool):
            if on_switch_change:
                on_switch_change(new_enabled)
            try:
                if self._page:
                    card_stack.update()
            except:
                pass
        
        switch_module = self._card_switch.create(
            section=section,
            on_toggle=on_toggle,
            theme_colors=theme_colors,
        )
        
        controls_module = self._card_controls.create(
            section=section,
            on_change=on_control_change,
            theme_colors=theme_colors,
            controls_per_row=controls_per_row,
        )
        
        right_margin = CardControls.get_right_margin()
        
        right_area = ft.Row([
            ft.Container(expand=True),
            controls_module,
            ft.Container(width=right_margin),
        ], spacing=0, vertical_alignment=ft.CrossAxisAlignment.CENTER, expand=True)
        
        container = CardContainer.create(
            content=right_area,
            height=height,
            width=width,
        )
        
        def get_switch_state() -> bool:
            return self._card_switch.get_state(section)
        
        def set_switch_state(state: bool):
            self._card_switch.set_state(section, state)
        
        def get_all_values() -> Dict[str, Any]:
            return self._card_controls.get_all_values(section)
        
        switch_height = CardSwitch.get_divider_height()
        top_offset = (height - switch_height) / 2
        
        switch_container = ft.Container(
            content=switch_module,
            alignment=ft.alignment.Alignment(0.5, 0.5),
            top=top_offset,
            left=0,
            right=0,
        )
        
        card_stack = ft.Stack([
            container,
            switch_container,
        ], clip_behavior=ft.ClipBehavior.NONE)
        
        card_stack.height = height
        card_stack.width = width
        
        card_stack.get_switch_state = get_switch_state
        card_stack.set_switch_state = set_switch_state
        card_stack.get_all_values = get_all_values
        
        if section:
            self._cards[section] = card_stack
        
        return card_stack
    
    def destroy_all(self):
        """销毁所有下拉框菜单"""
        self._card_controls.dropdown.destroy_all()
        self._cards.clear()

# *** 标准测试格式: 仅调用被测模块,AI不得添加数据 ***
if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    
    from 前端.V2.业务层.服务.配置服务 import ConfigService
    
    def main(page: ft.Page):
        page.title = "卡片组测试"
        
        config_service = ConfigService()
        CardGroup.set_config_service(config_service)
        
        def on_switch(enabled):
            print(f"开关状态: {enabled}")
        
        def on_control_change(section, control_id, value):
            print(f"控件变更: {section}.{control_id} = {value}")
        
        card_group = CardGroup(page, config_service)
        
        card = card_group.create(
            section="建筑设置.主帅主城",
            page=page,
            on_switch_change=on_switch,
            on_control_change=on_control_change,
        )
        
        page.add(ft.Column([
            ft.Text("卡片组测试", size=20, weight=ft.FontWeight.BOLD),
            card,
        ]))
    
    ft.run(main)
