# -*- coding: utf-8 -*-
"""
标签文本 - 零件层（新思路）

设计思路:
    通用标签文本模块，通过参数配置可复用为主标题/副标题/帮助文字等。
    自适应宽度，支持状态切换。

功能:
    1. 文字显示
    2. 自适应宽度
    3. 角色预设：primary(主标题)/secondary(副标题)/help(帮助文字)
    4. 状态切换：透明度变化

数据来源:
    所有配置数据从配置目录获取。

使用场景:
    被其他零件模块调用，也可独立使用。

可独立运行调试: python 标签文本.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import flet as ft
from typing import Callable, Optional
from 配置.界面配置 import 界面配置


# *** 用户指定变量 - AI不得修改 ***
# 默认尺寸
DEFAULT_PRIMARY_SIZE = 14
DEFAULT_SECONDARY_SIZE = 12
DEFAULT_HELP_SIZE = 11
# *********************************


class LabelText:
    """标签文本 - 通用文本标签模块"""
    
    def __init__(self, config):
        """初始化标签文本（支持调试逻辑）"""
        self.config = config
    
    def render(self):
        """渲染标签文本（支持调试逻辑）"""
        return LabelText.create(
            config=self.config,
            text="测试标签",
            role="primary",
            enabled=True,
        )
    
    @staticmethod
    def create(
        config: 界面配置,
        text: str,
        role: str = "primary",
        size: int = None,
        color: str = None,
        weight: ft.FontWeight = None,
        enabled: bool = True,
        **kwargs
    ) -> ft.Text:
        """
        创建标签文本
        
        参数:
            config: 界面配置对象
            text: 文本内容
            role: 角色预设 - "primary"(主标题)/"secondary"(副标题)/"help"(帮助文字)
            size: 字体大小（可选，默认根据角色预设）
            color: 文字颜色（可选，默认根据角色预设）
            weight: 字重（可选，默认根据角色预设）
            enabled: 启用状态
        
        返回:
            ft.Text: 文本控件，具备状态切换能力
        """
        theme_colors = config.当前主题颜色
        weight_config = config.定义尺寸.get("字重", {})
        
        # 根据角色预设默认值
        if role == "primary":
            default_size = DEFAULT_PRIMARY_SIZE
            default_color = theme_colors.get("text_primary")
            default_weight = weight_config.get("font_weight_medium", ft.FontWeight.W_500)
        elif role == "secondary":
            default_size = DEFAULT_SECONDARY_SIZE
            default_color = theme_colors.get("text_secondary", "#888888")
            default_weight = None
        elif role == "help":
            default_size = DEFAULT_HELP_SIZE
            default_color = theme_colors.get("text_secondary", "#888888")
            default_weight = None
        else:
            default_size = DEFAULT_PRIMARY_SIZE
            default_color = theme_colors.get("text_primary")
            default_weight = None
        
        # 使用传入值或默认值
        text_size = size if size is not None else default_size
        text_color = color if color is not None else default_color
        text_weight = weight if weight is not None else default_weight
        
        label = ft.Text(
            text,
            size=text_size,
            color=text_color,
            weight=text_weight,
            opacity=1.0 if enabled else 0.4,
        )
        
        # 暴露控制接口
        def set_state(new_enabled: bool):
            label.opacity = 1.0 if new_enabled else 0.4
            label.update()
        
        label.set_state = set_state
        label.get_state = lambda: enabled
        
        return label


# 兼容别名
标签文本 = LabelText


# ==================== 调试逻辑 ====================
if __name__ == "__main__":
    # 1. 界面配置初始化
    配置 = 界面配置()
    
    # 2. 自动加载用户数据覆盖默认值（在界面配置.__init__中自动完成）
    
    # 3. 正常启动被测模块
    def main(page: ft.Page):
        page.padding = 0
        page.bgcolor = 配置.当前主题颜色["bg_primary"]
        page.add(LabelText(配置).render())  # 只能更改此处**被测调用模块名称**
    
    ft.run(main)
