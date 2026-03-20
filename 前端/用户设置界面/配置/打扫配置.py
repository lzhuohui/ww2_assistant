# -*- coding: utf-8 -*-
"""
打扫配置 - 配置层

设计思路:
    定义打扫相关的卡片配置，包括打扫城区和打扫政区。

功能:
    1. 打扫城区卡片配置
    2. 打扫政区卡片配置

数据来源:
    静态配置数据。
"""

# ==================== 打扫城区卡片 ====================

打扫城区配置 = {
    "card_type": "switch_dropdown",
    "title": "打扫城区",
    "icon": "CLEANING_SERVICES",
    "subtitle": "开启后执行打扫城区任务",
    "enabled": True,
    "switch_config": {
        "config_key": "开关",
        "default_value": True,
    },
    "dropdown_configs": [],
}


# ==================== 打扫政区卡片 ====================

打扫政区配置 = {
    "card_type": "switch_dropdown",
    "title": "打扫政区",
    "icon": "LOCATION_CITY",
    "subtitle": "开启后执行打扫政区任务",
    "enabled": True,
    "switch_config": {
        "config_key": "开关",
        "default_value": True,
    },
    "dropdown_configs": [],
}


# ==================== 所有卡片配置 ====================

打扫卡片配置 = {
    "打扫城区": 打扫城区配置,
    "打扫政区": 打扫政区配置,
}
