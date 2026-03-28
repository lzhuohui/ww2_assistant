#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整配置测试 - 使用配置JSON和选项数据
测试下拉框与配置文件的集成
"""

import flet as ft
import json
import os
from 下拉框_合格版 import create_dropdown
from 建筑选项 import (
    get_city_options,
    get_building_levels,
    get_building_types,
    get_upgrade_strategies,
    get_user_preferences,
    get_config_value,
)


def load_building_config():
    """加载建筑配置"""
    config_path = os.path.join(os.path.dirname(__file__), "建筑配置.json")
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"配置文件不存在: {config_path}")
        return {}


def save_building_config(config):
    """保存建筑配置"""
    config_path = os.path.join(os.path.dirname(__file__), "建筑配置.json")
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        print(f"配置已保存到: {config_path}")
        return True
    except Exception as e:
        print(f"保存配置失败: {e}")
        return False


def main(page: ft.Page):
    page.title = "完整配置测试"
    page.window_width = 600
    page.window_height = 700
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    
    # 加载配置
    config = load_building_config()
    user_prefs = get_user_preferences()
    
    # 标题
    title = ft.Text("🏗️ 建筑配置完整测试", size=24, weight=ft.FontWeight.BOLD)
    
    # 配置信息
    config_info = ft.Container(
        content=ft.Column([
            ft.Text("📋 配置信息", size=18, weight=ft.FontWeight.W_500),
            ft.Text(f"版本: {config.get('version', '未知')}", size=14),
            ft.Text(f"最后修改: {config.get('last_modified', '未知')}", size=14),
            ft.Text(f"懒加载启用: {get_config_value('全局配置.性能设置.懒加载启用', False)}", size=14),
            ft.Divider(height=10),
        ], spacing=5),
        padding=10,
        border=ft.border.all(1, "#E9ECEF"),
        border_radius=8,
    )
    
    # 用户偏好
    prefs = user_prefs.get("快捷配置", {})
    quick_settings = ft.Container(
        content=ft.Column([
            ft.Text("⚡ 用户快捷设置", size=16, weight=ft.FontWeight.W_500),
            ft.Text(f"常用城市: {', '.join(prefs.get('常用城市', []))}", size=12),
            ft.Text(f"常用等级: {', '.join(prefs.get('常用等级', []))}", size=12),
            ft.Text(f"常用建筑: {', '.join(prefs.get('常用建筑', []))}", size=12),
        ], spacing=5),
        padding=10,
        border=ft.border.all(1, "#E9ECEF"),
        border_radius=8,
        bgcolor="#F8F9FA",
    )
    
    # 存储当前值
    current_values = {
        "city": user_prefs.get("最近使用的城市", "北京"),
        "level": user_prefs.get("最近使用的等级", "17"),
        "building": user_prefs.get("最近使用的建筑", "市政厅"),
        "strategy": "优先升级",
    }
    
    # 城市选择下拉框
    city_dropdown = create_dropdown(
        options=get_city_options(),
        current_value=current_values["city"],
        width=180,
        on_change=lambda v: on_value_change("city", v, city_dropdown),
    )
    
    # 建筑等级下拉框（懒加载）
    level_dropdown = create_dropdown(
        current_value=current_values["level"],
        width=100,
        option_loader=get_building_levels,
        on_change=lambda v: on_value_change("level", v, level_dropdown),
    )
    
    # 建筑类型下拉框
    building_dropdown = create_dropdown(
        options=get_building_types(),
        current_value=current_values["building"],
        width=180,
        on_change=lambda v: on_value_change("building", v, building_dropdown),
    )
    
    # 升级策略下拉框
    strategy_dropdown = create_dropdown(
        options=get_upgrade_strategies(),
        current_value=current_values["strategy"],
        width=200,
        on_change=lambda v: on_value_change("strategy", v, strategy_dropdown),
    )
    
    # 值变化处理
    def on_value_change(field, value, dropdown):
        current_values[field] = value
        print(f"{field} 更新为: {value}")
        
        # 更新用户偏好
        user_prefs[f"最近使用的{field}"] = value
        
        # 更新界面显示
        update_status()
    
    # 状态显示
    status_text = ft.Text("", size=14, color="#666666")
    
    def update_status():
        status = f"当前配置: {current_values['city']} - {current_values['building']} (等级{current_values['level']}) - {current_values['strategy']}"
        status_text.value = status
        page.update()
    
    # 保存按钮
    def save_config_click(e):
        # 更新配置
        config["用户偏好"] = user_prefs
        
        # 保存到文件
        if save_building_config(config):
            status_text.value = "✅ 配置已保存到建筑配置.json"
            status_text.color = "#4CAF50"
        else:
            status_text.value = "❌ 保存配置失败"
            status_text.color = "#F44336"
        
        page.update()
    
    save_button = ft.ElevatedButton(
        "💾 保存配置",
        icon="save",
        on_click=save_config_click,
        style=ft.ButtonStyle(
            bgcolor={"": "#0078D4"},
            color={"": "#FFFFFF"},
        )
    )
    
    # 重置按钮
    def reset_config_click(e):
        # 重置为默认值
        current_values.update({
            "city": "北京",
            "level": "17",
            "building": "市政厅",
            "strategy": "优先升级",
        })
        
        # 更新下拉框
        city_dropdown.set_value("北京")
        level_dropdown.set_value("17")
        building_dropdown.set_value("市政厅")
        strategy_dropdown.set_value("优先升级")
        
        status_text.value = "🔄 已重置为默认值"
        status_text.color = "#FF9800"
        page.update()
    
    reset_button = ft.OutlinedButton(
        "🔄 重置",
        on_click=reset_config_click,
    )
    
    # 测试区域
    test_area = ft.Container(
        content=ft.Column([
            ft.Text("🧪 测试区域", size=18, weight=ft.FontWeight.W_500),
            ft.Text("验证下拉框不推挤下方控件", size=14, color="#666666"),
            ft.Divider(height=10),
            
            ft.TextField(
                label="测试文本框",
                hint_text="下拉框打开时，这个控件的位置应该保持不变",
                width=300,
            ),
            
            ft.Row([
                ft.Checkbox(label="自动保存", value=True),
                ft.Checkbox(label="启用动画", value=True),
            ], spacing=20),
        ], spacing=15),
        padding=20,
        border=ft.border.all(1, "#E9ECEF"),
        border_radius=8,
        bgcolor="#FFFFFF",
    )
    
    # 主布局
    page.add(
        ft.Column([
            title,
            ft.Divider(height=20),
            
            config_info,
            ft.Divider(height=10),
            quick_settings,
            ft.Divider(height=20),
            
            ft.Text("🏙️ 城市选择:", size=16),
            city_dropdown,
            ft.Divider(height=10),
            
            ft.Text("📊 建筑等级:", size=16),
            level_dropdown,
            ft.Divider(height=10),
            
            ft.Text("🏗️ 建筑类型:", size=16),
            building_dropdown,
            ft.Divider(height=10),
            
            ft.Text("⚙️ 升级策略:", size=16),
            strategy_dropdown,
            ft.Divider(height=20),
            
            ft.Row([save_button, reset_button], spacing=10),
            ft.Divider(height=10),
            status_text,
            ft.Divider(height=20),
            
            test_area,
            ft.Divider(height=20),
            
            ft.Text("✅ 完整配置测试就绪", size=16, color="#4CAF50"),
            ft.Text("所有下拉框都使用配置和选项数据", size=14),
        ], spacing=15, scroll=ft.ScrollMode.AUTO)
    )
    
    # 初始状态
    update_status()
    
    print("=" * 60)
    print("完整配置测试")
    print("=" * 60)
    print(f"配置文件: 建筑配置.json")
    print(f"选项数据: 建筑选项.py")
    print(f"当前配置: {current_values}")
    print("=" * 60)


if __name__ == "__main__":
    ft.app(target=main)