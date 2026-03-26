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


# *** 用户指定变量: 变量值必须生效,AI不得更改数据 ***
USER_APP_NAME = "二战风云辅助工具"  # 应用名称
USER_NAV_ITEMS = [  # 导航项列表
    {"id": "系统", "icon": "SETTINGS", "label": "系统配置"},
    {"id": "策略", "icon": "ROCKET_LAUNCH", "label": "策略配置"},
    {"id": "任务", "icon": "ASSIGNMENT", "label": "任务"},
    {"id": "建筑", "icon": "APARTMENT", "label": "建筑"},
    {"id": "集资", "icon": "ATTACH_MONEY", "label": "集资"},
    {"id": "账号", "icon": "ACCOUNT_CIRCLE", "label": "账号设置"},
    {"id": "打扫", "icon": "CLEANING_SERVICES", "label": "打扫"},
    {"id": "打野", "icon": "EXPLORE", "label": "打野"},
    {"id": "配置方案", "icon": "FOLDER", "label": "配置方案"},
    {"id": "个性化", "icon": "PALETTE", "label": "个性化"},
    {"id": "关于", "icon": "INFO", "label": "关于"},
]
USER_AUTHORIZED_COUNT = 15  # 授权账号数量
# *********************************


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
