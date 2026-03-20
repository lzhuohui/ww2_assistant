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
    "挂机模式": {
        "card_type": "switch_dropdown",
        "title": "挂机模式",
        "icon": "POWER_SETTINGS_NEW",
        "subtitle": "全自动:自动挂机,无需人为干预 | 半自动:点击头像,自动切换账号",
        "enabled": True,
        "switch_config": {
            "config_key": "挂机模式_开关",
            "default_value": True,
        },
        "dropdown_configs": [
            {
                "config_key": "挂机模式",
                "label": "模式选择:",
                "options": ["自动", "手动"],
                "default_value": "自动",
            },
        ],
    },
    "指令速度": {
        "card_type": "switch_dropdown",
        "title": "指令速度",
        "icon": "SPEED",
        "subtitle": "运行指令间隔频率(毫秒)，数值越小速度越快",
        "enabled": True,
        "switch_config": {
            "config_key": "指令速度_开关",
            "default_value": True,
        },
        "dropdown_configs": [
            {
                "config_key": "指令速度",
                "label": "速度选择:",
                "options": ["100毫秒", "150毫秒", "200毫秒", "250毫秒", "300毫秒", "350毫秒", "400毫秒", "450毫秒", "500毫秒"],
                "default_value": "100",
                "unit": "毫秒",
            },
        ],
    },
    "尝试次数": {
        "card_type": "switch_dropdown",
        "title": "尝试次数",
        "icon": "REFRESH",
        "subtitle": "连续操作失败达到最大尝试次数后,触发自动纠错系统",
        "enabled": True,
        "switch_config": {
            "config_key": "尝试次数_开关",
            "default_value": True,
        },
        "dropdown_configs": [
            {
                "config_key": "尝试次数",
                "label": "次数选择:",
                "options": ["10次", "15次", "20次", "25次", "30次"],
                "default_value": "10",
                "unit": "次",
            },
        ],
    },
    "清缓限量": {
        "card_type": "switch_dropdown",
        "title": "清缓限量",
        "icon": "DELETE_SWEEP",
        "subtitle": "达到设置系统缓存清理阈值(M)后,自动清理缓存",
        "enabled": True,
        "switch_config": {
            "config_key": "清缓限量_开关",
            "default_value": True,
        },
        "dropdown_configs": [
            {
                "config_key": "清缓限量",
                "label": "限量选择:",
                "options": ["1.0M", "1.5M", "2.0M", "2.5M", "3.0M", "3.5M", "4.0M", "4.5M", "5.0M"],
                "default_value": "1.0",
                "unit": "M",
            },
        ],
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
