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

from 前端.V3.层级0_数据管理.配置数据 import ConfigData

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
    
    # ============================================
    # 界面配置接口
    # ============================================
    
    def get_interface_names(self) -> List[str]:
        """获取所有界面名称列表"""
        return self._data.get_interface_names()
    
    def get_interface_layout(self, interface: str) -> Dict[str, Any]:
        """
        获取界面布局配置
        
        参数:
            interface: 界面名称
        
        返回:
            {"下拉框宽度": 70, "输入框宽度": 100, "每行控件数": 3}
        """
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
        """获取卡片开关状态"""
        return self._data.get_user_enabled(interface, card, default)
    
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
        raw_options = control_config.get("options", [])
        return [{"text": str(opt), "value": str(opt)} for opt in raw_options]
    
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
        """获取当前主题名称"""
        prefs = self._data.load_user_preference()
        theme_section = prefs.get("主题", {})
        return theme_section.get("当前主题", "dark")
    
    def set_current_theme(self, theme_name: str) -> bool:
        """设置当前主题"""
        prefs = self._data.load_user_preference()
        if "主题" not in prefs:
            prefs["主题"] = {}
        prefs["主题"]["当前主题"] = theme_name
        result = self._data.save_user_preference(prefs)
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
        """获取当前强调色名称"""
        prefs = self._data.load_user_preference()
        theme_section = prefs.get("主题", {})
        return theme_section.get("当前强调色", "blue")
    
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
            "项间距": lambda: self.get_ui_size("边距", "中"),
            "项内边距": lambda: self.get_ui_size("边距", "中"),
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
