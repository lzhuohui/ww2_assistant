# -*- coding: utf-8 -*-
"""
模块名称：服务模块包
设计思路: 提供数据收集和输出服务
模块隔离: 服务层独立于界面层
"""

from .配置收集器 import ConfigCollector
from .数据输出服务 import DataOutputService

__all__ = ["ConfigCollector", "DataOutputService"]
