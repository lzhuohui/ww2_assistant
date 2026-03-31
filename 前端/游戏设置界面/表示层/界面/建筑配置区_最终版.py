#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
建筑配置区最终版 - 直接使用简化选项管理器
遵循下拉框测试目录的实现方式
"""

import flet as ft
from typing import Dict, Any, List, Callable, Optional, Tuple
import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from 核心层.配置.界面配置 import UIConfig
from 配置.简化选项管理器 import get_simple_option_manager
from 表示层.组件.基础.下拉框 import create_dropdown
from 表示层.组件.复合.卡片组管理器 import CardGroupManager, create_managed_card
from 业务层.服务.配置服务 import ConfigService


# *** 用户指定变量: 变量值必须生效,AI不得更改数据 ***
USER_CARD_SPACING = 5  # 卡片间距
USER_DROPDOWN_WIDTH = 60  # 下拉框宽度
# *********************************


def create_building_config_section(
    config: UIConfig = None,
    config_service: ConfigService = None,
    save_callback: Optional[Callable[[str, str, str], None]] = None,
) -> Tuple[ft.Column, Any]:
    """创建建筑配置区（最终版）
    
    Args:
        config: 界面配置
        config_service: 配置服务（用于保存/加载）
        save_callback: 保存回调函数（兼容接口）
        
    Returns:
        (配置区容器, 管理器) - 兼容原接口
    """
    if config is None:
        config = UIConfig()
    
    if config_service is None:
        config_service = ConfigService()
        config_service.load_config()
    
    theme_colors = config.当前主题颜色
    
    # 获取简化选项管理器
    option_manager = get_simple_option_manager()
    
    # 创建卡片组管理器
    manager = CardGroupManager()
    
    # 主容器
    section_container = ft.Column(spacing=USER_CARD_SPACING)
    
    # ========== 创建下拉框的辅助函数 ==========
    def create_building_dropdown(config_key: str, label: str, default_value: str) -> ft.Control:
        """创建建筑等级下拉框"""
        saved_value = config_service.get_value("building_config", config_key)
        current_value = saved_value if saved_value is not None else default_value
        
        # 创建保存回调
        def on_change(value):
            config_service.set_value("building_config", config_key, value)
            if save_callback:
                save_callback("building_config", config_key, value)
        
        dropdown = create_dropdown(
            current_value=current_value,
            width=USER_DROPDOWN_WIDTH,
            config=config,
            option_loader=option_manager.get_option_loader("building_level", max_level=40),
            on_change=on_change,
        )
        
        return ft.Row([
            ft.Text(f"{label}:", width=60, size=14, color=theme_colors["text_secondary"]),
            dropdown,
        ], spacing=10)
    
    # ========== 主帅主城建筑配置 ==========
    commander_buildings = []
    
    # 使用循环创建所有建筑下拉框
    building_configs = [
        ("主帅主城_城市", "城市", "17"),
        ("主帅主城_兵工", "兵工", "17"),
        ("主帅主城_陆军", "陆军", "14"),
        ("主帅主城_空军", "空军", "03"),
        ("主帅主城_商业", "商业", "04"),
        ("主帅主城_补给", "补给", "03"),
        ("主帅主城_内塔", "内塔", "04"),
        ("主帅主城_村庄", "村庄", "03"),
        ("主帅主城_资源", "资源", "03"),
        ("主帅主城_军工", "军工", "03"),
        ("主帅主城_港口", "港口", "03"),
        ("主帅主城_外塔", "外塔", "03"),
    ]
    
    for config_key, label, default_value in building_configs:
        commander_buildings.append(create_building_dropdown(config_key, label, default_value))
    
    # 创建主帅主城卡片
    commander_card = create_managed_card(
        manager=manager,
        title="主帅主城",
        icon="CASTLE",
        subtitle="设置主帅主城建筑等级",
        controls=commander_buildings,
        enabled=True,
        config=config,
    )
    
    # ========== 副将主城建筑配置 ==========
    deputy_buildings = []
    
    deputy_configs = [
        ("副将主城_城市", "城市", "15"),
        ("副将主城_兵工", "兵工", "10"),
        ("副将主城_陆军", "陆军", "10"),
        ("副将主城_空军", "空军", "03"),
        ("副将主城_商业", "商业", "04"),
        ("副将主城_补给", "补给", "03"),
        ("副将主城_内塔", "内塔", "03"),
        ("副将主城_村庄", "村庄", "03"),
        ("副将主城_资源", "资源", "03"),
        ("副将主城_军工", "军工", "03"),
        ("副将主城_港口", "港口", "03"),
        ("副将主城_外塔", "外塔", "03"),
    ]
    
    for config_key, label, default_value in deputy_configs:
        deputy_buildings.append(create_building_dropdown(config_key, label, default_value))
    
    # 创建副将主城卡片
    deputy_card = create_managed_card(
        manager=manager,
        title="副将主城",
        icon="ACCOUNT_BALANCE",
        subtitle="设置副将主城建筑等级",
        controls=deputy_buildings,
        enabled=True,
        config=config,
    )
    
    # ========== 小号主城建筑配置 ==========
    minor_buildings = []
    
    minor_configs = [
        ("小号主城_城市", "城市", "15"),
        ("小号主城_兵工", "兵工", "10"),
        ("小号主城_陆军", "陆军", "10"),
        ("小号主城_空军", "空军", "03"),
        ("小号主城_商业", "商业", "04"),
        ("小号主城_补给", "补给", "03"),
        ("小号主城_内塔", "内塔", "03"),
        ("小号主城_村庄", "村庄", "03"),
        ("小号主城_资源", "资源", "03"),
        ("小号主城_军工", "军工", "03"),
        ("小号主城_港口", "港口", "03"),
        ("小号主城_外塔", "外塔", "03"),
    ]
    
    for config_key, label, default_value in minor_configs:
        minor_buildings.append(create_building_dropdown(config_key, label, default_value))
    
    # 创建小号主城卡片
    minor_card = create_managed_card(
        manager=manager,
        title="小号主城",
        icon="HOUSE",
        subtitle="设置小号主城建筑等级",
        controls=minor_buildings,
        enabled=True,
        config=config,
    )
    
    # ========== 资源号建筑配置 ==========
    resource_buildings = []
    
    resource_configs = [
        ("资源号_城市", "城市", "05"),
        ("资源号_兵工", "兵工", "05"),
        ("资源号_陆军", "陆军", "05"),
        ("资源号_空军", "空军", "03"),
        ("资源号_商业", "商业", "04"),
        ("资源号_补给", "补给", "03"),
        ("资源号_内塔", "内塔", "03"),
        ("资源号_村庄", "村庄", "03"),
        ("资源号_资源", "资源", "03"),
        ("资源号_军工", "军工", "03"),
        ("资源号_港口", "港口", "03"),
        ("资源号_外塔", "外塔", "03"),
    ]
    
    for config_key, label, default_value in resource_configs:
        resource_buildings.append(create_building_dropdown(config_key, label, default_value))
    
    # 创建资源号卡片
    resource_card = create_managed_card(
        manager=manager,
        title="资源号",
        icon="WAREHOUSE",
        subtitle="设置资源号建筑等级",
        controls=resource_buildings,
        enabled=True,
        config=config,
    )
    
    # 将所有卡片添加到主容器
    section_container.controls.extend([
        commander_card,
        deputy_card,
        minor_card,
        resource_card,
    ])
    
    # 返回配置区和管理器
    return section_container, manager


# ========== 测试代码 ==========
if __name__ == "__main__":
    import flet as ft
    
    def main(page: ft.Page):
        config = UIConfig()
        page.title = "建筑配置区测试"
        page.window_width = 500
        page.window_height = 600
        page.padding = 20
        
        # 创建建筑配置区
        section, _ = create_building_config_section(config=config)
        
        # 添加标题
        title = ft.Text("🏗️ 建筑配置区最终版", size=20, weight=ft.FontWeight.BOLD)
        
        # 添加说明
        description = ft.Text(
            "所有下拉框直接使用简化选项管理器\n"
            "选项集中管理，实现方式简单直接",
            size=12,
            color=config.当前主题颜色["text_secondary"]
        )
        
        page.add(ft.Column([
            title,
            ft.Divider(height=10),
            description,
            ft.Divider(height=20),
            section,
        ], spacing=10))
    
    ft.run(main)