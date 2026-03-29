# -*- coding: utf-8 -*-
"""
模块名称：ConfigSchemeSection
模块功能：配置方案界面，支持5套固定配置管理
实现步骤：
- 创建5个固定配置方案卡片
- 支持加载/保存配置
- 按钮文字替换提示反馈
- 与账号界面联动
"""

import flet as ft
from typing import Dict, Any, List, Callable, Optional
import json
import os
import asyncio

from 前端.游戏设置界面.核心层.配置.界面配置 import UIConfig
from 前端.游戏设置界面.表示层.组件.复合.卡片组管理器 import CardGroupManager, create_managed_card
from 前端.游戏设置界面.表示层.组件.基础.输入框 import InputBox
from 前端.游戏设置界面.业务层.服务.配置服务 import ConfigService


# *** 用户指定变量: 变量值必须生效,AI不得更改数据 ***
USER_CARD_SPACING = 10  # 卡片间距
USER_SCHEME_DIR = "前端/游戏设置界面/配置/方案"  # 配置方案目录
USER_SCHEME_COUNT = 5  # 方案数量
USER_FEEDBACK_DURATION = 1  # 反馈提示持续时间(秒)
USER_BTN_WIDTH = 180  # 按钮宽度
USER_INPUT_WIDTH = 180  # 输入框宽度
# *********************************


