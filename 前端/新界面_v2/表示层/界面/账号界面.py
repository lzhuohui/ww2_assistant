# -*- coding: utf-8 -*-
"""
模块名称：账号界面
设计思路: 账号配置界面，使用折叠卡片和输入框组件
模块隔离: 界面层依赖组件层和业务层
"""

import flet as ft
from typing import Dict, Any, List, Callable

from 前端.新界面_v2.核心.配置.界面配置 import 界面配置
from 前端.新界面_v2.表示层.组件.复合.折叠卡片 import 折叠卡片
from 前端.新界面_v2.表示层.组件.基础.下拉框 import 下拉框
from 前端.新界面_v2.表示层.组件.基础.输入框 import 输入框
from 前端.新界面_v2.核心.常量.全局常量 import USER_SPACING, USER_CARD_SPACING


# *** 用户指定变量 - AI不得修改 ***
USER_MAX_ACCOUNTS = 15
DROPDOWN_WIDTH = 70
INPUT_WIDTH = 120
# *********************************


class 账号界面:
    """账号配置界面"""
    
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
            默认类型: str="付帅",
            启用: bool=True,
        ) -> ft.Container:
            def 处理保存(配置键: str, 值: str):
                if 卡片ID not in 卡片数据:
                    卡片数据[卡片ID] = {}
                卡片数据[卡片ID][配置键] = 值
                if 保存回调:
                    保存回调(卡片ID, 配置键, 值)
            
            类型下拉框 = 下拉框.创建(
                选项列表=["主帅", "付帅"],
                当前值=默认类型,
                宽度=DROPDOWN_WIDTH,
                启用=启用,
                变更回调=lambda v: 处理保存("类型", v),
                配置=配置,
            )
            
            平台下拉框 = 下拉框.创建(
                选项列表=["Tap", "官方", "其他"],
                当前值="Tap",
                宽度=DROPDOWN_WIDTH,
                启用=启用,
                变更回调=lambda v: 处理保存("平台", v),
                配置=配置,
            )
            
            名称输入框 = 输入框.创建(
                配置=配置,
                提示文本="名称",
                宽度=INPUT_WIDTH,
                启用=启用,
                变更回调=lambda v: 处理保存("名称", v),
            )
            
            账号输入框 = 输入框.创建(
                配置=配置,
                提示文本="账号",
                宽度=INPUT_WIDTH,
                启用=启用,
                变更回调=lambda v: 处理保存("账号", v),
            )
            
            密码输入框 = 输入框.创建(
                配置=配置,
                提示文本="密码",
                宽度=INPUT_WIDTH,
                密码模式=True,
                启用=启用,
                变更回调=lambda v: 处理保存("密码", v),
            )
            
            控件列表 = [
                类型下拉框,
                名称输入框,
                账号输入框,
                密码输入框,
                平台下拉框,
            ]
            
            卡片 = 折叠卡片.创建(
                标题=标题,
                图标=图标,
                副标题=副标题,
                启用=启用,
                控件=控件列表,
                每行控件数=5,
                保存回调=处理保存,
                配置=配置,
            )
            卡片列表.append(卡片)
            return 卡片
        
        for i in range(1, USER_MAX_ACCOUNTS + 1):
            卡片ID = f"account_{i:02d}"
            标题 = f"{i:02d}账号"
            默认类型 = "主帅" if i == 1 else "付帅"
            
            创建卡片(
                卡片ID=卡片ID,
                标题=标题,
                图标="ACCOUNT_CIRCLE",
                副标题=f"配置第{i}个账号信息",
                默认类型=默认类型,
            )
        
        标题栏 = ft.Row([
            ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=20, color=主题颜色.get("accent")),
            ft.Container(width=6),
            ft.Text("账号设置", size=16, weight=ft.FontWeight.BOLD, color=主题颜色.get("text_primary")),
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
    ft.run(lambda page: page.add(账号界面.创建()))
