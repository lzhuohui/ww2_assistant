# -*- coding: utf-8 -*-
"""
模块名称：入口层
设计思路: 应用入口，组装各层模块
模块隔离: 入口层依赖所有层，不被任何层依赖
"""

from .主界面 import MainInterface

__all__ = ["MainInterface"]
