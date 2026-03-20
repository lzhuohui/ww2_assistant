# -*- coding: utf-8 -*-
"""
模块名称：文本标签
设计思路及联动逻辑:
    提供文本显示功能，支持不同角色和样式。
    1. 通过ThemeProvider获取主题，无需传入config
    2. 支持Win11风格和样式合并机制
模块隔离原则:
    1. 不直接创建被调用模块的内容
    2. 不覆盖被调用模块的计算结果
    3. 用户指定变量除外
"""

from typing import Optional

import flet as ft

from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider
from 前端.用户设置界面.配置.界面配置 import 界面配置


# *** 用户指定变量 - AI不得修改, 变量值必须生效 ***
USER_SIZE = 14  # 默认字体大小
# *********************************

# 默认值常量 - 供调用者获取
DEFAULT_TEXT = "文本标签示例"
DEFAULT_ROLE = "body"
DEFAULT_SIZE = USER_SIZE


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


# *** 调试逻辑 ***
if __name__ == "__main__":
    ft.run(lambda page: page.add(LabelText.create()))
