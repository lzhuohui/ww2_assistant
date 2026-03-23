# -*- coding: utf-8 -*-
"""
模块名称：容器标题

设计思路及联动逻辑:
    最小模块化的标题容器组件，标题在容器中居中。
    1. 指定文字大小和边距
    2. 按默认尺寸创建容器，高度=文字大小+边距*2
    3. 容器透明，容器本身的边距=0
    4. 放入标签
    5. 计算容器宽度：文字大小*文字数量+边距*2
    6. 文字在容器中居中放置
    7. 返回的容器可直接设置left/top属性定位，无需重新包装

模块隔离原则:
    1. 不直接创建被调用模块的内容
    2. 不覆盖被调用模块的计算结果
    3. 用户指定变量除外
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft
from 前端.用户设置界面.单元模块.文本标签 import LabelText


# *** 用户指定变量 - AI不得修改, 变量值必须生效 ***
USER_TEXT_SIZE = 14  # 文字大小
USER_PADDING = 3  # 边距
# *********************************


class ContainerTitle:
    """容器标题 - 标题在容器中居中"""
    
    @staticmethod
    def create(
        title: str = "测试标题",
        text_size: int = USER_TEXT_SIZE,
        padding: int = USER_PADDING,
        enabled: bool = True,
        role: str = "h3",
        weight: ft.FontWeight = None,
    ) -> ft.Container:
        title_text = LabelText.create(
            text=title,
            role=role,
            size=text_size,
            weight=weight,
            enabled=enabled,
            win11_style=True
        )
        
        container_height = text_size + padding * 2
        
        char_count = len(title)
        container_width = text_size * char_count + padding * 2
        
        return ft.Container(
            content=title_text,
            width=container_width,
            height=container_height,
            padding=0,
            alignment=ft.Alignment(0.5, 0.5),
        )


# *** 调试逻辑 ***
if __name__ == "__main__":
    ft.run(lambda page: page.add(ContainerTitle.create()))
