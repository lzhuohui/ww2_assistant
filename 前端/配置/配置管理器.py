# -*- coding: utf-8 -*-
"""
配置管理器 - 配置层

设计思路:
    统一管理所有配置，提供加载、保存、获取、设置功能。
    支持配置的持久化存储。

功能:
    1. 加载配置
    2. 保存配置
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
from 前端.配置.卡片配置 import 卡片配置


class ConfigManager:
    """配置管理器 - 统一管理所有配置"""
    
    def __init__(self, config_dir: str = None):
        """
        初始化配置管理器
        
        参数:
            config_dir: 配置文件目录（可选，默认为前端/配置）
        """
        self.config_dir = Path(config_dir) if config_dir else Path(__file__).parent
        self.user_config_file = self.config_dir / "用户配置.json"
        
        # 加载卡片配置
        self.card_configs = 卡片配置.copy()
        
        # 加载用户配置
        self.user_config = self._load_user_config()
    
    def _load_user_config(self) -> Dict[str, Any]:
        """加载用户配置"""
        if self.user_config_file.exists():
            try:
                with open(self.user_config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载用户配置失败: {e}")
                return {}
        return {}
    
    def _save_user_config(self):
        """保存用户配置"""
        try:
            with open(self.user_config_file, 'w', encoding='utf-8') as f:
                json.dump(self.user_config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存用户配置失败: {e}")
    
    def get_card_config(self, card_name: str) -> Optional[Dict[str, Any]]:
        """
        获取卡片配置
        
        参数:
            card_name: 卡片名称
        
        返回:
            卡片配置字典，如果不存在则返回 None
        """
        return self.card_configs.get(card_name)
    
    def get_all_card_configs(self) -> Dict[str, Any]:
        """获取所有卡片配置"""
        return self.card_configs
    
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
        # 优先从用户配置中获取
        user_key = f"{card_name}.{config_key}"
        if user_key in self.user_config:
            return self.user_config[user_key]
        
        # 从卡片配置中获取默认值
        card_config = self.get_card_config(card_name)
        if card_config:
            # 对于基础设置类型的卡片
            if "controls" in card_config:
                for control in card_config["controls"]:
                    if control.get("config_key") == config_key:
                        return control.get("value", default)
            # 对于主题/调色板类型的卡片
            elif "config_key" in card_config and card_config["config_key"] == config_key:
                return card_config.get("selected", default)
        
        return default
    
    def set_value(self, card_name: str, config_key: str, value: Any):
        """
        设置配置值
        
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
        重置配置值为默认值
        
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
            # 对于基础设置类型的卡片
            if "controls" in card_config:
                for control in card_config["controls"]:
                    config_key = control.get("config_key")
                    if config_key:
                        values[config_key] = self.get_value(card_name, config_key)
            # 对于主题/调色板类型的卡片
            elif "config_key" in card_config:
                config_key = card_config["config_key"]
                values[config_key] = self.get_value(card_name, config_key)
        
        return values


# 兼容别名
配置管理器 = ConfigManager
