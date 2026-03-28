# -*- coding: utf-8 -*-
"""
模块名称:CardGroupManager
模块功能:卡片组管理器，界面级销毁管理
实现步骤:
- 管理卡片列表
- 导航切换时销毁所有卡片控件
"""

import flet as ft
from typing import List, Dict, Any, Callable

import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, project_root)

try:
    from 核心层.配置.界面配置 import UIConfig
except ImportError:
    # 尝试相对导入
    from ...核心层.配置.界面配置 import UIConfig


class CardGroupManager:
    """卡片组管理器 - 界面级销毁管理"""
    
    def __init__(self):
        self.cards: List[ft.Container] = []
    
    def add_card(self, card: ft.Container) -> None:
        """添加卡片到管理器"""
        self.cards.append(card)
    
    def destroy_all(self) -> None:
        """销毁所有卡片的选项列表（界面级销毁）"""
        for card in self.cards:
            if hasattr(card, 'destroy_controls'):
                card.destroy_controls()
        
        try:
            from 表示层.组件.基础.下拉框 import get_manager
            manager = get_manager()
            manager.close_all()
        except:
            pass
    
    def get_all_cards(self) -> List[ft.Container]:
        """获取所有卡片"""
        return self.cards.copy()
    
    def clear(self) -> None:
        """清空管理器"""
        self.destroy_all()
        self.cards.clear()


def create_managed_card(
    manager: CardGroupManager,
    title: str,
    icon: str,
    subtitle: str,
    enabled: bool = True,
    controls: List[ft.Control] = None,
    controls_config: List[Dict[str, Any]] = None,
    controls_per_row: int = 6,
    width: int = None,
    on_value_change: Callable[[str, Any], None] = None,
    on_save: Callable[[str, str], None] = None,
    config: UIConfig = None,
) -> ft.Container:
    try:
        from 表示层.组件.复合.可开关卡片 import SwitchableCard
    except ImportError:
        # 尝试相对导入
        from .可开关卡片 import SwitchableCard
    
    card = SwitchableCard.create(
        title=title,
        icon=icon,
        subtitle=subtitle,
        enabled=enabled,
        controls=controls,
        controls_config=controls_config,
        controls_per_row=controls_per_row,
        width=width,
        on_value_change=on_value_change,
        on_save=on_save,
        config=config,
    )
    
    manager.add_card(card)
    
    return card


# *** 标准测试格式: 仅调用被测模块,AI不得添加数据 ***
if __name__ == "__main__":
    def main(page: ft.Page):
        config = UIConfig()
        manager = CardGroupManager()
        
        card1 = create_managed_card(
            manager=manager,
            title="测试卡片1",
            icon="SETTINGS",
            subtitle="这是测试卡片1",
            config=config,
        )
        
        card2 = create_managed_card(
            manager=manager,
            title="测试卡片2",
            icon="ACCOUNT",
            subtitle="这是测试卡片2",
            config=config,
        )
        
        page.add(ft.Column([card1, card2], spacing=10))
    
    ft.app(target=main)
