# -*- coding: utf-8 -*-
"""
模块名称：卡片容器测试

设计思路及联动逻辑:
    测试卡片容器模块的功能和合规性，验证规则优化后的效果。
    1. 导入卡片容器模块
    2. 创建测试页面
    3. 测试卡片容器的基本功能
    4. 测试卡片容器的交互效果

模块隔离原则:
    1. 不直接创建被调用模块的内容
    2. 不覆盖被调用模块的计算结果
    3. 通过公开接口访问模块
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import flet as ft
from 前端.用户设置界面.单元模块.卡片容器 import 卡片容器

# *** 用户指定变量 - AI不得修改, 变量值必须生效 ***
# （用户未指定变量）
# *********************************


def main(page: ft.Page):
    """测试主函数"""
    # 设置页面属性
    page.title = "卡片容器测试"
    page.padding = 20
    page.bgcolor = "#f0f0f0"
    
    # 测试1: 基本卡片容器
    测试容器1 = 卡片容器.create(
        width=300,
        height=200,
        title="测试卡片 1",
        subtitle="这是一个测试卡片",
        icon="HOME"
    )
    
    # 测试2: 带点击事件的卡片容器
    def on_click():
        print("卡片被点击了！")
        测试容器2.content.controls[0].value = "已点击"
        page.update()
    
    测试容器2 = 卡片容器.create(
        width=300,
        height=200,
        title="测试卡片 2",
        subtitle="点击我试试",
        icon="STAR",
        on_click=on_click
    )
    
    # 测试3: 自定义样式的卡片容器
    测试容器3 = 卡片容器.create(
        width=300,
        height=200,
        title="测试卡片 3",
        subtitle="自定义样式",
        icon="SETTINGS",
        border_color="#4CAF50",
        shadow_color="#8BC34A"
    )
    
    # 测试4: 禁用状态的卡片容器
    测试容器4 = 卡片容器.create(
        width=300,
        height=200,
        title="测试卡片 4",
        subtitle="禁用状态",
        icon="BLOCK",
        enabled=False
    )
    
    # 测试5: 带自定义分隔线的卡片容器
    自定义分隔线 = ft.Container(
        width=280,
        height=2,
        bgcolor="#FF5722"
    )
    
    测试容器5 = 卡片容器.create(
        width=300,
        height=200,
        title="测试卡片 5",
        subtitle="自定义分隔线",
        icon="LINEAR_SCALE",
        divider=自定义分隔线
    )
    
    # 布局测试容器
    测试网格 = ft.GridView(
        controls=[
            测试容器1,
            测试容器2,
            测试容器3,
            测试容器4,
            测试容器5
        ],
        runs_count=2,
        spacing=20,
        run_spacing=20,
        max_extent=320
    )
    
    # 添加到页面
    page.add(
        ft.Text("卡片容器模块测试", size=24, weight="bold"),
        ft.Divider(height=20),
        测试网格
    )


# *** 调试逻辑 ***
if __name__ == "__main__":
    ft.run(main)