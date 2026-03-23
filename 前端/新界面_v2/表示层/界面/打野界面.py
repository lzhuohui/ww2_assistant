# -*- coding: utf-8 -*-
"""
模块名称：打野界面
设计思路: 打野配置界面，使用折叠卡片模式
模块隔离: 界面层依赖组件层和业务层
"""

import flet as ft
from typing import Dict, Any, List, Callable

from 前端.新界面_v2.核心.配置.界面配置 import 界面配置
from 前端.新界面_v2.表示层.组件.复合.折叠卡片 import 折叠卡片
from 前端.新界面_v2.核心.常量.全局常量 import USER_SPACING, USER_CARD_SPACING


# *** 用户指定变量 - AI不得修改 ***
# （用户未指定变量）
# *********************************


class 打野界面:
    """打野配置界面"""
    
    @staticmethod
    def 创建(
        配置: 界面配置=None,
        保存回调: Callable[[str, str, str], None]=None,
    ) -> ft.Container:
        if 配置 is None:
            配置 = 界面配置()
        
        主题颜色 = 配置.当前主题颜色
        卡片列表: List[ft.Control] = []
        卡片数据: Dict[str, Dict[str, Any]] = {}
        
        def 创建卡片(
            卡片ID: str,
            标题: str,
            图标: str,
            副标题: str,
            控件配置: List[Dict[str, Any]],
            启用: bool=True,
        ) -> ft.Container:
            def 处理保存(配置键: str, 值: str):
                if 卡片ID not in 卡片数据:
                    卡片数据[卡片ID] = {}
                卡片数据[卡片ID][配置键] = 值
                if 保存回调:
                    保存回调(卡片ID, 配置键, 值)
            
            卡片 = 折叠卡片.创建(
                标题=标题,
                图标=图标,
                副标题=副标题,
                启用=启用,
                控件配置=控件配置,
                每行控件数=4,
                保存回调=处理保存,
                配置=配置,
            )
            卡片列表.append(卡片)
            return 卡片
        
        创建卡片(
            卡片ID="auto_hunting",
            标题="自动打野",
            图标="EXPLORE",
            副标题="自动搜索并攻击野怪",
            控件配置=[
                {"type": "dropdown", "config_key": "level", "label": "野怪等级", "value": "全部", "options": ["全部", "1-3级", "4-6级", "7-9级", "10级以上"]},
                {"type": "dropdown", "config_key": "frequency", "label": "搜索频率", "value": "每小时", "options": ["每30分钟", "每小时", "每2小时", "每4小时"]},
            ],
        )
        
        标题栏 = ft.Row([
            ft.Icon(ft.Icons.EXPLORE, size=20, color=主题颜色.get("accent")),
            ft.Container(width=6),
            ft.Text("打野设置", size=16, weight=ft.FontWeight.BOLD, color=主题颜色.get("text_primary")),
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
    ft.run(lambda page: page.add(打野界面.创建()))
