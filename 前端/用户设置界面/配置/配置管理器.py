# -*- coding: utf-8 -*-
"""
配置管理器 - 配置层

设计思路:
    统一管理所有配置，提供加载、保存、获取、设置功能。
    支持配置的持久化存储。

优化:
    即时保存机制，每次修改立即保存。

功能:
    1. 加载配置
    2. 即时保存配置
    3. 获取配置
    4. 设置配置
    5. 配置持久化

数据来源:
    卡片配置文件、用户配置文件。

使用场景:
    被组件层调用。
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional
from .卡片配置 import 卡片配置
from .策略配置 import 策略配置
from .建筑配置 import 建筑配置
from .集资配置 import 集资卡片配置
from .打扫配置 import 打扫城区配置, 打扫政区配置
from .打野配置 import 自动打野配置
from .账号配置 import 账号卡片配置
from .任务配置 import 任务卡片配置


class ConfigManager:
    """配置管理器 - 统一管理所有配置（即时保存）"""
    
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, config_dir: str = None):
        if hasattr(self, '_initialized') and self._initialized:
            return
        
        self.config_dir = Path(config_dir) if config_dir else Path(__file__).parent
        self.user_config_file = self.config_dir / "用户配置.json"
        self.default_config_file = self.config_dir / "默认配置.json"
        
        self.card_configs = 卡片配置.copy()
        self.strategy_configs = 策略配置.copy()
        self.building_configs = 建筑配置.copy()
        self.fundraising_configs = 集资卡片配置.copy()
        self.other_configs = {
            "打扫城区": 打扫城区配置,
            "打扫政区": 打扫政区配置,
            "自动打野": 自动打野配置,
        }
        self.account_configs = 账号卡片配置.copy()
        self.all_configs = {**self.card_configs, **self.strategy_configs, **self.building_configs, **self.fundraising_configs, **self.other_configs, **self.account_configs}
        
        self.user_config = self._load_user_config()
        self._initialized = True
    
    def _load_user_config(self) -> Dict[str, Any]:
        """加载用户配置（自动初始化）"""
        if not self.user_config_file.exists():
            return self._create_default_config()
        
        try:
            with open(self.user_config_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content:
                    return self._create_default_config()
                return json.loads(content)
        except Exception as e:
            print(f"加载用户配置失败: {e}")
            return self._create_default_config()
    
    def _create_default_config(self) -> Dict[str, Any]:
        """创建默认配置"""
        if self.default_config_file.exists():
            try:
                with open(self.default_config_file, 'r', encoding='utf-8') as f:
                    default_config = json.load(f)
                self.user_config = default_config
                self._save_user_config()
                print("已自动创建默认配置文件")
                return default_config
            except Exception as e:
                print(f"加载默认配置失败: {e}")
        return {}
    
    def _save_user_config(self):
        """保存用户配置到文件"""
        try:
            with open(self.user_config_file, 'w', encoding='utf-8') as f:
                json.dump(self.user_config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存用户配置失败: {e}")
    
    def save_all(self):
        """保存所有配置（兼容旧接口）"""
        self._save_user_config()
    
    def get_card_config(self, card_name: str) -> Optional[Dict[str, Any]]:
        """
        获取卡片配置
        
        参数:
            card_name: 卡片名称
        
        返回:
            卡片配置字典，如果不存在则返回 None
        """
        return self.all_configs.get(card_name)
    
    def get_all_card_configs(self) -> Dict[str, Any]:
        """获取所有卡片配置"""
        return self.all_configs
    
    def get_value(self, card_name: str, config_key: str, default: Any = None) -> Any:
        """
        获取配置值
        
        参数:
            card_name: 卡片名称
            config_key: 配置键
            default: 默认值
        
        返回:
            配置值，如果不存在则返回默认值
        """
        user_key = f"{card_name}.{config_key}"
        if user_key in self.user_config:
            return self.user_config[user_key]
        
        card_config = self.get_card_config(card_name)
        if card_config:
            if "controls" in card_config:
                for control in card_config["controls"]:
                    if control.get("config_key") == config_key:
                        return control.get("value", default)
            elif "config_key" in card_config and card_config["config_key"] == config_key:
                return card_config.get("selected", default)
        
        return default
    
    def set_value(self, card_name: str, config_key: str, value: Any):
        """
        设置配置值（即时保存）
        
        参数:
            card_name: 卡片名称
            config_key: 配置键
            value: 配置值
        """
        user_key = f"{card_name}.{config_key}"
        self.user_config[user_key] = value
        self._save_user_config()
    
    def reset_value(self, card_name: str, config_key: str):
        """
        重置配置值为默认值（即时保存）
        
        参数:
            card_name: 卡片名称
            config_key: 配置键
        """
        user_key = f"{card_name}.{config_key}"
        if user_key in self.user_config:
            del self.user_config[user_key]
            self._save_user_config()
    
    def get_all_values(self, card_name: str) -> Dict[str, Any]:
        """
        获取卡片的所有配置值
        
        参数:
            card_name: 卡片名称
        
        返回:
            配置值字典
        """
        values = {}
        card_config = self.get_card_config(card_name)
        
        if card_config:
            if "controls" in card_config:
                for control in card_config["controls"]:
                    config_key = control.get("config_key")
                    if config_key:
                        values[config_key] = self.get_value(card_name, config_key)
            elif "config_key" in card_config:
                config_key = card_config["config_key"]
                values[config_key] = self.get_value(card_name, config_key)
        
        return values


配置管理器 = ConfigManager
