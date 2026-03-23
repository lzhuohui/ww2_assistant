# -*- coding: utf-8 -*-
"""
模块名称：配置服务
设计思路: 提供配置管理的业务逻辑
模块隔离: 服务层依赖数据层和核心层，不依赖表示层
"""

from typing import Dict, Any, List, Callable
from 前端.新界面_v2.数据层.仓库.配置仓库 import 配置仓库
from 前端.新界面_v2.数据层.仓库.导出仓库 import 导出仓库


# *** 用户指定变量 - AI不得修改 ***
# （用户未指定变量）
# *********************************


class 配置服务:
    """配置服务 - 配置管理的业务逻辑"""
    
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
        self._配置仓库 = 配置仓库()
        self._导出仓库 = 导出仓库()
        self._配置缓存: Dict[str, Any] = {}
        self._回调列表: List[Callable] = []
        self._initialized = True
    
    def 注册回调(self, 回调函数: Callable) -> None:
        self._回调列表.append(回调函数)
    
    def 设置值(self, 界面ID: str, 卡片ID: str, 配置键: str, 值: Any) -> None:
        键名 = f"{卡片ID}.{配置键}"
        self._配置缓存[键名] = 值
        self._触发回调(界面ID, 卡片ID, 配置键, 值)
    
    def 获取值(self, 卡片ID: str, 配置键: str, 默认值: Any=None) -> Any:
        键名 = f"{卡片ID}.{配置键}"
        return self._配置缓存.get(键名, 默认值)
    
    def 获取全部配置(self) -> Dict[str, Any]:
        return self._配置缓存.copy()
    
    def 加载配置(self) -> Dict[str, Any]:
        self._配置缓存 = self._配置仓库.读取配置()
        return self._配置缓存
    
    def 保存配置(self) -> str:
        return self._配置仓库.保存配置(self._配置缓存)
    
    def 导出游戏配置(self) -> Dict[str, Any]:
        from .导出服务 import 导出服务
        服务 = 导出服务()
        return 服务.生成游戏配置(self._配置缓存)
    
    def 保存游戏配置(self) -> str:
        游戏配置 = self.导出游戏配置()
        return self._导出仓库.导出配置(游戏配置)
    
    def _触发回调(self, 界面ID: str, 卡片ID: str, 配置键: str, 值: Any) -> None:
        for 回调 in self._回调列表:
            try:
                回调(界面ID, 卡片ID, 配置键, 值)
            except Exception as e:
                print(f"回调执行失败: {e}")
    
    def 获取统计信息(self) -> Dict[str, Any]:
        统计 = {"总配置项": len(self._配置缓存), "界面分布": {}, "账号数量": 0}
        for 键名 in self._配置缓存.keys():
            部分 = 键名.split(".")
            if len(部分) >= 1:
                界面 = 部分[0]
                统计["界面分布"][界面] = 统计["界面分布"].get(界面, 0) + 1
            if "账号" in 键名 and ".开关" in 键名 and self._配置缓存[键名]:
                统计["账号数量"] += 1
        return 统计
