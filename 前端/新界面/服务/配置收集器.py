# -*- coding: utf-8 -*-
"""
模块名称：配置收集器
设计思路: 从各个界面模块收集用户设置数据
模块隔离: 只负责数据收集，不包含业务逻辑
"""

from typing import Dict, Any, List, Optional
from pathlib import Path
import json


# *** 用户指定变量 - AI不得修改 ***
USER_CONFIG_FILE = "user_config.json"
# *********************************


class ConfigCollector:
    """配置收集器 - 收集各界面模块的用户设置"""
    
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        
        self._config: Dict[str, Any] = {}
        self._callbacks: List[callable] = []
        self._initialized = True
    
    def register_callback(self, callback: callable):
        """注册配置变更回调"""
        self._callbacks.append(callback)
    
    def set_value(self, interface_id: str, card_id: str, config_key: str, value: Any):
        """
        设置单个配置值
        
        参数:
            interface_id: 界面ID（如"系统"、"策略"）
            card_id: 卡片ID（如"挂机模式"、"建筑速建"）
            config_key: 配置键（如"挂机模式"、"速建限级"）
            value: 配置值
        """
        key = f"{card_id}.{config_key}"
        self._config[key] = value
        
        for callback in self._callbacks:
            try:
                callback(interface_id, card_id, config_key, value)
            except Exception as e:
                print(f"回调执行失败: {e}")
    
    def set_switch(self, card_id: str, enabled: bool):
        """设置开关状态"""
        key = f"{card_id}.开关"
        self._config[key] = enabled
    
    def set_dropdown(self, card_id: str, config_key: str, value: str):
        """设置下拉框值"""
        key = f"{card_id}.{config_key}"
        self._config[key] = value
    
    def set_account(self, account_id: str, account_data: Dict[str, Any]):
        """
        设置账号配置
        
        参数:
            account_id: 账号ID（如"01账号"）
            account_data: 账号数据
        """
        for key, value in account_data.items():
            full_key = f"{account_id}.{key}"
            self._config[full_key] = value
    
    def get_value(self, card_id: str, config_key: str, default: Any = None) -> Any:
        """获取单个配置值"""
        key = f"{card_id}.{config_key}"
        return self._config.get(key, default)
    
    def get_all_config(self) -> Dict[str, Any]:
        """获取所有配置"""
        return self._config.copy()
    
    def get_interface_config(self, interface_id: str) -> Dict[str, Any]:
        """获取指定界面的配置"""
        return {
            k: v for k, v in self._config.items()
            if k.startswith(interface_id)
        }
    
    def clear_config(self):
        """清空配置"""
        self._config.clear()
    
    def load_config(self, file_path: str = None) -> Dict[str, Any]:
        """
        从文件加载配置
        
        参数:
            file_path: 配置文件路径（可选）
        
        返回:
            加载的配置数据
        """
        if file_path is None:
            file_path = Path(__file__).parent.parent / "配置" / USER_CONFIG_FILE
        else:
            file_path = Path(file_path)
        
        if not file_path.exists():
            return {}
        
        with open(file_path, 'r', encoding='utf-8') as f:
            self._config = json.load(f)
        
        return self._config
    
    def save_config(self, file_path: str = None) -> str:
        """
        保存配置到文件
        
        参数:
            file_path: 配置文件路径（可选）
        
        返回:
            保存的文件路径
        """
        if file_path is None:
            config_dir = Path(__file__).parent.parent / "配置"
            config_dir.mkdir(parents=True, exist_ok=True)
            file_path = config_dir / USER_CONFIG_FILE
        else:
            file_path = Path(file_path)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self._config, f, ensure_ascii=False, indent=2)
        
        return str(file_path)
    
    def export_for_game(self) -> Dict[str, Any]:
        """
        导出游戏控制配置
        
        返回:
            游戏控制配置数据
        """
        from .数据输出服务 import DataOutputService
        
        service = DataOutputService()
        return service.generate_game_config(self._config)
    
    def get_config_stats(self) -> Dict[str, Any]:
        """
        获取配置统计信息
        
        返回:
            统计信息
        """
        stats = {
            "总配置项": len(self._config),
            "界面分布": {},
            "账号数量": 0,
        }
        
        for key in self._config.keys():
            parts = key.split(".")
            if len(parts) >= 1:
                interface = parts[0]
                stats["界面分布"][interface] = stats["界面分布"].get(interface, 0) + 1
            
            if "账号" in key and ".开关" in key and self._config[key]:
                stats["账号数量"] += 1
        
        return stats


if __name__ == "__main__":
    collector = ConfigCollector()
    
    collector.set_value("系统", "挂机模式", "挂机模式", "自动")
    collector.set_value("系统", "指令速度", "指令速度", "100毫秒")
    collector.set_value("系统", "尝试次数", "尝试次数", "10次")
    
    collector.set_account("01账号", {
        "开关": True,
        "统帅种类": "主帅",
        "名称": "测试统帅",
        "账号": "test@example.com",
        "密码": "password123",
        "平台": "Tap",
    })
    
    print("配置统计:", collector.get_config_stats())
    print("\n所有配置:")
    print(json.dumps(collector.get_all_config(), ensure_ascii=False, indent=2))
    
    print("\n游戏配置:")
    game_config = collector.export_for_game()
    print(json.dumps(game_config, ensure_ascii=False, indent=2))
