# -*- coding: utf-8 -*-

"""
模块名称：配置仓库.py
模块功能：V2配置数据存储和读取

实现步骤：
- 管理配置文件路径
- 读取配置文件
- 保存配置文件
- 缓存配置数据

职责：
- 文件读写
- 数据缓存
- 路径管理

不负责：
- 业务逻辑
- UI显示
"""

import json
import os
from typing import Any, Dict, List, Optional

# ============================================
# 数据和文件接口（前置，方便查看和修改）
# ============================================

CONFIG_DIR = "配置/V2"
SCHEMES_DIR = "配置/V2/方案"
USER_PREFERENCE_FILE = "配置/V2/用户偏好.json"
DEFAULT_SCHEME_FILE = "配置/V2/方案/默认方案.json"
SCHEME_LIST_FILE = "配置/V2/方案/方案列表.json"
USER_CONFIG_FILE = "配置/V2/用户配置.json"
UI_CONFIG_FILE = "配置/V2/界面配置.json"
DEFAULT_CONFIG_FILE = "配置/V2/默认配置.json"

# ============================================
# 公开接口
# ============================================

class ConfigRepository:
    """
    配置仓库 - V2版本
    
    职责：
    - 文件读写
    - 数据缓存
    - 路径管理
    
    不负责：
    - 业务逻辑
    - UI显示
    
    数据结构说明：
    用户配置.json采用二级嵌套结构：
    {
        "系统设置": {
            "挂机模式": {
                "enabled": true,
                "挂机模式": "全自动"
            }
        }
    }
    
    section格式: "系统设置.挂机模式" -> 一级.二级
    """
    
    def __init__(self, base_dir: str = None):
        self._base_dir = base_dir or os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        self._cache: Dict[str, Any] = {}
        self._scheme_cache: Dict[str, Dict] = {}
        self._user_config_cache: Dict[str, Any] = None
    
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
    
    def _parse_section(self, section: str) -> tuple:
        """
        解析section为一级和二级键名
        
        参数:
            section: 格式如 "系统设置.挂机模式"
        
        返回:
            (一级键, 二级键) 如 ("系统设置", "挂机模式")
        """
        parts = section.split(".", 1)
        if len(parts) == 2:
            return parts[0], parts[1]
        return parts[0], ""
    
    def load_scheme_list(self) -> Dict[str, Any]:
        """加载方案列表"""
        if "scheme_list" in self._cache:
            return self._cache["scheme_list"]
        
        data = self._read_json(SCHEME_LIST_FILE, {"schemes": [], "current": "默认方案"})
        self._cache["scheme_list"] = data
        return data
    
    def save_scheme_list(self, data: Dict[str, Any]) -> bool:
        """保存方案列表"""
        self._cache["scheme_list"] = data
        return self._write_json(SCHEME_LIST_FILE, data)
    
    def get_current_scheme_name(self) -> str:
        """获取当前方案名称"""
        data = self.load_scheme_list()
        return data.get("current", "默认方案")
    
    def set_current_scheme_name(self, name: str) -> bool:
        """设置当前方案名称"""
        data = self.load_scheme_list()
        data["current"] = name
        return self.save_scheme_list(data)
    
    def load_scheme(self, scheme_name: str) -> Dict[str, Any]:
        """加载方案配置"""
        if scheme_name in self._scheme_cache:
            return self._scheme_cache[scheme_name]
        
        file_path = f"{SCHEMES_DIR}/方案_{scheme_name}.json" if scheme_name != "默认方案" else DEFAULT_SCHEME_FILE
        data = self._read_json(file_path, {})
        
        if not data:
            data = self._read_json(DEFAULT_SCHEME_FILE, {})
        
        self._scheme_cache[scheme_name] = data
        return data
    
    def save_scheme(self, scheme_name: str, data: Dict[str, Any]) -> bool:
        """保存方案配置"""
        self._scheme_cache[scheme_name] = data
        file_path = f"{SCHEMES_DIR}/方案_{scheme_name}.json" if scheme_name != "默认方案" else DEFAULT_SCHEME_FILE
        return self._write_json(file_path, data)
    
    def load_default_scheme(self) -> Dict[str, Any]:
        """加载默认方案"""
        return self._read_json(DEFAULT_SCHEME_FILE, {})
    
    def get_scheme_value(self, section: str, key: str, default: Any = None) -> Any:
        """获取方案配置值"""
        scheme_name = self.get_current_scheme_name()
        scheme = self.load_scheme(scheme_name)
        
        section_data = scheme.get(section, {})
        if isinstance(section_data, dict):
            return section_data.get(key, default)
        return default
    
    def set_scheme_value(self, section: str, key: str, value: Any) -> bool:
        """设置方案配置值"""
        scheme_name = self.get_current_scheme_name()
        scheme = self.load_scheme(scheme_name)
        
        if section not in scheme:
            scheme[section] = {}
        
        scheme[section][key] = value
        return self.save_scheme(scheme_name, scheme)
    
    def get_scheme_section(self, section: str) -> Dict[str, Any]:
        """获取方案配置节"""
        scheme_name = self.get_current_scheme_name()
        scheme = self.load_scheme(scheme_name)
        return scheme.get(section, {})
    
    def load_user_preference(self) -> Dict[str, Any]:
        """加载用户偏好"""
        if "user_preference" in self._cache:
            return self._cache["user_preference"]
        
        data = self._read_json(USER_PREFERENCE_FILE, {"theme": "dark", "accent": "blue"})
        self._cache["user_preference"] = data
        return data
    
    def save_user_preference(self, data: Dict[str, Any]) -> bool:
        """保存用户偏好"""
        self._cache["user_preference"] = data
        return self._write_json(USER_PREFERENCE_FILE, data)
    
    def load_user_config(self) -> Dict[str, Any]:
        """加载用户配置"""
        if self._user_config_cache is not None:
            return self._user_config_cache
        
        self._user_config_cache = self._read_json(USER_CONFIG_FILE, {})
        return self._user_config_cache
    
    def save_user_config(self, data: Dict[str, Any]) -> bool:
        """保存用户配置"""
        self._user_config_cache = data
        return self._write_json(USER_CONFIG_FILE, data)
    
    def get_user_config_value(self, section: str, key: str, default: Any = None) -> Any:
        """
        获取用户配置值（二级嵌套结构）
        
        参数:
            section: 格式如 "系统设置.挂机模式"
            key: 控件ID，如 "挂机模式"
            default: 默认值
        """
        config = self.load_user_config()
        level1, level2 = self._parse_section(section)
        
        level1_data = config.get(level1, {})
        if not isinstance(level1_data, dict):
            return default
        
        level2_data = level1_data.get(level2, {})
        if not isinstance(level2_data, dict):
            return default
        
        return level2_data.get(key, default)
    
    def set_user_config_value(self, section: str, key: str, value: Any) -> bool:
        """
        设置用户配置值（二级嵌套结构）
        
        参数:
            section: 格式如 "系统设置.挂机模式"
            key: 控件ID，如 "挂机模式"
            value: 要设置的值
        """
        config = self.load_user_config()
        level1, level2 = self._parse_section(section)
        
        if level1 not in config:
            config[level1] = {}
        
        if level2 not in config[level1]:
            config[level1][level2] = {"enabled": True}
        
        config[level1][level2][key] = value
        return self.save_user_config(config)
    
    def get_user_config_enabled(self, section: str, default: bool = True) -> bool:
        """
        获取用户配置的开关状态（二级嵌套结构）
        
        参数:
            section: 格式如 "系统设置.挂机模式"
            default: 默认值
        """
        config = self.load_user_config()
        level1, level2 = self._parse_section(section)
        
        level1_data = config.get(level1, {})
        if not isinstance(level1_data, dict):
            return default
        
        level2_data = level1_data.get(level2, {})
        if not isinstance(level2_data, dict):
            return default
        
        return level2_data.get("enabled", default)
    
    def set_user_config_enabled(self, section: str, enabled: bool) -> bool:
        """
        设置用户配置的开关状态（二级嵌套结构）
        
        参数:
            section: 格式如 "系统设置.挂机模式"
            enabled: 开关状态
        """
        config = self.load_user_config()
        level1, level2 = self._parse_section(section)
        
        if level1 not in config:
            config[level1] = {}
        
        if level2 not in config[level1]:
            config[level1][level2] = {}
        
        config[level1][level2]["enabled"] = enabled
        return self.save_user_config(config)
    
    def get_user_config_section(self, section: str) -> Dict[str, Any]:
        """
        获取用户配置的整个卡片配置（二级嵌套结构）
        
        参数:
            section: 格式如 "系统设置.挂机模式"
        
        返回:
            卡片配置字典，如 {"enabled": true, "挂机模式": "全自动"}
        """
        config = self.load_user_config()
        level1, level2 = self._parse_section(section)
        
        level1_data = config.get(level1, {})
        if not isinstance(level1_data, dict):
            return {}
        
        return level1_data.get(level2, {})
    
    def get_current_theme(self) -> str:
        """获取当前主题名称"""
        prefs = self.load_user_preference()
        theme_section = prefs.get("主题", {})
        return theme_section.get("当前主题", "light")
    
    def set_current_theme(self, theme_name: str) -> bool:
        """设置当前主题"""
        prefs = self.load_user_preference()
        if "主题" not in prefs:
            prefs["主题"] = {}
        prefs["主题"]["当前主题"] = theme_name
        return self.save_user_preference(prefs)
    
    def get_theme_colors(self, theme_name: str = None) -> Dict[str, str]:
        """
        获取主题颜色配置
        
        参数:
            theme_name: 主题名称，如 "light" 或 "dark"，为None时使用当前主题
        
        返回:
            颜色配置字典，如 {"text_primary": "#000000", ...}
        """
        if theme_name is None:
            theme_name = self.get_current_theme()
        
        prefs = self.load_user_preference()
        theme_configs = prefs.get("主题配置", {})
        colors = theme_configs.get(theme_name, {})
        
        if not colors:
            colors = {
                "text_primary": "#FFFFFF",
                "text_secondary": "#C5C5C5",
                "text_disabled": "#656565",
                "bg_primary": "#202020",
                "bg_secondary": "#282828",
                "bg_card": "#2D2D2D",
                "border": "#3D3D3D",
            }
        else:
            colors = colors.copy()
        
        accent_value = self.get_accent_color()
        colors["accent"] = accent_value
        
        return colors
    
    def get_current_accent(self) -> str:
        """获取当前强调色名称"""
        prefs = self.load_user_preference()
        theme_section = prefs.get("主题", {})
        return theme_section.get("当前强调色", "blue")
    
    def set_current_accent(self, accent_name: str) -> bool:
        """设置当前强调色"""
        prefs = self.load_user_preference()
        if "主题" not in prefs:
            prefs["主题"] = {}
        prefs["主题"]["当前强调色"] = accent_name
        return self.save_user_preference(prefs)
    
    def get_accent_color(self, accent_name: str = None) -> str:
        """
        获取强调色值
        
        参数:
            accent_name: 强调色名称，如 "blue" 或 "red"，为None时使用当前强调色
        
        返回:
            强调色值，如 "#0078D4"
        """
        if accent_name is None:
            accent_name = self.get_current_accent()
        
        prefs = self.load_user_preference()
        accent_configs = prefs.get("强调色配置", {})
        accent_data = accent_configs.get(accent_name, {})
        
        if isinstance(accent_data, dict):
            return accent_data.get("value", "#0078D4")
        return "#0078D4"
    
    def get_all_themes(self) -> List[str]:
        """获取所有主题名称列表"""
        prefs = self.load_user_preference()
        theme_configs = prefs.get("主题配置", {})
        return list(theme_configs.keys())
    
    def get_all_accents(self) -> List[Dict[str, str]]:
        """获取所有强调色列表（name/value格式）"""
        prefs = self.load_user_preference()
        accent_configs = prefs.get("强调色配置", {})
        result = []
        for key, data in accent_configs.items():
            if isinstance(data, dict):
                result.append({
                    "key": key,
                    "name": data.get("name", key),
                    "value": data.get("value", "#0078D4")
                })
        return result
    
    def get_ui_config(self, category: str, key: str, default: Any = None) -> Any:
        """
        获取UI配置值
        
        参数:
            category: 配置分类，如 "卡片"、"下拉框"、"输入框"、"控件布局"、"导航"、"图标"
            key: 配置键，如 "最小高度"、"宽度"、"高度"等
            default: 默认值
        
        返回:
            配置值
        """
        prefs = self.load_user_preference()
        ui_config = prefs.get("UI配置", {})
        
        category_config = ui_config.get(category, {})
        return category_config.get(key, default)
    
    def get_ui_category(self, category: str) -> Dict[str, Any]:
        """
        获取UI配置分类
        
        参数:
            category: 配置分类，如 "卡片"、"下拉框"等
        
        返回:
            该分类的完整配置字典
        """
        prefs = self.load_user_preference()
        ui_config = prefs.get("UI配置", {})
        return ui_config.get(category, {})
    
    def set_ui_config(self, category: str, key: str, value: Any) -> bool:
        """
        设置UI配置值
        
        参数:
            category: 配置分类
            key: 配置键
            value: 配置值
        
        返回:
            是否保存成功
        """
        prefs = self.load_user_preference()
        if "UI配置" not in prefs:
            prefs["UI配置"] = {}
        if category not in prefs["UI配置"]:
            prefs["UI配置"][category] = {}
        
        prefs["UI配置"][category][key] = value
        return self.save_user_preference(prefs)
    
    def load_ui_config(self) -> Dict[str, Any]:
        """
        加载界面配置（从界面配置.json读取）
        
        返回:
            界面配置字典，包含所有界面配置信息
        """
        if "ui_config" in self._cache:
            return self._cache["ui_config"]
        
        data = self._read_json(UI_CONFIG_FILE, {})
        self._cache["ui_config"] = data
        return data

# *** 标准测试格式: 仅调用被测模块,AI不得添加数据 ***
if __name__ == "__main__":
    repo = ConfigRepository()
    
    print("测试配置仓库...")
    print(f"当前方案: {repo.get_current_scheme_name()}")
    
    print("\n--- 测试二级嵌套结构 ---")
    print(f"挂机模式值: {repo.get_user_config_value('系统设置.挂机模式', '挂机模式')}")
    print(f"挂机模式enabled: {repo.get_user_config_enabled('系统设置.挂机模式')}")
    print(f"速建限级: {repo.get_user_config_value('策略设置.建筑速建', '速建限级')}")
    print(f"账号01类型: {repo.get_user_config_value('账号设置.账号01', '类型')}")
    
    print("\n--- 测试主题配置 ---")
    print(f"当前主题: {repo.get_current_theme()}")
    print(f"当前强调色: {repo.get_current_accent()}")
    print(f"主题颜色: {repo.get_theme_colors()}")
    print(f"强调色值: {repo.get_accent_color()}")
    print(f"所有主题: {repo.get_all_themes()}")
    print(f"所有强调色: {repo.get_all_accents()}")
    
    print("\n测试完成")
