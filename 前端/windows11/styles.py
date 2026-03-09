#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows 11风格 - 样式定义

创建日期: 2026-03-08
作者: AI
版本: v1.0.0

说明：Windows 11设计风格的颜色和样式定义，支持主题切换
"""

import json
import os


class Theme:
    """主题类"""
    def __init__(self, name, colors):
        self.name = name
        self.colors = colors


# 预设主题
THEMES = {
    "dark": Theme(
        "深色",
        {
            "bg_primary": "#1C1C1C",      # 深色背景
            "bg_secondary": "#2D2D2D",    # 卡片背景
            "text_primary": "#F2F2F2",    # 主要文字
            "text_secondary": "#CCCCCC",  # 次要文字
            "accent": "#0078D4",         # 蓝色强调
            "accent_light": "#1E3A5F",    # 深色强调
            "border": "#404040",         # 边框颜色
            "success": "#10B981",         # 成功色
            "warning": "#F59E0B",         # 警告色
            "error": "#EF4444",           # 错误色
        }
    ),
    "light": Theme(
        "浅色",
        {
            "bg_primary": "#F3F4F6",      # 浅灰色背景
            "bg_secondary": "#FFFFFF",    # 白色卡片
            "text_primary": "#1F2937",    # 主要文字
            "text_secondary": "#6B7280",  # 次要文字
            "accent": "#0078D4",         # 蓝色强调
            "accent_light": "#E1EBF7",    # 浅色强调
            "border": "#E5E7EB",         # 边框颜色
            "success": "#10B981",         # 成功色
            "warning": "#F59E0B",         # 警告色
            "error": "#EF4444",           # 错误色
        }
    )
}

# 当前主题
current_theme = THEMES["dark"]

# 主题变更回调
_theme_callbacks = []


def get_color(color_name):
    """获取当前主题的颜色"""
    return current_theme.colors.get(color_name, "#FFFFFF")


def get_theme_name():
    """获取当前主题名称"""
    for name, theme in THEMES.items():
        if theme == current_theme:
            return name
    return "dark"


def set_theme(theme_name):
    """设置主题"""
    global current_theme, WINDOWS_11_COLORS
    if theme_name in THEMES:
        current_theme = THEMES[theme_name]
        # 更新向后兼容变量
        WINDOWS_11_COLORS = current_theme.colors
        # 保存用户偏好
        save_theme_preference(theme_name)
        # 通知所有回调
        for callback in _theme_callbacks:
            try:
                callback()
            except Exception as e:
                print(f"主题回调错误: {e}")
        return True
    return False


def register_theme_callback(callback):
    """注册主题变更回调"""
    if callback not in _theme_callbacks:
        _theme_callbacks.append(callback)


def unregister_theme_callback(callback):
    """注销主题变更回调"""
    if callback in _theme_callbacks:
        _theme_callbacks.remove(callback)

# 字体大小
FONT_SIZES = {
    "title": 24,
    "subtitle": 18,
    "body": 14,
    "caption": 12,
}

# 间距
SPACING = {
    "xs": 4,
    "sm": 8,
    "md": 16,
    "lg": 20,
    "xl": 24,
}

# 圆角
BORDER_RADIUS = {
    "sm": 4,
    "md": 8,
    "lg": 10,
}

# 阴影
BOX_SHADOWS = {
    "sm": {
        "spread_radius": 0,
        "blur_radius": 3,
        "color": "#00000005",
        "offset": (0, 1)
    },
    "md": {
        "spread_radius": 0,
        "blur_radius": 5,
        "color": "#00000008",
        "offset": (0, 2)
    },
    "lg": {
        "spread_radius": 0,
        "blur_radius": 10,
        "color": "#00000010",
        "offset": (0, 4)
    },
}


def get_config_dir():
    """获取配置目录"""
    config_dir = os.path.join(os.path.dirname(__file__), "..", "config")
    os.makedirs(config_dir, exist_ok=True)
    return config_dir


def save_theme_preference(theme_name):
    """保存主题偏好"""
    config = {"theme": theme_name}
    config_file = os.path.join(get_config_dir(), "user_config.json")
    try:
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"保存主题偏好失败: {e}")
        return False


def load_theme_preference():
    """加载主题偏好"""
    config_file = os.path.join(get_config_dir(), "user_config.json")
    try:
        if os.path.exists(config_file):
            with open(config_file, "r", encoding="utf-8") as f:
                config = json.load(f)
                theme_name = config.get("theme", "dark")
                if theme_name in THEMES:
                    set_theme(theme_name)
    except Exception as e:
        print(f"加载主题偏好失败: {e}")


# 加载用户主题偏好
load_theme_preference()

# 向后兼容：为旧代码提供WINDOWS_11_COLORS变量
WINDOWS_11_COLORS = current_theme.colors