# -*- coding: utf-8 -*-
"""
模块名称：分割线 | 层级：单元层
设计思路：
    最小模块化的垂直分割线组件，用于分隔左右区域。
    分割线在容器中居中。
模块隔离原则：
    1. 不直接创建被调用模块的内容
    2. 不覆盖被调用模块的计算结果
    3. 用户指定变量除外
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft
from 前端.用户设置界面.配置.界面配置 import 界面配置


# *** 用户指定变量 - AI不得修改, 变量值必须生效 ***
USER_CONTAINER_WIDTH = 10
USER_CONTAINER_HEIGHT = 100
USER_LINE_WIDTH = 5
# *********************************


class Divider:
    """分割线 - 垂直分割线，在容器中居中"""
    
    @staticmethod
    def create(
        config: 界面配置 = None,
        height: int = None,
        enabled: bool = True,
        **kwargs
    ) -> ft.Container:
        if config is None:
            config = 界面配置()
        
        theme_colors = config.当前主题颜色
        
        container_width = USER_CONTAINER_WIDTH
        container_height = height if height is not None else USER_CONTAINER_HEIGHT
        line_width = USER_LINE_WIDTH
        
        line = ft.Container(
            width=line_width,
            height=container_height,
            bgcolor=theme_colors.get("accent"),
            opacity=0.7 if enabled else 0.2,
        )
        
        return ft.Container(
            width=container_width + line_width * 4,
            height=container_height,
            content=line,
            alignment=ft.Alignment(0, 0),
        )


# *** 调试逻辑 ***
if __name__ == "__main__":
    ft.run(lambda page: page.add(Divider.create()))
