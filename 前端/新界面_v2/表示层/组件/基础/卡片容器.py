# -*- coding: utf-8 -*-
"""
模块名称：卡片容器
设计思路: Win11风格卡片，支持阴影、圆角、悬停效果
模块隔离: 基础组件，不依赖其他业务组件
"""

import flet as ft
from typing import Optional

from 前端.新界面_v2.核心.配置.界面配置 import 界面配置


# *** 用户指定变量 - AI不得修改, 变量值必须生效 ***
USER_WIDTH = 500  # 默认卡片宽度
USER_HEIGHT = 200  # 默认卡片高度
USER_PADDING = 20  # 默认卡片内边距
# *********************************


class 卡片容器:
    """Win11风格卡片容器"""
    
    @staticmethod
    def 创建(
        内容: ft.Control=None,
        配置: 界面配置=None,
        宽度: Optional[int]=None,
        高度: Optional[int]=USER_HEIGHT,
        内边距: int=USER_PADDING,
        圆角: int=8,
        悬停效果: bool=False,
        阴影效果: bool=True,
    ) -> ft.Container:
        if 配置 is None:
            配置 = 界面配置()
        
        if 内容 is None:
            内容 = ft.Text("卡片内容示例", size=14)
        
        主题颜色 = 配置.当前主题颜色
        
        默认阴影 = ft.BoxShadow(
            spread_radius=0,
            blur_radius=4,
            color="rgba(0, 0, 0, 0.25)",
            offset=ft.Offset(0, 2),
        ) if 阴影效果 else None
        
        悬停阴影 = ft.BoxShadow(
            spread_radius=0,
            blur_radius=8,
            color="rgba(0, 0, 0, 0.3)",
            offset=ft.Offset(0, 4),
        ) if 阴影效果 else None
        
        容器 = ft.Container(
            content=内容,
            width=宽度,
            height=高度,
            padding=内边距,
            bgcolor=主题颜色.get("bg_card"),
            border_radius=圆角,
            shadow=默认阴影,
            animate=ft.Animation(167, ft.AnimationCurve.EASE_OUT) if 悬停效果 else None,
        )
        
        if 悬停效果:
            def 处理悬停(e):
                if e.data == "true":
                    容器.shadow = 悬停阴影
                else:
                    容器.shadow = 默认阴影
                try:
                    if 容器.page:
                        容器.update()
                except:
                    pass
            
            容器.on_hover = 处理悬停
        
        return 容器


# *** 调试逻辑 ***
if __name__ == "__main__":
    ft.run(lambda page: page.add(卡片容器.创建()))
