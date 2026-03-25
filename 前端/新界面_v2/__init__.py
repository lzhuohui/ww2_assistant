# -*- coding: utf-8 -*-
"""
模块名称：新界面_v2
设计思路: 完全模块化的界面系统，采用分层架构
模块隔离: 各层独立，单向依赖

架构说明:
├── 入口层 - 应用入口，组装各层
├── 表示层 - UI组件和界面
├── 业务层 - 业务逻辑和事件
├── 数据层 - 数据模型和仓库
└── 核心 - 配置、常量、工具

依赖方向: 入口 → 表示 → 业务 → 数据 → 核心
"""

from .入口 import MainInterface
from .核心 import ThemeConfig, UIConfig, GlobalConstants, CommonUtils
from .数据层 import UserConfigModel, ConfigRepository, ExportRepository
from .业务层 import ConfigService, ExportService, EventBus, EventType
from .表示层 import TextLabel, CardContainer, Dropdown, CollapsibleCard, SystemPage

__all__ = [
    "MainInterface",
    "ThemeConfig", "UIConfig", "GlobalConstants", "CommonUtils",
    "UserConfigModel", "ConfigRepository", "ExportRepository",
    "ConfigService", "ExportService", "EventBus", "EventType",
    "TextLabel", "CardContainer", "Dropdown", "CollapsibleCard", "SystemPage",
]
