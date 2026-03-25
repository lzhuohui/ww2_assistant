# -*- coding: utf-8 -*-
"""
模块名称：TextLabel
设计思路: 提供文本显示功能，支持不同角色和样式
模块隔离: 纯UI组件，不包含业务逻辑
"""

from typing import Optional
import flet as ft

from 前端.新界面_v2.核心.配置.界面配置 import UIConfig


# *** 用户指定变量 - AI不得修改, 变量值必须生效 ***
USER_DEFAULT_SIZE = 14  # 默认文本大小
# *********************************


class TextLabel:
    """文本标签 - 纯UI控件"""
    
    @staticmethod
    def create(
        text: str="文本标签示例",
        size: int=USER_DEFAULT_SIZE,
        bold: bool=False,
        color: str=None,
        config: UIConfig=None,
    ) -> ft.Text:
        if config is None:
            config = UIConfig()
        
        actual_color = color or config.get_color("text_primary")
        
        return ft.Text(
            value=text,
            size=size,
            weight=ft.FontWeight.BOLD if bold else ft.FontWeight.NORMAL,
            color=actual_color,
        )


# *** 调试逻辑 ***
if __name__ == "__main__":
    ft.run(lambda page: page.add(TextLabel.create()))
