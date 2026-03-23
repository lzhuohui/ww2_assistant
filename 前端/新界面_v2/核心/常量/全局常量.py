# -*- coding: utf-8 -*-
"""
模块名称：全局常量
设计思路: 定义全局使用的常量
模块隔离: 纯常量模块，无依赖
"""

# *** 用户指定变量 - AI不得修改 ***
USER_APP_NAME = "二战风云辅助"
USER_APP_VERSION = "1.0.0"
USER_SPACING = 10
USER_CARD_HEIGHT = 70
USER_CARD_SPACING = USER_SPACING // 2
# *********************************


class 全局常量:
    """全局常量定义"""
    
    APP_NAME = USER_APP_NAME
    APP_VERSION = USER_APP_VERSION
    SPACING = USER_SPACING
    CARD_HEIGHT = USER_CARD_HEIGHT
    CARD_SPACING = USER_CARD_SPACING
    
    NAV_ITEMS = [
        {"id": "系统", "icon": "SETTINGS"},
        {"id": "策略", "icon": "ROCKET_LAUNCH"},
        {"id": "任务", "icon": "ASSIGNMENT"},
        {"id": "建筑", "icon": "DOMAIN"},
        {"id": "集资", "icon": "SHOPPING_CART"},
        {"id": "账号", "icon": "ACCOUNT_CIRCLE"},
        {"id": "打扫", "icon": "CLEANING_SERVICES"},
        {"id": "打野", "icon": "EXPLORE"},
        {"id": "个性化", "icon": "PALETTE"},
        {"id": "关于", "icon": "INFO"},
    ]
    
    MAX_ACCOUNTS = 15
    DEFAULT_ANIMATION_DURATION = 200
    DEFAULT_DESTROY_DELAY = 30
