# -*- coding: utf-8 -*-

"""
模块名称：分割线.py
模块功能：分割线组件

实现步骤：
- 创建水平/垂直分割线
- 支持主题颜色
- 支持自定义粗细

职责：
- 分隔显示

不负责：
- 布局
- 销毁（不需要销毁）

设计原则（符合V2版本模块化设计补充共识）：
- 用户偏好.json是UI配置唯一来源
- 分割线粗细是固定值，不是风格配置，使用硬编码默认值
"""

import flet as ft
from typing import Dict, Optional

# ============================================
# 数据和文件接口（前置，方便查看和修改）
# ============================================

# 分割线粗细是固定值，不是风格配置，使用硬编码默认值
DEFAULT_HEIGHT = 1
DEFAULT_WIDTH = 1

# ============================================
# 公开接口
# ============================================

class Divider:
    """
    分割线组件
    
    职责：
    - 分隔显示
    
    不负责：
    - 布局
    - 销毁（不需要销毁）
    """
    
    _config_service = None
    
    @classmethod
    def set_config_service(cls, config_service):
        """设置配置服务实例"""
        cls._config_service = config_service
    
    @staticmethod
    def _check_config_service():
        """检查配置服务是否已设置"""
        if Divider._config_service is None:
            raise RuntimeError(
                "Divider模块未设置config_service，"
                "请先调用 Divider.set_config_service(config_service)"
            )
    
    @staticmethod
    def _get_theme_colors() -> Dict[str, str]:
        """获取主题颜色"""
        Divider._check_config_service()
        return Divider._config_service.get_theme_colors()
    
    @staticmethod
    def create_horizontal(
        height: int = 1,
        color_type: str = "divider",
        theme_colors: Dict[str, str] = None,
    ) -> ft.Divider:
        """
        创建水平分割线
        
        参数：
        - height: 分割线高度（粗细）
        - color_type: 颜色类型 (divider/accent)
        - theme_colors: 主题颜色
        """
        if theme_colors is None:
            theme_colors = Divider._get_theme_colors()
        
        color = theme_colors.get(color_type, theme_colors.get("divider"))
        
        return ft.Divider(
            height=height,
            thickness=height,
            color=color,
        )
    
    @staticmethod
    def create_vertical(
        width: int = 1,
        color_type: str = "divider",
        theme_colors: Dict[str, str] = None,
    ) -> ft.VerticalDivider:
        """
        创建垂直分割线
        
        参数：
        - width: 分割线宽度（粗细）
        - color_type: 颜色类型 (divider/accent)
        - theme_colors: 主题颜色
        """
        if theme_colors is None:
            theme_colors = Divider._get_theme_colors()
        
        color = theme_colors.get(color_type, theme_colors.get("divider"))
        
        return ft.VerticalDivider(
            width=width,
            thickness=width,
            color=color,
        )

# *** 标准测试格式: 仅调用被测模块,AI不得添加数据 ***
if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
    
    from 前端.V2.业务层.服务.配置服务 import ConfigService
    
    def main(page: ft.Page):
        page.title = "分割线测试"
        
        config_service = ConfigService()
        Divider.set_config_service(config_service)
        
        column = ft.Column([
            ft.Text("上方内容"),
            Divider.create_horizontal(),
            ft.Text("下方内容"),
        ])
        page.add(column)
    
    ft.run(main)
