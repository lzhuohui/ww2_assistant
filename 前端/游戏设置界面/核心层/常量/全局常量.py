# -*- coding: utf-8 -*-
"""
模块名称：GlobalConstants
模块功能：全局常量定义
实现步骤：
- 定义应用名称
- 定义导航项
- 定义功能项
"""

from typing import List, Dict, Any


USER_APP_NAME = "二战风云辅助工具"
USER_NAV_ITEMS = [
    {"id": "系统", "icon": "SETTINGS", "label": "系统配置"},
    {"id": "策略", "icon": "ROCKET_LAUNCH", "label": "策略配置"},
    {"id": "账号", "icon": "ACCOUNT_CIRCLE", "label": "账号设置"},
    {"id": "个性化", "icon": "PALETTE", "label": "个性化"},
]
USER_AUTHORIZED_COUNT = 15


class GlobalConstants:
    """全局常量"""
    
    APP_NAME = USER_APP_NAME
    NAV_ITEMS = USER_NAV_ITEMS
    AUTHORIZED_COUNT = USER_AUTHORIZED_COUNT
    
    @staticmethod
    def get_nav_item_by_id(item_id: str) -> Dict[str, Any]:
        """根据ID获取导航项"""
        for item in USER_NAV_ITEMS:
            if item["id"] == item_id:
                return item
        return {}


# *** 标准测试格式: 仅调用被测模块,AI不得添加数据 ***
if __name__ == "__main__":
    print(f"应用名称: {GlobalConstants.APP_NAME}")
    print(f"导航项: {GlobalConstants.NAV_ITEMS}")
