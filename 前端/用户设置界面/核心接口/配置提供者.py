# -*- coding: utf-8 -*-
"""
配置提供者 - 核心接口

设计思路:
    提供配置管理的统一访问接口，负责配置的加载、获取和设置。

功能:
    1. 配置初始化：加载配置管理器
    2. 配置获取：获取配置值
    3. 配置设置：设置配置值
    4. 配置重置：重置配置值

数据来源:
    所有配置数据从配置管理器获取。

使用场景:
    被界面层、组件层、单元层调用。

可独立运行调试: python 配置提供者.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from 前端.用户设置界面.配置.配置管理器 import ConfigManager


class ConfigProvider:
    """配置提供者 - 核心接口"""
    
    _instance = None
    _config_manager = None
    
    def __new__(cls):
        """单例模式"""
        if cls._instance is None:
            cls._instance = super(ConfigProvider, cls).__new__(cls)
        return cls._instance
    
    @classmethod
    def initialize(cls):
        """
        初始化配置提供者
        """
        if not cls._config_manager:
            cls._config_manager = ConfigManager()
    
    @classmethod
    def get_config_manager(cls) -> ConfigManager:
        """
        获取配置管理器实例
        
        返回:
            ConfigManager: 配置管理器实例
        """
        if not cls._config_manager:
            cls.initialize()
        return cls._config_manager
    
    @classmethod
    def get_value(cls, card_name: str, config_key: str, default: any = None) -> any:
        """
        获取配置值
        
        参数:
            card_name: 卡片名称
            config_key: 配置键
            default: 默认值
        
        返回:
            any: 配置值
        """
        if not cls._config_manager:
            cls.initialize()
        return cls._config_manager.get_value(card_name, config_key, default)
    
    @classmethod
    def set_value(cls, card_name: str, config_key: str, value: any):
        """
        设置配置值
        
        参数:
            card_name: 卡片名称
            config_key: 配置键
            value: 配置值
        """
        if not cls._config_manager:
            cls.initialize()
        cls._config_manager.set_value(card_name, config_key, value)
    
    @classmethod
    def reset_value(cls, card_name: str, config_key: str):
        """
        重置配置值为默认值
        
        参数:
            card_name: 卡片名称
            config_key: 配置键
        """
        if not cls._config_manager:
            cls.initialize()
        cls._config_manager.reset_value(card_name, config_key)
    
    @classmethod
    def get_all_values(cls, card_name: str) -> dict:
        """
        获取卡片的所有配置值
        
        参数:
            card_name: 卡片名称
        
        返回:
            dict: 配置值字典
        """
        if not cls._config_manager:
            cls.initialize()
        return cls._config_manager.get_all_values(card_name)
    
    @classmethod
    def get_card_config(cls, card_name: str) -> dict:
        """
        获取卡片配置
        
        参数:
            card_name: 卡片名称
        
        返回:
            dict: 卡片配置字典
        """
        if not cls._config_manager:
            cls.initialize()
        return cls._config_manager.get_card_config(card_name)
    
    @classmethod
    def get_all_card_configs(cls) -> dict:
        """
        获取所有卡片配置
        
        返回:
            dict: 所有卡片配置字典
        """
        if not cls._config_manager:
            cls.initialize()
        return cls._config_manager.get_all_card_configs()


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    # 1. 初始化配置提供者
    ConfigProvider.initialize()
    
    # 2. 测试获取配置值
    print("=== 测试获取配置值 ===")
    test_value = ConfigProvider.get_value("测试卡片", "test_key", "默认值")
    print(f"获取配置值: {test_value}")
    
    # 3. 测试设置配置值
    print("\n=== 测试设置配置值 ===")
    ConfigProvider.set_value("测试卡片", "test_key", "测试值")
    test_value = ConfigProvider.get_value("测试卡片", "test_key", "默认值")
    print(f"设置后配置值: {test_value}")
    
    # 4. 测试重置配置值
    print("\n=== 测试重置配置值 ===")
    ConfigProvider.reset_value("测试卡片", "test_key")
    test_value = ConfigProvider.get_value("测试卡片", "test_key", "默认值")
    print(f"重置后配置值: {test_value}")
    
    # 5. 测试获取所有卡片配置
    print("\n=== 测试获取所有卡片配置 ===")
    all_configs = ConfigProvider.get_all_card_configs()
    print(f"卡片配置数量: {len(all_configs)}")
    print(f"卡片名称列表: {list(all_configs.keys())}")