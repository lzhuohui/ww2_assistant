# -*- coding: utf-8 -*-

"""
模块名称：用户信息卡片.py
模块功能：用户信息卡片组件，显示用户名和账号信息

实现步骤：
- 创建用户名显示
- 创建账号信息显示
- 创建卡片容器
- 组合布局

职责：
- 用户名显示
- 账号信息显示
- 卡片容器
- 从配置服务获取用户信息、主题颜色

不负责：
- 布局
- 销毁（不需要销毁）

设计原则（符合V2版本模块化设计补充共识）：
- 定义1：自己获取用户名、账号信息、主题颜色
- 定义2：上层只传递section
- 定义3：theme_colors可覆盖
- 定义4：create()
"""

import flet as ft
from typing import Dict, Optional

from 前端.V2.层级5_基础模块.卡片容器 import CardContainer
from 前端.V2.层级5_基础模块.标签 import Label
from 前端.V2.层级5_基础模块.头像 import Avatar

# ============================================
# 数据和文件接口（前置，方便查看和修改）
# ============================================

# *** 用户指定变量: 变量值必须生效,AI不得更改数据 ***
USER_WIDTH = 200      # 卡片宽度（None表示自适应）
USER_HEIGHT = 80     # 卡片高度（None表示从用户偏好.json获取）
# *********************************

# 用户信息卡片无默认值配置，所有UI配置从用户偏好.json获取
# 如果用户偏好.json缺少配置，抛出错误而非掩盖

# ============================================
# 公开接口
# ============================================

class UserInfoCard:
    """
    用户信息卡片组件（层级4：复合模块）
    
    职责：
    - 用户名显示
    - 账号信息显示
    - 卡片容器
    - 从配置服务获取用户信息、主题颜色
    
    不负责：
    - 布局
    - 销毁（不需要销毁）
    """
    
    _config_service = None
    
    @classmethod
    def set_config_service(cls, config_service):
        """设置配置服务实例"""
        cls._config_service = config_service
        CardContainer.set_config_service(config_service)
        Label.set_config_service(config_service)
        Avatar.set_config_service(config_service)
    
    @staticmethod
    def get_username_size() -> int:
        """获取用户名尺寸（从用户偏好.json获取基础大小*1.14）"""
        UserInfoCard._check_config_service()
        base_size = Label.get_base_size()
        return int(base_size * 1.14)
    
    @staticmethod
    def get_info_size() -> int:
        """获取信息尺寸（从用户偏好.json获取基础大小*0.86）"""
        UserInfoCard._check_config_service()
        base_size = Label.get_base_size()
        return int(base_size * 0.86)
    
    @staticmethod
    def get_card_height() -> int:
        """获取卡片高度（从用户偏好.json获取）"""
        UserInfoCard._check_config_service()
        value = UserInfoCard._config_service.get_ui_config("用户信息卡片", "高度")
        if value is None:
            raise RuntimeError("用户偏好.json缺少配置: 用户信息卡片.高度")
        return value
    
    @staticmethod
    def _check_config_service():
        """检查配置服务是否已设置"""
        if UserInfoCard._config_service is None:
            raise RuntimeError(
                "UserInfoCard模块未设置config_service，"
                "请先调用 UserInfoCard.set_config_service(config_service)"
            )
    
    @staticmethod
    def create(
        section: str = "用户信息",
        theme_colors: Dict[str, str] = None,
        width: int = None,
        height: int = None,
    ) -> ft.Container:
        """
        创建用户信息卡片（模块自己从配置服务获取用户信息）
        
        参数：
        - section: 配置节
        - theme_colors: 主题颜色（可选，不传则从配置服务获取）
        - width: 宽度（可选，优先级：USER_WIDTH > 参数 > 自适应）
        - height: 高度（可选，优先级：USER_HEIGHT > 参数 > 用户偏好.json）
        
        注意：用户名、账号信息由模块自己从config_service获取
        """
        if UserInfoCard._config_service is None:
            raise RuntimeError("UserInfoCard模块未设置config_service，请先调用UserInfoCard.set_config_service()")
        
        if theme_colors is None:
            theme_colors = UserInfoCard._config_service.get_theme_colors()
        
        width = USER_WIDTH if USER_WIDTH is not None else width
        height = USER_HEIGHT if USER_HEIGHT is not None else (height if height is not None else UserInfoCard.get_card_height())
        
        username = UserInfoCard._config_service.get_value(section, "username", "用户名")
        account_info = UserInfoCard._config_service.get_value(section, "account_info", "账号信息")
        
        username_size = UserInfoCard.get_username_size()
        info_size = UserInfoCard.get_info_size()
        
        avatar = Avatar.create(
            text=username if username else None,
            on_text_change=None,
            theme_colors=theme_colors,
            enabled=True,
        )
        
        username_text = Label.create(
            text=username,
            size=username_size,
            weight=ft.FontWeight.BOLD,
            color_type="primary",
        )
        
        info_text = Label.create(
            text=account_info,
            size=info_size,
            color_type="secondary",
        )
        
        right_column = ft.Column([
            username_text,
            info_text,
        ], spacing=4, alignment=ft.MainAxisAlignment.CENTER)
        
        content = ft.Row([
            avatar,
            ft.Container(width=12),
            right_column,
        ], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER)
        
        container = CardContainer.create(
            content=content,
            height=height,
            width=width,
        )
        
        return container

# *** 标准测试格式: 仅调用被测模块,AI不得添加数据 ***
if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    
    from 前端.V2.业务层.服务.配置服务 import ConfigService
    
    def main(page: ft.Page):
        page.title = "用户信息卡片测试"
        
        config_service = ConfigService()
        UserInfoCard.set_config_service(config_service)
        
        card = UserInfoCard.create()
        page.add(card)
    
    ft.run(main)
