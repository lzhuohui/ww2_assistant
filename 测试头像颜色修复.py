#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试头像颜色修复
"""

import flet as ft
from 前端.用户设置界面.界面模块.用户界面 import UserInfoCard

def main(page: ft.Page):
    page.title = "测试头像颜色修复"
    page.padding = 20
    page.bgcolor = "#202020"
    
    # 创建用户信息卡片
    card = UserInfoCard.create(
        username="测试用户",
        is_registered=True,
        expire_days=30,
    )
    
    page.add(card)
    
    # 添加说明
    page.add(ft.Text("头像应该显示金色文字和深灰色背景", color="#FFFFFF"))

if __name__ == "__main__":
    ft.run(main)