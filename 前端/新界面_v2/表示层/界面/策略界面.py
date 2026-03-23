# -*- coding: utf-8 -*-
"""
模块名称：策略界面
设计思路: 游戏策略配置界面，使用折叠卡片模式
模块隔离: 界面层依赖组件层和业务层
"""

import flet as ft
from typing import Dict, Any, List, Callable

from 前端.新界面_v2.核心.配置.界面配置 import 界面配置
from 前端.新界面_v2.表示层.组件.复合.折叠卡片 import 折叠卡片
from 前端.新界面_v2.核心.常量.全局常量 import USER_SPACING, USER_CARD_HEIGHT, USER_CARD_SPACING


# *** 用户指定变量 - AI不得修改 ***
# （用户未指定变量）
# *********************************


class 策略界面:
    """游戏策略配置界面"""
    
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
            卡片ID="quick_build",
            标题="建筑速建",
            图标="APARTMENT",
            副标题="达到设置主城等级后,允许加速建筑建设",
            控件配置=[
                {"type": "dropdown", "config_key": "速建限级", "label": "限级:", "value": "08", "options": ["05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15"]},
                {"type": "dropdown", "config_key": "速建类型", "label": "类型:", "value": "城资建筑", "options": ["城资建筑", "城市建筑", "资源建筑"]},
            ],
        )
        
        创建卡片(
            卡片ID="quick_produce",
            标题="资源速产",
            图标="INVENTORY_2",
            副标题="达到设置主城等级后,允许加速资源生产",
            控件配置=[
                {"type": "dropdown", "config_key": "速产限级", "label": "限级:", "value": "07", "options": ["05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15"]},
                {"type": "dropdown", "config_key": "速产类型", "label": "类型:", "value": "平衡资源", "options": ["平衡资源", "战时经济", "钢铁熔炉", "橡胶采集", "石油开采"]},
            ],
        )
        
        创建卡片(
            卡片ID="point_reserve",
            标题="策点保留",
            图标="SAVINGS",
            副标题="达到设置保留的策略点数后,允许使用策略",
            控件配置=[
                {"type": "dropdown", "config_key": "保留点数", "label": "点数:", "value": "60", "options": ["30", "60", "90", "120", "150", "180", "210", "240"]},
            ],
        )
        
        标题栏 = ft.Row([
            ft.Icon(ft.Icons.ROCKET_LAUNCH, size=20, color=主题颜色.get("accent")),
            ft.Container(width=6),
            ft.Text("策略配置", size=16, weight=ft.FontWeight.BOLD, color=主题颜色.get("text_primary")),
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
        
        def 获取所有值() -> Dict[str, Dict[str, str]]:
            结果 = {}
            for i, 卡片 in enumerate(卡片列表):
                if hasattr(卡片, '获取值'):
                    卡片ID = list(卡片数据.keys())[i] if i < len(卡片数据) else f"card_{i}"
                    结果[卡片ID] = 卡片.获取值()
            return 结果
        
        def 设置所有值(值字典: Dict[str, Dict[str, str]]):
            for i, 卡片 in enumerate(卡片列表):
                if hasattr(卡片, '设置值'):
                    卡片ID = list(卡片数据.keys())[i] if i < len(卡片数据) else f"card_{i}"
                    if 卡片ID in 值字典:
                        卡片.设置值(值字典[卡片ID])
        
        内容列.获取所有值 = 获取所有值
        内容列.设置所有值 = 设置所有值
        
        return ft.Container(
            content=内容列,
            expand=True,
        )


# *** 调试逻辑 ***
if __name__ == "__main__":
    ft.run(lambda page: page.add(策略界面.创建()))
