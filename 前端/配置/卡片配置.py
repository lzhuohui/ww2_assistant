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
        "title": "主题设置",
        "icon": "PALETTE",
        "subtitle": "主题配置描述",
        "controls_type": "theme_block",
        "themes": ["浅色", "深色", "日出", "捕捉", "聚焦"],
        "selected": "深色",
        "config_key": "主题模式"
    },
    "调色板设置": {
        "title": "调色板",
        "icon": "CONTRAST",
        "subtitle": "高对比度调色板配置",
        "controls_type": "palette_block",
        "palettes": ["水生", "沙漠", "黄昏", "夜空"],
        "selected": None,
        "config_key": "调色板模式"
    }
}
