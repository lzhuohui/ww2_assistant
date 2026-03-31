# -*- coding: utf-8 -*-

"""
模块名称：卡片容器.py
模块功能：基础卡片容器组件，支持阴影效果

实现步骤：
- 创建圆角卡片容器
- 支持阴影效果
- 支持主题配置
- Win11风格

职责：
- 布局容器
- 阴影效果
- 从用户偏好.json获取UI配置

不负责：
- 内部内容
- 控件高度和间距
- 销毁（不需要销毁）

设计原则（符合V2版本模块化设计补充共识）：
- 用户偏好.json是UI配置唯一来源
- 如果用户偏好.json缺少配置，抛出错误
- 不使用DEFAULT_XXX掩盖问题
- 容器只做主题细节的处理
"""

import flet as ft
from typing import Dict, Optional, Callable

# ============================================
# 数据和文件接口（前置，方便查看和修改）
# ============================================

# *** 用户指定变量: 变量值必须生效,AI不得更改数据 ***
USER_CARD_HEIGHT = 100         # 卡片高度（像素）
# *********************************

# ============================================
# 公开接口
# ============================================

class CardContainer:
    """
    基础卡片容器 - 支持阴影立体效果（层级5：基础模块）
    
    职责：
    - 布局容器
    - 阴影效果
    - 从用户偏好.json获取UI配置
    
    不负责：
    - 内部内容
    - 控件高度和间距
    - 销毁（不需要销毁）
    
    设计原则：
    - 用户偏好.json是UI配置唯一来源
    - 如果缺少配置，抛出错误而非掩盖
    - 容器只做主题细节的处理
    """
    
    _config_service = None
    
    @classmethod
    def set_config_service(cls, config_service):
        """设置配置服务实例（供上层模块调用）"""
        cls._config_service = config_service
    
    @staticmethod
    def _check_config_service():
        """检查配置服务是否已设置"""
        if CardContainer._config_service is None:
            raise RuntimeError(
                "CardContainer模块未设置config_service，"
                "请先调用 CardContainer.set_config_service(config_service)"
            )
    
    @staticmethod
    def get_height() -> int:
        """获取卡片高度（用户指定变量）"""
        return USER_CARD_HEIGHT
    
    @staticmethod
    def get_width() -> Optional[int]:
        """获取卡片宽度（从配置服务获取）"""
        return None
    
    @staticmethod
    def get_padding() -> int:
        """获取内边距（从用户偏好.json获取）"""
        CardContainer._check_config_service()
        padding = CardContainer._config_service.get_ui_config("卡片", "内边距")
        if padding is None:
            raise RuntimeError("用户偏好.json缺少配置: 卡片.内边距")
        return padding
    
    @staticmethod
    def get_border_radius() -> int:
        """获取圆角半径（从用户偏好.json获取）"""
        CardContainer._check_config_service()
        radius = CardContainer._config_service.get_ui_config("卡片", "圆角")
        if radius is None:
            raise RuntimeError("用户偏好.json缺少配置: 卡片.圆角")
        return radius
    
    @staticmethod
    def _get_theme_colors() -> Dict[str, str]:
        """获取主题颜色"""
        CardContainer._check_config_service()
        return CardContainer._config_service.get_theme_colors()
    
    @staticmethod
    def create(
        content: ft.Control,
        height: int = None,
        width: int = None,
        on_click: Callable = None,
        on_hover: Callable = None,
    ) -> ft.Container:
        """
        创建卡片容器
        
        参数：
        - content: 容器内容
        - height: 容器高度（可选，默认从模块变量获取）
        - width: 容器宽度（可选）
        - on_click: 点击回调
        - on_hover: 悬停回调
        """
        theme_colors = CardContainer._get_theme_colors()
        
        container_height = height if height is not None else CardContainer.get_height()
        container_width = width
        padding = CardContainer.get_padding()
        border_radius = CardContainer.get_border_radius()
        
        container = ft.Container(
            content=content,
            width=container_width,
            height=container_height,
            padding=padding,
            border_radius=border_radius,
            bgcolor=theme_colors.get("bg_card"),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=4,
                color=theme_colors.get("shadow", "rgba(0, 0, 0, 0.25)"),
                offset=ft.Offset(0, 2),
            ),
            on_click=on_click,
            on_hover=on_hover,
            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
        )
        
        return container

# *** 标准测试格式: 仅调用被测模块,AI不得添加数据 ***
if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
    
    from 前端.V2.业务层.服务.配置服务 import ConfigService
    
    def main(page: ft.Page):
        page.title = "卡片容器测试"
        
        config_service = ConfigService()
        CardContainer.set_config_service(config_service)
        
        print(f"卡片高度: {CardContainer.get_height()}")
        print(f"卡片内边距: {CardContainer.get_padding()}")
        print(f"卡片圆角: {CardContainer.get_border_radius()}")
        
        card1 = CardContainer.create(
            content=ft.Text("测试卡片"),
            height=80,
        )
        page.add(card1)
    
    ft.run(main)
