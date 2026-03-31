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
- 从配置服务获取UI配置

不负责：
- 内部内容
- 销毁（不需要销毁）

设计原则（符合V2版本模块化设计补充共识）：
- 从配置服务获取UI配置
- 定义DEFAULT_XXX作为fallback（确保模块可独立测试）
- 不在模块中硬编码配置值
"""

import flet as ft
from typing import Callable, Dict, Optional, Any

# ============================================
# 默认配置（fallback，用于模块独立测试）
# ============================================

DEFAULT_WIDTH = None
DEFAULT_HEIGHT = 92
DEFAULT_PADDING = 6
DEFAULT_BORDER_RADIUS = 8
CONTROL_ROW_HEIGHT = 36
CONTROL_V_SPACING = 8

# ============================================
# 公开接口
# ============================================

class CardContainer:
    """
    基础卡片容器 - 支持阴影立体效果（层级5：基础模块）
    
    职责：
    - 布局容器
    - 阴影效果
    - 从配置服务获取UI配置
    
    不负责：
    - 内部内容
    - 销毁（不需要销毁）
    
    设计原则：
    - 优先从config_service获取配置
    - 使用DEFAULT_XXX作为fallback
    - 确保模块可独立运行测试
    """
    
    # 缓存配置服务实例
    _config_service = None
    
    @classmethod
    def set_config_service(cls, config_service):
        """设置配置服务实例（供上层模块调用）"""
        cls._config_service = config_service
    
    @staticmethod
    def get_height() -> int:
        """获取卡片最小高度（从配置服务获取，fallback到默认值）"""
        if CardContainer._config_service:
            return CardContainer._config_service.get_card_min_height()
        return DEFAULT_HEIGHT
    
    @staticmethod
    def get_width() -> Optional[int]:
        """获取卡片宽度（从配置服务获取）"""
        return DEFAULT_WIDTH
    
    @staticmethod
    def get_padding() -> int:
        """获取内边距（从配置服务获取，fallback到默认值）"""
        if CardContainer._config_service:
            return CardContainer._config_service.get_card_padding()
        return DEFAULT_PADDING
    
    @staticmethod
    def get_border_radius() -> int:
        """获取圆角半径"""
        return DEFAULT_BORDER_RADIUS
    
    @staticmethod
    def get_control_row_height() -> int:
        """获取每行控件高度"""
        if CardContainer._config_service:
            return CardContainer._config_service.get_ui_config("卡片", "控件行高", CONTROL_ROW_HEIGHT)
        return CONTROL_ROW_HEIGHT
    
    @staticmethod
    def get_control_v_spacing() -> int:
        """获取控件垂直间距"""
        if CardContainer._config_service:
            return CardContainer._config_service.get_ui_config("卡片", "控件行间距", CONTROL_V_SPACING)
        return CONTROL_V_SPACING
    
    @staticmethod
    def calculate_height(control_rows: int = 1) -> int:
        """
        计算卡片高度（最小高度为DEFAULT_HEIGHT，确保统一风格）
        
        参数：
        - control_rows: 控件行数
        
        返回：
        - 计算后的卡片高度（不小于最小高度）
        
        设计说明：
        - 最小高度92px对应2行控件，是大多数卡片的常见情况
        - 统一最小高度可保证同一界面内卡片高度一致，视觉整齐美观
        - 控件行数超过2行时自动扩展高度
        """
        min_height = CardContainer.get_height()
        
        if control_rows <= 0:
            return min_height
        
        row_height = CardContainer.get_control_row_height()
        v_spacing = CardContainer.get_control_v_spacing()
        
        # 控件区域高度 = 控件行数 * 行高 + (行数-1) * 行间距
        control_area_height = control_rows * row_height
        if control_rows > 1:
            control_area_height += (control_rows - 1) * v_spacing
        
        # 计算高度 = 内边距 + 控件区域高度
        padding = CardContainer.get_padding()
        calculated_height = padding * 2 + control_area_height
        
        # 返回不小于最小高度的高度值
        return max(min_height, calculated_height)
    
    @staticmethod
    def create(
        content: ft.Control = None,
        height: int = None,
        width: int = None,
        padding: int = None,
        on_click: Callable = None,
        elevation: int = 1,
        theme_colors: Dict[str, str] = None,
    ) -> ft.Container:
        """
        创建卡片容器
        
        参数：
        - content: 内部内容
        - height: 高度（默认从配置服务获取）
        - width: 宽度（默认从配置服务获取）
        - padding: 内边距（默认从配置服务获取）
        - on_click: 点击回调
        - elevation: 阴影层级
        - theme_colors: 主题颜色
        """
        if height is None:
            height = CardContainer.get_height()
        if width is None:
            width = CardContainer.get_width()
        if padding is None:
            padding = CardContainer.get_padding()
        
        if theme_colors is None:
            theme_colors = {
                "bg_card": "#2D2D2D",
                "shadow": "rgba(0, 0, 0, 0.25)",
                "shadow_hover": "rgba(0, 0, 0, 0.35)",
            }
        
        shadow = ft.BoxShadow(
            spread_radius=0,
            blur_radius=4 * elevation,
            color=theme_colors.get("shadow", "#26000000"),
            offset=ft.Offset(0, 2 * elevation),
        )
        
        container = ft.Container(
            content=content,
            width=width,
            height=height,
            padding=padding,
            bgcolor=theme_colors.get("bg_card", "#FFFFFF"),
            border_radius=DEFAULT_BORDER_RADIUS,
            on_click=on_click,
            shadow=shadow,
            animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
        )
        
        def handle_hover(e):
            if e.data == "true":
                container.shadow = ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=8,
                    color=theme_colors.get("shadow_hover", "#33000000"),
                    offset=ft.Offset(0, 4),
                )
            else:
                container.shadow = shadow
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
        page.title = "卡片容器测试"
        
        # 测试1：不使用配置服务（使用fallback）
        card1 = CardContainer.create(
            content=ft.Text("测试卡片（无配置服务）"),
            height=80,
        )
        page.add(card1)
        
        # 测试2：计算高度
        print(f"1行控件高度: {CardContainer.calculate_height(1)}")
        print(f"2行控件高度: {CardContainer.calculate_height(2)}")
        print(f"3行控件高度: {CardContainer.calculate_height(3)}")
    
    ft.app(target=main)
