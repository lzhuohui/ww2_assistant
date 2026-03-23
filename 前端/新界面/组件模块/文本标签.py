# -*- coding: utf-8 -*-
"""模块名称：文本标签 | 设计思路：提供文本显示功能，支持不同角色和样式 | 模块隔离原则"""

from typing import Optional
import flet as ft

from 前端.新界面.核心接口.主题提供者 import ThemeProvider
from 前端.新界面.核心接口.界面配置 import 界面配置


# *** 用户指定变量 - AI不得修改, 变量值必须生效 ***
USER_SIZE = 14
# *********************************


class LabelText:
    """文本标签 - 纯UI控件"""
    
    @staticmethod
    def create(
        text: str="文本标签示例",
        role: str="body",
        size: Optional[int]=None,
        weight: Optional[ft.FontWeight]=None,
        enabled: bool=True,
        win11_style: bool=True,
        max_lines: Optional[int]=None,
        **kwargs
    ) -> ft.Text:
        配置 = 界面配置()
        ThemeProvider.initialize(配置)
        
        if win11_style:
            style = ThemeProvider.get_win11_text_style(role, size, weight)
        else:
            style = ThemeProvider.get_default_text_style()
            if size:
                style["size"] = size
            if weight:
                style["weight"] = weight
        
        return ft.Text(
            value=text,
            size=style["size"],
            weight=style["weight"],
            color=style["color"],
            font_family=style["font_family"],
            opacity=1.0 if enabled else 0.4,
            max_lines=max_lines,
            **kwargs
        )


if __name__ == "__main__":
    ft.run(lambda page: page.add(LabelText.create()))
