# -*- coding: utf-8 -*-
"""
模块名称：SharedOptions
模块功能：定义共享的下拉框选项列表，避免重复创建
根据按键精灵界面布局.txt中的实际选项范围定义
"""

from typing import List

# ==================== 数字选项列表 ====================

# 00-06 (7个选项) - 24个下拉框使用
SHARED_OPTIONS_00_TO_06 = [f"{i:02d}" for i in range(0, 7)]

# 00-10 (11个选项) - 7个下拉框使用
SHARED_OPTIONS_00_TO_10 = [f"{i:02d}" for i in range(0, 11)]

# 00-15 (16个选项) - 3个下拉框使用
SHARED_OPTIONS_00_TO_15 = [f"{i:02d}" for i in range(0, 16)]

# 00-25 (26个选项) - 6个下拉框使用
SHARED_OPTIONS_00_TO_25 = [f"{i:02d}" for i in range(0, 26)]

# 00-40 (41个选项) - 3个下拉框使用
SHARED_OPTIONS_00_TO_40 = [f"{i:02d}" for i in range(0, 41)]

# ==================== 文本选项列表 ====================

# 自动/手动
SHARED_TEXT_AUTO_MANUAL = ["自动", "手动"]

# 城市/资源/城资
SHARED_TEXT_CITY_RESOURCE = ["城市", "资源", "城资"]

# 自动/经济/铁矿/橡胶/油井
SHARED_TEXT_AUTO_ECONOMY = ["自动", "经济", "铁矿", "橡胶", "油井"]

# 停止攻占/自动攻占
SHARED_TEXT_STOP_AUTO = ["停止攻占", "自动攻占"]

# 城区战场/政区战场
SHARED_TEXT_BATTLEFIELD = ["城区战场", "政区战场"]

# 1级步兵旅/2级侦察旅/3级轻坦师
SHARED_TEXT_TROOP_LEVEL = ["1级步兵旅", "2级侦察旅", "3级轻坦师"]

# 平台选项
SHARED_TEXT_PLATFORM = ["Tap", "九游", "Fan", " 小7", "Vivo", "Opop"]

# 主帅/付帅
SHARED_TEXT_COMMANDER = ["主帅", "付帅"]

# 野怪等级选择
SHARED_TEXT_MONSTER_LEVEL = ["全部", "1-3级", "4-6级", "7-9级", "10级以上"]

# 搜索频率选择
SHARED_TEXT_SEARCH_FREQUENCY = ["每30分钟", "每小时", "每2小时", "每4小时"]

# 建筑优先 - 资源建筑选项 (24个选项)
SHARED_TEXT_BUILDING_PRIORITY = [
    "自动平衡", "农场/铁矿/油井/橡胶", "农场/橡胶/铁矿/油井", "农场/橡胶/油井/铁矿",
    "农场/油井/铁矿/橡胶", "农场/油井/橡胶/铁矿", "铁矿/农场/橡胶/油井",
    "铁矿/农场/油井/橡胶", "铁矿/橡胶/农场/油井", "铁矿/橡胶/油井/农场",
    "铁矿/油井/农场/橡胶", "铁矿/油井/橡胶/农场", "橡胶/农场/铁矿/油井",
    "橡胶/农场/油井/铁矿", "橡胶/铁矿/农场/油井", "橡胶/铁矿/油井/农场",
    "橡胶/油井/农场/铁矿", "橡胶/油井/铁矿/农场", "油井/农场/铁矿/橡胶",
    "油井/农场/橡胶/铁矿", "油井/铁矿/农场/橡胶", "油井/铁矿/橡胶/农场",
    "油井/橡胶/农场/铁矿", "油井/橡胶/铁矿/农场"
]

# 建筑优先 - 塔防建筑选项 (2个选项)
SHARED_TEXT_DEFENSE_PRIORITY = ["炮塔/岸防", "岸防/炮塔"]

# ==================== 其他系统选项 ====================

# 控制3选项: 100-500ms (9个选项)
SHARED_OPTIONS_MS_LIMIT = ["100", "150", "200", "250", "300", "350", "400", "450", "500"]

# 控制4选项: 尝试次数 (5个选项)
SHARED_OPTIONS_TRY_COUNT = ["10", "15", "20", "25", "30"]

# 控制5选项: 清缓大小 (9个选项)
SHARED_OPTIONS_CLEAR_SIZE = ["1.0", "1.5", "2.0", "2.5", "3.0", "3.5", "4.0", "4.5", "5.0"]

# 控制6/8/11选项: 城加速 (11个选项)
SHARED_OPTIONS_CITY_SPEED = ["05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15"]

