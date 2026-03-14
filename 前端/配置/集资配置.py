# -*- coding: utf-8 -*-
"""
集资配置 - 配置层

设计思路:
    定义集资相关的卡片配置。

功能:
    1. 小号上贡卡片配置
    2. 分城纳租卡片配置

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
            "options": ["05级", "06级", "07级", "08级", "09级", "10级", "11级", "12级", "13级", "14级", "15级"],
            "default": "05级",
            "width": 80,
        },
        {
            "type": "dropdown",
            "label": "上贡限量",
            "config_key": "小号上贡_上贡限量",
            "options": ["2万", "3万", "4万", "5万", "6万", "7万", "8万", "9万", "10万", "11万", "12万", "13万", "14万", "15万", "16万", "17万", "18万", "19万", "20万"],
            "default": "2万",
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


# ==================== 分城纳租卡片 ====================

分城纳租配置 = {
    "card_name": "分城纳租",
    "title": "分城纳租",
    "icon": "ATTACH_MONEY",
    "subtitle": "设置分城纳租相关参数",
    "card_type": "standard",
    "controls_per_row": 2,
    "controls": [
        {
            "type": "dropdown",
            "label": "纳租限级",
            "config_key": "分城纳租_纳租限级",
            "options": ["05级", "06级", "07级", "08级", "09级", "10级", "11级", "12级", "13级", "14级", "15级"],
            "default": "05级",
            "width": 80,
        },
        {
            "type": "dropdown",
            "label": "纳租限量",
            "config_key": "分城纳租_纳租限量",
            "options": ["2万", "3万", "4万", "5万", "6万", "7万", "8万", "9万", "10万", "11万", "12万", "13万", "14万", "15万", "16万", "17万", "18万", "19万", "20万"],
            "default": "2万",
            "width": 80,
        },
    ],
}


# ==================== 所有卡片配置 ====================

集资卡片配置 = {
    "小号上贡": 小号上贡配置,
    "分城纳租": 分城纳租配置,
}
