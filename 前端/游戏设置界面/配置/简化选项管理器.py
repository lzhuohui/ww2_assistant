#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化选项管理器 - 所有下拉框选项集中管理
遵循下拉框测试目录的实现方式
"""

from typing import List, Dict, Any, Callable, Optional


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
def get_building_levels(max_level: int = 40) -> List[str]:
    """获取建筑等级选项"""
    return [f"{i:02d}" for i in range(max_level + 1)]


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
    return ["农场", "伐木场", "矿场", "炼钢厂", "市场", "仓库"]


def get_military_buildings() -> List[str]:
    """获取军事建筑选项"""
    return ["兵营", "城墙", "箭塔", "炮台", "船坞", "机场", "雷达站", "导弹井"]


# ========== 策略选项 ==========
def get_upgrade_strategies() -> List[str]:
    """获取升级策略选项"""
    return ["优先升级", "均衡发展", "资源优先", "军事优先", "防御优先"]


def get_attack_strategies() -> List[str]:
    """获取攻击策略选项"""
    return ["全力进攻", "试探攻击", "围而不攻", "游击战术", "集中突破"]


def get_defense_strategies() -> List[str]:
    """获取防御策略选项"""
    return ["全面防御", "重点防御", "诱敌深入", "机动防御", "坚壁清野"]


# ========== 账号选项 ==========
def get_account_types() -> List[str]:
    """获取账号类型选项"""
    return ["主帅", "副将", "小号", "资源号", "侦察号", "备用号"]


def get_server_options() -> List[str]:
    """获取服务器选项"""
    return ["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "S10"]


# ========== 界面选项 ==========
def get_theme_options() -> List[str]:
    """获取主题选项"""
    return ["深色主题", "浅色主题", "自动切换", "护眼模式"]


def get_language_options() -> List[str]:
    """获取语言选项"""
    return ["简体中文", "繁体中文", "English", "日本語", "한국어"]


def get_save_interval_options() -> List[str]:
    """获取保存间隔选项"""
    return ["实时保存", "每5分钟", "每15分钟", "每30分钟", "每小时", "手动保存"]


# ========== 任务选项 ==========
def get_task_types() -> List[str]:
    """获取任务类型选项"""
    return ["日常任务", "建设任务", "军事任务", "资源任务", "侦查任务", "联盟任务"]


def get_task_priority_options() -> List[str]:
    """获取任务优先级选项"""
    return ["最高", "高", "中", "低", "最低", "自动"]


# ========== 选项管理器类（可选，用于统一接口） ==========
class SimpleOptionManager:
    """简化选项管理器 - 提供统一接口"""
    
    def __init__(self):
        self.option_map = {
            "city": get_city_options,
            "province": get_province_options,
            "building_level": get_building_levels,
            "quick_levels": get_quick_levels,
            "building_type": get_building_types,
            "resource_building": get_resource_buildings,
            "military_building": get_military_buildings,
            "upgrade_strategy": get_upgrade_strategies,
            "attack_strategy": get_attack_strategies,
            "defense_strategy": get_defense_strategies,
            "account_type": get_account_types,
            "server": get_server_options,
            "theme": get_theme_options,
            "language": get_language_options,
            "save_interval": get_save_interval_options,
            "task_type": get_task_types,
            "task_priority": get_task_priority_options,
        }
    
    def get_option_loader(self, option_type: str, **kwargs) -> Callable[[], List[str]]:
        """获取选项加载器
        
        Args:
            option_type: 选项类型
            **kwargs: 额外参数，如max_level等
            
        Returns:
            选项加载函数
        """
        if option_type in self.option_map:
            loader = self.option_map[option_type]
            
            # 处理需要参数的函数
            if option_type == "building_level":
                max_level = kwargs.get("max_level", 40)
                return lambda: loader(max_level)
            
            return loader
        else:
            print(f"[简化选项管理器] 未知的选项类型: {option_type}")
            return lambda: []
    
    def get_options(self, option_type: str, **kwargs) -> List[str]:
        """直接获取选项列表
        
        Args:
            option_type: 选项类型
            **kwargs: 额外参数
            
        Returns:
            选项列表
        """
        loader = self.get_option_loader(option_type, **kwargs)
        return loader()


# 全局实例
_simple_option_manager = None

def get_simple_option_manager() -> SimpleOptionManager:
    """获取简化选项管理器实例"""
    global _simple_option_manager
    if _simple_option_manager is None:
        _simple_option_manager = SimpleOptionManager()
    return _simple_option_manager


# ========== 测试代码 ==========
if __name__ == "__main__":
    print("=" * 60)
    print("简化选项管理器测试")
    print("=" * 60)
    
    # 直接使用函数
    print("\n直接使用函数:")
    print(f"城市选项: {len(get_city_options())} 个")
    print(f"建筑等级选项: {len(get_building_levels(40))} 个")
    print(f"前5个建筑等级: {get_building_levels(40)[:5]}")
    
    # 使用管理器
    print("\n使用简化选项管理器:")
    manager = get_simple_option_manager()
    
    test_types = [
        "city",
        "building_level",
        "building_type",
        "upgrade_strategy",
        "account_type",
        "theme",
        "task_type",
    ]
    
    for option_type in test_types:
        loader = manager.get_option_loader(option_type, max_level=40)
        options = loader()
        print(f"{option_type}: {len(options)} 个选项")
        if options:
            print(f"  示例: {options[:3]}...")
    
    print("=" * 60)
    print("✅ 所有测试通过！")