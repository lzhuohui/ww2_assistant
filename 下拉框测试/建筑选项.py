#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
建筑选项数据 - 用于下拉框懒加载测试
包含各种建筑相关的选项数据
"""

from typing import List, Dict, Any
import json
import os


# ========== 城市选项 ==========
def get_city_options() -> List[str]:
    """获取城市选项"""
    return [
        "北京", "上海", "广州", "深圳", "杭州", "成都", "南京", "武汉",
        "西安", "重庆", "天津", "苏州", "郑州", "长沙", "沈阳", "青岛",
        "大连", "厦门", "宁波", "无锡", "佛山", "东莞", "济南", "合肥"
    ]


def get_province_options() -> List[str]:
    """获取省份选项"""
    return [
        "北京市", "上海市", "广东省", "江苏省", "浙江省", "四川省", "湖北省",
        "陕西省", "重庆市", "天津市", "河南省", "湖南省", "辽宁省", "山东省",
        "福建省", "安徽省", "河北省", "山西省", "吉林省", "黑龙江省"
    ]


# ========== 建筑等级选项 ==========
def get_building_levels() -> List[str]:
    """获取建筑等级选项 (1-50级)"""
    return [f"{i:02d}" for i in range(1, 51)]


def get_quick_levels() -> List[str]:
    """获取常用等级选项"""
    return ["05", "10", "15", "20", "25", "30", "35", "40", "45", "50"]


# ========== 建筑类型选项 ==========
def get_building_types() -> List[str]:
    """获取建筑类型选项"""
    return [
        "市政厅", "兵营", "研究所", "医院", "农场", "伐木场", "矿场", "炼钢厂",
        "城墙", "箭塔", "炮台", "仓库", "市场", "使馆", "学院", "工坊",
        "船坞", "机场", "雷达站", "导弹井"
    ]


def get_resource_buildings() -> List[str]:
    """获取资源建筑选项"""
    return ["农场", "伐木场", "矿场", "炼钢厂", "油井", "发电厂", "水厂"]


def get_military_buildings() -> List[str]:
    """获取军事建筑选项"""
    return ["兵营", "城墙", "箭塔", "炮台", "兵工厂", "训练场", "防御工事"]


def get_research_buildings() -> List[str]:
    """获取科研建筑选项"""
    return ["研究所", "学院", "实验室", "图书馆", "科技中心"]


# ========== 升级策略选项 ==========
def get_upgrade_strategies() -> List[str]:
    """获取升级策略选项"""
    return [
        "优先升级", "资源充足时升级", "科技优先", "防御优先", "攻击优先",
        "资源优先", "保持最低等级", "手动升级", "自动升级", "按计划升级"
    ]


# ========== 配置相关 ==========
def load_config() -> Dict[str, Any]:
    """加载配置文件"""
    config_path = os.path.join(os.path.dirname(__file__), "建筑配置.json")
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def get_config_value(key_path: str, default=None) -> Any:
    """获取配置值"""
    config = load_config()
    
    # 支持点分隔的路径，如 "全局配置.性能设置.懒加载启用"
    keys = key_path.split('.')
    value = config
    
    for key in keys:
        if isinstance(value, dict) and key in value:
            value = value[key]
        else:
            return default
    
    return value


def get_user_preferences() -> Dict[str, Any]:
    """获取用户偏好"""
    config = load_config()
    return config.get("用户偏好", {})


def get_quick_settings() -> Dict[str, List[str]]:
    """获取快捷设置"""
    prefs = get_user_preferences()
    return prefs.get("快捷配置", {})


# ========== 测试数据生成 ==========
def generate_test_data(count: int = 100) -> List[str]:
    """生成测试数据"""
    return [f"测试选项_{i:03d}" for i in range(1, count + 1)]


def generate_building_names(prefix: str = "建筑", count: int = 50) -> List[str]:
    """生成建筑名称"""
    return [f"{prefix}_{i:02d}" for i in range(1, count + 1)]


# ========== 数据验证 ==========
def validate_option(option: str, options_list: List[str]) -> bool:
    """验证选项是否有效"""
    return option in options_list


def get_default_value(options_list: List[str]) -> str:
    """获取默认值（第一个选项）"""
    return options_list[0] if options_list else ""


# ========== 导出函数 ==========
__all__ = [
    # 城市选项
    "get_city_options",
    "get_province_options",
    
    # 建筑等级
    "get_building_levels",
    "get_quick_levels",
    
    # 建筑类型
    "get_building_types",
    "get_resource_buildings",
    "get_military_buildings",
    "get_research_buildings",
    
    # 升级策略
    "get_upgrade_strategies",
    
    # 配置相关
    "load_config",
    "get_config_value",
    "get_user_preferences",
    "get_quick_settings",
    
    # 测试数据
    "generate_test_data",
    "generate_building_names",
    
    # 数据验证
    "validate_option",
    "get_default_value",
]


if __name__ == "__main__":
    # 测试数据输出
    print("=" * 60)
    print("建筑选项数据测试")
    print("=" * 60)
    
    print(f"城市选项: {len(get_city_options())} 个")
    print(f"建筑等级: {len(get_building_levels())} 个")
    print(f"建筑类型: {len(get_building_types())} 个")
    print(f"升级策略: {len(get_upgrade_strategies())} 个")
    
    # 测试配置加载
    config = load_config()
    if config:
        print(f"\n配置加载成功，版本: {config.get('version', '未知')}")
        print(f"建筑类型数量: {len(config.get('建筑类型配置', {}))}")
    else:
        print("\n配置加载失败，请检查建筑配置.json文件")
    
    print("=" * 60)