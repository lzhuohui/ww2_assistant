# -*- coding: utf-8 -*-
"""
模块名称：主题色块
设计思路: 纯UI控件，用于主题颜色选择
模块隔离: 基础组件，不依赖其他业务组件
"""

import flet as ft
from typing import Callable, List, Dict

from 前端.新界面_v2.核心.配置.界面配置 import 界面配置


# *** 用户指定变量 - AI不得修改 ***
USER_SIZE = 40
# *********************************


class 主题色块:
    """主题色块组件"""
    
    @staticmethod
    def 创建(
        颜色值: str="#FF5722",
        颜色名称: str="",
        选中: bool=False,
        点击回调: Callable[[str], None]=None,
        大小: int=USER_SIZE,
        配置: 界面配置=None,
    ) -> ft.Container:
        if 配置 is None:
            配置 = 界面配置()
        
        主题颜色 = 配置.当前主题颜色
        边框颜色 = 主题颜色.get("accent") if 选中 else "transparent"
        边框宽度 = 3 if 选中 else 0
        
        def 处理点击(e):
            if 点击回调:
                点击回调(颜色值)
        
        return ft.Container(
            width=大小,
            height=大小,
            bgcolor=颜色值,
            border=ft.Border.all(边框宽度, 边框颜色),
            border_radius=ft.BorderRadius.all(大小 // 3),
            on_click=处理点击,
            tooltip=颜色名称 if 颜色名称 else 颜色值,
            ink=True,
        )
    
    @staticmethod
    def 创建组(
        颜色列表: List[Dict]=None,
        选中颜色: str="",
        选择回调: Callable[[str], None]=None,
        大小: int=USER_SIZE,
        间距: int=10,
        配置: 界面配置=None,
    ) -> ft.Row:
        if 颜色列表 is None:
            颜色列表 = [
                {"名称": "红色", "值": "#FF5722"},
                {"名称": "蓝色", "值": "#2196F3"},
                {"名称": "绿色", "值": "#4CAF50"},
            ]
        
        if 配置 is None:
            配置 = 界面配置()
        
        色块列表 = []
        
        for 颜色项 in 颜色列表:
            颜色值 = 颜色项.get("值", "#000000")
            颜色名称 = 颜色项.get("名称", "")
            
            色块 = 主题色块.创建(
                颜色值=颜色值,
                颜色名称=颜色名称,
                选中=(颜色值 == 选中颜色),
                点击回调=选择回调,
                大小=大小,
                配置=配置,
            )
            色块列表.append(色块)
        
        return ft.Row(
            controls=色块列表,
            spacing=间距,
            wrap=True,
        )


# *** 调试逻辑 ***
if __name__ == "__main__":
    ft.run(lambda page: page.add(主题色块.创建组()))
