# -*- coding: utf-8 -*-
"""
模块名称：文本标签
设计思路: 提供文本显示功能，支持不同角色和样式
模块隔离: 纯UI组件，不包含业务逻辑
"""

from typing import Optional
import flet as ft

from 前端.新界面_v2.核心.配置.界面配置 import 界面配置


# *** 用户指定变量 - AI不得修改 ***
USER_DEFAULT_SIZE = 14
# *********************************


class 文本标签:
    """文本标签 - 纯UI控件"""
    
    @staticmethod
    def 创建(
        文本: str="文本标签示例",
        尺寸: int=USER_DEFAULT_SIZE,
        粗体: bool=False,
        颜色: str=None,
        配置: 界面配置=None,
    ) -> ft.Text:
        if 配置 is None:
            配置 = 界面配置()
        
        实际颜色 = 颜色 or 配置.获取颜色("text_primary")
        
        return ft.Text(
            value=文本,
            size=尺寸,
            weight=ft.FontWeight.BOLD if 粗体 else ft.FontWeight.NORMAL,
            color=实际颜色,
        )


# *** 调试逻辑 ***
if __name__ == "__main__":
    ft.run(lambda page: page.add(文本标签.创建()))
