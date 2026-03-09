#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows 11风格界面 - 主入口

创建日期: 2026-03-08
作者: AI
版本: v2.0.0

说明：基于Windows 11设计风格的Flet界面实现 - 工厂装配式设计
"""

import sys
from pathlib import Path

# 添加正确的路径
当前目录 = Path(__file__).parent
sys.path.insert(0, str(当前目录))
sys.path.insert(0, str(当前目录 / "windows11_v2"))

import flet as ft
from 主界面 import 主界面


def main(page: ft.Page):
    """主函数"""
    # 设置页面
    page.title = "二战风云 - Windows 11风格"
    page.window.width = 1200
    page.window.height = 540
    page.padding = 0
    page.bgcolor = "#1C1C1C"
    
    # 清空页面
    page.clean()
    
    # 创建主界面
    界面 = 主界面(page)
    page.add(界面.render())


if __name__ == "__main__":
    print("正在启动Windows 11风格界面...")
    print("基于工厂装配式设计理念")
    print("零件→组件→部件→设备→系统")
    print("请稍候，界面即将出现...")
    ft.run(main)
