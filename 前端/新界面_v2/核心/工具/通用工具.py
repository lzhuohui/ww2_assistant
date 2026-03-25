# -*- coding: utf-8 -*-
"""
模块名称：CommonUtils
设计思路: 提供通用工具函数
模块隔离: 工具层独立，无业务依赖
"""

from typing import Any, Callable


# *** 用户指定变量 - AI不得修改, 变量值必须生效 ***
# （用户未指定变量）
# *********************************


class CommonUtils:
    """通用工具类"""
    
    @staticmethod
    def safe_call(func: Callable, default: Any=None, *args, **kwargs) -> Any:
        """安全调用函数，捕获异常"""
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"调用失败: {e}")
            return default
    
    @staticmethod
    def format_key(card_id: str, config_key: str) -> str:
        """格式化配置键名"""
        return f"{card_id}.{config_key}"
    
    @staticmethod
    def parse_key(key: str) -> tuple:
        """解析配置键名"""
        parts = key.split(".", 1)
        if len(parts) == 2:
            return parts[0], parts[1]
        return key, ""


# *** 调试逻辑 ***
if __name__ == "__main__":
    print("CommonUtils 测试")
