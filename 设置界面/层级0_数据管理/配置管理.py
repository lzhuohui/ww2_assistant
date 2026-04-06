# -*- coding: utf-8 -*-

"""
模块名称：配置管理.py
模块功能：V3配置管理业务逻辑

职责：
- 界面配置读取
- 用户配置读写
- 三级优先级机制
- ID映射转换

不负责：
- 文件读写（由配置数据负责）
- UI显示
"""

from typing import Any, Callable, Dict, List, Optional

from 设置界面.层级0_数据管理.配置数据 import ConfigData

# ============================================
# 数据和文件接口（前置，方便查看和修改）
# ============================================

# ============================================
# 公开接口
# ============================================

class ConfigManager:
    """
    配置管理 - V3版本
    
    职责：
    - 界面配置读取
    - 用户配置读写
    - 三级优先级机制
    - ID映射转换
    
    不负责：
    - 文件读写
    - UI显示
    """
    
    def __init__(self):
        self._data = ConfigData()
        self._on_change_callbacks: List[Callable] = []
        self._layout_cache: Dict[str, Any] = {}
        self._exclude_values: Dict[str, List[str]] = {}
        self._visited_interfaces: set = set()
        self._scheme_names_cache: List[str] = None
    
    # ============================================
    # 界面配置接口
    # ============================================
    
    def get_interface_names(self) -> List[str]:
        """获取所有界面名称列表"""
        return self._data.get_interface_names()
    
    def mark_interface_visited(self, interface: str):
        """标记界面已访问（用于保存时只合并访问过的界面）"""
        self._visited_interfaces.add(interface)
    
    def get_visited_interfaces(self) -> set:
        """获取已访问的界面集合"""
        return self._visited_interfaces.copy()
    
    def clear_visited_interfaces(self):
        """清空已访问界面记录（切换方案时调用）"""
        self._visited_interfaces.clear()
    
    def get_interface_layout(self, interface: str) -> Dict[str, Any]:
        """
        获取界面布局配置
        
        参数:
            interface: 界面名称
        
        返回:
            {"下拉框宽度": 70, "输入框宽度": 100, "每行控件数": 3}
        """
        self.mark_interface_visited(interface)
        config = self._data.load_interface_config(interface)
        return config.get("界面布局", {})
    
    def get_card_names(self, interface: str) -> List[str]:
        """
        获取界面下的卡片名称列表
        
        参数:
            interface: 界面名称
        
        返回:
            卡片名称列表（排除"界面布局"）
        """
        config = self._data.load_interface_config(interface)
        return [k for k in config.keys() if k != "界面布局"]
    
    def get_card_info(self, interface: str, card: str) -> Dict[str, Any]:
        """
        获取卡片信息
        
        参数:
            interface: 界面名称
            card: 卡片名称
        
        返回:
            {"title": "挂机模式", "icon": "POWER_SETTINGS_NEW", ...}
        """
        config = self._data.load_interface_config(interface)
        card_config = config.get(card, {})
        return card_config.get("卡片信息", {"title": card, "icon": "HOME", "subtitle": "", "enabled": True})
    
    def get_controls(self, interface: str, card: str) -> List[Dict[str, Any]]:
        """
        获取控件列表
        
        参数:
            interface: 界面名称
            card: 卡片名称
        
        返回:
            [{"id": "挂机模式", "type": "dropdown", ...}, ...]
        """
        config = self._data.load_interface_config(interface)
        card_config = config.get(card, {})
        return card_config.get("控件列表", [])
    
    def get_control_config(self, interface: str, card: str, control_id: str) -> Dict[str, Any]:
        """获取单个控件配置"""
        controls = self.get_controls(interface, card)
        for ctrl in controls:
            if ctrl.get("id") == control_id:
                return ctrl
        return {}
    
    # ============================================
    # 三级优先级机制
    # ============================================
    
    def get_layout_value(self, interface: str, card: str, key: str, control_id: str = None) -> Any:
        """
        按优先级获取布局值：控件级 > 卡片级 > 界面级 > 默认值
        
        参数:
            interface: 界面名称
            card: 卡片名称
            key: 布局键，如 "下拉框宽度"、"每行控件数"
            control_id: 控件ID（可选，用于控件级覆盖）
        
        返回:
            布局值
        """
        cache_key = f"{interface}.{card}.{key}.{control_id or ''}"
        if cache_key in self._layout_cache:
            return self._layout_cache[cache_key]
        
        result = None
        
        if control_id:
            control_config = self.get_control_config(interface, card, control_id)
            if key in control_config:
                result = control_config[key]
            elif key == "dropdown_width" and "width" in control_config:
                result = control_config["width"]
            elif key == "input_width" and "width" in control_config:
                result = control_config["width"]
        
        if result is None:
            card_info = self.get_card_info(interface, card)
            if key in card_info:
                result = card_info[key]
        
        if result is None:
            interface_layout = self.get_interface_layout(interface)
            if key in interface_layout:
                result = interface_layout[key]
        
        if result is None:
            default_map = {
                "dropdown_width": self.get_ui_config("控件", "下拉框宽度"),
                "input_width": self.get_ui_config("控件", "输入框宽度"),
                "controls_per_row": self.get_ui_config("控件", "每行控件数")
            }
            result = default_map.get(key)
        
        self._layout_cache[cache_key] = result
        return result
    
    def get_card_height(self, interface: str, card: str) -> int:
        """
        按优先级获取卡片高度：卡片级 > 界面级 > 用户偏好 > 默认值
        
        参数:
            interface: 界面名称
            card: 卡片名称
        
        返回:
            卡片高度
        """
        cache_key = f"{interface}.{card}.height"
        if cache_key in self._layout_cache:
            return self._layout_cache[cache_key]
        
        result = None
        
        card_info = self.get_card_info(interface, card)
        if "height" in card_info:
            result = card_info["height"]
        
        if result is None:
            interface_layout = self.get_interface_layout(interface)
            if "card_height" in interface_layout:
                result = interface_layout["card_height"]
        
        if result is None:
            result = self.get_ui_config("卡片", "最小高度")
        
        if result is None:
            result = 100
        
        self._layout_cache[cache_key] = result
        return result
    
    # ============================================
    # 用户配置接口
    # ============================================
    
    def get_value(self, interface: str, card: str, control_id: str, default: Any = None) -> Any:
        """获取用户配置值"""
        return self._data.get_user_value(interface, card, control_id, default)
    
    def set_value(self, interface: str, card: str, control_id: str, value: Any) -> bool:
        """设置用户配置值"""
        if isinstance(value, dict) and "text" in value:
            value = value.get("text", "")
        result = self._data.set_user_value(interface, card, control_id, value)
        self._notify_change(f"{interface}.{card}.{control_id}", value)
        return result
    
    def get_enabled(self, interface: str, card: str, default: bool = True) -> bool:
        """获取卡片开关状态（从用户数据读取）"""
        return self._data.get_user_enabled(interface, card, default)
    
    def get_enabled_default(self, interface: str, card: str) -> bool:
        """获取卡片开关默认值（从配置文件读取）"""
        card_info = self.get_card_info(interface, card)
        return card_info.get("enabled", True)
    
    def set_enabled(self, interface: str, card: str, enabled: bool) -> bool:
        """设置卡片开关状态"""
        result = self._data.set_user_enabled(interface, card, enabled)
        self._notify_change(f"{interface}.{card}.enabled", enabled)
        return result
    
    def get_options(self, interface: str, card: str, control_id: str) -> List[Dict[str, str]]:
        """
        获取选项列表（text/value格式）
        
        参数:
            interface: 界面名称
            card: 卡片名称
            control_id: 控件ID
        """
        control_config = self.get_control_config(interface, card, control_id)
        
        dynamic_options = control_config.get("dynamic_options", "")
        
        if dynamic_options == "commanders":
            state = self.get_commander_dropdown_state(interface, card, control_id)
            return state["options"]
        elif dynamic_options == "commanders_exclude_primary":
            key = f"{interface}.{card}.{control_id}"
            primary_key = key.replace("次要统帅", "主要统帅")
            primary_commander = ""
            if primary_key in self._exclude_values:
                exclude_list = self._exclude_values[primary_key]
                if exclude_list:
                    primary_commander = exclude_list[0]
            state = self.get_commander_dropdown_state(interface, card, control_id, primary_commander)
            return state["options"]
        elif dynamic_options == "schemes":
            if self._scheme_names_cache is None:
                self._scheme_names_cache = self.get_scheme_names()
            return [{"text": name, "value": name} for name in self._scheme_names_cache]
        else:
            raw_options = control_config.get("options", [])
            return [{"text": str(opt), "value": str(opt)} for opt in raw_options]
    
    def set_exclude_value(self, interface: str, card: str, control_id: str, exclude_values: List[str]):
        """
        设置控件的排除值（用于联动下拉框）
        
        参数:
            interface: 界面名称
            card: 卡片名称
            control_id: 控件ID
            exclude_values: 要排除的值列表
        """
        key = f"{interface}.{card}.{control_id}"
        self._exclude_values[key] = exclude_values
    
    def clear_exclude_value(self, interface: str = None, card: str = None, control_id: str = None):
        """
        清除排除值
        
        参数:
            interface: 界面名称（可选，不传则清除所有）
            card: 卡片名称（可选）
            control_id: 控件ID（可选）
        """
        if interface is None:
            self._exclude_values.clear()
        elif card is None:
            keys_to_remove = [k for k in self._exclude_values if k.startswith(f"{interface}.")]
            for k in keys_to_remove:
                del self._exclude_values[k]
        elif control_id is None:
            keys_to_remove = [k for k in self._exclude_values if k.startswith(f"{interface}.{card}.")]
            for k in keys_to_remove:
                del self._exclude_values[k]
        else:
            key = f"{interface}.{card}.{control_id}"
            if key in self._exclude_values:
                del self._exclude_values[key]
    
    def get_default(self, interface: str, card: str, control_id: str) -> str:
        """获取控件默认值"""
        control_config = self.get_control_config(interface, card, control_id)
        return control_config.get("default", "")
    
    def get_raw_value(self, interface: str, card: str, control_id: str) -> str:
        """
        获取原始配置值（不加载选项列表，用于懒加载）
        
        优先级：
        1. 用户保存的配置值
        2. 控件默认值
        3. 空字符串
        """
        raw_value = self.get_value(interface, card, control_id, "")
        if raw_value:
            if isinstance(raw_value, dict):
                return raw_value.get("text", "")
            return str(raw_value)
        
        default_value = self.get_default(interface, card, control_id)
        if default_value:
            return str(default_value)
        
        return ""
    
    def get_text_value(self, interface: str, card: str, control_id: str) -> Dict[str, str]:
        """
        获取text/value格式的配置值（会加载选项列表，仅用于匹配验证）
        
        注意：此方法会调用get_options()，破坏懒加载
        懒加载场景请使用get_raw_value()
        """
        raw_value = self.get_value(interface, card, control_id, "")
        
        if isinstance(raw_value, dict) and "text" in raw_value and "value" in raw_value:
            return raw_value
        
        if raw_value:
            options = self.get_options(interface, card, control_id)
            for opt in options:
                if opt.get("text") == raw_value or opt.get("value") == raw_value:
                    return {"text": opt.get("text", raw_value), "value": opt.get("value", raw_value)}
            return {"text": str(raw_value), "value": str(raw_value)}
        
        default_value = self.get_default(interface, card, control_id)
        if default_value:
            options = self.get_options(interface, card, control_id)
            for opt in options:
                if opt.get("text") == default_value or opt.get("value") == default_value:
                    return {"text": opt.get("text", default_value), "value": opt.get("value", default_value)}
            return {"text": str(default_value), "value": str(default_value)}
        
        return {"text": "", "value": ""}
    
    # ============================================
    # 用户偏好接口
    # ============================================
    
    def get_current_theme(self) -> str:
        """获取当前主题名称（从方案文件读取）"""
        return self.get_raw_value("个性化界面", "主题模式", "theme_selector") or "dark"
    
    def set_current_theme(self, theme_name: str) -> bool:
        """设置当前主题（保存到方案文件）"""
        result = self.set_value("个性化界面", "主题模式", "theme_selector", theme_name)
        self._notify_change("theme", theme_name)
        return result
    
    def get_theme_colors(self, theme_name: str = None) -> Dict[str, str]:
        """获取主题颜色配置"""
        if theme_name is None:
            theme_name = self.get_current_theme()
        
        prefs = self._data.load_user_preference()
        theme_configs = prefs.get("主题配置", {})
        colors = theme_configs.get(theme_name, {})
        
        if not colors:
            colors = {
                "bg_primary": "#202020",
                "bg_secondary": "#1E1E1E",
                "bg_tertiary": "#2D2D2D",
                "bg_card": "#2D2D2D",
                "bg_hover": "#3A3A3A",
                "bg_selected": "#3A3A3A",
                "text_primary": "#FFFFFF",
                "text_secondary": "#B0B0B0",
                "text_disabled": "#666666",
                "border": "#3D3D3D",
                "border_hover": "#5C5C5C",
                "accent": "#0078D4",
                "accent_hover": "#1A86D9",
                "accent_pressed": "#006CBD",
            }
        
        colors = colors.copy()
        accent_value = self.get_accent_color()
        colors["accent"] = accent_value
        
        return colors
    
    def get_current_accent(self) -> str:
        """获取当前强调色名称（从方案文件读取）"""
        return self.get_raw_value("个性化界面", "强调色", "accent_selector") or "blue"
    
    def get_accent_color(self, accent_name: str = None) -> str:
        """获取强调色值"""
        if accent_name is None:
            accent_name = self.get_current_accent()
        
        prefs = self._data.load_user_preference()
        accent_configs = prefs.get("强调色配置", {})
        accent_data = accent_configs.get(accent_name, {})
        
        if isinstance(accent_data, dict):
            return accent_data.get("value", "#0078D4")
        return "#0078D4"
    
    def set_current_accent(self, accent_name: str) -> bool:
        """设置当前强调色（保存到方案文件）"""
        result = self.set_value("个性化界面", "强调色", "accent_selector", accent_name)
        self._notify_change("accent", accent_name)
        return result
    
    def get_accent_list(self) -> List[Dict[str, str]]:
        """获取强调色列表"""
        prefs = self._data.load_user_preference()
        accent_configs = prefs.get("强调色配置", {})
        result = []
        for key, data in accent_configs.items():
            if isinstance(data, dict):
                result.append({
                    "key": key,
                    "name": data.get("name", key),
                    "value": data.get("value", "#0078D4"),
                })
        return result
    
    def get_theme_list(self) -> List[Dict[str, str]]:
        """获取主题列表"""
        return [
            {"key": "light", "name": "浅色", "value": "#FFFFFF"},
            {"key": "dark", "name": "深色", "value": "#202020"},
        ]
    
    def get_active_commanders(self) -> List[str]:
        """从账号配置中获取参与挂机的主帅列表"""
        commanders = []
        scheme_name = self.get_current_scheme()
        scheme_data = self._data.load_scheme(scheme_name)
        account_section = scheme_data.get("账号界面", {})
        
        for i in range(1, 16):
            card_id = f"账号{i:02d}"
            account_data = account_section.get(card_id, {})
            
            account_type = account_data.get("类型", "")
            is_enabled = account_data.get("enabled", False)
            name = account_data.get("名称", "")
            
            if account_type == "主帅" and is_enabled and name:
                commanders.append(name)
        return commanders
    
    def get_commander_options(self, exclude_values: List[str] = None) -> List[Dict[str, str]]:
        """
        获取主帅选项列表（带"没有主帅"提示）
        
        参数:
            exclude_values: 需要排除的值列表
        
        返回:
            选项列表，如果没有主帅则返回提示选项
        """
        commanders = self.get_active_commanders()
        
        if exclude_values:
            commanders = [c for c in commanders if c not in exclude_values]
        
        if not commanders:
            return [{"text": "没有主帅", "value": ""}]
        
        return [{"text": c, "value": c} for c in commanders]
    
    def get_commander_dropdown_state(
        self,
        interface: str,
        card: str,
        control_id: str,
        primary_commander: str = None
    ) -> Dict[str, Any]:
        """
        获取统帅下拉框的完整状态（初始值 + 选项列表）
        
        场景逻辑：
        1. 加载方案值
        2. 如方案值没有，且账号没有主帅，显示"没有主帅"
        3. 如方案值没有，而账号有主帅，显示第一个主帅
        4. 次要统帅排除主要统帅
        
        参数:
            interface: 界面名称
            card: 卡片名称
            control_id: 控件ID ("主要统帅" 或 "次要统帅")
            primary_commander: 主要统帅值（用于次要统帅排除）
        
        返回:
            {
                "current_value": {"text": "...", "value": "..."},
                "options": [{"text": "...", "value": "..."}, ...]
            }
        """
        all_commanders = self.get_active_commanders()
        
        is_secondary = (control_id == "次要统帅")
        
        if is_secondary and primary_commander:
            available_commanders = [c for c in all_commanders if c != primary_commander]
        else:
            available_commanders = all_commanders
        
        if not all_commanders:
            return {
                "current_value": {"text": "没有主帅", "value": ""},
                "options": [{"text": "没有主帅", "value": ""}]
            }
        
        if not available_commanders:
            return {
                "current_value": {"text": "没有可选主帅", "value": ""},
                "options": [{"text": "没有可选主帅", "value": ""}]
            }
        
        options = [{"text": c, "value": c} for c in available_commanders]
        
        saved_value = self.get_raw_value(interface, card, control_id)
        
        if saved_value and saved_value in available_commanders:
            current_value = {"text": saved_value, "value": saved_value}
        else:
            current_value = {"text": available_commanders[0], "value": available_commanders[0]}
        
        return {
            "current_value": current_value,
            "options": options
        }
    
    def get_ui_config(self, category: str, key: str, default: Any = None) -> Any:
        """获取UI配置值"""
        prefs = self._data.load_user_preference()
        ui_config = prefs.get("UI配置", {})
        category_config = ui_config.get(category, {})
        return category_config.get(key, default)
    
    def get_text_config(self, control_type: str, key: str, default: str = "") -> str:
        """
        获取文本配置值（占位符、提示文本等）
        
        参数:
            control_type: 控件类型，如 "下拉框"、"输入框"
            key: 配置键，如 "占位符"、"加载中"
            default: 默认值
        
        返回:
            文本字符串
        """
        prefs = self._data.load_user_preference()
        text_config = prefs.get("文本配置", {})
        control_config = text_config.get(control_type, {})
        return control_config.get(key, default)
    
    def get_radius(self, size: str = "中") -> int:
        """
        获取圆角规格值
        
        参数:
            size: 圆角大小，可选 "小"、"中"、"大"
        
        返回:
            圆角像素值
        """
        prefs = self._data.load_user_preference()
        ui_config = prefs.get("UI配置", {})
        radius_config = ui_config.get("规格", {}).get("圆角", {})
        return radius_config.get(size, 6)
    
    def get_shadow_config(self, shadow_type: str = "菜单") -> Dict[str, Any]:
        """
        获取阴影配置
        
        参数:
            shadow_type: 阴影类型，可选 "菜单"、"卡片"、"对话框"
        
        返回:
            {
                "blur_radius": int,
                "spread_radius": int,
                "offset_x": int,
                "offset_y": int,
                "opacity": float
            }
        """
        defaults = {
            "菜单": {"blur_radius": 16, "spread_radius": 0, "offset_x": 0, "offset_y": 4, "opacity": 0.16},
            "卡片": {"blur_radius": 8, "spread_radius": 1, "offset_x": 0, "offset_y": 2, "opacity": 0.12},
            "对话框": {"blur_radius": 32, "spread_radius": 0, "offset_x": 0, "offset_y": 8, "opacity": 0.20},
        }
        
        prefs = self._data.load_user_preference()
        ui_config = prefs.get("UI配置", {})
        shadow_config = ui_config.get("阴影", {})
        type_config = shadow_config.get(shadow_type, {})
        
        default = defaults.get(shadow_type, defaults["菜单"])
        
        return {
            "blur_radius": type_config.get("blur_radius", default["blur_radius"]),
            "spread_radius": type_config.get("spread_radius", default["spread_radius"]),
            "offset_x": type_config.get("offset_x", default["offset_x"]),
            "offset_y": type_config.get("offset_y", default["offset_y"]),
            "opacity": type_config.get("opacity", default["opacity"]),
        }
    
    def get_animation_config(self) -> Dict[str, Any]:
        """
        获取动画配置
        
        返回:
            {
                "transition_duration": int,  # 过渡时长 ms
                "fast_transition": int,      # 快速过渡 ms
                "slow_transition": int,      # 慢速过渡 ms
                "easing": str                # 缓动函数
            }
        """
        defaults = {
            "transition_duration": 167,
            "fast_transition": 83,
            "slow_transition": 250,
            "easing": "easeOut",
        }
        
        prefs = self._data.load_user_preference()
        ui_config = prefs.get("UI配置", {})
        animation_config = ui_config.get("动画", {})
        
        return {
            "transition_duration": animation_config.get("过渡时长", defaults["transition_duration"]),
            "fast_transition": animation_config.get("快速过渡", defaults["fast_transition"]),
            "slow_transition": animation_config.get("慢速过渡", defaults["slow_transition"]),
            "easing": animation_config.get("缓动函数", defaults["easing"]),
        }
    
    def get_nav_config(self, key: str, default: Any = None) -> Any:
        """
        获取导航配置值，通用项使用全局UI配置
        
        映射关系：
        - 图标大小 → UI配置.使用.图标大小
        - 字体大小 → UI配置.使用.正文字体
        - 项间距 → UI配置.边距.中
        - 项内边距 → UI配置.边距.中
        - 项圆角 → UI配置.使用.卡片圆角
        
        参数:
            key: 配置键
            default: 默认值
        
        返回:
            配置值
        """
        global_mapping = {
            "图标大小": lambda: self.get_ui_size("字体", "图标大小"),
            "字体大小": lambda: self.get_ui_size("字体", "正文字体"),
            "项间距": lambda: self.get_ui_size("边距", "控件间距"),
            "项内边距": lambda: self.get_ui_size("边距", "控件区内边距"),
            "项圆角": lambda: self.get_ui_size("圆角", "卡片圆角"),
        }
        
        if key in global_mapping:
            return global_mapping[key]()
        
        return self.get_ui_config("导航", key, default)
    
    def get_nav_item_height(self) -> int:
        """获取导航项高度"""
        return self.get_nav_config("项高度", 40)
    
    def get_nav_item_radius(self) -> int:
        """
        获取导航项圆角，使用全局卡片圆角配置
        
        返回:
            圆角像素值
        """
        return self.get_nav_config("项圆角", 6)
    
    def get_nav_indicator_size(self) -> Dict[str, int]:
        """
        获取导航指示条尺寸
        
        指示条高度联动计算：
        指示条高度 = 项高度 - 2 × 圆角(小)
        
        使用圆角规格中的"小"值，确保指示条高度足够
        
        返回:
            {"width": 3, "height": 34}
        """
        item_height = self.get_nav_item_height()
        radius_small = self.get_radius("小")
        
        indicator_height = item_height - 2 * radius_small
        
        return {
            "width": self.get_nav_config("指示条宽度", 3),
            "height": indicator_height
        }
    
    def calc_nav_indicator_top(self) -> int:
        """
        计算导航指示条顶部位置（在导航项容器内垂直居中）
        
        计算逻辑：
        - 指示条在导航项容器内垂直居中
        - 不受容器内边距影响
        - top = (项高度 - 指示条高度) / 2
        
        返回:
            指示条top值
        """
        item_height = self.get_nav_item_height()
        indicator_size = self.get_nav_indicator_size()
        indicator_height = indicator_size["height"]
        
        indicator_top = (item_height - indicator_height) // 2
        
        return indicator_top
    
    def get_ui_size(self, size_type: str, usage: str) -> int:
        """
        获取UI尺寸值（固定三档）
        
        参数:
            size_type: 尺寸类型 - "字体"、"边距"、"圆角"
            usage: 使用场景 - 如 "界面内边距"、"卡片圆角"、"标题字体"
        
        返回:
            实际尺寸值
        """
        prefs = self._data.load_user_preference()
        ui_config = prefs.get("UI配置", {})
        
        usage_config = ui_config.get("使用", {})
        level = usage_config.get(usage, "中")
        
        size_config = ui_config.get(size_type, {})
        value = size_config.get(level, 8)
        
        return value
    
    # ============================================
    # ID映射接口
    # ============================================
    
    def get_id_by_name(self, interface: str, card: str, control_id: str) -> Optional[str]:
        """通过名称获取ID"""
        return self._data.get_id_by_name(interface, card, control_id)
    
    def get_location_by_id(self, config_id: str) -> Optional[Dict[str, str]]:
        """通过ID获取位置信息"""
        return self._data.get_location_by_id(config_id)
    
    def refresh_id_map(self) -> Dict[str, Any]:
        """刷新ID映射表（界面配置变更后调用）"""
        return self._data.refresh_id_map()
    
    def clear_cache(self):
        """清空所有缓存（退出时调用）"""
        self._layout_cache.clear()
        self._data.clear_cache()
    
    # ============================================
    # 方案管理接口
    # ============================================
    
    def get_scheme_names(self) -> List[str]:
        """获取所有方案名称列表"""
        return self._data.get_scheme_names()
    
    def refresh_scheme_names_cache(self):
        """刷新方案名称缓存"""
        self._scheme_names_cache = self._data.get_scheme_names()
    
    def get_current_scheme(self) -> str:
        """获取当前方案名称"""
        return self._data.get_current_scheme()
    
    def switch_scheme(self, scheme_name: str) -> bool:
        """
        切换方案
        
        参数:
            scheme_name: 方案名称
        
        返回:
            是否成功
        """
        if scheme_name not in self.get_scheme_names():
            return False
        
        self._data.switch_scheme(scheme_name)
        self._layout_cache.clear()
        self.clear_visited_interfaces()  # 切换方案时清空已访问界面记录
        self._notify_change("scheme", scheme_name)
        return True
    
    def save_current_to_scheme(self, scheme_name: str) -> bool:
        """
        保存当前配置到指定方案（合并模式）
        
        只合并已访问过的界面配置，未访问界面保留原有值
        
        参数:
            scheme_name: 方案名称
        
        返回:
            是否成功
        """
        current_config = self._data.load_user_config()
        visited = self.get_visited_interfaces()
        return self._data.save_scheme_with_merge(scheme_name, current_config, visited)
    
    def create_scheme(self, scheme_name: str) -> bool:
        """
        创建新方案（基于当前配置，合并默认配置）
        
        参数:
            scheme_name: 方案名称
        
        返回:
            是否成功
        """
        scheme_list = self._data.load_scheme_list()
        
        for scheme in scheme_list.get("方案列表", []):
            if scheme.get("名称") == scheme_name:
                return False
        
        scheme_list["方案列表"].append({
            "名称": scheme_name,
            "文件": f"{scheme_name}.json"
        })
        
        self._data.save_scheme_list(scheme_list)
        
        current_config = self._data.load_user_config()
        visited = self.get_visited_interfaces()
        self._data.save_scheme_with_merge(scheme_name, current_config, visited)
        
        return True
    
    def delete_scheme(self, scheme_name: str) -> bool:
        """
        删除方案
        
        参数:
            scheme_name: 方案名称
        
        返回:
            是否成功
        """
        if scheme_name == "默认方案":
            return False
        
        scheme_list = self._data.load_scheme_list()
        new_list = [s for s in scheme_list.get("方案列表", []) if s.get("名称") != scheme_name]
        
        if len(new_list) == len(scheme_list.get("方案列表", [])):
            return False
        
        scheme_list["方案列表"] = new_list
        self._data.save_scheme_list(scheme_list)
        
        return True
    
    def rename_scheme(self, old_name: str, new_name: str) -> bool:
        """
        重命名方案
        
        参数:
            old_name: 原方案名称
            new_name: 新方案名称
        
        返回:
            是否成功
        """
        if not new_name.strip():
            return False
        
        result = self._data.rename_scheme(old_name, new_name)
        if result:
            self._layout_cache.clear()
            self._notify_change("scheme", new_name)
        return result
    
    def save_and_rename_scheme(self, old_name: str, new_name: str) -> bool:
        """
        保存当前配置到方案并重命名
        
        参数:
            old_name: 原方案名称
            new_name: 新方案名称
        
        返回:
            是否成功
        """
        if not new_name.strip():
            return False
        
        if not self.save_current_to_scheme(old_name):
            return False
        
        if old_name != new_name:
            return self.rename_scheme(old_name, new_name)
        
        return True
    
    # ============================================
    # 回调机制
    # ============================================
    
    def register_on_change(self, callback: Callable):
        """注册配置变更回调"""
        self._on_change_callbacks.append(callback)
    
    def unregister_on_change(self, callback: Callable):
        """注销配置变更回调"""
        if callback in self._on_change_callbacks:
            self._on_change_callbacks.remove(callback)
    
    def _notify_change(self, key: str, value: Any):
        """通知配置变更"""
        for callback in self._on_change_callbacks:
            try:
                callback(key, value)
            except Exception:
                pass

# *** 标准测试格式: 仅调用被测模块,AI不得添加数据 ***
if __name__ == "__main__":
    manager = ConfigManager()
    
    print("测试V3配置管理...")
    
    print("\n--- 测试界面配置 ---")
    print(f"界面列表: {manager.get_interface_names()}")
    print(f"系统界面卡片: {manager.get_card_names('系统界面')}")
    print(f"挂机模式卡片信息: {manager.get_card_info('系统界面', '挂机模式')}")
    
    print("\n--- 测试三级优先级 ---")
    print(f"下拉框宽度: {manager.get_layout_value('系统界面', '挂机模式', '下拉框宽度')}")
    print(f"每行控件数: {manager.get_layout_value('系统界面', '挂机模式', '每行控件数')}")
    
    print("\n--- 测试用户配置 ---")
    print(f"挂机模式值: {manager.get_value('系统界面', '挂机模式', '挂机模式')}")
    print(f"选项列表: {manager.get_options('系统界面', '挂机模式', '挂机模式')}")
    
    print("\n--- 测试ID映射 ---")
    print(f"挂机模式ID: {manager.get_id_by_name('系统界面', '挂机模式', '挂机模式')}")
    
    print("\n测试完成")
