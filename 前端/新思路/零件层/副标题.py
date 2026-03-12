# -*- coding: utf-8 -*-
"""
副标题 - 零件层（新思路）

设计思路:
    兼容别名模块，调用标签文本模块。
    保持向后兼容性。

功能:
    1. 文字显示
    2. 自适应宽度
    3. 状态切换：透明度变化

数据来源:
    所有配置数据从配置目录获取。

使用场景:
    被组件层模块调用，也可独立使用。

可独立运行调试: python 副标题.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft
from typing import Callable, Optional
from 配置.界面配置 import 界面配置
from 新思路.零件层.标签文本 import LabelText


# *** 用户指定变量 - AI不得修改 ***
DEFAULT_SUBTITLE_SIZE = 12
# *********************************


class SubTitle:
    """副标题 - 兼容别名，调用标签文本模块"""
    
    def __init__(self, config):
        """初始化副标题（支持调试逻辑）"""
        self.config = config
    
    def render(self):
        """渲染副标题（支持调试逻辑）"""
        return SubTitle.create(
            config=self.config,
            text="这是副标题",
            enabled=True,
        )
    
    @staticmethod
    def create(
        config: 界面配置,
        text: str,
        enabled: bool = True,
        size: int = None,
        **kwargs
    ) -> ft.Text:
        """
        创建副标题
        
        参数:
            config: 界面配置对象
            text: 副标题文字
            enabled: 启用状态
            size: 字体大小（可选，默认12）
        
        返回:
            ft.Text: 副标题文本控件
        """
        return LabelText.create(
            config=config,
            text=text,
            role="secondary",
            size=size,
            enabled=enabled,
        )


# 兼容别名
副标题 = SubTitle


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    # 1. 界面配置初始化
    配置 = 界面配置()
    
    # 2. 自动加载用户数据覆盖默认值（在界面配置.__init__中自动完成）
    
    # 3. 正常启动被测模块
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        page.add(SubTitle(配置).render())  # 只能更改此处**被测调用模块名称**
    
    ft.run(main)
