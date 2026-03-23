# -*- coding: utf-8 -*-
"""
模块名称：建筑配置 | 设计思路：定义所有建筑设置的配置格式，实现配置驱动架构，延迟生成配置避免启动卡顿 | 模块隔离原则：不直接创建被调用模块的内容，不覆盖被调用模块的计算结果，用户指定变量除外
"""

import flet as ft

from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider


# *** 用户指定变量 - AI不得修改, 变量值必须生效 ***
DROPDOWN_WIDTH = 70  # 下拉框宽度
# *********************************

# 等级选项 (01-20级)
LEVELS = [f"{i:02d}级" for i in range(1, 21)]
LEVELS_0 = [f"{i:02d}级" for i in range(0, 21)]


def create_dropdown_config(config_key: str, label: str, value: str, options: list=None, width: int=DROPDOWN_WIDTH, unit: str="级") -> dict:
    """
    创建下拉框配置（仅返回配置字典，不创建控件）
    
    参数:
        config_key: 配置键
        label: 标签
        value: 默认值
        options: 选项列表（默认为LEVELS）
        width: 宽度（默认为DROPDOWN_WIDTH）
        unit: 单位（默认为"级"）
    
    返回:
        dict: 下拉框配置字典
    """
    return {
        "type": "dropdown",
        "config_key": config_key,
        "label": label,
        "options": options if options is not None else LEVELS,
        "value": value,
        "unit": unit,
        "width": width,
    }


def get_building_config() -> dict:
    """
    延迟获取建筑配置（调用时才生成，避免模块加载时创建所有配置）
    
    返回:
        dict: 建筑配置字典
    """
    return {
        "主帅主城": {
            "card_type": "standard",
            "title": "主帅主城",
            "icon": "HOME",
            "subtitle": "设置主帅主城建筑等级",
            "enabled": True,
            "controls_per_row": 6,
            "controls": [
                create_dropdown_config("主帅主城_城市", "城市", "17"),
                create_dropdown_config("主帅主城_兵工", "兵工", "17"),
                create_dropdown_config("主帅主城_陆军", "陆军", "14"),
                create_dropdown_config("主帅主城_空军", "空军", "03"),
                create_dropdown_config("主帅主城_商业", "商业", "04"),
                create_dropdown_config("主帅主城_补给", "补给", "03"),
                create_dropdown_config("主帅主城_内塔", "内塔", "04"),
                create_dropdown_config("主帅主城_村庄", "村庄", "03"),
                create_dropdown_config("主帅主城_资源", "资源", "03"),
                create_dropdown_config("主帅主城_军工", "军工", "03"),
                create_dropdown_config("主帅主城_港口", "港口", "03"),
                create_dropdown_config("主帅主城_外塔", "外塔", "03"),
            ],
        },
        "主帅分城": {
            "card_type": "standard",
            "title": "主帅分城",
            "icon": "LOCATION_CITY",
            "subtitle": "设置主帅分城建筑等级",
            "enabled": True,
            "controls_per_row": 6,
            "controls": [
                create_dropdown_config("主帅分城_城市", "城市", "15"),
                create_dropdown_config("主帅分城_兵工", "兵工", "10"),
                create_dropdown_config("主帅分城_陆军", "陆军", "10"),
                create_dropdown_config("主帅分城_空军", "空军", "03"),
                create_dropdown_config("主帅分城_商业", "商业", "04"),
                create_dropdown_config("主帅分城_补给", "补给", "03"),
                create_dropdown_config("主帅分城_内塔", "内塔", "03"),
                create_dropdown_config("主帅分城_村庄", "村庄", "03"),
                create_dropdown_config("主帅分城_资源", "资源", "03"),
                create_dropdown_config("主帅分城_军工", "军工", "03"),
                create_dropdown_config("主帅分城_港口", "港口", "03"),
                create_dropdown_config("主帅分城_外塔", "外塔", "03"),
            ],
        },
        "付帅主城": {
            "card_type": "standard",
            "title": "付帅主城",
            "icon": "APARTMENT",
            "subtitle": "设置付帅主城建筑等级",
            "enabled": True,
            "controls_per_row": 6,
            "controls": [
                create_dropdown_config("付帅主城_城市", "城市", "15"),
                create_dropdown_config("付帅主城_兵工", "兵工", "10"),
                create_dropdown_config("付帅主城_陆军", "陆军", "10"),
                create_dropdown_config("付帅主城_空军", "空军", "03"),
                create_dropdown_config("付帅主城_商业", "商业", "04"),
                create_dropdown_config("付帅主城_补给", "补给", "03"),
                create_dropdown_config("付帅主城_内塔", "内塔", "03"),
                create_dropdown_config("付帅主城_村庄", "村庄", "03"),
                create_dropdown_config("付帅主城_资源", "资源", "03"),
                create_dropdown_config("付帅主城_军工", "军工", "03"),
                create_dropdown_config("付帅主城_港口", "港口", "03"),
                create_dropdown_config("付帅主城_外塔", "外塔", "03"),
            ],
        },
        "付帅分城": {
            "card_type": "standard",
            "title": "付帅分城",
            "icon": "BUSINESS",
            "subtitle": "设置付帅分城建筑等级",
            "enabled": True,
            "controls_per_row": 6,
            "controls": [
                create_dropdown_config("付帅分城_城市", "城市", "15"),
                create_dropdown_config("付帅分城_兵工", "兵工", "10"),
                create_dropdown_config("付帅分城_陆军", "陆军", "10"),
                create_dropdown_config("付帅分城_空军", "空军", "03"),
                create_dropdown_config("付帅分城_商业", "商业", "04"),
                create_dropdown_config("付帅分城_补给", "补给", "03"),
                create_dropdown_config("付帅分城_内塔", "内塔", "03"),
                create_dropdown_config("付帅分城_村庄", "村庄", "03"),
                create_dropdown_config("付帅分城_资源", "资源", "03"),
                create_dropdown_config("付帅分城_军工", "军工", "03"),
                create_dropdown_config("付帅分城_港口", "港口", "03"),
                create_dropdown_config("付帅分城_外塔", "外塔", "03"),
            ],
        },
        "军团城市": {
            "card_type": "standard",
            "title": "军团城市",
            "icon": "FORT",
            "subtitle": "设置军团城市建筑等级",
            "enabled": True,
            "controls_per_row": 4,
            "controls": [
                create_dropdown_config("军团城市_城市", "城市", "05"),
                create_dropdown_config("军团城市_兵工", "兵工", "05"),
                create_dropdown_config("军团城市_军需", "军需", "05"),
                create_dropdown_config("军团城市_编号", "编号", "01"),
                create_dropdown_config("军团城市_陆军", "陆军", "00", LEVELS_0),
                create_dropdown_config("军团城市_空军", "空军", "00", LEVELS_0),
                create_dropdown_config("军团城市_炮塔", "炮塔", "00", LEVELS_0),
            ],
        },
    }


# 兼容旧代码的别名
建筑配置 = None

def _get_config_lazy():
    """延迟加载配置"""
    global 建筑配置
    if 建筑配置 is None:
        建筑配置 = get_building_config()
    return 建筑配置
