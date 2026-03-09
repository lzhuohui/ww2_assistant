#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主题系统测试脚本

创建日期: 2026-03-08
作者: AI
版本: v1.0.0

说明：测试主题系统的功能
"""

import sys
sys.path.append('.')

from windows11.styles import get_color, get_theme_name, set_theme, THEMES

print("=== 主题系统测试 ===")
print(f"当前主题: {get_theme_name()}")
print(f"当前主题颜色:")
print(f"  bg_primary: {get_color('bg_primary')}")
print(f"  bg_secondary: {get_color('bg_secondary')}")
print(f"  text_primary: {get_color('text_primary')}")
print(f"  text_secondary: {get_color('text_secondary')}")
print(f"  accent: {get_color('accent')}")

print("\n切换到浅色主题...")
set_theme('light')
print(f"当前主题: {get_theme_name()}")
print(f"当前主题颜色:")
print(f"  bg_primary: {get_color('bg_primary')}")
print(f"  bg_secondary: {get_color('bg_secondary')}")
print(f"  text_primary: {get_color('text_primary')}")
print(f"  text_secondary: {get_color('text_secondary')}")
print(f"  accent: {get_color('accent')}")

print("\n切换到深色主题...")
set_theme('dark')
print(f"当前主题: {get_theme_name()}")
print(f"当前主题颜色:")
print(f"  bg_primary: {get_color('bg_primary')}")
print(f"  bg_secondary: {get_color('bg_secondary')}")
print(f"  text_primary: {get_color('text_primary')}")
print(f"  text_secondary: {get_color('text_secondary')}")
print(f"  accent: {get_color('accent')}")

print("\n=== 测试完成 ===")
