# -*- coding: utf-8 -*-
"""
模块名称：ConfigRepository
设计思路: 提供配置文件的读写操作
模块隔离: 数据层只依赖核心层，不依赖其他层
"""

import os
import json
import shutil
from typing import Dict, Any


class ConfigRepository:
    """配置仓库 - 配置文件的读写操作"""
    
    def __init__(self):
        self._config_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "配置")
        self._default_config_path = os.path.join(self._config_dir, "默认配置.json")
        self._user_config_path = os.path.join(self._config_dir, "用户配置.json")
        self._ensure_config_dir_exists()
    
    def _ensure_config_dir_exists(self) -> None:
        """确保配置目录存在"""
        if not os.path.exists(self._config_dir):
            os.makedirs(self._config_dir, exist_ok=True)
    
    def read_config(self) -> Dict[str, Any]:
        """读取配置文件"""
        try:
            if os.path.exists(self._user_config_path):
                with open(self._user_config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return self._load_default_config()
        except Exception as e:
            print(f"读取配置失败: {e}")
            return self._load_default_config()
    
    def _load_default_config(self) -> Dict[str, Any]:
        """加载默认配置并复制到用户配置"""
        try:
            if os.path.exists(self._default_config_path):
                with open(self._default_config_path, 'r', encoding='utf-8') as f:
                    default_config = json.load(f)
                shutil.copy(self._default_config_path, self._user_config_path)
                return default_config
            else:
                return {}
        except Exception as e:
            print(f"加载默认配置失败: {e}")
            return {}
    
    def save_config(self, config_data: Dict[str, Any]) -> str:
        """保存配置文件"""
        try:
            with open(self._user_config_path, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, ensure_ascii=False, indent=2)
            return f"配置保存成功: {self._user_config_path}"
        except Exception as e:
            return f"配置保存失败: {e}"
    
    def reset_to_default(self) -> str:
        """重置为默认配置"""
        try:
            if os.path.exists(self._default_config_path):
                shutil.copy(self._default_config_path, self._user_config_path)
                return "已重置为默认配置"
            else:
                return "默认配置文件不存在"
        except Exception as e:
            return f"重置失败: {e}"