class ConfigSchemeSection:
    """配置方案界面 - 固定5套配置管理"""
    
    _scheme_names: List[str] = []
    _on_scheme_change: Optional[Callable[[], None]] = None
    
    @staticmethod
    def get_scheme_names() -> List[str]:
        """获取所有已保存的配置方案名称"""
        return ConfigSchemeSection._scheme_names.copy()
    
    @staticmethod
    def refresh_scheme_names():
        """刷新配置方案名称列表"""
        os.makedirs(USER_SCHEME_DIR, exist_ok=True)
        names = []
        for i in range(1, USER_SCHEME_COUNT + 1):
            scheme_id = f"scheme_{i:02d}"
            meta_file = os.path.join(USER_SCHEME_DIR, f"{scheme_id}_meta.json")
            if os.path.exists(meta_file):
                with open(meta_file, 'r', encoding='utf-8') as f:
                    meta = json.load(f)
                    name = meta.get("name", "")
                    if name:
                        names.append(name)
        ConfigSchemeSection._scheme_names = names
    
    @staticmethod
    def create(
        config: UIConfig = None,
        config_service: ConfigService = None,
        save_callback: Callable[[str, str, str], None] = None,
        on_scheme_change: Callable[[], None] = None,
    ) -> tuple:
        if config is None:
            config = UIConfig()
        if config_service is None:
            config_service = ConfigService()
        
        ConfigSchemeSection._on_scheme_change = on_scheme_change
        
        theme_colors = config.当前主题颜色
        manager = CardGroupManager()
        card_refs: Dict[str, ft.Container] = {}
        
        os.makedirs(USER_SCHEME_DIR, exist_ok=True)
        
        def load_scheme_meta(scheme_id: str) -> Dict[str, Any]:
            meta_file = os.path.join(USER_SCHEME_DIR, f"{scheme_id}_meta.json")
            if os.path.exists(meta_file):
                with open(meta_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {"id": scheme_id, "name": ""}
        
        def save_scheme_meta(scheme_id: str, name: str):
            meta_file = os.path.join(USER_SCHEME_DIR, f"{scheme_id}_meta.json")
            with open(meta_file, 'w', encoding='utf-8') as f:
                json.dump({"id": scheme_id, "name": name}, f, ensure_ascii=False, indent=2)
        
        def load_scheme(scheme_id: str) -> bool:
            scheme_file = os.path.join(USER_SCHEME_DIR, f"{scheme_id}.json")
            if os.path.exists(scheme_file):
                with open(scheme_file, 'r', encoding='utf-8') as f:
                    scheme_config = json.load(f)
                    for key, value in scheme_config.items():
                        config_service._repository.set_value(key, value)
                return True
            return False
        
        def save_scheme(scheme_id: str) -> bool:
            os.makedirs(USER_SCHEME_DIR, exist_ok=True)
            scheme_file = os.path.join(USER_SCHEME_DIR, f"{scheme_id}.json")
            current_config = config_service._repository._cache.copy()
            with open(scheme_file, 'w', encoding='utf-8') as f:
                json.dump(current_config, f, ensure_ascii=False, indent=2)
            return True
        
        def scheme_exists(scheme_id: str) -> bool:
            scheme_file = os.path.join(USER_SCHEME_DIR, f"{scheme_id}.json")
            return os.path.exists(scheme_file)
        
        def create_scheme_card(scheme_id: str, scheme_name: str) -> ft.Container:
            name_input = InputBox.create(
                config=config,
                hint_text="输入名称保存当前配置",
                value=scheme_name,
                width=USER_INPUT_WIDTH,
                max_length=4,
            )
            
            load_text = ft.Text("加载配置", color=theme_colors.get("accent"), size=14)
            load_btn = ft.OutlinedButton(
                content=load_text,
                width=USER_BTN_WIDTH,
                style=ft.ButtonStyle(
                    side=ft.BorderSide(1, theme_colors.get("accent")),
                ),
            )
            
            save_text = ft.Text("保存配置", color=theme_colors.get("accent"), size=14)
            save_btn = ft.OutlinedButton(
                content=save_text,
                width=USER_BTN_WIDTH,
                style=ft.ButtonStyle(
                    side=ft.BorderSide(1, theme_colors.get("accent")),
                ),
            )
            
            async def show_feedback(btn_text: ft.Text, original: str, message: str):
                btn_text.value = message
                try:
                    btn_text.update()
                except:
                    pass
                
                await asyncio.sleep(USER_FEEDBACK_DURATION)
                
                btn_text.value = original
                try:
                    btn_text.update()
                except:
                    pass
            
            def handle_load(e):
                name = name_input.value.strip()
                if not name:
                    asyncio.create_task(show_feedback(load_text, "加载配置", "请输入名称"))
                    return
                
                if not scheme_exists(scheme_id):
                    asyncio.create_task(show_feedback(load_text, "加载配置", "配置不存在"))
                    return
                
                if load_scheme(scheme_id):
                    asyncio.create_task(show_feedback(load_text, "加载配置", "加载成功"))
                else:
                    asyncio.create_task(show_feedback(load_text, "加载配置", "加载失败"))
            
            def handle_save(e):
                name = name_input.value.strip()
                if not name:
                    asyncio.create_task(show_feedback(save_text, "保存配置", "请输入名称"))
                    return
                
                if save_scheme(scheme_id):
                    save_scheme_meta(scheme_id, name)
                    asyncio.create_task(show_feedback(save_text, "保存配置", "保存成功"))
                    ConfigSchemeSection.refresh_scheme_names()
                    if ConfigSchemeSection._on_scheme_change:
                        ConfigSchemeSection._on_scheme_change()
                else:
                    asyncio.create_task(show_feedback(save_text, "保存配置", "保存失败"))
            
            load_btn.on_click = handle_load
            save_btn.on_click = handle_save
            
            controls = [
                load_btn,
                name_input,
                save_btn,
            ]
            
            card = create_managed_card(
                manager=manager,
                title=f"{scheme_id[-2:]}方案",
                icon="FOLDER",
                subtitle="加载：切换配置 | 保存：存储当前配置",
                enabled=True,
                controls=controls,
                controls_per_row=3,
                config=config,
            )
            
            card_refs[scheme_id] = card
            return card
        
        ConfigSchemeSection.refresh_scheme_names()
        
        card_list = []
        for i in range(1, USER_SCHEME_COUNT + 1):
            scheme_id = f"scheme_{i:02d}"
            meta = load_scheme_meta(scheme_id)
            card_list.append(create_scheme_card(scheme_id, meta.get("name", "")))
        
        card_column = ft.Column(
            controls=card_list,
            spacing=USER_CARD_SPACING,
            scroll=ft.ScrollMode.HIDDEN,
            expand=True,
        )
        
        content_column = ft.Column(
            controls=[
                card_column,
            ],
            spacing=0,
            expand=True,
        )
        
        content_column.card_manager = manager
        
        return content_column, manager


# *** 标准测试格式: 仅调用被测模块,AI不得添加数据 ***
if __name__ == "__main__":
    def main(page: ft.Page):
        config = UIConfig()
        service = ConfigService()
        section, manager = ConfigSchemeSection.create(config=config, config_service=service)
        page.add(section)
    
    ft.app(target=main)
