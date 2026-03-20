# -*- coding: utf-8 -*-
"""
自动打野配置 - 配置层

设计思路:
    定义自动打野相关的卡片配置。

功能:
    自动打野卡片配置

数据来源:
    静态配置数据。
"""

# ==================== 自动打野卡片 ====================

自动打野配置 = {
    "card_type": "switch_dropdown",
    "title": "自动打野",
    "icon": "EXPLORE",
    "subtitle": "开启后执行自动打野任务",
    "enabled": True,
    "switch_config": {
        "config_key": "开关",
        "default_value": True,
    },
    "dropdown_configs": [],
}


# ==================== 所有卡片配置 ====================

打野卡片配置 = {
    "自动打野": 自动打野配置,
}
