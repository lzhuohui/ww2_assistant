# -*- coding: utf-8 -*-
"""
模块名称：ConfigService
设计思路: 提供配置管理的业务逻辑
模块隔离: 服务层依赖数据层和核心层，不依赖表示层
"""

from typing import Dict, Any
from 前端.新界面_v2.数据层.仓库.配置仓库 import ConfigRepository
from 前端.新界面_v2.数据层.仓库.导出仓库 import ExportRepository


class ConfigService:
    """配置服务 - 配置管理的业务逻辑"""
    
    def __init__(self):
        self._config_repo = ConfigRepository()
        self._export_repo = ExportRepository()
        self._config_cache: Dict[str, Any] = {}
    
    def set_value(self, page_id: str, card_id: str, config_key: str, value: Any) -> None:
        """设置配置值"""
        key_name = f"{card_id}.{config_key}"
        self._config_cache[key_name] = value
        self.save_config()
    
    def get_value(self, card_id: str, config_key: str, default_value: Any=None) -> Any:
        """获取配置值"""
        key_name = f"{card_id}.{config_key}"
        return self._config_cache.get(key_name, default_value)
    
    def get_all_config(self) -> Dict[str, Any]:
        """获取所有配置"""
        return self._config_cache.copy()
    
    def load_config(self) -> Dict[str, Any]:
        """加载配置"""
        self._config_cache = self._config_repo.read_config()
        return self._config_cache
    
    def save_config(self) -> str:
        """保存配置"""
        return self._config_repo.save_config(self._config_cache)
    
    def reset_to_default(self) -> str:
        """重置为默认配置"""
        result = self._config_repo.reset_to_default()
        self._config_cache = self._config_repo.read_config()
        return result
    
    def export_game_config(self) -> Dict[str, Any]:
        """导出游戏配置"""
        from .导出服务 import ExportService
        service = ExportService()
        return service.generate_game_config(self._config_cache)
    
    def save_game_config(self) -> str:
        """保存游戏配置"""
        game_config = self.export_game_config()
        return self._export_repo.export_config(game_config)