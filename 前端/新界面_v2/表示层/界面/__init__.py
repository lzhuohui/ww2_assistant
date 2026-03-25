# -*- coding: utf-8 -*-
"""
模块名称：界面包
设计思路: 提供各功能界面
模块隔离: 界面层依赖组件层和业务层
"""

from .系统界面 import SystemPage
from .策略界面 import StrategyPage
from .任务界面 import TaskPage
from .建筑界面 import BuildingPage
from .集资界面 import FundingPage
from .账号界面 import AccountPage
from .打扫界面 import CleaningPage
from .打野界面 import HuntingPage
from .个性化界面 import PersonalizationPage
from .关于界面 import AboutPage

__all__ = [
    "SystemPage", "StrategyPage", "TaskPage", "BuildingPage",
    "FundingPage", "AccountPage", "CleaningPage", "HuntingPage",
    "PersonalizationPage", "AboutPage"
]
