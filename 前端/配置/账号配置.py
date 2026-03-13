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
DEFAULT_AUTHORIZED_COUNT = 3


def create_account_config(index: int) -> dict:
    """创建单个账号配置"""
    return {
        "card_name": f"{index:02d}账号",
        "title": f"{index:02d}账号",
        "icon": "ACCOUNT_CIRCLE",
        "card_type": "switch_dropdown",
        "enabled": False,
        "settings": [
            {
                "type": "dropdown",
                "label": "统帅种类",
                "config_key": f"账号{index:02d}_统帅种类",
                "options": ["统帅A", "统帅B", "统帅C", "统帅D", "统帅E"],
                "default": "统帅A",
                "width": 80,
            },
            {
                "type": "textfield",
                "label": "输入框",
                "config_key": f"账号{index:02d}_输入框",
                "default": "",
                "width": 100,
            },
            {
                "type": "dropdown",
                "label": "平台",
                "config_key": f"账号{index:02d}_平台",
                "options": ["平台1", "平台2", "平台3", "平台4", "平台5"],
                "default": "平台1",
                "width": 80,
            },
        ],
    }


账号卡片配置 = {}
for i in range(1, MAX_ACCOUNTS + 1):
    账号卡片配置[f"{i:02d}账号"] = create_account_config(i)
