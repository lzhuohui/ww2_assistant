# -*- coding: utf-8 -*-

"""
模块名称：账号界面.py
模块功能：账号管理界面

职责：
- 管理账号卡片
- 响应配置变更
- 加载默认值
- 动态副标题显示账号状态

不负责：
- 数据存储
- 界面布局（由界面容器负责）
"""

import flet as ft
from typing import Callable, Dict, Any, List

from 设置界面.层级0_数据管理.配置管理 import ConfigManager
from 设置界面.层级3_功能卡片.功能卡片 import FunctionCard
from 设置界面.层级3_功能卡片.界面容器 import InterfaceContainer


class AccountInterface:
    """账号界面 - V3版本"""
    
    INTERFACE_NAME = "账号界面"
    INTERFACE_TITLE = "账号管理"
    INTERFACE_HINT = "管理多个游戏账号信息"
    
    SUBTITLE_INCOMPLETE = "请完善账号信息"
    SUBTITLE_ACTIVE = "参与挂机状态"
    SUBTITLE_DISABLED = "禁止挂机状态"
    
    def __init__(self, page: ft.Page, config_manager: ConfigManager, on_scheme_change: Callable[[str], None] = None, on_start: Callable[[], None] = None):
        self._page = page
        self._config_manager = config_manager
        self._on_scheme_change = on_scheme_change
        self._on_start: Callable[[], None] = None
        self._on_start = on_start
        self._function_card = FunctionCard(page, config_manager)
        self._interface_container = InterfaceContainer(page, config_manager)
        self._cards: Dict[str, ft.Container] = {}
        self._container: ft.Container = None
        self._subtitle_text: ft.Text = None
        self._interface_container_ref: InterfaceContainer = None
    
    def build(self) -> ft.Container:
        """构建账号界面"""
        theme_colors = self._config_manager.get_theme_colors()
        
        card_names = self._config_manager.get_card_names(self.INTERFACE_NAME)
        
        # 自动关闭信息不完整的账号开关
        for card_name in card_names:
            enabled = self._config_manager.get_enabled(self.INTERFACE_NAME, card_name)
            if enabled:
                name = self._config_manager.get_raw_value(self.INTERFACE_NAME, card_name, "名称") or ""
                account = self._config_manager.get_raw_value(self.INTERFACE_NAME, card_name, "账号") or ""
                password = self._config_manager.get_raw_value(self.INTERFACE_NAME, card_name, "密码") or ""
                
                if not (name and account and password):
                    # 信息不完整，自动关闭开关
                    self._config_manager.set_enabled(self.INTERFACE_NAME, card_name, False)
        
        cards = []
        for card_name in card_names:
            card = self._function_card.create(
                interface=self.INTERFACE_NAME,
                card=card_name,
                on_change=self._on_change,
                on_toggle=self._on_toggle,
                theme_colors=theme_colors,
            )
            cards.append(card)
            self._cards[card_name] = card
        
        interface_hint = self._calculate_interface_hint()
        
        self._container = self._interface_container.create(
            title=self.INTERFACE_TITLE,
            hint=interface_hint,
            cards=cards,
            on_scheme_change=self._on_scheme_change,
            on_load_defaults=self._on_load_defaults,
            on_start=self._on_start,
        )
        
        self._interface_container_ref = self._interface_container
        
        for card_name in card_names:
            subtitle = self._calculate_card_subtitle(card_name)
            self._function_card.set_subtitle(self.INTERFACE_NAME, card_name, subtitle, update_now=False)
        
        self._page.update()
        
        return self._container
    
    def _calculate_card_subtitle(self, card: str) -> str:
        """计算卡片副标题
        
        场景逻辑：
        - 场景1：信息不完整 + 开关打开 → "请完善账号信息"
        - 场景2：信息不完整 + 开关关闭 → "禁止挂机（信息不完整）"
        - 场景3：信息完整 + 开关打开 → "参与挂机状态"
        - 场景4：信息完整 + 开关关闭 → "禁止挂机状态"
        """
        enabled = self._config_manager.get_enabled(self.INTERFACE_NAME, card)
        
        name = self._config_manager.get_raw_value(self.INTERFACE_NAME, card, "名称") or ""
        account = self._config_manager.get_raw_value(self.INTERFACE_NAME, card, "账号") or ""
        password = self._config_manager.get_raw_value(self.INTERFACE_NAME, card, "密码") or ""
        
        info_complete = bool(name and account and password)
        
        if not info_complete:
            if enabled:
                return "请完善账号信息"
            else:
                return "禁止挂机（信息不完整）"
        else:
            if enabled:
                return "参与挂机状态"
            else:
                return "禁止挂机状态"
    
    def _calculate_interface_hint(self) -> str:
        """计算界面副标题（显示参与挂机账号数量）"""
        card_names = self._config_manager.get_card_names(self.INTERFACE_NAME)
        active_count = 0
        
        for card_name in card_names:
            enabled = self._config_manager.get_enabled(self.INTERFACE_NAME, card_name)
            if enabled:
                name = self._config_manager.get_raw_value(self.INTERFACE_NAME, card_name, "名称") or ""
                account = self._config_manager.get_raw_value(self.INTERFACE_NAME, card_name, "账号") or ""
                password = self._config_manager.get_raw_value(self.INTERFACE_NAME, card_name, "密码") or ""
                if name and account and password:
                    active_count += 1
        
        return f"{active_count}个账号参与挂机"
    
    def _update_card_subtitle(self, card: str, immediate: bool = False):
        """更新卡片副标题
        
        参数：
        - card: 卡片名称
        - immediate: 是否立即更新（用于开关状态变更）
        """
        subtitle = self._calculate_card_subtitle(card)
        self._function_card.set_subtitle(self.INTERFACE_NAME, card, subtitle)
    
    def _update_interface_hint(self):
        """更新界面副标题（显示参与挂机账号数量）"""
        interface_hint = self._calculate_interface_hint()
        if self._interface_container_ref:
            self._interface_container_ref.set_hint(interface_hint)
    
    def _on_change(self, interface: str, card: str, control_id: str, value: Any):
        """控件值变更回调"""
        if control_id in ["名称", "账号", "密码"]:
            # 检查信息是否完整
            name = self._config_manager.get_raw_value(self.INTERFACE_NAME, card, "名称") or ""
            account = self._config_manager.get_raw_value(self.INTERFACE_NAME, card, "账号") or ""
            password = self._config_manager.get_raw_value(self.INTERFACE_NAME, card, "密码") or ""
            
            info_complete = bool(name and account and password)
            
            # 如果信息不完整，自动关闭开关
            if not info_complete:
                enabled = self._config_manager.get_enabled(self.INTERFACE_NAME, card)
                if enabled:
                    self._config_manager.set_enabled(self.INTERFACE_NAME, card, False)
                    # 需要重新创建卡片以更新开关状态
                    theme_colors = self._config_manager.get_theme_colors()
                    new_card = self._function_card.create(
                        interface=self.INTERFACE_NAME,
                        card=card,
                        on_change=self._on_change,
                        on_toggle=self._on_toggle,
                        theme_colors=theme_colors,
                    )
                    self._cards[card] = new_card
                    
                    # 更新界面中的卡片
                    if self._container:
                        main_column = self._container.content
                        cards_column = main_column.controls[1]
                        for i, c in enumerate(cards_column.controls):
                            if hasattr(c, 'key') and c.key == f"{self.INTERFACE_NAME}.{card}":
                                cards_column.controls[i] = new_card
                                break
            
            self._update_card_subtitle(card)
            self._update_interface_hint()
    
    def _on_toggle(self, interface: str, card: str, enabled: bool):
        """开关状态变更回调"""
        self._update_card_subtitle(card, immediate=True)
        self._update_interface_hint()
    
    def _on_load_defaults(self):
        """加载默认值回调"""
        theme_colors = self._config_manager.get_theme_colors()
        
        card_names = self._config_manager.get_card_names(self.INTERFACE_NAME)
        
        new_cards = []
        for card_name in card_names:
            card = self._function_card.create(
                interface=self.INTERFACE_NAME,
                card=card_name,
                on_change=self._on_change,
                on_toggle=self._on_toggle,
                theme_colors=theme_colors,
                use_defaults=True,
            )
            new_cards.append(card)
            self._cards[card_name] = card
        
        if self._container:
            main_column = self._container.content
            cards_column = main_column.controls[1]
            cards_column.controls = new_cards
            
            for card_name in card_names:
                subtitle = self._calculate_card_subtitle(card_name)
                self._function_card.set_subtitle(self.INTERFACE_NAME, card_name, subtitle, update_now=False)
            
            self._page.update()
    
    def destroy(self):
        """销毁界面（只清理界面级缓存，下拉框销毁由层级1负责）"""
        self._function_card.destroy()
        self._cards.clear()
        self._container = None
