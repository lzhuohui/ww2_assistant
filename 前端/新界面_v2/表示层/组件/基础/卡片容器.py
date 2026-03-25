# -*- coding: utf-8 -*-
"""
模块名称：卡片容器
模块功能：Win11风格卡片容器，支持阴影、圆角、悬停效果
实现步骤：
- 创建Container组件
- 设置默认阴影和悬停阴影
- 绑定悬停事件实现动态效果
"""

import flet as ft
from typing import Optional

from 前端.新界面_v2.核心.配置.界面配置 import UIConfig

# *** 用户指定变量: 变量值必须生效,AI不得更改数据 ***
USER_WIDTH = 500       # 默认卡片宽度
USER_HEIGHT = 100      # 默认卡片高度
USER_PADDING = 5       # 默认卡片内边距
# *********************************

class CardContainer:
    """Win11风格卡片容器"""
    
    @staticmethod
    def create(
        content: ft.Control = None,
        config: UIConfig = None,
        width: Optional[int] = USER_WIDTH,
        height: Optional[int] = USER_HEIGHT,
        padding: int = USER_PADDING,
        radius: int = 8,
        hover_effect: bool = False,
        shadow_effect: bool = True,
    ) -> ft.Container:
        if config is None:
            config = UIConfig()
        
        if content is None:
            content = ft.Text("卡片内容示例", size=14)
        
        theme_colors = config.当前主题颜色
        
        default_shadow = ft.BoxShadow(
            spread_radius=0,
            blur_radius=4,
            color="rgba(0, 0, 0, 0.25)",
            offset=ft.Offset(0, 2),
        ) if shadow_effect else None
        
        hover_shadow = ft.BoxShadow(
            spread_radius=0,
            blur_radius=8,
            color="rgba(0, 0, 0, 0.3)",
            offset=ft.Offset(0, 4),
        ) if shadow_effect else None
        
        container = ft.Container(
            content=content,
            width=width,
            height=height,
            padding=padding,
            bgcolor=theme_colors.get("bg_card"),
            border_radius=radius,
            shadow=default_shadow,
            animate=ft.Animation(167, ft.AnimationCurve.EASE_OUT) if hover_effect else None,
        )
        
        if hover_effect:
            def handle_hover(e):
                if e.data == "true":
                    container.shadow = hover_shadow
                else:
                    container.shadow = default_shadow
                try:
                    if container.page:
                        container.update()
                except:
                    pass
            
            container.on_hover = handle_hover
        
        return container


# *** 标准测试格式: 仅调用被测模块,AI不得添加数据 ***
if __name__ == "__main__":
    def main(page: ft.Page):
        page.add(CardContainer.create())
    
    ft.app(target=main)
