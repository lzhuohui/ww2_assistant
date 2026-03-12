# -*- coding: utf-8 -*-
"""
建筑配置 - 配置层

设计思路:
    定义所有建筑设置的配置格式，实现配置驱动架构。
    统一配置格式，便于管理和扩展。

功能:
    1. 定义建筑配置格式
    2. 提供建筑配置数据
    3. 支持配置扩展

数据来源:
    静态配置数据。

使用场景:
    被 ConfigManager 调用。
"""

# *** 用户指定变量 - AI不得修改 ***
DEFAULT_DROPDOWN_WIDTH = 60  # 下拉框默认宽度
# *********************************

# 等级选项 (01-20)
LEVELS = [f"{i:02d}" for i in range(1, 21)]
LEVELS_0 = [f"{i:02d}" for i in range(0, 21)]


def create_dropdown(config_key: str, label: str, value: str, options: list = None):
    """
    创建下拉框配置
    
    参数:
        config_key: 配置键
        label: 标签
        value: 默认值
        options: 选项列表（默认为LEVELS）
    
    返回:
        dict: 下拉框配置字典
    """
    return {
        "type": "dropdown",
        "config_key": config_key,
        "label": label,
        "options": options if options is not None else LEVELS,
        "value": value,
        "width": DEFAULT_DROPDOWN_WIDTH,
    }


# 建筑配置字典
建筑配置 = {
    "主帅主城": {
        "card_type": "standard",
        "title": "主帅主城",
        "icon": "HOME",
        "subtitle": "",
        "enabled": True,
        "controls_per_row": 6,
        "controls": [
            create_dropdown("主帅主城_城市", "城市", "17"),
            create_dropdown("主帅主城_兵工", "兵工", "17"),
            create_dropdown("主帅主城_陆军", "陆军", "14"),
            create_dropdown("主帅主城_空军", "空军", "03"),
            create_dropdown("主帅主城_商业", "商业", "04"),
            create_dropdown("主帅主城_补给", "补给", "03"),
            create_dropdown("主帅主城_内塔", "内塔", "04"),
            create_dropdown("主帅主城_村庄", "村庄", "03"),
            create_dropdown("主帅主城_资源", "资源", "03"),
            create_dropdown("主帅主城_军工", "军工", "03"),
            create_dropdown("主帅主城_港口", "港口", "03"),
            create_dropdown("主帅主城_外塔", "外塔", "03"),
        ],
    },
    "主帅分城": {
        "card_type": "standard",
        "title": "主帅分城",
        "icon": "LOCATION_CITY",
        "subtitle": "",
        "enabled": True,
        "controls_per_row": 6,
        "controls": [
            create_dropdown("主帅分城_城市", "城市", "15"),
            create_dropdown("主帅分城_兵工", "兵工", "10"),
            create_dropdown("主帅分城_陆军", "陆军", "10"),
            create_dropdown("主帅分城_空军", "空军", "03"),
            create_dropdown("主帅分城_商业", "商业", "04"),
            create_dropdown("主帅分城_补给", "补给", "03"),
            create_dropdown("主帅分城_内塔", "内塔", "03"),
            create_dropdown("主帅分城_村庄", "村庄", "03"),
            create_dropdown("主帅分城_资源", "资源", "03"),
            create_dropdown("主帅分城_军工", "军工", "03"),
            create_dropdown("主帅分城_港口", "港口", "03"),
            create_dropdown("主帅分城_外塔", "外塔", "03"),
        ],
    },
    "付帅主城": {
        "card_type": "standard",
        "title": "付帅主城",
        "icon": "APARTMENT",
        "subtitle": "",
        "enabled": True,
        "controls_per_row": 6,
        "controls": [
            create_dropdown("付帅主城_城市", "城市", "15"),
            create_dropdown("付帅主城_兵工", "兵工", "10"),
            create_dropdown("付帅主城_陆军", "陆军", "10"),
            create_dropdown("付帅主城_空军", "空军", "03"),
            create_dropdown("付帅主城_商业", "商业", "04"),
            create_dropdown("付帅主城_补给", "补给", "03"),
            create_dropdown("付帅主城_内塔", "内塔", "03"),
            create_dropdown("付帅主城_村庄", "村庄", "03"),
            create_dropdown("付帅主城_资源", "资源", "03"),
            create_dropdown("付帅主城_军工", "军工", "03"),
            create_dropdown("付帅主城_港口", "港口", "03"),
            create_dropdown("付帅主城_外塔", "外塔", "03"),
        ],
    },
    "付帅分城": {
        "card_type": "standard",
        "title": "付帅分城",
        "icon": "BUSINESS",
        "subtitle": "",
        "enabled": True,
        "controls_per_row": 6,
        "controls": [
            create_dropdown("付帅分城_城市", "城市", "15"),
            create_dropdown("付帅分城_兵工", "兵工", "10"),
            create_dropdown("付帅分城_陆军", "陆军", "10"),
            create_dropdown("付帅分城_空军", "空军", "03"),
            create_dropdown("付帅分城_商业", "商业", "04"),
            create_dropdown("付帅分城_补给", "补给", "03"),
            create_dropdown("付帅分城_内塔", "内塔", "03"),
            create_dropdown("付帅分城_村庄", "村庄", "03"),
            create_dropdown("付帅分城_资源", "资源", "03"),
            create_dropdown("付帅分城_军工", "军工", "03"),
            create_dropdown("付帅分城_港口", "港口", "03"),
            create_dropdown("付帅分城_外塔", "外塔", "03"),
        ],
    },
    "军团城市": {
        "card_type": "standard",
        "title": "军团城市",
        "icon": "FORT",
        "subtitle": "",
        "enabled": True,
        "controls_per_row": 4,
        "controls": [
            create_dropdown("军团城市_城市", "城市", "05"),
            create_dropdown("军团城市_兵工", "兵工", "05"),
            create_dropdown("军团城市_军需", "军需", "05"),
            create_dropdown("军团城市_编号", "编号", "01"),
            create_dropdown("军团城市_陆军", "陆军", "00", LEVELS_0),
            create_dropdown("军团城市_空军", "空军", "00", LEVELS_0),
            create_dropdown("军团城市_炮塔", "炮塔", "00", LEVELS_0),
        ],
    },
}


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    import json
    
    print("=" * 50)
    print("建筑配置调试")
    print("=" * 50)
    
    print(f"\n用户指定变量:")
    print(f"  DEFAULT_DROPDOWN_WIDTH = {DEFAULT_DROPDOWN_WIDTH}")
    
    print(f"\n等级选项:")
    print(f"  LEVELS: {LEVELS[:5]} ... {LEVELS[-5:]}")
    print(f"  LEVELS_0: {LEVELS_0[:5]} ... {LEVELS_0[-5:]}")
    
    print(f"\n建筑配置:")
    for card_name, card_config in 建筑配置.items():
        print(f"\n  {card_name}:")
        print(f"    标题: {card_config['title']}")
        print(f"    图标: {card_config['icon']}")
        print(f"    副标题: {card_config['subtitle']}")
        print(f"    每行控件数: {card_config['controls_per_row']}")
        print(f"    控件数量: {len(card_config['controls'])}")
    
    print(f"\n完整配置（JSON格式）:")
    print(json.dumps(建筑配置, ensure_ascii=False, indent=2))
