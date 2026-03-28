# -*- coding: utf-8 -*-
"""
模块名称：SystemConfigSection
模块功能：系统配置区，包含挂机模式、指令速度等配置
实现步骤：
- 创建系统配置卡片
- 使用unload_options销毁策略
- 支持配置保存和加载
"""

import flet as ft
from typing import Dict, Any, List, Callable, Optional
import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

try:
    from 核心层.配置.界面配置 import UIConfig
    from 表示层.组件.复合.卡片组管理器 import CardGroupManager, create_managed_card
    from 业务层.服务.配置服务 import ConfigService
    from 核心层.常量.共享选项 import get_options_for_control
except ImportError:
    # 尝试相对导入
    from ..核心层.配置.界面配置 import UIConfig
    from ..表示层.组件.复合.卡片组管理器 import CardGroupManager, create_managed_card
    from ..业务层.服务.配置服务 import ConfigService
    from ..核心层.常量.共享选项 import get_options_for_control


# *** 用户指定变量: 变量值必须生效,AI不得更改数据 ***
USER_CARD_SPACING = 10  # 卡片间距
USER_SPACING = 10  # 通用间距
# *********************************


class SystemConfigSection:
    """系统配置区 - 使用unload_options策略"""
    
    @staticmethod
    def create(
        config: UIConfig = None,
        config_service: ConfigService = None,
        save_callback: Callable[[str, str, str], None] = None,
    ) -> tuple:
        if config is None:
            config = UIConfig()
        if config_service is None:
            config_service = ConfigService()
        
        theme_colors = config.当前主题颜色
        manager = CardGroupManager()
        card_data: Dict[str, Dict[str, Any]] = {}
        
        def create_card(
            card_id: str,
            title: str,
            icon: str,
            subtitle: str,
            controls_config: List[Dict[str, Any]],
            enabled: bool = True,
        ) -> ft.Container:
            saved_enabled = config_service.get_value(card_id, "enabled")
            if saved_enabled is None:
                saved_enabled = enabled
                if save_callback:
                    save_callback(card_id, "enabled", str(enabled))
            
            for control_config in controls_config:
                config_key = control_config.get("config_key")
                if config_key:
                    saved_value = config_service.get_value(card_id, config_key)
                    if saved_value is not None:
                        control_config["value"] = saved_value
                    else:
                        default_value = control_config.get("value")
                        if default_value is not None:
                            control_config["value"] = default_value
                            if save_callback:
                                save_callback(card_id, config_key, default_value)
            
            def handle_save(config_key: str, value: str):
                if card_id not in card_data:
                    card_data[card_id] = {}
                card_data[card_id][config_key] = value
                if save_callback:
                    save_callback(card_id, config_key, value)
            
            card = create_managed_card(
                manager=manager,
                title=title,
                icon=icon,
                subtitle=subtitle,
                enabled=saved_enabled,
                controls_config=controls_config,
                controls_per_row=4,
                on_save=handle_save,
                config=config,
            )
            
            return card
        
        card_list = []
        
        card_list.append(create_card(
            card_id="hangup_mode",
            title="挂机模式",
            icon="POWER_SETTINGS_NEW",
            subtitle="全自动:自动挂机,无需人为干预 | 半自动:点击头像,自动切换账号",
            controls_config=[
                {"type": "dropdown", "config_key": "挂机模式", "label": "模式选择:", "value": "全自动", "options": get_options_for_control("控制1")},
            ],
        ))
        
        card_list.append(create_card(
            card_id="command_speed",
            title="指令速度",
            icon="SPEED",
            subtitle="运行指令间隔频率(毫秒)，数值越小速度越快",
            controls_config=[
                {"type": "dropdown", "config_key": "指令速度", "label": "速度选择:", "value": "100", "options": get_options_for_control("控制3")},
            ],
        ))
        
        card_list.append(create_card(
            card_id="retry_count",
            title="尝试次数",
            icon="REFRESH",
            subtitle="连续操作失败达到最大尝试次数后,触发自动纠错系统",
            controls_config=[
                {"type": "dropdown", "config_key": "尝试次数", "label": "次数选择:", "value": "15", "options": get_options_for_control("控制4")},
            ],
        ))
        
        card_list.append(create_card(
            card_id="cache_limit",
            title="清缓限量",
            icon="DELETE_SWEEP",
            subtitle="达到设置系统缓存清理阈值(M)后,自动清理缓存",
            controls_config=[
                {"type": "dropdown", "config_key": "清缓限量", "label": "限量选择:", "value": "1.0", "options": get_options_for_control("控制5")},
            ],
        ))
        
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
        section, manager = SystemConfigSection.create(config=config, config_service=service)
        page.add(section)
    
    ft.app(target=main)
