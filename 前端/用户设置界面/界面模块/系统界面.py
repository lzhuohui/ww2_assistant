# -*- coding: utf-8 -*-
"""
模块名称：系统界面 | 层级：界面模块层
设计思路：
    系统界面，包含挂机模式、指令速度、尝试次数、清缓限量等设置卡片。
    使用配置管理器获取和保存配置值。

功能：
    1. 挂机模式设置
    2. 指令速度设置
    3. 尝试次数设置
    4. 清缓限量设置

对外接口：
    - create(): 创建系统界面
"""

import flet as ft
from typing import Callable
from 前端.用户设置界面.配置.界面配置 import 界面配置
from 前端.用户设置界面.配置.配置管理器 import ConfigManager
from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider
from 前端.用户设置界面.组件模块.通用卡片 import UniversalCard
from 前端.用户设置界面.组件模块.功能容器 import FunctionContainer
from 前端.用户设置界面.单元模块.下拉框 import Dropdown
from 前端.用户设置界面.单元模块.文本标签 import LabelText

# *** 用户指定变量 - AI不得修改 ***
# *********************************


class SystemInterface:
    """系统界面 - 界面模块层"""
    
    @staticmethod
    def create(page: ft.Page = None, on_refresh: Callable[[], None] = None) -> ft.Container:
        """
        创建系统界面
        
        参数：
            page: 页面对象（可选，用于更新页面显示）
            on_refresh: 刷新回调
        
        返回：
            ft.Container: 系统界面容器
        """
        配置 = 界面配置()
        
        try:
            config_manager = ConfigManager()
        except ImportError:
            config_manager = None
        
        def on_value_change(card_name: str, config_key: str, value):
            """值变化回调 - 保存配置"""
            print(f"配置变化: {card_name}.{config_key} = {value}")
            if config_manager:
                config_manager.set_value(card_name, config_key, value)
        
        def create_dropdown_control(label: str, options: list, value: str, card_name: str, config_key: str, width: int = None):
            """创建下拉框控件"""
            dropdown = Dropdown.create(
                options=options,
                value=value,
                width=width,
                on_change=lambda v: on_value_change(card_name, config_key, v),
            )
            
            label_text = LabelText.create(
                text=label,
                role="secondary",
                size=14,
                enabled=True
            )
            
            return ft.Row(
                [label_text, dropdown],
                alignment=ft.MainAxisAlignment.END,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8,
                expand=True,
            )
        
        auto_mode_value = config_manager.get_value("挂机模式", "挂机模式", "自动") if config_manager else "自动"
        auto_mode_control = create_dropdown_control(
            label="模式选择:",
            options=["自动", "手动"],
            value=auto_mode_value,
            card_name="挂机模式",
            config_key="挂机模式",
        )
        
        auto_mode_card = UniversalCard.create(
            title="挂机模式",
            icon="POWER_SETTINGS_NEW",
            subtitle="全自动:自动挂机,无需人为干预 | 半自动:点击头像,自动切换账号",
            enabled=True,
            controls=[auto_mode_control],
        )
        
        speed_value = config_manager.get_value("指令速度", "指令速度", "100毫秒") if config_manager else "100毫秒"
        speed_control = create_dropdown_control(
            label="速度选择:",
            options=["100毫秒", "150毫秒", "200毫秒", "250毫秒", "300毫秒", "350毫秒", "400毫秒", "450毫秒", "500毫秒"],
            value=speed_value,
            card_name="指令速度",
            config_key="指令速度",
        )
        
        speed_card = UniversalCard.create(
            title="指令速度",
            icon="SPEED",
            subtitle="运行指令间隔频率(毫秒)，数值越小速度越快",
            enabled=True,
            controls=[speed_control],
        )
        
        retry_value = config_manager.get_value("尝试次数", "尝试次数", "10次") if config_manager else "10次"
        retry_control = create_dropdown_control(
            label="次数选择:",
            options=["10次", "15次", "20次", "25次", "30次"],
            value=retry_value,
            card_name="尝试次数",
            config_key="尝试次数",
        )
        
        retry_card = UniversalCard.create(
            title="尝试次数",
            icon="REFRESH",
            subtitle="连续操作失败达到最大尝试次数后,触发自动纠错系统",
            enabled=True,
            controls=[retry_control],
        )
        
        cache_value = config_manager.get_value("清缓限量", "清缓限量", "1.0M") if config_manager else "1.0M"
        cache_control = create_dropdown_control(
            label="限量选择:",
            options=["1.0M", "1.5M", "2.0M", "2.5M", "3.0M", "3.5M", "4.0M", "4.5M", "5.0M"],
            value=cache_value,
            card_name="清缓限量",
            config_key="清缓限量",
        )
        
        cache_card = UniversalCard.create(
            title="清缓限量",
            icon="DELETE_SWEEP",
            subtitle="达到设置系统缓存清理阈值(M)后,自动清理缓存",
            enabled=True,
            controls=[cache_control],
        )
        
        return FunctionContainer.create(
            config=配置,
            title="系统设置",
            icon="SETTINGS",
            cards=[auto_mode_card, speed_card, retry_card, cache_card],
            expand=True,
        )


# *** 调试逻辑 ***
if __name__ == "__main__":
    配置 = 界面配置()
    ThemeProvider.initialize(配置)
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        page.add(SystemInterface.create())
    ft.run(main)
