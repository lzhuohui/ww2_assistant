# -*- coding: utf-8 -*-
"""
系统配置 - 配置层

模块定位:
    管理系统级配置参数。

功能原理:
    1. 定义系统级常量
    2. 管理路径配置
    3. 提供系统参数管理

数据来源:
    无

使用场景:
    被系统级模块和业务模块调用。

可独立运行调试: python 系统配置.py
"""

import os
from pathlib import Path


class 系统配置:
    """系统配置类 - 提供系统级配置管理"""
    
    # ==================== 系统常量 ====================
    系统常量 = {
        # 应用信息
        "app_name": "二战风云辅助",
        "app_version": "1.0.0",
        "app_author": "chmm1",
        
        # 时间配置
        "timeout": 30,                # 超时时间（秒）
        "retry_count": 3,             # 重试次数
        "sleep_interval": 0.5,        # 睡眠间隔（秒）
        
        # 设备配置
        "adb_port": 5037,            # ADB端口
        "screen_width": 1080,         # 屏幕宽度
        "screen_height": 1920,        # 屏幕高度
        
        # 业务配置
        "max_building_level": 12,     # 建筑最大等级
        "max_hero_level": 100,       # 英雄最大等级
        "max_troop_count": 100000,    # 最大兵力
    }
    
    # ==================== 路径配置 ====================
    def __init__(self):
        """初始化系统配置"""
        self._base_dir = Path(__file__).parent.parent.parent
        self._frontend_dir = self._base_dir / "前端"
        self._config_dir = self._frontend_dir / "配置"
        self._logs_dir = self._base_dir / "日志"
        
        # 确保目录存在
        self._logs_dir.mkdir(parents=True, exist_ok=True)
    
    def 获取常量(self, 名称: str):
        """获取系统常量"""
        return self.系统常量.get(名称)
    
    @property
    def 基础目录(self):
        """获取基础目录"""
        return str(self._base_dir)
    
    @property
    def 前端目录(self):
        """获取前端目录"""
        return str(self._frontend_dir)
    
    @property
    def 配置目录(self):
        """获取配置目录"""
        return str(self._config_dir)
    
    @property
    def 日志目录(self):
        """获取日志目录"""
        return str(self._logs_dir)


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    配置 = 系统配置()
    print(f"应用名称: {配置.获取常量('app_name')}")
    print(f"应用版本: {配置.获取常量('app_version')}")
    print(f"基础目录: {配置.基础目录}")
    print(f"前端目录: {配置.前端目录}")
    print(f"配置目录: {配置.配置目录}")
    print(f"日志目录: {配置.日志目录}")
