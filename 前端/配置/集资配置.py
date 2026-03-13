# -*- coding: utf-8 -*-
"""
集资配置 - 配置层

设计思路:
    定义集资相关的卡片配置。

功能:
    1. 小号上贡卡片配置
    2. 分成纳租卡片配置

数据来源:
    部分数据来自按键精灵脚本。
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


# ==================== 小号上贡卡片 ====================

小号上贡配置 = {
    "card_name": "小号上贡",
    "title": "小号上贡",
    "icon": "UPLOAD",
    "subtitle": "设置小号上贡相关参数",
    "card_type": "standard",
    "controls_per_row": 2,
    "controls": [
        {
            "type": "dropdown",
            "label": "上贡限级",
            "config_key": "小号上贡_上贡限级",
            "options": ["1级", "2级", "3级", "4级", "5级", "6级", "7级", "8级", "9级", "10级"],
            "default": "5级",
            "width": 80,
        },
        {
            "type": "dropdown",
            "label": "上贡限量",
            "config_key": "小号上贡_上贡限量",
            "options": ["100", "200", "300", "400", "500", "600", "700", "800", "900", "1000"],
            "default": "500",
            "width": 80,
        },
        {
            "type": "dropdown",
            "label": "主要统帅",
            "config_key": "小号上贡_主要统帅",
            "options": ["统帅A", "统帅B", "统帅C", "统帅D", "统帅E"],
            "default": "统帅A",
            "width": 80,
        },
        {
            "type": "dropdown",
            "label": "备用统帅",
            "config_key": "小号上贡_备用统帅",
            "options": ["统帅A", "统帅B", "统帅C", "统帅D", "统帅E"],
            "default": "统帅B",
            "width": 80,
        },
    ],
}


# ==================== 分成纳租卡片 ====================

分成纳租配置 = {
    "card_name": "分成纳租",
    "title": "分成纳租",
    "icon": "ATTACH_MONEY",
    "subtitle": "设置分成纳租相关参数",
    "card_type": "standard",
    "controls_per_row": 2,
    "controls": [
        {
            "type": "dropdown",
            "label": "分成比例",
            "config_key": "分成纳租_分成比例",
            "options": ["10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%"],
            "default": "50%",
            "width": 80,
        },
        {
            "type": "dropdown",
            "label": "纳租方式",
            "config_key": "分成纳租_纳租方式",
            "options": ["按日", "按周", "按月"],
            "default": "按日",
            "width": 80,
        },
    ],
}


# ==================== 所有卡片配置 ====================

集资卡片配置 = {
    "小号上贡": 小号上贡配置,
    "分成纳租": 分成纳租配置,
}
