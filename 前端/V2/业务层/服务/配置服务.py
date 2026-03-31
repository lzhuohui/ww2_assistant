# -*- coding: utf-8 -*-

"""
模块名称：配置服务.py
模块功能：V2配置管理业务逻辑

职责：
- 方案管理（创建、切换、删除）
- 配置值读写
- 选项列表获取
- 导出配置

不负责：
- 文件读写（由配置仓库负责）
- UI显示
"""

from typing import Any, Callable, Dict, List, Optional

from 前端.V2.数据层.仓库.配置仓库 import ConfigRepository

# ============================================
# 数据和文件接口（前置，方便查看和修改）
# ============================================

DEFAULT_SCHEME_NAME = "默认方案"

# ============================================
# 公开接口
# ============================================

class ConfigService:
    """
    配置服务 - V2版本
    
    职责：
    - 方案管理
    - 配置值读写
    - 选项列表获取
    
    不负责：
    - 文件读写
    - UI显示
    """
    
    def __init__(self):
        self._repository = ConfigRepository()
        self._on_change_callbacks: List[Callable] = []
    
    def get_current_scheme_name(self) -> str:
        """获取当前方案名称"""
        return self._repository.get_current_scheme_name()
    
    def get_scheme_list(self) -> List[Dict[str, Any]]:
        """获取方案列表"""
        data = self._repository.load_scheme_list()
        return data.get("schemes", [])
    
    def switch_scheme(self, scheme_name: str) -> bool:
        """切换方案"""
        self._repository.set_current_scheme_name(scheme_name)
        self._notify_change("scheme_switch", scheme_name)
        return True
    
    def create_scheme(self, scheme_name: str, base_scheme: str = None) -> bool:
        """创建新方案"""
        if base_scheme:
            base_data = self._repository.load_scheme(base_scheme)
        else:
            base_data = self._repository.load_default_scheme()
        self._repository.save_scheme(scheme_name, base_data)
        
        scheme_list = self._repository.load_scheme_list()
        scheme_list["schemes"].append({"name": scheme_name})
        self._repository.save_scheme_list(scheme_list)
        return True
    
    def delete_scheme(self, scheme_name: str) -> bool:
        """删除方案"""
        if scheme_name == DEFAULT_SCHEME_NAME:
            return False
        
        scheme_list = self._repository.load_scheme_list()
        scheme_list["schemes"] = [s for s in scheme_list["schemes"] if s["name"] != scheme_name]
        self._repository.save_scheme_list(scheme_list)
        return True
    
    def get_value(self, section: str, key: str, default: Any = None) -> Any:
        """获取配置值（从用户配置.json读取）"""
        return self._repository.get_user_config_value(section, key, default)
    
    def set_value(self, section: str, key: str, value: Any) -> bool:
        """设置配置值（保存到用户配置.json）"""
        if isinstance(value, dict):
            value = value.get("text", "")
        result = self._repository.set_user_config_value(section, key, value)
        self._notify_change(f"{section}.{key}", value)
        return result
    
    def get_section(self, section: str) -> Dict[str, Any]:
        """获取配置节"""
        return self._repository.get_scheme_section(section)
    
    def get_enabled(self, section: str, default: bool = True) -> bool:
        """获取开关状态（从用户配置.json读取）"""
        return self._repository.get_user_config_enabled(section, default)
    
    def set_enabled(self, section: str, enabled: bool) -> bool:
        """设置开关状态（保存到用户配置.json）"""
        result = self._repository.set_user_config_enabled(section, enabled)
        self._notify_change(f"{section}.enabled", enabled)
        return result
    
    def get_options(self, section: str, control_id: str) -> List[Dict[str, str]]:
        """
        获取选项列表（text/value格式）
        
        数据来源：界面配置.json（唯一数据源）
        格式转换：字符串数组 → text/value格式
        """
        raw_options = self.get_control_options(section, control_id)
        return [{"text": str(opt), "value": str(opt)} for opt in raw_options]
    
    def get_all_options(self) -> Dict[str, Dict[str, List[Dict[str, str]]]]:
        """
        获取所有选项列表
        
        数据来源：界面配置.json（唯一数据源）
        """
        all_options = {}
        ui_config = self._repository.load_ui_config()
        interface_config = ui_config.get("界面配置", {})
        
        for section, section_data in interface_config.items():
            controls = section_data.get("控件列表", [])
            section_options = {}
            for control in controls:
                control_id = control.get("id", "")
                raw_options = control.get("options", [])
                section_options[control_id] = [
                    {"text": str(opt), "value": str(opt)} for opt in raw_options
                ]
            if section_options:
                all_options[section] = section_options
        
        return all_options
    
    def get_text_value(self, section: str, key: str) -> Dict[str, str]:
        """获取text/value格式的配置值（从用户配置.json读取字符串，匹配选项列表）"""
        raw_value = self.get_value(section, key, "")
        
        if isinstance(raw_value, dict) and "text" in raw_value and "value" in raw_value:
            return raw_value
        
        if raw_value:
            options = self.get_options(section, key)
            for opt in options:
                if opt.get("text") == raw_value or opt.get("value") == raw_value:
                    return {"text": opt.get("text", raw_value), "value": opt.get("value", raw_value)}
            return {"text": str(raw_value), "value": str(raw_value)}
        
        return {"text": "", "value": ""}
    
    def set_text_value(self, section: str, key: str, text: str, value: str) -> bool:
        """设置text/value格式的配置值"""
        return self.set_value(section, key, {"text": text, "value": value})
    
    def export_config(self, export_path: str) -> bool:
        """导出配置到指定路径"""
        import json
        import os
        
        scheme_name = self.get_current_scheme_name()
        scheme_data = self._repository.load_scheme(scheme_name)
        
        os.makedirs(os.path.dirname(export_path), exist_ok=True)
        with open(export_path, 'w', encoding='utf-8') as f:
            json.dump(scheme_data, f, ensure_ascii=False, indent=2)
        return True
    
    def get_user_preference(self, key: str, default: Any = None) -> Any:
        """获取用户偏好"""
        prefs = self._repository.load_user_preference()
        return prefs.get(key, default)
    
    def set_user_preference(self, key: str, value: Any) -> bool:
        """设置用户偏好"""
        prefs = self._repository.load_user_preference()
        prefs[key] = value
        return self._repository.save_user_preference(prefs)
    
    def get_current_theme(self) -> str:
        """获取当前主题名称"""
        return self._repository.get_current_theme()
    
    def set_current_theme(self, theme_name: str) -> bool:
        """设置当前主题"""
        result = self._repository.set_current_theme(theme_name)
        self._notify_change("theme", theme_name)
        return result
    
    def get_theme_colors(self, theme_name: str = None) -> Dict[str, str]:
        """
        获取主题颜色配置
        
        参数:
            theme_name: 主题名称，为None时使用当前主题
        
        返回:
            颜色配置字典
        """
        return self._repository.get_theme_colors(theme_name)
    
    def get_current_accent(self) -> str:
        """获取当前强调色名称"""
        return self._repository.get_current_accent()
    
    def set_current_accent(self, accent_name: str) -> bool:
        """设置当前强调色"""
        result = self._repository.set_current_accent(accent_name)
        self._notify_change("accent", accent_name)
        return result
    
    def get_accent_color(self, accent_name: str = None) -> str:
        """
        获取强调色值
        
        参数:
            accent_name: 强调色名称，为None时使用当前强调色
        
        返回:
            强调色值，如 "#0078D4"
        """
        return self._repository.get_accent_color(accent_name)
    
    def get_all_themes(self) -> List[str]:
        """获取所有主题名称列表"""
        return self._repository.get_all_themes()
    
    def get_all_accents(self) -> List[Dict[str, str]]:
        """获取所有强调色列表"""
        return self._repository.get_all_accents()
    
    # ============================================
    # UI配置接口
    # ============================================
    
    def get_ui_config(self, category: str, key: str, default: Any = None) -> Any:
        """
        获取UI配置值
        
        参数:
            category: 配置分类，如 "卡片"、"下拉框"、"输入框"、"控件布局"、"导航"、"图标"
            key: 配置键，如 "最小高度"、"宽度"、"高度"等
            default: 默认值
        
        返回:
            配置值
        
        示例:
            config_service.get_ui_config("卡片", "最小高度", 92)
            config_service.get_ui_config("下拉框", "宽度", 120)
        """
        return self._repository.get_ui_config(category, key, default)
    
    def get_ui_category(self, category: str) -> Dict[str, Any]:
        """
        获取UI配置分类的完整配置
        
        参数:
            category: 配置分类
        
        返回:
            该分类的完整配置字典
        """
        return self._repository.get_ui_category(category)
    
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
        return self._repository.set_ui_config(category, key, value)
    
    # ============================================
    # 便捷方法：常用UI配置
    # ============================================
    
    def get_card_min_height(self) -> int:
        """获取卡片最小高度"""
        return self.get_ui_config("卡片", "最小高度", 92)
    
    def get_card_padding(self) -> int:
        """获取卡片内边距"""
        return self.get_ui_config("卡片", "内边距", 6)
    
    def get_dropdown_size(self) -> Dict[str, int]:
        """获取下拉框尺寸"""
        return {
            "width": self.get_ui_config("下拉框", "宽度", 120),
            "height": self.get_ui_config("下拉框", "高度", 30)
        }
    
    def get_input_size(self) -> Dict[str, int]:
        """获取输入框尺寸"""
        return {
            "width": self.get_ui_config("输入框", "宽度", 120),
            "height": self.get_ui_config("输入框", "高度", 30)
        }
    
    def get_control_layout(self) -> Dict[str, int]:
        """获取控件布局参数"""
        return {
            "per_row": self.get_ui_config("控件布局", "每行控件数", 6),
            "h_spacing": self.get_ui_config("控件布局", "水平间距", 12),
            "v_spacing": self.get_ui_config("控件布局", "垂直间距", 8),
            "right_margin": self.get_ui_config("控件布局", "右边距", 16)
        }
    
    def get_nav_width(self) -> int:
        """获取导航栏宽度"""
        return self.get_ui_config("导航", "宽度", 240)
    
    def get_icon_sizes(self) -> Dict[str, int]:
        """获取图标相关尺寸"""
        return {
            "card_icon": self.get_ui_config("图标", "卡片图标大小", 22),
            "title_font": self.get_ui_config("图标", "标题字体大小", 14),
            "subtitle_font": self.get_ui_config("图标", "副标题字体大小", 11)
        }
    
    def register_on_change(self, callback: Callable):
        """注册配置变更回调"""
        self._on_change_callbacks.append(callback)
    
    def unregister_on_change(self, callback: Callable):
        """注销配置变更回调"""
        if callback in self._on_change_callbacks:
            self._on_change_callbacks.remove(callback)
    
    # ============================================
    # 界面配置接口（从界面配置.json读取）
    # ============================================
    
    def get_card_info(self, section: str) -> Dict[str, Any]:
        """
        获取卡片信息（从界面配置.json读取）
        
        参数:
            section: 配置节，如 "建筑设置.主帅主城"
        
        返回:
            {"title": "主帅主城", "icon": "DOMAIN", "subtitle": "设置主帅主城建筑等级", "enabled": true}
        """
        ui_config = self._repository.load_ui_config()
        section_config = ui_config.get("界面配置", {}).get(section, {})
        return section_config.get("卡片信息", {"title": section, "icon": "HOME", "subtitle": "", "enabled": true})
    
    def get_card_enabled_default(self, section: str) -> bool:
        """
        获取卡片默认开关状态（从界面配置.json读取）
        
        参数:
            section: 配置节
        
        返回:
            默认开关状态
        """
        card_info = self.get_card_info(section)
        return card_info.get("enabled", True)
    
    def get_controls(self, section: str) -> List[Dict[str, Any]]:
        """
        获取控件列表（从界面配置.json读取）
        
        参数:
            section: 配置节
        
        返回:
            [{"id": "城市等级", "type": "dropdown", "label": "城市", "options": [...], "default": "17"}, ...]
        """
        ui_config = self._repository.load_ui_config()
        section_config = ui_config.get("界面配置", {}).get(section, {})
        return section_config.get("控件列表", [])
    
    def get_control_config(self, section: str, control_id: str) -> Dict[str, Any]:
        """
        获取单个控件配置（从界面配置.json读取）
        
        参数:
            section: 配置节
            control_id: 控件ID
        
        返回:
            {"id": "城市等级", "type": "dropdown", "label": "城市", "options": [...], "default": "17"}
        """
        controls = self.get_controls(section)
        for ctrl in controls:
            if ctrl.get("id") == control_id:
                return ctrl
        return {}
    
    def get_control_label(self, section: str, control_id: str) -> str:
        """获取控件标签"""
        config = self.get_control_config(section, control_id)
        return config.get("label", control_id)
    
    def get_control_options(self, section: str, control_id: str) -> List[str]:
        """获取控件选项列表（简化格式）"""
        config = self.get_control_config(section, control_id)
        return config.get("options", [])
    
    def get_control_default(self, section: str, control_id: str) -> str:
        """获取控件默认值"""
        config = self.get_control_config(section, control_id)
        return config.get("default", "")
    
    def reset_section_to_default(self, section: str) -> bool:
        """
        恢复指定section的所有控件为默认值
        
        参数:
            section: 配置节
        
        返回:
            是否成功
        """
        controls = self.get_controls(section)
        for ctrl in controls:
            control_id = ctrl.get("id")
            default_value = ctrl.get("default", "")
            if control_id and default_value:
                self.set_value(section, control_id, default_value)
        return True
    
    def get_all_sections(self) -> List[str]:
        """获取所有配置节列表"""
        ui_config = self._repository.load_ui_config()
        return list(ui_config.get("界面配置", {}).keys())

# ============================================
# 内部逻辑（不暴露）
# ============================================

def _notify_change(self, key: str, value: Any):
    """通知配置变更"""
    for callback in self._on_change_callbacks:
        try:
            callback(key, value)
        except Exception:
            pass

ConfigService._notify_change = _notify_change

# *** 标准测试格式: 仅调用被测模块,AI不得添加数据 ***
if __name__ == "__main__":
    service = ConfigService()
    
    print("测试配置服务...")
    print(f"当前方案: {service.get_current_scheme_name()}")
    print(f"方案列表: {service.get_scheme_list()}")
    
    service.set_text_value("系统设置", "挂机速度", "100", "100")
    print(f"挂机速度: {service.get_text_value('系统设置', '挂机速度')}")
    
    print("\n--- 测试主题配置 ---")
    print(f"当前主题: {service.get_current_theme()}")
    print(f"当前强调色: {service.get_current_accent()}")
    print(f"主题颜色: {service.get_theme_colors()}")
    print(f"强调色值: {service.get_accent_color()}")
    print(f"所有主题: {service.get_all_themes()}")
    print(f"所有强调色: {service.get_all_accents()}")
    
    print("\n测试完成")
