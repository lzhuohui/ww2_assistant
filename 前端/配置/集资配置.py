# -*- coding: utf-8 -*-
"""
集资配置 - 配置层

设计思路:
    定义集资相关的卡片配置。
    使用配置驱动架构，统一配置格式。

功能:
    1. 小号上贡卡片配置
    2. 分城纳租卡片配置

数据来源:
    部分数据来自按键精灵脚本。

使用场景:
    被 ConfigManager 调用。
"""

# *** 用户指定变量 - AI不得修改 ***
DROPDOWN_WIDTH = 80  # 下拉框宽度
# *********************************

# 等级选项 (05-15级)
LEVELS = [f"{i:02d}级" for i in range(5, 16)]

# 数量选项 (2-20万)
AMOUNTS = [f"{i}万" for i in range(2, 21)]

# 统帅选项
COMMANDERS = ["统帅A", "统帅B", "统帅C", "统帅D", "统帅E"]


def create_dropdown(config_key: str, label: str, value: str, options: list = None, width: int = DROPDOWN_WIDTH, unit: str = ""):
    """
    创建下拉框配置
    
    参数:
        config_key: 配置键
        label: 标签
        value: 默认值
        options: 选项列表
        width: 宽度（默认为DROPDOWN_WIDTH）
        unit: 单位
    
    返回:
        dict: 下拉框配置字典
    """
    dropdown_config = {
        "type": "dropdown",
        "config_key": config_key,
        "label": label,
        "options": options if options is not None else LEVELS,
        "value": value,
        "unit": unit,
        "width": width,
    }
    
    return dropdown_config


# ==================== 小号上贡卡片 ====================

小号上贡配置 = {
    "card_name": "小号上贡",
    "title": "小号上贡",
    "icon": "UPLOAD",
    "subtitle": "设置小号上贡相关参数",
    "card_type": "standard",
    "controls_per_row": 2,
    "controls": [
        create_dropdown(
            config_key="上贡限级",
            label="上贡限级:",
            value="05级",
            options=LEVELS,
        ),
        create_dropdown(
            config_key="上贡限量",
            label="上贡限量:",
            value="2万",
            options=AMOUNTS,
        ),
        create_dropdown(
            config_key="主要统帅",
            label="主要统帅:",
            value="统帅A",
            options=COMMANDERS,
        ),
        create_dropdown(
            config_key="备用统帅",
            label="备用统帅:",
            value="统帅B",
            options=COMMANDERS,
        ),
    ],
}


# ==================== 分城纳租卡片 ====================

分城纳租配置 = {
    "card_name": "分城纳租",
    "title": "分城纳租",
    "icon": "ATTACH_MONEY",
    "subtitle": "设置分城纳租相关参数",
    "card_type": "standard",
    "controls_per_row": 2,
    "controls": [
        create_dropdown(
            config_key="纳租限级",
            label="纳租限级:",
            value="05级",
            options=LEVELS,
        ),
        create_dropdown(
            config_key="纳租限量",
            label="纳租限量:",
            value="2万",
            options=AMOUNTS,
        ),
    ],
}


# ==================== 所有卡片配置 ====================

集资卡片配置 = {
    "小号上贡": 小号上贡配置,
    "分城纳租": 分城纳租配置,
}


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    print("=== 集资配置调试 ===")
    print(f"下拉框宽度: {DROPDOWN_WIDTH}")
    print(f"等级选项: {LEVELS}")
    print(f"数量选项: {AMOUNTS}")
    print(f"统帅选项: {COMMANDERS}")
    print(f"\n卡片配置数量: {len(集资卡片配置)}")
    for name, config in 集资卡片配置.items():
        print(f"  - {name}: {len(config.get('controls', []))} 个控件")
