# -*- coding: utf-8 -*-
"""
模块名称：GlobalConstants
设计思路: 定义全局使用的常量
模块隔离: 纯常量模块，无依赖
"""

# *** 用户指定变量 - AI不得修改, 变量值必须生效 ***
USER_APP_NAME = "二战风云辅助"  # 应用名称
USER_APP_VERSION = "1.0.0"  # 应用版本
USER_SPACING = 10  # 默认间距
USER_CARD_HEIGHT = 70  # 默认卡片高度
USER_CARD_SPACING = USER_SPACING // 2  # 卡片间距
# *********************************


class GlobalConstants:
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


# *** 调试逻辑 ***
if __name__ == "__main__":
    print(f"应用名称: {GlobalConstants.APP_NAME}")
    print(f"应用版本: {GlobalConstants.APP_VERSION}")
    print(f"导航项数量: {len(GlobalConstants.NAV_ITEMS)}")
