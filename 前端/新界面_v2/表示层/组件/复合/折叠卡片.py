# -*- coding: utf-8 -*-
"""
模块名称：折叠卡片
设计思路: 卡片高度固定，支持配置模式和只读模式
模块隔离: 复合组件，依赖基础组件
"""

import flet as ft
from typing import Callable, Dict, Any, List, Optional

from 前端.新界面_v2.核心.配置.界面配置 import 界面配置
from 前端.新界面_v2.表示层.组件.基础.卡片容器 import 卡片容器, USER_WIDTH, USER_PADDING, USER_HEIGHT
from 前端.新界面_v2.表示层.组件.基础.下拉框 import 下拉框, USER_WIDTH as DROPDOWN_WIDTH


# *** 用户指定变量 - AI不得修改 ***
USER_ANIMATION_DURATION = 150
USER_DESTROY_DELAY_SECONDS = 30
USER_ICON_SIZE = 22
USER_TITLE_SIZE = 14
USER_SUBTITLE_SIZE = 12
# *********************************


class 折叠卡片:
    """折叠卡片 - 支持配置模式和只读模式"""
    
    @staticmethod
    def 创建(
        标题: str="卡片标题",
        图标: str="HOME",
        副标题: str="",
        启用: bool=True,
        只读模式: bool=False,
        控件: List[ft.Control]=None,
        控件配置: List[Dict[str, Any]]=None,
        每行控件数: int=6,
        宽度: int=None,
        值变更回调: Callable[[str, Any], None]=None,
        保存回调: Callable[[str, str], None]=None,
        配置: 界面配置=None,
    ) -> ft.Container:
        if 配置 is None:
            配置 = 界面配置()
        
        主题颜色 = 配置.当前主题颜色
        间距配置 = 配置.定义尺寸.get("间距", {})
        控件水平间距 = 间距配置.get("spacing_md", 12)
        控件垂直间距 = 间距配置.get("spacing_sm", 8)
        控件右边距 = 间距配置.get("spacing_xl", 20)
        
        卡片高度 = USER_HEIGHT
        卡片内边距 = USER_PADDING
        
        已加载 = [False]
        已启用 = [启用]
        开关状态 = [启用]
        控件字典: Dict[str, ft.Control] = {}
        当前值: Dict[str, str] = {}
        初始值: Dict[str, str] = {}
        
        图标控件 = ft.Icon(
            getattr(ft.Icons, 图标.upper(), ft.Icons.HOME),
            size=USER_ICON_SIZE,
            color=主题颜色.get("accent"),
            opacity=1.0 if 启用 else 0.4,
        )
        
        标题文本 = ft.Text(
            标题,
            size=USER_TITLE_SIZE,
            weight=ft.FontWeight.BOLD,
            color=主题颜色.get("text_primary"),
            opacity=1.0 if 启用 else 0.4,
        )
        
        加载图标 = ft.Icon(
            ft.Icons.PLAY_ARROW,
            size=18,
            color=主题颜色.get("text_secondary"),
        )
        
        副标题文本 = ft.Text(
            副标题,
            size=USER_SUBTITLE_SIZE,
            color=主题颜色.get("text_secondary"),
        )
        
        控件列 = ft.Column([], spacing=控件垂直间距, alignment=ft.MainAxisAlignment.CENTER)
        
        控件容器 = ft.Container(
            content=控件列,
            opacity=0.0 if not 只读模式 else 1.0,
            animate=ft.Animation(USER_ANIMATION_DURATION, ft.AnimationCurve.EASE_OUT) if not 只读模式 else None,
            right=控件右边距,
            top=0,
            bottom=0,
            alignment=ft.alignment.Alignment(1.0, 0.5),
            clip_behavior=ft.ClipBehavior.NONE,
        )
        
        副标题容器 = ft.Container(
            content=ft.Row([
                副标题文本,
                ft.Container(width=8) if not 只读模式 else ft.Container(),
                加载图标 if not 只读模式 else ft.Container(),
            ], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            opacity=1.0 if not 只读模式 else 0.0,
            animate=ft.Animation(USER_ANIMATION_DURATION, ft.AnimationCurve.EASE_OUT) if not 只读模式 else None,
            alignment=ft.Alignment(0, 0.5),
        )
        
        右侧堆栈 = ft.Stack([
            副标题容器,
            控件容器,
        ], clip_behavior=ft.ClipBehavior.NONE)
        
        右侧容器 = ft.Container(
            content=右侧堆栈,
            expand=True,
            clip_behavior=ft.ClipBehavior.NONE,
        )
        
        左侧内容 = ft.Column([
            图标控件,
            ft.Container(height=4),
            标题文本,
        ], spacing=0, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        左侧容器 = ft.Container(
            content=左侧内容,
            padding=ft.Padding(left=卡片内边距, top=0, right=卡片内边距, bottom=0),
            expand=False,
        )
        
        分割线 = ft.Container(
            width=2,
            bgcolor=主题颜色.get("accent", "#0078d4"),
            height=卡片高度 - 卡片内边距,
            margin=ft.Margin(0, 卡片内边距 / 2, 0, 卡片内边距 / 2)
        )
        
        主行 = ft.Row([
            ft.Container(
                content=ft.Row([
                    左侧容器,
                    分割线,
                ], spacing=0, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                alignment=ft.Alignment(0, 0),
                expand=False,
            ),
            右侧容器,
        ], height=卡片高度, spacing=0, vertical_alignment=ft.CrossAxisAlignment.CENTER, expand=True if 宽度 is None else False)
        
        容器 = 卡片容器.创建(
            配置=配置,
            内容=主行,
            高度=卡片高度,
            宽度=宽度,
            内边距=卡片内边距,
        )
        容器.clip_behavior = ft.ClipBehavior.NONE
        
        def 处理开关切换():
            if 只读模式:
                return
            新状态 = not 开关状态[0]
            开关状态[0] = 新状态
            已启用[0] = 新状态
            
            if 保存回调:
                保存回调("enabled", 新状态)
            
            更新卡片状态()
        
        def 更新卡片状态():
            if 只读模式:
                容器.opacity = 1.0
                图标控件.opacity = 1.0
                标题文本.opacity = 1.0
                return
            
            if 开关状态[0]:
                容器.opacity = 1.0
                右侧容器.on_click = lambda e: 加载控件()
                加载图标.color = 主题颜色.get("text_secondary")
                副标题文本.color = 主题颜色.get("text_secondary")
                图标控件.opacity = 1.0
                标题文本.opacity = 1.0
                
                if 已加载[0]:
                    for 控件实例 in 控件字典.values():
                        if hasattr(控件实例, '设置启用'):
                            控件实例.设置启用(True)
            else:
                容器.opacity = 0.5
                右侧容器.on_click = None
                加载图标.color = 主题颜色.get("text_disabled", "#888888")
                副标题文本.color = 主题颜色.get("text_disabled", "#888888")
                图标控件.opacity = 0.4
                标题文本.opacity = 0.4
                
                if 已加载[0]:
                    for 控件实例 in 控件字典.values():
                        if hasattr(控件实例, '设置启用'):
                            控件实例.设置启用(False)
            
            try:
                if 容器.page:
                    容器.page.update()
            except:
                pass
        
        if not 只读模式:
            左侧容器.on_click = lambda e: 处理开关切换()
        
        def 从配置创建控件() -> List[ft.Control]:
            创建的控件 = []
            
            for 控件配置项 in 控件配置:
                if 控件配置项.get("type") == "dropdown":
                    配置键 = 控件配置项.get("config_key", "")
                    标签 = 控件配置项.get("label", "")
                    选项列表 = 控件配置项.get("options", [])
                    值 = 控件配置项.get("value", 选项列表[0] if 选项列表 else "")
                    控件宽度 = 控件配置项.get("width", DROPDOWN_WIDTH)
                    
                    当前值[配置键] = 值
                    初始值[配置键] = 值
                    
                    标签文本 = ft.Text(
                        标签,
                        size=14,
                        color=主题颜色.get("text_secondary"),
                    )
                    
                    下拉框实例 = 下拉框.创建(
                        选项列表=选项列表,
                        当前值=值,
                        宽度=控件宽度,
                        启用=已启用[0] if not 只读模式 else True,
                        变更回调=lambda v, k=配置键: 处理值变更(k, v),
                        配置=配置,
                    )
                    控件字典[配置键] = 下拉框实例
                    
                    单个控件 = ft.Row([
                        标签文本,
                        下拉框实例,
                    ], spacing=4, vertical_alignment=ft.CrossAxisAlignment.CENTER)
                    
                    创建的控件.append(单个控件)
            
            return 创建的控件
        
        def 布局控件(控件列表: List[ft.Control]):
            行列表 = []
            当前行控件 = []
            当前行控件数 = 0
            
            for 单个控件 in 控件列表:
                if 当前行控件数 >= 每行控件数 and 当前行控件:
                    行列表.append(ft.Row(
                        当前行控件,
                        spacing=控件水平间距,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.END,
                    ))
                    当前行控件 = []
                    当前行控件数 = 0
                
                当前行控件.append(单个控件)
                当前行控件数 += 1
            
            if 当前行控件:
                行列表.append(ft.Row(
                    当前行控件,
                    spacing=控件水平间距,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.END,
                ))
            
            控件列.controls = 行列表
            已加载[0] = True
        
        def 处理值变更(配置键: str, 值: Any):
            当前值[配置键] = 值
            
            if 初始值.get(配置键) != 值:
                if 值变更回调:
                    值变更回调(配置键, 值)
                
                if 保存回调:
                    保存回调(配置键, 值)
        
        def 加载控件():
            if 已加载[0] or (not 开关状态[0] and not 只读模式):
                return
            
            最终控件列表 = []
            
            if 控件 is not None:
                最终控件列表 = 控件
            elif 控件配置 is not None:
                最终控件列表 = 从配置创建控件()
            
            if 最终控件列表:
                布局控件(最终控件列表)
            
            if not 只读模式:
                副标题容器.opacity = 0.0
                控件容器.opacity = 1.0
                
                try:
                    if 容器.page:
                        容器.page.update()
                except:
                    pass
        
        def 获取值() -> Dict[str, str]:
            for 键, 控件实例 in 控件字典.items():
                if hasattr(控件实例, '获取值'):
                    当前值[键] = 控件实例.获取值()
            return 当前值.copy()
        
        def 设置值(值字典: Dict[str, str]):
            for 键, 值 in 值字典.items():
                if 键 in 控件字典:
                    控件实例 = 控件字典[键]
                    if hasattr(控件实例, '设置值'):
                        控件实例.设置值(值)
                    当前值[键] = 值
                    初始值[键] = 值
        
        def 获取开关状态() -> bool:
            return 开关状态[0]
        
        def 设置开关状态(状态: bool):
            if 只读模式:
                return
            开关状态[0] = 状态
            已启用[0] = 状态
            更新卡片状态()
        
        容器.获取值 = 获取值
        容器.设置值 = 设置值
        容器.加载控件 = 加载控件
        容器.是否已加载 = lambda: 已加载[0]
        容器.获取开关状态 = 获取开关状态
        容器.设置开关状态 = 设置开关状态
        
        if 只读模式 and (控件 is not None or 控件配置 is not None):
            加载控件()
        
        更新卡片状态()
        
        return 容器


# *** 调试逻辑 ***
if __name__ == "__main__":
    ft.run(lambda page: page.add(折叠卡片.创建()))
