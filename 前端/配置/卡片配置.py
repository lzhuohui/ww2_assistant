# -*- coding: utf-8 -*-
"""
卡片配置 - 配置层

设计思路:
    定义所有卡片的配置格式，实现配置驱动架构。
    统一配置格式，便于管理和扩展。

功能:
    1. 定义卡片配置格式
    2. 提供卡片配置数据
    3. 支持配置扩展

数据来源:
    静态配置数据。

使用场景:
    被 ConfigManager 调用。
"""

# 卡片配置字典
卡片配置 = {
    "基础设置": {
        "card_type": "standard",  # 卡片类型：standard/color_blocks
        "title": "基础设置",
        "icon": "SETTINGS",
        "subtitle": "通用配置描述",
        "controls_per_row": 2,
        "controls": [
            {
                "type": "dropdown",
                "label": "挂机模式:",
                "options": ["自动挂机", "手动挂机", "半自动挂机"],
                "value": "自动挂机",
                "config_key": "挂机模式"
            },
            {
                "type": "dropdown",
                "label": "指令速度:",
                "options": ["快速", "正常", "慢速"],
                "value": "正常",
                "config_key": "指令速度"
            },
            {
                "type": "dropdown",
                "label": "尝试次数:",
                "options": ["10", "15", "20", "25", "30"],
                "value": "15",
                "config_key": "尝试次数"
            },
            {
                "type": "dropdown",
                "label": "清换限量:",
                "options": ["1.0", "1.5", "2.0", "2.5", "3.0", "3.5", "4.0", "4.5", "5.0"],
                "value": "1.0",
                "config_key": "清换限量"
            }
        ]
    },
    "主题设置": {
        "card_type": "color_blocks",  # 色块类型卡片
        "title": "主题设置",
        "icon": "PALETTE",
        "subtitle": "主题配置描述",
        "controls_per_row": 6,
        "blocks_config": {
            "type": "theme",  # 色块类型：theme/palette/custom
            "items": [
                {"name": "浅色", "color": "#FFFFFF"},
                {"name": "深色", "color": "#1A1A2E"},
                {"name": "日出", "color": "#FFE4B5"},
                {"name": "捕捉", "color": "#98FB98"},
                {"name": "聚焦", "color": "#87CEEB"},
            ],
            "selected": "深色",
            "config_key": "主题模式",
            "supports_deselect": False,  # 不支持取消选择
        }
    },
    "调色板设置": {
        "card_type": "color_blocks",
        "title": "调色板",
        "icon": "CONTRAST",
        "subtitle": "高对比度调色板配置",
        "controls_per_row": 4,
        "blocks_config": {
            "type": "palette",
            "items": [
                {"name": "水生", "color": "#006994"},
                {"name": "沙漠", "color": "#C19A6B"},
                {"name": "黄昏", "color": "#FF6B6B"},
                {"name": "夜空", "color": "#2C3E50"},
            ],
            "selected": None,
            "config_key": "调色板模式",
            "supports_deselect": True,  # 支持取消选择
        }
    }
}
