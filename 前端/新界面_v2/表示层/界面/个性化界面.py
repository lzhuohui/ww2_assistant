# -*- coding: utf-8 -*-
"""
模块名称：个性化界面
设计思路: 个性化配置界面，使用主题色块组件
模块隔离: 界面层依赖组件层
"""

import flet as ft
from typing import Dict, Any, List, Callable

from 前端.新界面_v2.核心.配置.界面配置 import 界面配置
from 前端.新界面_v2.表示层.组件.复合.折叠卡片 import 折叠卡片
from 前端.新界面_v2.表示层.组件.基础.主题色块 import 主题色块
from 前端.新界面_v2.核心.常量.全局常量 import USER_SPACING, USER_CARD_SPACING


# *** 用户指定变量 - AI不得修改 ***
# （用户未指定变量）
# *********************************


class 个性化界面:
    """个性化配置界面"""
    
    @staticmethod
    def 创建(
        配置: 界面配置=None,
        保存回调: Callable[[str, str, str], None]=None,
    ) -> ft.Container:
        if 配置 is None:
            配置 = 界面配置()
        
        主题颜色 = 配置.当前主题颜色
        卡片列表: List[ft.Control] = []
        
        当前主题 = [配置.主题名称]
        
        主题颜色列表 = [
            {"名称": "浅色", "值": "#FFFFFF"},
            {"名称": "深色", "值": "#1A1A2E"},
            {"名称": "日出", "值": "#FFE4B5"},
            {"名称": "捕捉", "值": "#98FB98"},
            {"名称": "聚焦", "值": "#87CEEB"},
        ]
        
        def 处理主题切换(颜色值: str):
            for 项 in 主题颜色列表:
                if 项["值"] == 颜色值:
                    当前主题[0] = 项["名称"]
                    配置.切换主题(项["名称"])
                    if 保存回调:
                        保存回调("个性化", "theme", 项["名称"])
                    break
        
        选中主题颜色 = next((项["值"] for 项 in 主题颜色列表 if 项["名称"] == 当前主题[0]), "#1A1A2E")
        主题色块组 = 主题色块.创建组(
            颜色列表=主题颜色列表,
            选中颜色=选中主题颜色,
            选择回调=处理主题切换,
            配置=配置,
        )
        
        主题卡片 = 折叠卡片.创建(
            标题="主题设置",
            图标="PALETTE",
            只读模式=True,
            控件=[主题色块组],
            配置=配置,
        )
        卡片列表.append(主题卡片)
        
        标题栏 = ft.Row([
            ft.Icon(ft.Icons.PALETTE, size=20, color=主题颜色.get("accent")),
            ft.Container(width=6),
            ft.Text("个性化设置", size=16, weight=ft.FontWeight.BOLD, color=主题颜色.get("text_primary")),
        ], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER)
        
        卡片列 = ft.Column(
            controls=卡片列表,
            spacing=USER_CARD_SPACING,
            scroll=ft.ScrollMode.HIDDEN,
            expand=True,
        )
        
        内容列 = ft.Column(
            controls=[
                标题栏,
                ft.Container(height=USER_SPACING),
                卡片列,
            ],
            spacing=0,
            expand=True,
        )
        
        return ft.Container(
            content=内容列,
            expand=True,
        )


# *** 调试逻辑 ***
if __name__ == "__main__":
    ft.run(lambda page: page.add(个性化界面.创建()))
