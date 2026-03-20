# -*- coding: utf-8 -*-
"""
集资配置 - 配置层

设计思路:
    定义集资相关的卡片配置。
    使用配置驱动架构，统一配置格式。

功能:
    1. 小号上贡卡片配置
    2. 分城纳租卡片配置

数据来源:
    部分数据来自按键精灵脚本。

使用场景:
    被 ConfigManager 调用。
"""

# 等级选项 (05-15级)
LEVELS = [f"{i:02d}级" for i in range(5, 16)]

# 数量选项 (2-20万)
AMOUNTS = [f"{i}万" for i in range(2, 21)]

# 统帅选项
COMMANDERS = ["统帅A", "统帅B", "统帅C", "统帅D", "统帅E"]


# ==================== 小号上贡卡片 ====================

小号上贡配置 = {
    "card_type": "switch_dropdown",
    "title": "小号上贡",
    "icon": "UPLOAD",
    "subtitle": "设置小号上贡相关参数",
    "enabled": True,
    "switch_config": {
        "config_key": "上贡开关",
        "default_value": True,
    },
    "dropdown_configs": [
        {
            "config_key": "上贡限级",
            "label": "上贡限级:",
            "options": LEVELS,
            "default_value": "05",
            "unit": "级",
        },
        {
            "config_key": "上贡限量",
            "label": "上贡限量:",
            "options": AMOUNTS,
            "default_value": "2",
            "unit": "万",
        },
        {
            "config_key": "主要统帅",
            "label": "主要统帅:",
            "options": COMMANDERS,
            "default_value": "统帅A",
        },
        {
            "config_key": "备用统帅",
            "label": "备用统帅:",
            "options": COMMANDERS,
            "default_value": "统帅B",
        },
    ],
    "controls_per_row": 2,
}


# ==================== 分城纳租卡片 ====================

分城纳租配置 = {
    "card_type": "switch_dropdown",
    "title": "分城纳租",
    "icon": "ATTACH_MONEY",
    "subtitle": "设置分城纳租相关参数",
    "enabled": True,
    "switch_config": {
        "config_key": "纳租开关",
        "default_value": True,
    },
    "dropdown_configs": [
        {
            "config_key": "纳租限级",
            "label": "纳租限级:",
            "options": LEVELS,
            "default_value": "05",
            "unit": "级",
        },
        {
            "config_key": "纳租限量",
            "label": "纳租限量:",
            "options": AMOUNTS,
            "default_value": "2",
            "unit": "万",
        },
    ],
    "controls_per_row": 2,
}


# ==================== 所有卡片配置 ====================

集资卡片配置 = {
    "小号上贡": 小号上贡配置,
    "分城纳租": 分城纳租配置,
}
