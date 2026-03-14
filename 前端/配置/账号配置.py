# -*- coding: utf-8 -*-
"""
账号配置 - 配置层

设计思路:
    定义账号相关的卡片配置。
    固定15个账号栏，开关控制参与挂机状态。

功能:
    1. 15个账号卡片配置
    2. 每个账号包含：统帅种类、输入框、平台
    3. 开关控制参与挂机状态

数据来源:
    静态配置数据。
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


MAX_ACCOUNTS = 15
DEFAULT_AUTHORIZED_COUNT = 15


def create_account_config(index: int) -> dict:
    """创建单个账号配置"""
    is_first = (index == 1)
    default_role = "主帅" if is_first else "副帅"
    
    return {
        "card_name": f"{index:02d}账号",
        "title": f"{index:02d}账号",
        "icon": "ACCOUNT_CIRCLE",
        "card_type": "switch_dropdown",
        "enabled": True,
        "controls": [
            {
                "type": "dropdown",
                "label": "统帅种类",
                "config_key": "统帅种类",
                "options": ["主帅", "副帅"],
                "default": default_role,
                "width": 80,
            },
            {
                "type": "textfield",
                "label": "输入框",
                "config_key": "输入框",
                "default": "",
                "width": 100,
            },
            {
                "type": "dropdown",
                "label": "平台",
                "config_key": "平台",
                "options": ["Tap", "九游", "Fan", "小7", "Vivo", "Opop"],
                "default": "Tap",
                "width": 80,
            },
        ],
    }


账号卡片配置 = {}
for i in range(1, MAX_ACCOUNTS + 1):
    账号卡片配置[f"{i:02d}账号"] = create_account_config(i)
