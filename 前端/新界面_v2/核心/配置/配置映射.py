# -*- coding: utf-8 -*-
"""
模块名称：ConfigMapping
设计思路: 提供配置键名到按键精灵格式的映射
模块隔离: 核心层，不依赖其他层
"""

from typing import Dict, Any


class ConfigMapping:
    """配置映射 - 界面配置格式到按键精灵格式的映射"""
    
    CONTROL_MAPPING = {
        "hangup_mode.挂机模式": {"index": "控制1", "desc": "挂机模式"},
        "hangup_mode.enabled": {"index": "控制1_开关", "desc": "挂机模式开关"},
        "command_speed.指令速度": {"index": "控制3", "desc": "挂机速度"},
        "command_speed.enabled": {"index": "控制3_开关", "desc": "挂机速度开关"},
        "retry_count.尝试次数": {"index": "控制4", "desc": "尝试次数"},
        "retry_count.enabled": {"index": "控制4_开关", "desc": "尝试次数开关"},
        "cache_limit.清缓限量": {"index": "控制5", "desc": "缓存限制"},
        "cache_limit.enabled": {"index": "控制5_开关", "desc": "缓存限制开关"},
        "quick_build.速建限级": {"index": "控制6", "desc": "速建限级"},
        "quick_build.速建类型": {"index": "控制7", "desc": "速建类别"},
        "quick_build.enabled": {"index": "控制6_开关", "desc": "速建开关"},
        "quick_produce.速产限级": {"index": "控制8", "desc": "速产限级"},
        "quick_produce.速产类型": {"index": "控制9", "desc": "速产策略"},
        "quick_produce.enabled": {"index": "控制8_开关", "desc": "速产开关"},
        "point_reserve.保留点数": {"index": "控制10", "desc": "保留策点"},
        "point_reserve.enabled": {"index": "控制10_开关", "desc": "保留开关"},
    }
    
    ACCOUNT_MAPPING = {
        "类型": {"index_offset": 0, "desc": "统帅种类"},
        "名称": {"index_offset": 1, "desc": "统帅名称"},
        "账号": {"index_offset": 2, "desc": "统帅账号"},
        "密码": {"index_offset": 3, "desc": "统帅密码"},
        "平台": {"index_offset": 4, "desc": "统帅平台"},
        "开关": {"index_offset": 5, "desc": "统帅开关"},
    }
    
    @staticmethod
    def convert_to_jjm_format(user_config: Dict[str, Any]) -> Dict[str, Any]:
        """转换为按键精灵格式"""
        result = {}
        
        for key, value in user_config.items():
            if key in ConfigMapping.CONTROL_MAPPING:
                mapping = ConfigMapping.CONTROL_MAPPING[key]
                result[mapping["index"]] = str(value)
                result[mapping["desc"]] = str(value)
            elif key.startswith("account_"):
                parts = key.split(".")
                if len(parts) == 2:
                    account_id = parts[0]
                    field = parts[1]
                    if field in ConfigMapping.ACCOUNT_MAPPING:
                        account_num = account_id.replace("account_", "")
                        base_index = (int(account_num) - 1) * 4 + 1
                        mapping = ConfigMapping.ACCOUNT_MAPPING[field]
                        index_key = f"统帅{base_index + mapping['index_offset']}"
                        result[index_key] = str(value)
        
        return result