# -*- coding: utf-8 -*-
"""
模块名称：事件总线
设计思路: 提供模块间通信的事件机制
模块隔离: 事件层独立，支持松耦合通信
"""

from typing import Dict, Any, Callable, List
from dataclasses import dataclass
from enum import Enum


# *** 用户指定变量 - AI不得修改 ***
# （用户未指定变量）
# *********************************


class 事件类型(Enum):
    """事件类型枚举"""
    配置变更 = "config_changed"
    主题变更 = "theme_changed"
    界面切换 = "page_switched"
    导出完成 = "export_completed"
    错误发生 = "error_occurred"


@dataclass
class 事件:
    """事件数据类"""
    类型: 事件类型
    数据: Dict[str, Any]
    来源: str = ""


class 事件总线:
    """事件总线 - 模块间通信"""
    
    _instance = None
    
    @classmethod
    def 重置实例(cls):
        """重置单例实例（用于测试或内存释放）"""
        cls._instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        
        self._监听器: Dict[事件类型, List[Callable]] = {}
        self._initialized = True
    
    def 订阅(self, 事件类型: 事件类型, 监听器: Callable) -> None:
        """订阅事件"""
        if 事件类型 not in self._监听器:
            self._监听器[事件类型] = []
        self._监听器[事件类型].append(监听器)
    
    def 取消订阅(self, 事件类型: 事件类型, 监听器: Callable) -> None:
        """取消订阅"""
        if 事件类型 in self._监听器:
            if 监听器 in self._监听器[事件类型]:
                self._监听器[事件类型].remove(监听器)
    
    def 清理所有监听器(self) -> None:
        """清理所有监听器（用于内存释放）"""
        self._监听器.clear()
    
    def 发布(self, 事件: 事件) -> None:
        """发布事件"""
        if 事件.类型 in self._监听器:
            for 监听器 in self._监听器[事件.类型]:
                try:
                    监听器(事件)
                except Exception as e:
                    print(f"事件处理失败: {e}")
    
    def 发布配置变更(self, 界面ID: str, 卡片ID: str, 配置键: str, 值: Any) -> None:
        """发布配置变更事件"""
        事件对象 = 事件(
            类型=事件类型.配置变更,
            数据={
                "界面ID": 界面ID,
                "卡片ID": 卡片ID,
                "配置键": 配置键,
                "值": 值,
            },
            来源="配置服务",
        )
        self.发布(事件对象)
    
    def 发布主题变更(self, 主题名称: str) -> None:
        """发布主题变更事件"""
        事件对象 = 事件(
            类型=事件类型.主题变更,
            数据={"主题名称": 主题名称},
            来源="主题服务",
        )
        self.发布(事件对象)
    
    def 发布界面切换(self, 界面名称: str) -> None:
        """发布界面切换事件"""
        事件对象 = 事件(
            类型=事件类型.界面切换,
            数据={"界面名称": 界面名称},
            来源="主界面",
        )
        self.发布(事件对象)
