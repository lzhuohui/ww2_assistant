# -*- coding: utf-8 -*-
"""
模块名称：ConfigRepository
模块功能：配置文件读写操作
实现步骤：
- 读取JSON配置文件
- 写入JSON配置文件
- 支持默认配置
"""

import json
import os
from typing import Dict, Any, Optional


USER_DEFAULT_CONFIG_FILE = "前端/游戏设置界面/配置/默认配置.json"
USER_USER_CONFIG_FILE = "前端/游戏设置界面/配置/用户配置.json"


class ConfigRepository:
    """配置仓库 - 配置文件读写操作"""
    
    def __init__(
        self,
        default_file: str = USER_DEFAULT_CONFIG_FILE,
        user_file: str = USER_USER_CONFIG_FILE,
    ):
        self._default_file = default_file
        self._user_file = user_file
        self._cache: Dict[str, Any] = {}
    
    def load_config(self) -> Dict[str, Any]:
        """加载配置（优先用户配置）"""
        if os.path.exists(self._user_file):
            with open(self._user_file, 'r', encoding='utf-8') as f:
                self._cache = json.load(f)
        elif os.path.exists(self._default_file):
            with open(self._default_file, 'r', encoding='utf-8') as f:
                self._cache = json.load(f)
                self._save_to_file(self._user_file, self._cache)
        else:
            self._cache = {}
        return self._cache
    
    def save_config(self, config: Dict[str, Any]) -> bool:
        """保存配置到用户文件"""
        self._cache = config
        return self._save_to_file(self._user_file, config)
    
    def get_value(self, key: str, default: Any = None) -> Any:
        """获取配置值"""
        return self._cache.get(key, default)
    
    def set_value(self, key: str, value: Any) -> bool:
        """设置配置值并保存"""
        self._cache[key] = value
        return self._save_to_file(self._user_file, self._cache)
    
    def _save_to_file(self, file_path: str, data: Dict[str, Any]) -> bool:
        """保存数据到文件"""
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False
    
    def reset_to_default(self) -> bool:
        """重置为默认配置"""
        if os.path.exists(self._default_file):
            with open(self._default_file, 'r', encoding='utf-8') as f:
                self._cache = json.load(f)
            return self._save_to_file(self._user_file, self._cache)
        return False


# *** 标准测试格式: 仅调用被测模块,AI不得添加数据 ***
if __name__ == "__main__":
    USER_TEST_FILE = "前端/游戏设置界面/配置/test_config.json"
    
    repo = ConfigRepository(user_file=USER_TEST_FILE)
    repo.set_value("test.key", "test_value")
    result = repo.get_value("test.key")
    print(f"配置测试: test.key = {result}")
