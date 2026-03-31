# -*- coding: utf-8 -*-

"""
模块名称：卡片组.py
模块功能：卡片组组件，调用卡片开关和卡片控件

实现步骤：
- 调用卡片开关
- 调用卡片控件
- 布局（左侧开关 + 右侧控件区）
- 动态计算卡片高度

职责：
- 调用卡片开关
- 调用卡片控件
- 布局（左侧开关 + 右侧控件区）
- 根据控件数量动态计算卡片高度

不负责：
- 开关内部逻辑（由卡片开关模块自己处理）
- 控件创建逻辑（由卡片控件模块自己处理）
- 数据获取（由被调用模块自己获取）
"""

import flet as ft
from typing import Callable, Dict, List, Optional, Any

from 前端.V2.层级4_复合模块.卡片开关 import CardSwitch
from 前端.V2.层级4_复合模块.卡片控件 import CardControls
from 前端.V2.层级5_基础模块.卡片容器 import CardContainer

# ============================================
# 公开接口
# ============================================

class CardGroup:
    """
    卡片组V2（层级3）
    
    职责：
    - 调用卡片开关
    - 调用卡片控件
    - 布局（左侧开关 + 右侧控件区）
    - 根据控件数量动态计算卡片高度
    
    不负责：
    - 开关内部逻辑（由卡片开关模块自己处理）
    - 控件创建逻辑（由卡片控件模块自己处理）
    - 数据获取（由被调用模块自己获取）
    
    设计优化（参考V1，采用更优方案）：
    - V1: 固定高度100px + Stack布局
    - V2: 动态计算高度 + Stack布局
    - 优势: 控件数量多时自动增加高度，确保所有控件完整显示
    """
    
    def __init__(self, page: ft.Page, config_service):
        self._page = page
        self._config_service = config_service
        self._card_switch = CardSwitch(page, config_service)
        self._card_controls = CardControls(page, config_service)
        self._cards: Dict[str, ft.Container] = {}
    
    @property
    def dropdown(self):
        """提供下拉框实例访问（用于销毁）"""
        return self._card_controls.dropdown
    
    @staticmethod
    def get_card_height():
        """获取卡片基础高度（从卡片开关模块获取）"""
        return CardSwitch.get_height()
    
    @staticmethod
    def get_padding():
        """获取内边距（从卡片开关模块获取）"""
        return CardSwitch.get_padding()
    
    @staticmethod
    def calculate_card_height(control_count: int) -> int:
        """
        根据控件数量计算卡片高度
        
        参数：
        - control_count: 控件数量
        
        返回：
        - 计算后的卡片高度
        
        设计思路：
        - 基础高度：72px（单行控件的最小高度）
        - 每行控件高度：36px
        - 行间距：8px
        - 内边距：6px * 2
        """
        return CardContainer.calculate_height(
            CardControls.calculate_control_rows(control_count)
        )
    
    def create(
        self,
        section: str = "",
        title: str = "卡片标题",
        icon: str = "HOME",
        subtitle: str = "",
        controls_config: List[Dict[str, Any]] = None,
        has_switch: bool = True,
        on_change: Callable[[str, str, Any], None] = None,
        theme_colors: Dict[str, str] = None,
        controls_per_row: int = None,
    ) -> ft.Container:
        """
        创建卡片组
        
        参数：
        - section: 配置节
        - title: 卡片标题
        - icon: 图标名称
        - subtitle: 卡片副标题（说明文字）
        - controls_config: 控件配置列表
        - has_switch: 是否有开关
        - on_change: 值变更回调
        - theme_colors: 主题颜色
        - controls_per_row: 每行控件数（可选，默认从配置服务获取）
        
        注意：数据（开关状态、选项列表、当前值、宽度）由被调用模块自己从config_service获取
        """
        if theme_colors is None:
            theme_colors = {
                "text_primary": "#000000",
                "text_secondary": "#666666",
                "text_disabled": "#999999",
                "bg_card": "#FFFFFF",
                "accent": "#0078D4",
                "border": "#CCCCCC",
            }
        
        if controls_config is None:
            controls_config = []
        
        # 计算控件数量和卡片高度
        control_count = len(controls_config)
        card_height = self.calculate_card_height(control_count)
        padding = self.get_padding()
        
        def on_toggle(new_enabled: bool):
            controls_container.opacity = 1.0 if new_enabled else 0.5
            try:
                if self._page:
                    self._page.update()
            except:
                pass
        
        card_switch = self._card_switch.create(
            section=section if has_switch else "",
            title=title,
            icon=icon,
            subtitle=subtitle,
            on_toggle=on_toggle if has_switch else None,
            theme_colors=theme_colors,
        )
        
        controls_container = self._card_controls.create(
            section=section,
            controls_config=controls_config,
            on_change=on_change,
            theme_colors=theme_colors,
            controls_per_row=controls_per_row,
        )
        
        enabled = card_switch.get_state()
        controls_container.opacity = 1.0 if enabled else 0.5
        
        # 参考V1的Stack布局，采用更优的Row布局方案
        # V2优化：移除Row的固定高度限制，让控件区域自适应
        main_row = ft.Row([
            card_switch,
            controls_container,
        ], spacing=0, vertical_alignment=ft.CrossAxisAlignment.START, expand=True)
        
        container = CardContainer.create(
            content=main_row,
            height=card_height,
            padding=padding,
            theme_colors=theme_colors,
        )
        
        if section:
            self._cards[section] = container
        
        return container
    
    def destroy_all(self):
        """销毁所有下拉框菜单"""
        self._card_controls.dropdown.destroy_all()
        self._cards.clear()

# *** 标准测试格式: 仅调用被测模块,AI不得添加数据 ***
if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    
    from 前端.V2.数据层.仓库.配置仓库 import ConfigRepository
    from 前端.V2.业务层.服务.配置服务 import ConfigService
    
    def main(page: ft.Page):
        page.title = "卡片组测试"
        
        print("=" * 50)
        print("测试: 使用真实配置服务")
        print("=" * 50)
        
        repository = ConfigRepository()
        config_service = ConfigService(repository)
        
        card_group = CardGroup(page, config_service)
        
        print(f"卡片基础高度: {CardGroup.get_card_height()}")
        print(f"卡片内边距: {CardGroup.get_padding()}")
        
        theme_colors = config_service.get_theme_colors()
        
        controls_config = [
            {"id": "城市等级", "type": "dropdown", "label": "城市"},
            {"id": "兵工厂等级", "type": "dropdown", "label": "兵工"},
            {"id": "陆军基地", "type": "dropdown", "label": "陆军"},
            {"id": "空军基地", "type": "dropdown", "label": "空军"},
            {"id": "商业区", "type": "dropdown", "label": "商业"},
            {"id": "补给品厂", "type": "dropdown", "label": "补给"},
        ]
        
        card = card_group.create(
            section="建筑设置.主帅主城",
            title="主帅主城",
            icon="DOMAIN",
            subtitle="设置主帅主城建筑等级",
            controls_config=controls_config,
            has_switch=True,
            theme_colors=theme_colors,
        )
        
        page.add(ft.Column([
            ft.Text("卡片组测试", size=20, weight=ft.FontWeight.BOLD),
            card,
        ]))
    
    ft.app(target=main)
