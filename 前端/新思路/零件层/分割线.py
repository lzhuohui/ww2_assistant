# -*- coding: utf-8 -*-
"""
分割线 - 零件层（新思路）

设计思路:
    最小模块化的垂直分割线组件，用于分隔左右区域。
    分割线在容器中居中。

功能:
    1. 垂直线：在容器中居中
    2. 状态切换：启用/禁用透明度变化

数据来源:
    所有配置数据从配置目录获取。

使用场景:
    被组件层模块调用。

可独立运行调试: python 分割线.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft
from typing import Optional
from 配置.界面配置 import 界面配置


# *** 用户指定变量 - AI不得修改 ***
# 容器尺寸
CONTAINER_WIDTH = 10
CONTAINER_HEIGHT = 100
# 线型宽度
LINE_WIDTH = 2
# *********************************


class Divider:
    """分割线 - 垂直分割线，在容器中居中"""
    
    def __init__(self, config):
        """初始化分割线（支持调试逻辑）"""
        self.config = config
    
    def render(self):
        """渲染分割线（支持调试逻辑）"""
        return Divider.create(
            config=self.config,
            height=CONTAINER_HEIGHT,
            enabled=True,
        )
    
    @staticmethod
    def create(
        config: 界面配置,
        height: int = None,
        enabled: bool = True,
        **kwargs
    ) -> ft.Container:
        """
        创建分割线
        
        参数:
            config: 界面配置对象
            height: 容器高度（可选，默认60）
            enabled: 启用状态
        
        返回:
            ft.Container: 包含分割线的容器
        """
        theme_colors = config.当前主题颜色
        
        container_width = CONTAINER_WIDTH
        container_height = height if height is not None else CONTAINER_HEIGHT
        line_width = LINE_WIDTH
        
        # 分割线（垂直居中）
        line = ft.Container(
            width=line_width,
            height=container_height,
            bgcolor=theme_colors.get("accent"),
            opacity=0.7 if enabled else 0.2,
        )
        
        # 容器（分割线居中）
        return ft.Container(
            width=container_width,
            height=container_height,
            content=line,
            alignment=ft.Alignment(0, 0),  # 分割线居中
        )


# 兼容别名
分割线 = Divider


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    # 1. 界面配置初始化
    配置 = 界面配置()
    
    # 2. 自动加载用户数据覆盖默认值（在界面配置.__init__中自动完成）
    
    # 3. 正常启动被测模块
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        page.add(Divider(配置).render())  # 只能更改此处**被测调用模块名称**
    
    ft.run(main)
