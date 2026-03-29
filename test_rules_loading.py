# -*- coding: utf-8 -*-
"""
模块名称：规则加载测试

设计思路及联动逻辑:
    测试规则加载和执行情况。
    1. 验证核心规范自动加载
    2. 验证详细规范智能匹配
    3. 验证手动触发机制

模块隔离原则:
    1. 不直接创建被调用模块的内容
    2. 不覆盖被调用模块的计算结果
    3. 用户指定变量除外
"""

import flet as ft
from typing import Callable, Optional
from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider
from 前端.用户设置界面.配置.界面配置 import 界面配置


# *** 用户指定变量 - AI不得修改, 变量值必须生效 ***
USER_TEST_SIZE = 16  # 用户指定测试尺寸
USER_TEST_COLOR = "#FF0000"  # 用户指定测试颜色
# *********************************


class TestComponent:
    """测试组件 - 用于验证规则加载和执行"""
    
    @staticmethod
    def create(
        title: str = "测试标题",
        size: int = USER_TEST_SIZE,
        color: str = USER_TEST_COLOR,
        enabled: bool = True
    ) -> ft.Container:
        """
        创建测试组件
        
        参数:
            title: 组件标题
            size: 组件尺寸
            color: 组件颜色
            enabled: 是否启用
            
        返回:
            ft.Container: 包含测试组件的容器
        """
        配置 = 界面配置()
        ThemeProvider.initialize(配置)
        
        container = ft.Container(
            content=ft.Text(title),
            width=size,
            height=size,
            bgcolor=color,
            disabled=not enabled
        )
        
        return container


# *** 调试逻辑 ***
if __name__ == "__main__":
    ft.run(lambda page: page.add(TestComponent.create()))
