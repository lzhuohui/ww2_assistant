# -*- coding: utf-8 -*-
"""
模块名称：系统界面
设计思路: 系统配置界面，使用折叠卡片模式
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


class 系统界面:
    """系统配置界面"""
    
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
            卡片ID="hangup_mode",
            标题="挂机模式",
            图标="POWER_SETTINGS_NEW",
            副标题="全自动:自动挂机,无需人为干预 | 半自动:点击头像,自动切换账号",
            控件配置=[
                {"type": "dropdown", "config_key": "挂机模式", "label": "模式:", "value": "全自动", "options": ["全自动", "半自动"]},
            ],
        )
        
        创建卡片(
            卡片ID="command_speed",
            标题="指令速度",
            图标="SPEED",
            副标题="运行指令间隔频率(毫秒)，数值越小速度越快",
            控件配置=[
                {"type": "dropdown", "config_key": "指令速度", "label": "速度:", "value": "100", "options": ["100", "150", "200", "250", "300", "350", "400", "450", "500"]},
            ],
        )
        
        创建卡片(
            卡片ID="retry_count",
            标题="尝试次数",
            图标="REFRESH",
            副标题="连续操作失败达到最大尝试次数后,触发自动纠错系统",
            控件配置=[
                {"type": "dropdown", "config_key": "尝试次数", "label": "次数:", "value": "15", "options": ["10", "15", "20", "25", "30"]},
            ],
        )
        
        创建卡片(
            卡片ID="cache_limit",
            标题="清缓限量",
            图标="DELETE_SWEEP",
            副标题="达到设置系统缓存清理阈值(M)后,自动清理缓存",
            控件配置=[
                {"type": "dropdown", "config_key": "清缓限量", "label": "限量:", "value": "1.0", "options": ["1.0", "1.5", "2.0", "2.5", "3.0", "3.5", "4.0", "4.5", "5.0"]},
            ],
        )
        
        标题栏 = ft.Row([
            ft.Icon(ft.Icons.SETTINGS, size=20, color=主题颜色.get("accent")),
            ft.Container(width=6),
            ft.Text("系统配置", size=16, weight=ft.FontWeight.BOLD, color=主题颜色.get("text_primary")),
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
    ft.run(lambda page: page.add(系统界面.创建()))
