# -*- coding: utf-8 -*-
"""
模块名称：UserConfigModel
设计思路: 定义用户配置的数据结构
模块隔离: 纯数据模型，无业务逻辑
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime


# *** 用户指定变量 - AI不得修改, 变量值必须生效 ***
# （用户未指定变量）
# *********************************


@dataclass
class AccountConfig:
    """账号配置模型"""
    index: int = 1
    commander_type: str = "副帅"
    name: str = ""
    account: str = ""
    password: str = ""
    platform: str = "Tap"
    enabled: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "序号": self.index,
            "帅类": self.commander_type,
            "名称": self.name,
            "账号": self.account,
            "密码": self.password,
            "平台": self.platform,
            "挂机": self.enabled,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AccountConfig":
        return cls(
            index=data.get("序号", 1),
            commander_type=data.get("帅类", "副帅"),
            name=data.get("名称", ""),
            account=data.get("账号", ""),
            password=data.get("密码", ""),
            platform=data.get("平台", "Tap"),
            enabled=data.get("挂机", False),
        )


@dataclass
class SystemConfig:
    """系统配置模型"""
    hangup_mode: str = "自动挂机"
    hangup_speed: int = 100
    retry_count: int = 10
    cache_limit: float = 1048576.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "挂机模式": self.hangup_mode,
            "挂机速度": self.hangup_speed,
            "尝试次数": self.retry_count,
            "缓存限制": self.cache_limit,
        }


@dataclass
class StrategyConfig:
    """策略配置模型"""
    quick_build_level: int = 8
    quick_build_type: str = "城资"
    quick_build_enabled: bool = True
    quick_produce_level: int = 7
    quick_produce_strategy: str = "自动平衡"
    quick_produce_enabled: bool = True
    reserve_points: int = 60
    reserve_enabled: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "速建限级": self.quick_build_level,
            "速建类别": self.quick_build_type,
            "速建开关": self.quick_build_enabled,
            "速产限级": self.quick_produce_level,
            "速产策略": self.quick_produce_strategy,
            "速产开关": self.quick_produce_enabled,
            "保留策点": self.reserve_points,
            "保留开关": self.reserve_enabled,
        }


@dataclass
class UserConfigModel:
    """用户配置模型 - 完整配置"""
    __version__: str = "1.0.0"
    __timestamp__: str = field(default_factory=lambda: datetime.now().isoformat())
    
    system_settings: Dict[str, Any] = field(default_factory=dict)
    strategy_settings: Dict[str, Any] = field(default_factory=dict)
    task_settings: Dict[str, Any] = field(default_factory=dict)
    funding_settings: Dict[str, Any] = field(default_factory=dict)
    account_settings: List[Dict[str, Any]] = field(default_factory=list)
    cleaning_settings: Dict[str, Any] = field(default_factory=dict)
    hunting_settings: Dict[str, Any] = field(default_factory=dict)
    building_settings: Dict[str, Any] = field(default_factory=dict)
    commander_info: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "__version__": self.__version__,
            "__timestamp__": self.__timestamp__,
            "系统设置": self.system_settings,
            "策略设置": self.strategy_settings,
            "任务设置": self.task_settings,
            "集资设置": self.funding_settings,
            "账号设置": self.account_settings,
            "打扫设置": self.cleaning_settings,
            "打野设置": self.hunting_settings,
            "建筑设置": self.building_settings,
            "挂机统帅信息": self.commander_info,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserConfigModel":
        return cls(
            __version__=data.get("__version__", "1.0.0"),
            __timestamp__=data.get("__timestamp__", datetime.now().isoformat()),
            system_settings=data.get("系统设置", {}),
            strategy_settings=data.get("策略设置", {}),
            task_settings=data.get("任务设置", {}),
            funding_settings=data.get("集资设置", {}),
            account_settings=data.get("账号设置", []),
            cleaning_settings=data.get("打扫设置", {}),
            hunting_settings=data.get("打野设置", {}),
            building_settings=data.get("建筑设置", {}),
            commander_info=data.get("挂机统帅信息", ""),
        )