# 控制10选项: 库存时间 (8个选项)
SHARED_OPTIONS_STOCK_TIME = ["30", "60", "90", "120", "150", "180", "210", "240"]

# 控制15选项: 战场等级 (6个选项)
SHARED_OPTIONS_BATTLE_LEVEL = ["10", "11", "12", "13", "14", "15"]

# 控制17选项: 资源集结等级 (4个选项)
SHARED_OPTIONS_RESOURCE_LEVEL = ["10", "15", "20", "25"]

# 控制18选项: 资源数量 (19个选项)
SHARED_OPTIONS_RESOURCE_AMOUNT = ["2", "3", "4", "5", "6", "7", "8", "9", "10", 
                                  "11", "12", "13", "14", "15", "16", "17", "18", "19", "20"]

# ==================== 辅助函数 ====================

def get_options_for_building(config_key: str) -> list:
    """
    根据建筑配置键返回对应的共享选项列表
    
    Args:
        config_key: 配置键，如"主帅主城_城市"
    
    Returns:
        对应的共享选项列表
    
    注意：此函数返回建筑等级选项
    """
    # 建筑配置都使用00-40的建筑等级选项
    return SHARED_OPTIONS_00_TO_40


def get_options_for_control(control_name: str) -> list:
    """
    根据控制名称返回对应的共享选项列表
    
    Args:
        control_name: 控制名称，如"控制1"
    
    Returns:
        对应的共享选项列表
    """
    control_options = {
        "控制1": SHARED_TEXT_AUTO_MANUAL,
        "控制2": SHARED_TEXT_AUTO_MANUAL,
        "控制3": SHARED_OPTIONS_MS_LIMIT,
        "控制4": SHARED_OPTIONS_TRY_COUNT,
        "控制5": SHARED_OPTIONS_CLEAR_SIZE,
        "控制6": SHARED_OPTIONS_CITY_SPEED,
        "控制7": SHARED_TEXT_CITY_RESOURCE,
        "控制8": SHARED_OPTIONS_CITY_SPEED,
        "控制9": SHARED_TEXT_AUTO_ECONOMY,
        "控制10": SHARED_OPTIONS_STOCK_TIME,
        "控制11": SHARED_OPTIONS_CITY_SPEED,
        "控制13": SHARED_TEXT_BATTLEFIELD,
        "控制14": SHARED_TEXT_STOP_AUTO,
        "控制15": SHARED_OPTIONS_BATTLE_LEVEL,
        "控制16": SHARED_TEXT_TROOP_LEVEL,
        "控制17": SHARED_OPTIONS_RESOURCE_LEVEL,
        "控制18": SHARED_OPTIONS_RESOURCE_AMOUNT,
        "控制22": SHARED_TEXT_PLATFORM,
        "统帅1": SHARED_TEXT_COMMANDER,
        "统帅3": SHARED_TEXT_PLATFORM,
        "统帅5": SHARED_TEXT_COMMANDER,
        "统帅7": SHARED_TEXT_PLATFORM,
        # 可以继续添加其他控制
    }
    
    return control_options.get(control_name, SHARED_OPTIONS_00_TO_06)


# ==================== 测试代码 ====================

if __name__ == "__main__":
    # 测试建筑选项
    test_cases = [
        ("主帅主城_城市", "SHARED_OPTIONS_00_TO_40"),
        ("主帅主城_兵工", "SHARED_OPTIONS_00_TO_25"),
        ("主帅主城_陆军", "SHARED_OPTIONS_00_TO_25"),
        ("主帅主城_空军", "SHARED_OPTIONS_00_TO_15"),
        ("主帅主城_商业", "SHARED_OPTIONS_00_TO_06"),
        ("军团城市_编号", "SHARED_OPTIONS_00_TO_10"),
        ("资源建筑", "SHARED_TEXT_BUILDING_PRIORITY"),
        ("塔防建筑", "SHARED_TEXT_DEFENSE_PRIORITY"),
    ]
    
    print("测试建筑选项映射:")
    for config_key, expected in test_cases:
        options = get_options_for_building(config_key)
        if expected.startswith("SHARED_TEXT"):
            print(f"{config_key}: 文本选项 ({len(options)}个)")
        else:
            print(f"{config_key}: {options[0]}-{options[-1]} ({len(options)}个选项)")
    
    # 测试控制选项
    print("\n测试控制选项映射:")
    control_tests = ["控制1", "控制3", "控制6", "控制9", "控制14", "控制22"]
    for control in control_tests:
        options = get_options_for_control(control)
        print(f"{control}: {options[:3]}... ({len(options)}个选项)")