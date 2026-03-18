# -*- coding: utf-8 -*-
"""
模块名称：文本标签 | 层级：零件层
设计思路：
    提供文本显示功能，支持不同角色和样式。
    纯UI控件，无业务逻辑。
    通过ThemeProvider获取主题，无需传入config。
功能列表：
    1. 显示文本
    2. 支持不同角色（primary/secondary/help）
    3. 支持不同尺寸
对外接口：
    - create(): 创建文本标签
"""

import flet as ft
from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider
from 前端.配置.界面配置 import 界面配置

# *** 用户指定变量 - AI不得修改 ***
# *********************************


class LabelText:
    """文本标签 - 纯UI控件"""
    
    @staticmethod
    def create(
        text: str = "文本标签示例",
        role: str = "primary",
        size: int = 14,
        enabled: bool = True,
        **kwargs
    ) -> ft.Text:
        """
        创建文本标签
        
        参数:
            text: 文本内容（默认为示例文本）
            role: 文本角色（primary/secondary/help）
            size: 文本尺寸（默认14）
            enabled: 启用状态
            **kwargs: 其他Text参数
        
        返回:
            ft.Text: 文本控件
        """
        # 根据角色获取颜色
        if role == "primary":
            color = ThemeProvider.get_color("text_primary")
        elif role == "secondary":
            color = ThemeProvider.get_color("text_secondary")
        else:  # help
            color = ThemeProvider.get_color("text_hint")
        
        # Win11风格文本标签
        # 根据角色设置字重
        if role == "primary":
            weight = ft.FontWeight.W_500  # 主文本使用中等字重
        else:
            weight = ft.FontWeight.NORMAL  # 其他文本使用普通字重
        
        return ft.Text(
            value=text,
            color=color,
            size=size,
            opacity=1.0 if enabled else 0.4,
            font_family="Segoe UI",  # Win11默认字体
            weight=weight,  # 根据角色设置字重
            **kwargs
        )


# *** 调试逻辑 ***
if __name__ == "__main__":
    配置 = 界面配置()
    ThemeProvider.initialize(配置)
    def main(page: ft.Page):
        page.add(LabelText.create())
    ft.run(main)
