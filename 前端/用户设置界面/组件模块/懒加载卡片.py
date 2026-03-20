# -*- coding: utf-8 -*-
"""
模块名称：懒加载卡片 | 层级：组件模块层
设计思路：
    组合模式：组装状态管理、触发器、资源加载器、UI渲染器。
    单一职责：协调各模块，不直接实现具体功能。
    
    模块化拆分：
    - 状态管理：LazyState（懒加载状态管理器.py）
    - 触发检测：LazyTrigger（懒加载触发器.py）
    - 资源加载：LazyLoader（懒加载资源加载器.py）
    - UI渲染：LazyRenderer（懒加载UI渲染器.py）

功能：
    1. 未加载状态：左侧与通用卡片一致，右侧显示"点击加载数据"
    2. 已加载状态：调用通用卡片显示控件
    3. 点击时：保存上一个卡片 + 销毁上一个卡片 + 加载当前卡片

对外接口：
    - LazyCard: 懒加载卡片（协调器）
"""

import flet as ft
from typing import Callable, Dict, Any, Optional
from 前端.用户设置界面.组件模块.懒加载状态管理器 import LazyState
from 前端.用户设置界面.组件模块.懒加载触发器 import LazyTrigger
from 前端.用户设置界面.组件模块.懒加载资源加载器 import LazyLoader
from 前端.用户设置界面.组件模块.懒加载UI渲染器 import LazyRenderer, LAZY_HEIGHT
from 前端.用户设置界面.配置.界面配置 import 界面配置


class LazyCard:
    """懒加载卡片 - 协调器，组装各模块"""
    
    def __init__(
        self,
        card_name: str,
        card_config: Dict[str, Any],
        config_manager: Any = None,
        on_value_change: Callable[[str, Any], None] = None,
        is_default: bool = False,
    ):
        self.card_name = card_name
        self.card_config = card_config
        self.config_manager = config_manager
        self.on_value_change = on_value_change
        self.is_default = is_default
        
        self._is_loaded = False
        self._container: Optional[ft.Container] = None
        self._is_enabled = True
        self._hint_controls: Dict[str, ft.Control] = {}
        
        state = LazyState()
        state.register_card(card_name, self)
        if is_default:
            state.set_config_manager(config_manager)
    
    @property
    def is_loaded(self) -> bool:
        """是否已加载"""
        return self._is_loaded
    
    @property
    def is_enabled(self) -> bool:
        """是否启用"""
        return self._is_enabled
    
    def create(self) -> ft.Container:
        """创建卡片容器"""
        if self.is_default:
            self._container = self._render_loaded()
            self._is_loaded = True
            state = LazyState()
            state.set_current(self.card_name)
        else:
            self._container = self._render_lazy()
            self._container.on_click = self._on_click
        
        return self._container
    
    def load(self):
        """加载卡片内容"""
        if self._is_loaded:
            return
        
        new_container = self._render_loaded()
        
        self._container.content = new_container.content
        self._container.on_click = None
        self._container.height = new_container.height
        self._is_loaded = True
        
        state = LazyState()
        state.set_current(self.card_name)
        
        self._update_container()
    
    def destroy(self):
        """销毁卡片内容"""
        if not self._is_loaded:
            return
        
        lazy_result = LazyRenderer.render_lazy_state(
            card_config=self.card_config,
            enabled=True,
        )
        
        self._container.content = lazy_result["container"].content
        self._container.on_click = self._on_click
        self._container.height = LAZY_HEIGHT
        self._is_loaded = False
        
        self._hint_controls = lazy_result["hint_controls"]
        
        self._update_container()
    
    def _render_lazy(self) -> ft.Container:
        """渲染未加载状态"""
        def on_state_change(new_enabled: bool):
            self._is_enabled = new_enabled
            LazyRenderer.update_hint_state(self._hint_controls, new_enabled)
        
        result = LazyRenderer.render_lazy_state(
            card_config=self.card_config,
            enabled=self._is_enabled,
            on_state_change=on_state_change,
        )
        
        self._hint_controls = result["hint_controls"]
        
        return result["container"]
    
    def _render_loaded(self) -> ft.Container:
        """渲染已加载状态"""
        return LazyRenderer.render_loaded_state(
            card_config=self.card_config,
            card_name=self.card_name,
            config_manager=self.config_manager,
            on_value_change=self.on_value_change,
        )
    
    def _on_click(self, e: ft.ControlEvent):
        """点击事件处理"""
        if not LazyTrigger.can_trigger(self._is_loaded, self._is_enabled):
            return
        
        state = LazyState()
        
        current_card = state.get_current()
        if current_card:
            state.save_current()
            current_card_obj = state.get_card(current_card)
            if current_card_obj:
                current_card_obj.destroy()
        
        self.load()
    
    def _update_container(self):
        """更新容器显示"""
        try:
            if self._container and self._container.page:
                self._container.update()
        except RuntimeError:
            pass


懒加载卡片 = LazyCard


# *** 调试逻辑 ***
if __name__ == "__main__":
    from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider
    from 前端.配置.建筑配置 import 建筑配置
    
    配置 = 界面配置()
    ThemeProvider.initialize(配置)
    
    DEFAULT_CARD_NAME = "主帅主城"
    DEFAULT_CARD_CONFIG = 建筑配置.get(DEFAULT_CARD_NAME, {})
    
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        
        card = LazyCard(
            card_name=DEFAULT_CARD_NAME,
            card_config=DEFAULT_CARD_CONFIG,
            is_default=True,
        )
        page.add(card.create())
    
    ft.run(main)
