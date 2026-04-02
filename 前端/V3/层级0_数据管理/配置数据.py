# -*- coding: utf-8 -*-

"""
模块名称：配置数据.py
模块功能：V3配置数据存储和读取

职责：
- 文件读写（支持YAML和JSON）
- 数据缓存
- 路径管理
- ID映射表维护

不负责：
- 业务逻辑
- UI显示
"""

import json
import os
from typing import Any, Dict, List, Optional

import yaml

# ============================================
# 数据和文件接口（前置，方便查看和修改）
# ============================================

CONFIG_DIR = "前端/V3/层级0_数据管理"
USER_MAINTAIN_DIR = "前端/V3/层级0_数据管理/用户维护"
SCHEME_DIR = "前端/V3/层级0_数据管理/配置方案"
PERSONALIZE_DIR = "前端/V3/层级0_数据管理/个性化数据"
USER_PREFERENCE_FILE = "前端/V3/层级0_数据管理/个性化数据/用户偏好.yaml"
USER_CONFIG_FILE = "前端/V3/层级0_数据管理/配置方案/默认方案.json"
SCHEME_LIST_FILE = "前端/V3/层级0_数据管理/配置方案/方案列表.json"

# ============================================
# 公开接口
# ============================================

class ConfigData:
    """
    配置数据 - V3版本
    
    职责：
    - 文件读写（支持YAML和JSON）
    - 数据缓存
    - 路径管理
    - ID映射表维护
    
    不负责：
    - 业务逻辑
    - UI显示
    """
    
    def __init__(self, base_dir: str = None):
        self._base_dir = base_dir or os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        self._cache: Dict[str, Any] = {}
        self._id_map: Dict[str, Any] = None
        self._interface_cache: Dict[str, Dict] = {}
    
    def _get_full_path(self, relative_path: str) -> str:
        """获取完整路径"""
        return os.path.join(self._base_dir, relative_path)
    
    def _ensure_dir(self, file_path: str):
        """确保目录存在"""
        dir_path = os.path.dirname(file_path)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
    
    def _read_json(self, file_path: str, default: Any = None) -> Any:
        """读取JSON文件"""
        full_path = self._get_full_path(file_path)
        if os.path.exists(full_path):
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        return default if default is not None else {}
    
    def _write_json(self, file_path: str, data: Any) -> bool:
        """写入JSON文件"""
        full_path = self._get_full_path(file_path)
        try:
            self._ensure_dir(full_path)
            with open(full_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False
    
    def _read_yaml(self, file_path: str, default: Any = None) -> Any:
        """读取YAML文件"""
        full_path = self._get_full_path(file_path)
        if os.path.exists(full_path):
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f)
            except Exception:
                pass
        return default if default is not None else {}
    
    def _write_yaml(self, file_path: str, data: Any) -> bool:
        """写入YAML文件"""
        full_path = self._get_full_path(file_path)
        try:
            self._ensure_dir(full_path)
            with open(full_path, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
            return True
        except Exception:
            return False
    
    def load_interface_config(self, interface_name: str) -> Dict[str, Any]:
        """
        加载界面配置（YAML格式）
        
        参数:
            interface_name: 界面名称，如 "系统界面"
        
        返回:
            界面配置字典
        """
        if interface_name in self._interface_cache:
            return self._interface_cache[interface_name]
        
        file_path = f"{USER_MAINTAIN_DIR}/{interface_name}.yaml"
        data = self._read_yaml(file_path, {})
        self._interface_cache[interface_name] = data
        return data
    
    def get_interface_names(self) -> List[str]:
        """获取所有界面名称列表（按V2固定顺序）"""
        V2_INTERFACE_ORDER = [
            "系统界面",
            "策略界面",
            "任务界面",
            "建筑界面",
            "集资界面",
            "账号界面",
            "打扫界面",
            "打野界面",
            "个性化界面",
            "配置方案界面",
            "关于界面",
        ]
        
        interface_dir = self._get_full_path(USER_MAINTAIN_DIR)
        if not os.path.exists(interface_dir):
            return []
        
        existing_names = set()
        for file_name in os.listdir(interface_dir):
            if file_name.endswith('.yaml'):
                existing_names.add(file_name[:-5])
        
        ordered_names = [name for name in V2_INTERFACE_ORDER if name in existing_names]
        
        return ordered_names
    
    def load_user_preference(self) -> Dict[str, Any]:
        """加载用户偏好（YAML格式）"""
        if "user_preference" in self._cache:
            return self._cache["user_preference"]
        
        data = self._read_yaml(USER_PREFERENCE_FILE, {})
        self._cache["user_preference"] = data
        return data
    
    def save_user_preference(self, data: Dict[str, Any]) -> bool:
        """保存用户偏好"""
        self._cache["user_preference"] = data
        return self._write_yaml(USER_PREFERENCE_FILE, data)
    
    def load_user_config(self) -> Dict[str, Any]:
        """加载用户配置"""
        if "user_config" in self._cache:
            return self._cache["user_config"]
        
        data = self._read_json(USER_CONFIG_FILE, {})
        self._cache["user_config"] = data
        return data
    
    def save_user_config(self, data: Dict[str, Any]) -> bool:
        """保存用户配置"""
        self._cache["user_config"] = data
        return self._write_json(USER_CONFIG_FILE, data)
    
    def get_user_value(self, interface: str, card: str, control_id: str, default: Any = None) -> Any:
        """
        获取用户配置值
        
        参数:
            interface: 界面名称
            card: 卡片名称
            control_id: 控件ID
            default: 默认值
        """
        config = self.load_user_config()
        interface_data = config.get(interface, {})
        card_data = interface_data.get(card, {})
        return card_data.get(control_id, default)
    
    def set_user_value(self, interface: str, card: str, control_id: str, value: Any) -> bool:
        """设置用户配置值"""
        config = self.load_user_config()
        
        if interface not in config:
            config[interface] = {}
        if card not in config[interface]:
            config[interface][card] = {"enabled": True}
        
        config[interface][card][control_id] = value
        return self.save_user_config(config)
    
    def get_user_enabled(self, interface: str, card: str, default: bool = True) -> bool:
        """获取用户配置的开关状态"""
        config = self.load_user_config()
        interface_data = config.get(interface, {})
        card_data = interface_data.get(card, {})
        return card_data.get("enabled", default)
    
    def set_user_enabled(self, interface: str, card: str, enabled: bool) -> bool:
        """设置用户配置的开关状态"""
        config = self.load_user_config()
        
        if interface not in config:
            config[interface] = {}
        if card not in config[interface]:
            config[interface][card] = {}
        
        config[interface][card]["enabled"] = enabled
        return self.save_user_config(config)
    
    def load_id_map(self) -> Dict[str, Any]:
        """
        加载ID映射表（纯内存生成，不保存文件）
        
        启动时从界面配置生成，退出时清空
        """
        if self._id_map is not None:
            return self._id_map
        
        self._id_map = self.generate_id_map()
        return self._id_map
    
    def clear_cache(self):
        """
        清空所有缓存（退出时调用）
        
        包括：界面配置缓存、用户配置缓存、ID映射表
        """
        self._cache.clear()
        self._interface_cache.clear()
        self._id_map = None
    
    def refresh_id_map(self) -> Dict[str, Any]:
        """
        刷新ID映射表（界面配置变更后调用）
        """
        self._id_map = self.generate_id_map()
        return self._id_map
    
    def get_id_by_name(self, interface: str, card: str, control_id: str) -> Optional[str]:
        """
        通过名称获取ID
        
        参数:
            interface: 界面名称
            card: 卡片名称
            control_id: 控件ID
        
        返回:
            固定ID，如 "SYS_001"
        """
        id_map = self.load_id_map()
        key = f"{interface}.{card}.{control_id}"
        return id_map.get("映射", {}).get(key)
    
    def get_location_by_id(self, config_id: str) -> Optional[Dict[str, str]]:
        """
        通过ID获取位置信息
        
        参数:
            config_id: 固定ID
        
        返回:
            {"界面": "系统界面", "卡片": "挂机模式", "控件": "挂机模式"}
        """
        id_map = self.load_id_map()
        return id_map.get("反向映射", {}).get(config_id)
    
    def generate_id_map(self) -> Dict[str, Any]:
        """
        自动生成ID映射表
        
        扫描所有界面配置，生成名称到ID的映射
        """
        id_map = {"映射": {}, "反向映射": {}}
        id_counters = {}
        
        for interface_name in self.get_interface_names():
            config = self.load_interface_config(interface_name)
            
            prefix = self._get_id_prefix(interface_name)
            if prefix not in id_counters:
                id_counters[prefix] = 1
            
            for card_name, card_data in config.items():
                if card_name == "界面布局":
                    continue
                
                controls = card_data.get("控件列表", [])
                for control in controls:
                    control_id = control.get("id", "")
                    if control_id:
                        full_key = f"{interface_name}.{card_name}.{control_id}"
                        config_id = f"{prefix}_{id_counters[prefix]:03d}"
                        
                        id_map["映射"][full_key] = config_id
                        id_map["反向映射"][config_id] = {
                            "界面": interface_name,
                            "卡片": card_name,
                            "控件": control_id
                        }
                        id_counters[prefix] += 1
        
        return id_map
    
    def _get_id_prefix(self, interface_name: str) -> str:
        """获取界面对应的ID前缀"""
        prefix_map = {
            "系统界面": "SYS",
            "账号界面": "ACC",
            "建筑界面": "BLD",
            "策略界面": "STR",
            "任务界面": "TSK",
            "集资界面": "FUN",
            "打扫界面": "CLN",
            "打野界面": "HNT"
        }
        return prefix_map.get(interface_name, "CFG")

# *** 标准测试格式: 仅调用被测模块,AI不得添加数据 ***
if __name__ == "__main__":
    data = ConfigData()
    
    print("测试V3配置数据...")
    
    print("\n--- 测试界面配置 ---")
    print(f"界面列表: {data.get_interface_names()}")
    
    system_config = data.load_interface_config("系统界面")
    print(f"系统界面卡片: {list(system_config.keys())}")
    
    print("\n--- 测试用户配置 ---")
    print(f"挂机模式值: {data.get_user_value('系统界面', '挂机模式', '挂机模式')}")
    
    print("\n--- 测试ID映射 ---")
    id_map = data.generate_id_map()
    print(f"映射数量: {len(id_map['映射'])}")
    print(f"SYS_001位置: {data.get_location_by_id('SYS_001')}")
    
    print("\n测试完成")
