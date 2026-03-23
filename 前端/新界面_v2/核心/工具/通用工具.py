# -*- coding: utf-8 -*-
"""
模块名称：通用工具
设计思路: 提供通用工具函数
模块隔离: 工具层独立，无业务依赖
"""

import random
import time
from typing import Any, Callable


# *** 用户指定变量 - AI不得修改 ***
USER_DELAY_MULTIPLIER = 1.0
# *********************************


class 通用工具:
    """通用工具类"""
    
    @staticmethod
    def 随机延时(基础毫秒: int, 倍数: float=USER_DELAY_MULTIPLIER) -> None:
        """随机延时"""
        最小值 = int(基础毫秒 * 倍数)
        最大值 = int(基础毫秒 * (倍数 + 0.2))
        实际延时 = random.randint(最小值, 最大值) / 1000
        time.sleep(实际延时)
    
    @staticmethod
    def 安全调用(函数: Callable, 默认值: Any=None, *args, **kwargs) -> Any:
        """安全调用函数，捕获异常"""
        try:
            return 函数(*args, **kwargs)
        except Exception as e:
            print(f"调用失败: {e}")
            return 默认值
    
    @staticmethod
    def 格式化键名(卡片ID: str, 配置键: str) -> str:
        """格式化配置键名"""
        return f"{卡片ID}.{配置键}"
    
    @staticmethod
    def 解析键名(键名: str) -> tuple:
        """解析配置键名"""
        parts = 键名.split(".", 1)
        if len(parts) == 2:
            return parts[0], parts[1]
        return 键名, ""
