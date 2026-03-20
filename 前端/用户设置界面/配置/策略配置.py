# -*- coding: utf-8 -*-
"""
策略配置 - 配置层

设计思路:
    定义所有策略设置的配置格式，实现配置驱动架构。
    统一配置格式，便于管理和扩展。

功能:
    1. 定义策略配置格式
    2. 提供策略配置数据
    3. 支持配置扩展

数据来源:
    静态配置数据。

使用场景:
    被 ConfigManager 调用。
"""

# 策略配置字典
策略配置 = {
    "建筑速建": {
        "card_type": "switch_dropdown",  # 卡片类型：switch_dropdown
        "title": "建筑速建",
        "icon": "ROCKET_LAUNCH",
        "subtitle": "开启自动加速建设功能",
        "enabled": True,
        "switch_config": {
            "config_key": "速建开关",
            "default_value": True,
        },
        "dropdown_configs": [
            {
                "config_key": "速建限级",
                "label": "速建限级:",
                "options": ["05级", "06级", "07级", "08级", "09级", "10级", "11级", "12级", "13级", "14级", "15级"],
                "default_value": "08",
                "unit": "级",
            },
            {
                "config_key": "速建类型",
                "label": "建筑类型:",
                "options": ["城资建筑", "城市建筑", "资源建筑"],
                "default_value": "城资建筑",
            },
        ],
    },
    "资源速产": {
        "card_type": "switch_dropdown",
        "title": "资源速产",
        "icon": "BOLT",
        "subtitle": "开启自动加速生产功能",
        "enabled": True,
        "switch_config": {
            "config_key": "速产开关",
            "default_value": True,
        },
        "dropdown_configs": [
            {
                "config_key": "速产限级",
                "label": "速产限级:",
                "options": ["05级", "06级", "07级", "08级", "09级", "10级", "11级", "12级", "13级", "14级", "15级"],
                "default_value": "07",
                "unit": "级",
            },
            {
                "config_key": "速产类型",
                "label": "策略类型:",
                "options": ["平衡资源", "战时经济", "钢铁熔炉", "橡胶采集", "石油开采"],
                "default_value": "平衡资源",
            },
        ],
    },
    "策点保留": {
        "card_type": "switch_dropdown",
        "title": "策点保留",
        "icon": "SAVINGS",
        "subtitle": "达到设置保留的策略点数后允许使用策略",
        "enabled": True,
        "switch_config": {
            "config_key": "保留开关",
            "default_value": True,
        },
        "dropdown_configs": [
            {
                "config_key": "保留点数",
                "label": "保留点数:",
                "options": ["30点", "60点", "90点", "120点", "150点", "180点", "210点", "240点"],
                "default_value": "60",
                "unit": "点",
            },
        ],
    },
}
