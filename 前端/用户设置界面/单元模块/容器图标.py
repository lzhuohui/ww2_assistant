# -*- coding: utf-8 -*-
"""
容器图标

设计思路及联动逻辑:
    最小模块化的图标容器组件，图标在容器中居中。
    1. 图标容器中，指定图标大小和边距
    2. 容器透明，容器本身的边距=0
    3. 容器的大小=图标大小+边距*2
    4. 图标在容器中居中放置

模块隔离原则:
    1. 不直接创建被调用模块的内容
    2. 不覆盖被调用模块的计算结果
    3. 用户指定变量除外
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft


# *** 用户指定变量 - AI不得修改, 变量值必须生效 ***
USER_ICON_SIZE = 20  # 图标大小
USER_PADDING = 3  # 边距
# *********************************

# 默认值常量 - 供调用者获取
DEFAULT_ICON = "HOME"
DEFAULT_ICON_SIZE = USER_ICON_SIZE
DEFAULT_PADDING = USER_PADDING


class ContainerIcon:
    """容器图标 - 图标在容器中居中"""
    
    @staticmethod
    def create(
        icon: ft.Icon = None,
        icon_size: int = USER_ICON_SIZE,
        padding: int = USER_PADDING,
        enabled: bool = True,
    ) -> ft.Container:
        if icon is None:
            icon = ft.Icon(ft.Icons.HOME, size=icon_size)
        
        if hasattr(icon, 'opacity'):
            icon.opacity = 1.0 if enabled else 0.4
        
        container_size = icon_size + padding * 2
        
        return ft.Container(
            content=icon,
            width=container_size,
            height=container_size,
            padding=0,
            alignment=ft.Alignment(0.5, 0.5),
        )


# *** 调试逻辑 ***
if __name__ == "__main__":
    ft.run(lambda page: page.add(ContainerIcon.create()))
