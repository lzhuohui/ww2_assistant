# -*- coding: utf-8 -*-
"""
模块名称：导航按钮
设计思路: 可点击的导航按钮，支持选中状态，Win11风格背景块
模块隔离: 复合组件，依赖基础组件
"""

import flet as ft
from typing import Dict, Any, Callable

from 前端.新界面_v2.核心.配置.界面配置 import 界面配置
from 前端.新界面_v2.表示层.组件.基础.卡片容器 import 卡片容器


# *** 用户指定变量 - AI不得修改 ***
# （用户未指定变量）
# *********************************


class 导航按钮:
    """导航按钮 - 可点击的导航按钮，支持选中状态，Win11风格背景块"""
    
    @staticmethod
    def 创建(
        配置: 界面配置=None,
        项: Dict[str, Any]=None,
        索引: int=0,
        当前选中: list=None,
        处理导航点击: Callable=None,
        选中状态: bool=False,
        自适应高度: bool=False,
    ) -> ft.Container:
        if 配置 is None:
            配置 = 界面配置()
        
        if 项 is None:
            项 = {"id": "未命名", "icon": "INFO"}
        
        if 当前选中 is None:
            当前选中 = [0]
        
        主题颜色 = 配置.当前主题颜色
        图标名称 = 项.get("icon", "INFO")
        
        选中颜色 = 主题颜色.get("text_primary")
        未选中颜色 = 主题颜色.get("text_secondary")
        选中背景色 = 主题颜色.get("accent")
        悬停背景色 = 主题颜色.get("bg_card")
        
        图标控件 = ft.Icon(
            getattr(ft.Icons, 图标名称, ft.Icons.INFO),
            size=18,
            color=选中颜色 if 选中状态 else 未选中颜色,
        )
        
        文本控件 = ft.Text(
            项["id"],
            size=13,
            color=选中颜色 if 选中状态 else 未选中颜色,
        )
        
        按钮内容 = ft.Row([
            图标控件,
            ft.Container(width=8),
            文本控件,
        ], spacing=0, vertical_alignment=ft.CrossAxisAlignment.CENTER)
        
        背景块 = ft.Container(
            bgcolor=选中背景色 if 选中状态 else "transparent",
            border_radius=6,
            animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
            width=float("inf") if 选中状态 else 0,
            height=float("inf"),
        )
        
        内容容器 = ft.Container(
            content=按钮内容,
            padding=ft.Padding(left=12, right=12, top=8, bottom=8),
            alignment=ft.Alignment(-1, 0),
        )
        
        堆栈 = ft.Stack([
            背景块,
            内容容器,
        ], alignment=ft.Alignment(-1, 0))
        
        按钮 = ft.Container(
            content=堆栈,
            bgcolor=主题颜色.get("bg_secondary"),
            border_radius=6,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
        )
        
        if 自适应高度:
            按钮.expand = True
        
        选中状态存储 = [选中状态]
        
        def 更新选中(选中: bool):
            选中状态存储[0] = 选中
            if 选中:
                背景块.bgcolor = 选中背景色
                背景块.width = float("inf")
                图标控件.color = 选中颜色
                文本控件.color = 选中颜色
            else:
                背景块.bgcolor = "transparent"
                背景块.width = 0
                图标控件.color = 未选中颜色
                文本控件.color = 未选中颜色
            try:
                if 按钮.page:
                    按钮.update()
            except:
                pass
        
        def 处理悬停(e):
            if not 选中状态存储[0]:
                if e.data == "true":
                    背景块.bgcolor = 悬停背景色
                    背景块.width = float("inf")
                else:
                    背景块.bgcolor = "transparent"
                    背景块.width = 0
                try:
                    if 按钮.page:
                        按钮.update()
                except:
                    pass
        
        按钮.on_hover = 处理悬停
        
        if 处理导航点击:
            按钮.on_click = lambda e, idx=索引: 处理导航点击(idx)
        
        按钮.更新选中 = 更新选中
        
        return 按钮
    
    @staticmethod
    def 更新选中状态(按钮: ft.Container, 选中: bool, 配置: 界面配置=None) -> None:
        """更新按钮的选中状态"""
        if hasattr(按钮, '更新选中'):
            按钮.更新选中(选中)


# *** 调试逻辑 ***
if __name__ == "__main__":
    ft.run(lambda page: page.add(导航按钮.创建()))
