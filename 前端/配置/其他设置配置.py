# -*- coding: utf-8 -*-
"""
其他设置配置 - 配置层

设计思路:
    定义其他设置相关的卡片配置。

功能:
    1. 打扫城区卡片配置
    2. 打扫政区卡片配置
    3. 自动打野卡片配置

数据来源:
    静态配置数据。
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


# ==================== 打扫城区卡片 ====================

打扫城区配置 = {
    "card_name": "打扫城区",
    "title": "打扫城区",
    "icon": "CLEANING_SERVICES",
    "subtitle": "开启后执行打扫城区任务",
    "card_type": "switch_dropdown",
    "enabled": True,
    "settings": [],
}


# ==================== 打扫政区卡片 ====================

打扫政区配置 = {
    "card_name": "打扫政区",
    "title": "打扫政区",
    "icon": "DOMAIN",
    "subtitle": "开启后执行打扫政区任务",
    "card_type": "switch_dropdown",
    "enabled": True,
    "settings": [],
}


# ==================== 自动打野卡片 ====================

自动打野配置 = {
    "card_name": "自动打野",
    "title": "自动打野",
    "icon": "EXPLORE",
    "subtitle": "开启后执行自动打野任务",
    "card_type": "switch_dropdown",
    "enabled": True,
    "settings": [],
}


# ==================== 所有卡片配置 ====================

其他卡片配置 = {
    "打扫城区": 打扫城区配置,
    "打扫政区": 打扫政区配置,
    "自动打野": 自动打野配置,
}
