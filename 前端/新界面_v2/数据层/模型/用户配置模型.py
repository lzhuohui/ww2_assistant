# -*- coding: utf-8 -*-
"""
模块名称：用户配置模型
设计思路: 定义用户配置的数据结构
模块隔离: 纯数据模型，无业务逻辑
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime


# *** 用户指定变量 - AI不得修改 ***
# （用户未指定变量）
# *********************************


@dataclass
class 账号配置:
    """账号配置模型"""
    序号: int = 1
    帅类: str = "副帅"
    名称: str = ""
    账号: str = ""
    密码: str = ""
    平台: str = "Tap"
    挂机: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "序号": self.序号,
            "帅类": self.帅类,
            "名称": self.名称,
            "账号": self.账号,
            "密码": self.密码,
            "平台": self.平台,
            "挂机": self.挂机,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "账号配置":
        return cls(
            序号=data.get("序号", 1),
            帅类=data.get("帅类", "副帅"),
            名称=data.get("名称", ""),
            账号=data.get("账号", ""),
            密码=data.get("密码", ""),
            平台=data.get("平台", "Tap"),
            挂机=data.get("挂机", False),
        )


@dataclass
class 系统配置:
    """系统配置模型"""
    挂机模式: str = "自动挂机"
    挂机速度: int = 100
    尝试次数: int = 10
    缓存限制: float = 1048576.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "挂机模式": self.挂机模式,
            "挂机速度": self.挂机速度,
            "尝试次数": self.尝试次数,
            "缓存限制": self.缓存限制,
        }


@dataclass
class 策略配置:
    """策略配置模型"""
    速建限级: int = 8
    速建类别: str = "城资"
    速建开关: bool = True
    速产限级: int = 7
    速产策略: str = "自动平衡"
    速产开关: bool = True
    保留策点: int = 60
    保留开关: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "速建限级": self.速建限级,
            "速建类别": self.速建类别,
            "速建开关": self.速建开关,
            "速产限级": self.速产限级,
            "速产策略": self.速产策略,
            "速产开关": self.速产开关,
            "保留策点": self.保留策点,
            "保留开关": self.保留开关,
        }


@dataclass
class 用户配置模型:
    """用户配置模型 - 完整配置"""
    __version__: str = "1.0.0"
    __timestamp__: str = field(default_factory=lambda: datetime.now().isoformat())
    
    系统设置: Dict[str, Any] = field(default_factory=dict)
    策略设置: Dict[str, Any] = field(default_factory=dict)
    任务设置: Dict[str, Any] = field(default_factory=dict)
    集资设置: Dict[str, Any] = field(default_factory=dict)
    账号设置: List[Dict[str, Any]] = field(default_factory=list)
    打扫设置: Dict[str, Any] = field(default_factory=dict)
    打野设置: Dict[str, Any] = field(default_factory=dict)
    建筑设置: Dict[str, Any] = field(default_factory=dict)
    挂机统帅信息: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "__version__": self.__version__,
            "__timestamp__": self.__timestamp__,
            "系统设置": self.系统设置,
            "策略设置": self.策略设置,
            "任务设置": self.任务设置,
            "集资设置": self.集资设置,
            "账号设置": self.账号设置,
            "打扫设置": self.打扫设置,
            "打野设置": self.打野设置,
            "建筑设置": self.建筑设置,
            "挂机统帅信息": self.挂机统帅信息,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "用户配置模型":
        return cls(
            __version__=data.get("__version__", "1.0.0"),
            __timestamp__=data.get("__timestamp__", datetime.now().isoformat()),
            系统设置=data.get("系统设置", {}),
            策略设置=data.get("策略设置", {}),
            任务设置=data.get("任务设置", {}),
            集资设置=data.get("集资设置", {}),
            账号设置=data.get("账号设置", []),
            打扫设置=data.get("打扫设置", {}),
            打野设置=data.get("打野设置", {}),
            建筑设置=data.get("建筑设置", {}),
            挂机统帅信息=data.get("挂机统帅信息", ""),
        )
