# -*- coding: utf-8 -*-
"""
模块名称：核心配置包
设计思路: 提供主题和界面的配置管理
模块隔离: 配置层独立，不依赖其他业务模块
"""

from .主题配置 import ThemeConfig
from .界面配置 import UIConfig

__all__ = ["ThemeConfig", "UIConfig"]
