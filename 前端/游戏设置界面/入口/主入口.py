# -*- coding: utf-8 -*-
"""
模块名称：MainEntry
模块功能：应用入口，初始化界面
实现步骤：
- 初始化窗口配置
- 创建主界面
- 启动应用
"""

import flet as ft

from 前端.游戏设置界面.核心层.配置.界面配置 import UIConfig
from 前端.游戏设置界面.表示层.界面.游戏设置界面 import GameSettingsPage


USER_WINDOW_WIDTH = 1200
USER_WINDOW_HEIGHT = 540
USER_APP_TITLE = "游戏设置界面"
USER_SPACING = 10


def main(page: ft.Page):
    """应用入口函数"""
    config = UIConfig()
    theme_colors = config.当前主题颜色
    
    page.title = USER_APP_TITLE
    page.window.width = USER_WINDOW_WIDTH
    page.window.height = USER_WINDOW_HEIGHT
    page.window.resizable = False
    page.bgcolor = theme_colors.get("bg_primary")
    page.padding = USER_SPACING
    
    main_page = GameSettingsPage.create(config=config)
    page.add(main_page)


# *** 标准测试格式: 仅调用被测模块,AI不得添加数据 ***
if __name__ == "__main__":
    ft.app(target=main)
