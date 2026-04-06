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

CONFIG_DIR = "设置界面/层级0_数据管理"
USER_MAINTAIN_DIR = "设置界面/层级0_数据管理/用户维护"
SCHEME_DIR = "设置界面/层级0_数据管理/配置方案"
PERSONALIZE_DIR = "设置界面/层级0_数据管理/个性化数据"

# 数据文件路径（分离后）
USER_DATA_FILE = "设置界面/层级0_数据管理/个性化数据/用户数据.yaml"
WIN11_RENDER_FILE = "设置界面/层级0_数据管理/个性化数据/渲染规范.yaml"

# 兼容旧代码（将废弃）
USER_PREFERENCE_FILE = "设置界面/层级0_数据管理/个性化数据/用户偏好.yaml"
USER_CONFIG_FILE = "设置界面/层级0_数据管理/配置方案/方案01.json"

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
        self._base_dir = base_dir or os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self._cache: Dict[str, Any] = {}
        self._id_map: Dict[str, Any] = None
        self._interface_cache: Dict[str, Dict] = {}
        
        self._ensure_default_scheme()
        
        global USER_CONFIG_FILE
        current_scheme = self._get_initial_scheme()
        USER_CONFIG_FILE = f"{SCHEME_DIR}/{current_scheme}.json"
    
    def _get_initial_scheme(self) -> str:
        """获取初始方案名称（从用户数据读取）"""
        try:
            user_data = self._read_yaml(USER_DATA_FILE, {})
            return user_data.get("当前方案", "方案01")
        except:
            return "方案01"
    
    def _ensure_default_scheme(self):
        """确保至少存在一个默认方案文件"""
        scheme_names = self.get_scheme_names()
        if not scheme_names:
            self._create_default_scheme("方案01")
    
    def _create_default_scheme(self, scheme_name: str):
        """创建默认方案文件（包含所有界面的完整默认配置）"""
        default_config = self.generate_default_config()
        self.save_scheme(scheme_name, default_config)
    
    def generate_default_config(self) -> Dict[str, Any]:
        """
        生成所有界面的完整默认配置
        
        遍历所有界面配置，提取每个卡片的默认值
        确保新创建的方案包含所有界面的配置
        """
        config = {
            "说明": "用户配置文件V3 - 按卡片分组，包含开关状态和控件值",
            "版本": "3.0"
        }
        
        for interface_name in self.get_interface_names():
            interface_config = self.load_interface_config(interface_name)
            interface_data = {}
            
            for card_name, card_data in interface_config.items():
                if card_name == "界面布局":
                    continue
                
                card_info = card_data.get("卡片信息", {})
                controls = card_data.get("控件列表", [])
                
                card_config = {
                    "enabled": card_info.get("enabled", True)
                }
                
                for control in controls:
                    control_id = control.get("id", "")
                    default_value = control.get("default", "")
                    if control_id and default_value:
                        card_config[control_id] = default_value
                
                interface_data[card_name] = card_config
            
            if interface_data:
                config[interface_name] = interface_data
        
        return config
    
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
        
        file_name = interface_name.replace("界面", "配置")
        file_path = f"{USER_MAINTAIN_DIR}/{file_name}.yaml"
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
            "注册界面",
            "关于界面",
        ]
        
        interface_dir = self._get_full_path(USER_MAINTAIN_DIR)
        if not os.path.exists(interface_dir):
            return []
        
        existing_names = set()
        for file_name in os.listdir(interface_dir):
            if file_name.endswith('.yaml'):
                interface_name = file_name[:-5].replace("配置", "界面")
                existing_names.add(interface_name)
        
        ordered_names = [name for name in V2_INTERFACE_ORDER if name in existing_names]
        
        return ordered_names
    
    def load_user_data(self) -> Dict[str, Any]:
        """加载用户数据（YAML格式）"""
        if "user_data" in self._cache:
            return self._cache["user_data"]
        
        data = self._read_yaml(USER_DATA_FILE, {})
        self._cache["user_data"] = data
        return data
    
    def save_user_data(self, data: Dict[str, Any]) -> bool:
        """保存用户数据"""
        self._cache["user_data"] = data
        return self._write_yaml(USER_DATA_FILE, data)
    
    def load_win11_render(self) -> Dict[str, Any]:
        """加载渲染规范（YAML格式）"""
        if "win11_render" in self._cache:
            return self._cache["win11_render"]
        
        data = self._read_yaml(WIN11_RENDER_FILE, {})
        self._cache["win11_render"] = data
        return data
    
    def load_user_preference(self) -> Dict[str, Any]:
        """
        加载用户偏好（兼容方法，合并用户数据和渲染规范）
        
        返回合并后的数据，保持向后兼容
        """
        if "user_preference" in self._cache:
            return self._cache["user_preference"]
        
        user_data = self.load_user_data()
        win11_render = self.load_win11_render()
        
        merged = {}
        
        if "用户信息" in user_data:
            merged["用户信息"] = user_data["用户信息"]
        if "当前方案" in user_data:
            merged["当前方案"] = user_data["当前方案"]
        
        if "主题配置" in win11_render:
            merged["主题配置"] = win11_render["主题配置"]
        if "强调色配置" in win11_render:
            merged["强调色配置"] = win11_render["强调色配置"]
        if "UI配置" in win11_render:
            merged["UI配置"] = win11_render["UI配置"]
        if "文本配置" in win11_render:
            merged["文本配置"] = win11_render["文本配置"]
        
        if "用户偏好" in user_data:
            theme_mode = user_data["用户偏好"].get("主题模式", "dark")
            accent_color = user_data["用户偏好"].get("强调色", "blue")
            merged["用户偏好"] = {
                "主题模式": theme_mode,
                "强调色": accent_color,
            }
        
        self._cache["user_preference"] = merged
        return merged
    
    def save_user_preference(self, data: Dict[str, Any]) -> bool:
        """保存用户偏好（兼容方法，分离保存）"""
        user_data = self.load_user_data()
        
        if "用户信息" in data:
            user_data["用户信息"] = data["用户信息"]
        if "当前方案" in data:
            user_data["当前方案"] = data["当前方案"]
        if "用户偏好" in data:
            user_data["用户偏好"] = data["用户偏好"]
        
        self._cache["user_preference"] = data
        return self.save_user_data(user_data)
    
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
        """获取用户配置的开关状态
        
        优先级：
        1. 用户配置文件中的 enabled
        2. 配置文件中的 enabled 默认值
        3. 参数 default
        """
        config = self.load_user_config()
        interface_data = config.get(interface, {})
        card_data = interface_data.get(card, {})
        
        if "enabled" in card_data:
            return card_data["enabled"]
        
        interface_config = self.load_interface_config(interface)
        card_config = interface_config.get(card, {})
        card_info = card_config.get("卡片信息", {})
        
        if "enabled" in card_info:
            return card_info["enabled"]
        
        return default
    
    def set_user_enabled(self, interface: str, card: str, enabled: bool) -> bool:
        """设置用户配置的开关状态"""
        config = self.load_user_config()
        
        if interface not in config:
            config[interface] = {}
        if card not in config[interface]:
            config[interface][card] = {}
        
        config[interface][card]["enabled"] = enabled
        return self.save_user_config(config)
    
    def get_scheme_names(self) -> List[str]:
        """获取所有方案名称列表（扫描目录中的.json文件）"""
        scheme_dir = self._get_full_path(SCHEME_DIR)
        if not os.path.exists(scheme_dir):
            return []
        
        scheme_names = []
        for file_name in os.listdir(scheme_dir):
            if file_name.endswith('.json'):
                scheme_name = file_name[:-5]
                scheme_names.append(scheme_name)
        
        scheme_names.sort()
        return scheme_names
    
    def get_current_scheme(self) -> str:
        """获取当前方案名称（从用户偏好读取）"""
        preference = self.load_user_preference()
        return preference.get("当前方案", "方案01")
    
    def set_current_scheme(self, scheme_name: str) -> bool:
        """设置当前方案（保存到用户偏好）"""
        preference = self.load_user_preference()
        preference["当前方案"] = scheme_name
        return self.save_user_preference(preference)
    
    def get_scheme_file(self, scheme_name: str) -> str:
        """获取方案文件名（方案名.json）"""
        return f"{scheme_name}.json"
    
    def load_scheme(self, scheme_name: str) -> Dict[str, Any]:
        """加载指定方案的配置"""
        file_path = f"{SCHEME_DIR}/{scheme_name}.json"
        return self._read_json(file_path, {})
    
    def save_scheme(self, scheme_name: str, config: Dict[str, Any]) -> bool:
        """保存配置到指定方案"""
        file_path = f"{SCHEME_DIR}/{scheme_name}.json"
        return self._write_json(file_path, config)
    
    def save_scheme_with_merge(self, scheme_name: str, current_config: Dict[str, Any], visited_interfaces: set = None) -> bool:
        """
        保存配置到指定方案（合并模式）
        
        合并逻辑：
        1. 加载现有方案配置
        2. 如果方案不存在，使用完整默认配置作为基础
        3. 只合并访问过的界面配置
        4. 未访问界面保留原有配置
        
        参数:
            scheme_name: 方案名称
            current_config: 当前配置（可能不完整）
            visited_interfaces: 已访问的界面集合（None表示全部合并）
        
        返回:
            是否成功
        """
        existing_config = self.load_scheme(scheme_name)
        
        if not existing_config:
            existing_config = self.generate_default_config()
        
        merged_config = self._merge_configs(existing_config, current_config, visited_interfaces)
        
        return self.save_scheme(scheme_name, merged_config)
    
    def _merge_configs(self, base_config: Dict[str, Any], new_config: Dict[str, Any], visited_interfaces: set = None) -> Dict[str, Any]:
        """
        合并两个配置（深度合并）
        
        规则：
        - 只合并 visited_interfaces 中的界面
        - 未访问界面保留 base_config 的配置
        - 说明和版本字段始终更新
        """
        result = base_config.copy()
        
        for key, value in new_config.items():
            if key in ("说明", "版本"):
                result[key] = value
            elif key.endswith("界面"):
                # 只合并访问过的界面
                if visited_interfaces is None or key in visited_interfaces:
                    if isinstance(value, dict) and key in result and isinstance(result[key], dict):
                        result[key] = self._merge_card_configs(result[key], value)
                    else:
                        result[key] = value
                # 未访问的界面保留 base_config 中的值（不覆盖）
            else:
                if isinstance(value, dict) and key in result and isinstance(result[key], dict):
                    result[key] = self._merge_card_configs(result[key], value)
                else:
                    result[key] = value
        
        return result
    
    def _merge_card_configs(self, base_cards: Dict[str, Any], new_cards: Dict[str, Any]) -> Dict[str, Any]:
        """合并卡片级别的配置"""
        result = base_cards.copy()
        
        for card_name, card_data in new_cards.items():
            if isinstance(card_data, dict) and card_name in result and isinstance(result[card_name], dict):
                merged_card = result[card_name].copy()
                for k, v in card_data.items():
                    merged_card[k] = v
                result[card_name] = merged_card
            else:
                result[card_name] = card_data
        
        return result
    
    def switch_scheme(self, scheme_name: str) -> bool:
        """切换方案"""
        global USER_CONFIG_FILE
        USER_CONFIG_FILE = f"{SCHEME_DIR}/{scheme_name}.json"
        
        self._cache.pop("user_config", None)
        
        self.set_current_scheme(scheme_name)
        return True
    
    def rename_scheme(self, old_name: str, new_name: str) -> bool:
        """
        重命名方案（重命名文件）
        
        参数:
            old_name: 原方案名称
            new_name: 新方案名称
        
        返回:
            是否成功
        """
        if new_name in self.get_scheme_names():
            return False
        
        old_path = self._get_full_path(f"{SCHEME_DIR}/{old_name}.json")
        new_path = self._get_full_path(f"{SCHEME_DIR}/{new_name}.json")
        
        if not os.path.exists(old_path):
            return False
        
        os.rename(old_path, new_path)
        
        if self.get_current_scheme() == old_name:
            self.set_current_scheme(new_name)
        
        return True
    
    def create_scheme(self, scheme_name: str) -> bool:
        """
        创建新方案（包含所有界面的完整默认配置）
        
        参数:
            scheme_name: 方案名称
        
        返回:
            是否成功
        """
        if scheme_name in self.get_scheme_names():
            return False
        
        default_config = self.generate_default_config()
        return self.save_scheme(scheme_name, default_config)
    
    def delete_scheme(self, scheme_name: str) -> bool:
        """
        删除方案
        
        参数:
            scheme_name: 方案名称
        
        返回:
            是否成功
        """
        if scheme_name not in self.get_scheme_names():
            return False
        
        file_path = self._get_full_path(f"{SCHEME_DIR}/{scheme_name}.json")
        
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        
        return False
    
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
