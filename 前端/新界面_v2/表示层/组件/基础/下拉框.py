# -*- coding: utf-8 -*-
"""
模块名称：下拉框
设计思路: 使用PopupMenuButton实现下拉框，Win11风格控件状态
模块隔离: 纯UI组件，不包含业务逻辑
"""

from typing import Callable, List
import flet as ft

from 前端.新界面_v2.核心.配置.界面配置 import 界面配置


# *** 用户指定变量 - AI不得修改 ***
USER_WIDTH = 120
USER_HEIGHT = 32
# *********************************


class 下拉框:
    """下拉框 - 使用PopupMenuButton实现，Win11风格"""
    
    @staticmethod
    def 创建(
        选项列表: List[str]=None,
        当前值: str="",
        宽度: int=USER_WIDTH,
        高度: int=USER_HEIGHT,
        变更回调: Callable[[str], None]=None,
        启用: bool=True,
        配置: 界面配置=None,
    ) -> ft.Container:
        if 配置 is None:
            配置 = 界面配置()
        
        主题颜色 = 配置.当前主题颜色
        
        实际选项 = 选项列表 if 选项列表 else ["选项A", "选项B", "选项C"]
        实际当前值 = 当前值 if 当前值 else (实际选项[0] if 实际选项 else "")
        
        当前选中值 = [实际当前值]
        启用状态 = [启用]
        
        文字颜色 = 主题颜色.get("text_primary") if 启用 else 主题颜色.get("text_hint")
        图标颜色 = 主题颜色.get("text_secondary") if 启用 else 主题颜色.get("text_hint")
        背景颜色 = 主题颜色.get("bg_secondary") if 启用 else 主题颜色.get("bg_primary")
        边框颜色 = 主题颜色.get("border") if 启用 else "transparent"
        
        选中文本 = ft.Text(
            实际当前值,
            size=14,
            color=文字颜色,
            overflow=ft.TextOverflow.ELLIPSIS,
        )
        
        下拉图标 = ft.Icon(
            ft.Icons.KEYBOARD_ARROW_DOWN,
            size=18,
            color=图标颜色,
        )
        
        按钮内容 = ft.Container(
            content=ft.Row(
                [选中文本, 下拉图标],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=宽度,
            height=高度,
            border_radius=6,
            bgcolor=背景颜色,
            border=ft.Border.all(1, 边框颜色),
            padding=ft.Padding(left=12, right=8, top=0, bottom=0),
            animate=ft.Animation(167, ft.AnimationCurve.EASE_OUT),
        )
        
        def 创建菜单项():
            菜单项列表 = []
            for 选项 in 实际选项:
                def 创建回调(值=选项):
                    def 回调(e):
                        当前选中值[0] = 值
                        选中文本.value = 值
                        if 容器.page:
                            容器.update()
                        if 变更回调:
                            变更回调(值)
                    return 回调
                
                菜单项 = ft.PopupMenuItem(
                    content=ft.Text(
                        选项,
                        size=14,
                        color=主题颜色.get("text_primary"),
                    ),
                    on_click=创建回调(),
                )
                菜单项列表.append(菜单项)
            return 菜单项列表
        
        弹出按钮 = ft.PopupMenuButton(
            content=按钮内容,
            items=创建菜单项(),
            disabled=not 启用,
            bgcolor=主题颜色.get("bg_card"),
            menu_padding=ft.Padding.all(4),
            align=ft.Alignment.TOP_LEFT,
        )
        
        容器 = ft.Container(
            content=弹出按钮,
            width=宽度,
        )
        
        def 处理悬停(e):
            if not 启用状态[0]:
                return
            if e.data == "true":
                按钮内容.border = ft.Border.all(1, 主题颜色.get("accent"))
            else:
                按钮内容.border = ft.Border.all(1, 主题颜色.get("border"))
            try:
                if 容器.page:
                    容器.update()
            except:
                pass
        
        容器.on_hover = 处理悬停
        
        def 获取值() -> str:
            return 当前选中值[0]
        
        def 设置值(新值: str):
            if 新值 in 实际选项:
                当前选中值[0] = 新值
                选中文本.value = 新值
                if 容器.page:
                    容器.update()
        
        def 设置启用(状态: bool):
            启用状态[0] = 状态
            文字色 = 主题颜色.get("text_primary") if 状态 else 主题颜色.get("text_hint")
            图标色 = 主题颜色.get("text_secondary") if 状态 else 主题颜色.get("text_hint")
            背景色 = 主题颜色.get("bg_secondary") if 状态 else 主题颜色.get("bg_primary")
            边框色 = 主题颜色.get("border") if 状态 else "transparent"
            
            选中文本.color = 文字色
            下拉图标.color = 图标色
            按钮内容.bgcolor = 背景色
            按钮内容.border = ft.Border.all(1, 边框色)
            弹出按钮.disabled = not 状态
            
            try:
                if 容器.page:
                    容器.update()
            except:
                pass
        
        容器.获取值 = 获取值
        容器.设置值 = 设置值
        容器.设置启用 = 设置启用
        
        return 容器


# *** 调试逻辑 ***
if __name__ == "__main__":
    ft.run(lambda page: page.add(下拉框.创建()))
