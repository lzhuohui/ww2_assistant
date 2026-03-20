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

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


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