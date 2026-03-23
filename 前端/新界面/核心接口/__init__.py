# -*- coding: utf-8 -*-
"""模块名称：核心接口包 | 设计思路：提供主题和配置的核心接口 | 模块隔离原则"""

from .主题提供者 import ThemeProvider
from .界面配置 import 界面配置

__all__ = ["ThemeProvider", "界面配置"]
