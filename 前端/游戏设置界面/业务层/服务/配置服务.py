# -*- coding: utf-8 -*-
"""
模块名称：ConfigService
模块功能：配置业务逻辑，提供配置管理接口
实现步骤：
- 封装配置仓库操作
- 提供配置分组管理
- 支持配置导出
"""

from typing import Dict, Any, Optional, Callable
import os
import time

from 前端.游戏设置界面.数据层.仓库.配置仓库 import ConfigRepository


USER_GAME_CONFIG_FILE = "前端/output/game_config.json"


class ConfigService:
    """配置服务 - 配置业务逻辑"""
    
    def __init__(self):
        self._repository = ConfigRepository()
        self._loaded = False
    
    def load_config(self) -> Dict[str, Any]:
        """加载配置"""
        if not self._loaded:
            self._repository.load_config()
            self._loaded = True
        return self._repository._cache
    
    def get_value(self, card_id: str, config_key: str) -> Optional[str]:
        """获取配置值"""
        self.load_config()
        key = f"{card_id}.{config_key}"
        return self._repository.get_value(key)
    
    def set_value(self, card_id: str, config_key: str, value: Any) -> bool:
        """设置配置值"""
        self.load_config()
        key = f"{card_id}.{config_key}"
        return self._repository.set_value(key, value)
    
    def get_card_config(self, card_id: str) -> Dict[str, Any]:
        """获取卡片的所有配置"""
        self.load_config()
        result = {}
        for key, value in self._repository._cache.items():
            if key.startswith(f"{card_id}."):
                config_key = key[len(card_id) + 1:]
                result[config_key] = value
        return result
    
    def export_game_config(self) -> Dict[str, Any]:
        """导出游戏配置"""
        self.load_config()
        return self._repository._cache.copy()
    
    def save_game_config(self) -> str:
        """保存游戏配置到文件"""
        self.load_config()
        config = self.export_game_config()
        os.makedirs(os.path.dirname(USER_GAME_CONFIG_FILE), exist_ok=True)
        with open(USER_GAME_CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        return USER_GAME_CONFIG_FILE


# *** 标准测试格式: 仅调用被测模块,AI不得添加数据 ***
if __name__ == "__main__":
    import json
    
    service = ConfigService()
    service.set_value("test_card", "test_key", "test_value")
    result = service.get_value("test_card", "test_key")
    print(f"服务测试: test_card.test_key = {result}")
