# -*- coding: utf-8 -*-
"""
测试主界面布局对齐问题
"""

import flet as ft
from 前端.新界面_v2.入口.主界面 import MainInterface
from 前端.新界面_v2.核心.配置.界面配置 import UIConfig
from 前端.新界面_v2.核心.常量.全局常量 import USER_SPACING
from 前端.新界面_v2.表示层.界面.系统界面 import SystemPage
from 前端.新界面_v2.表示层.组件.复合.用户信息卡片 import UserInfoCard

def test_layout_alignment(page: ft.Page):
    """测试布局对齐"""
    config = UIConfig()
    
    # 设置窗口
    page.window.width = 1200
    page.window.height = 540
    page.window.resizable = False
    page.bgcolor = config.当前主题颜色.get("bg_primary")
    page.padding = 0
    
    # 创建主界面
    main_interface = MainInterface.create(config)
    page.add(main_interface)
    
    # 测试信息
    test_info = ft.Container(
        content=ft.Column([
            ft.Text("布局对齐测试", size=16, weight=ft.FontWeight.BOLD),
            ft.Text(f"USER_SPACING: {USER_SPACING}", size=14),
            ft.Text("右侧界面顶部应该距离窗口顶部10px", size=14),
            ft.Text("与左侧用户信息卡片顶部对齐", size=14),
        ]),
        padding=USER_SPACING,
        bgcolor="rgba(255,255,255,0.1)",
        border_radius=4,
    )
    
    print(f"主界面创建完成")
    print(f"USER_SPACING 值: {USER_SPACING}")
    print(f"窗口尺寸: {page.window.width}x{page.window.height}")
    print(f"布局对齐测试启动")

if __name__ == "__main__":
    ft.run(test_layout_alignment)