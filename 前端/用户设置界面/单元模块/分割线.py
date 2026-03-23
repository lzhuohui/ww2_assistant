# -*- coding: utf-8 -*-
"""
模块名称：分割线
设计思路：
    最小模块化的垂直分割线组件，用于分隔左右区域。
    分割线在容器中居中。
    返回的容器可直接设置left/top属性定位，无需重新包装。
模块隔离原则：
    1. 不直接创建被调用模块的内容
    2. 不覆盖被调用模块的计算结果
    3. 用户指定变量除外
"""

import flet as ft
from 前端.用户设置界面.配置.界面配置 import 界面配置


# *** 用户指定变量 - AI不得修改, 变量值必须生效 ***
USER_CONTAINER_WIDTH = 20  # 分割线容器宽度
USER_CONTAINER_HEIGHT = 100  # 分割线容器高度
USER_LINE_WIDTH = 5  # 分割线线宽
# *********************************


class Divider:
    """分割线 - 垂直分割线，在容器中居中"""
    
    @staticmethod
    def create(
        config: 界面配置 = None,
        width: int = USER_CONTAINER_WIDTH,
        height: int = USER_CONTAINER_HEIGHT,
        line_width: int = USER_LINE_WIDTH,
        enabled: bool = True
    ) -> ft.Container:
        if config is None:
            config = 界面配置()
        
        theme_colors = config.当前主题颜色
        
        container_width = width
        container_height = height
        final_line_width = line_width
        
        line = ft.Container(
            width=final_line_width,
            height=container_height,
            bgcolor=theme_colors.get("accent"),
            opacity=0.7 if enabled else 0.2,
        )
        
        return ft.Container(
            width=container_width,
            height=container_height,
            content=line,
            alignment=ft.Alignment(0, 0),
        )


# *** 调试逻辑 ***
if __name__ == "__main__":
    ft.run(lambda page: page.add(Divider.create()))
