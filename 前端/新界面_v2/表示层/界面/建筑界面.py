# -*- coding: utf-8 -*-
"""
模块名称：建筑界面
设计思路: 建筑配置界面，使用折叠卡片模式
模块隔离: 界面层依赖组件层和业务层
"""

import flet as ft
from typing import Dict, Any, List, Callable

from 前端.新界面_v2.核心.配置.界面配置 import 界面配置
from 前端.新界面_v2.表示层.组件.复合.折叠卡片 import 折叠卡片
from 前端.新界面_v2.核心.常量.全局常量 import USER_SPACING, USER_CARD_SPACING


# *** 用户指定变量 - AI不得修改 ***
# （用户未指定变量）
# *********************************


class 建筑界面:
    """建筑配置界面"""
    
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
            每行控件数: int=6,
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
                每行控件数=每行控件数,
                保存回调=处理保存,
                配置=配置,
            )
            卡片列表.append(卡片)
            return 卡片
        
        等级选项 = [f"{i:02d}" for i in range(1, 21)]
        等级选项_含0 = [f"{i:02d}" for i in range(0, 21)]
        下拉框宽度 = 70
        
        创建卡片(
            卡片ID="main_city",
            标题="主帅主城",
            图标="DOMAIN",
            副标题="设置主帅主城建筑等级",
            控件配置=[
                {"type": "dropdown", "config_key": "主帅主城_城市", "label": "城市:", "value": "17", "options": 等级选项, "width": 下拉框宽度},
                {"type": "dropdown", "config_key": "主帅主城_兵工", "label": "兵工:", "value": "17", "options": 等级选项, "width": 下拉框宽度},
                {"type": "dropdown", "config_key": "主帅主城_陆军", "label": "陆军:", "value": "14", "options": 等级选项, "width": 下拉框宽度},
                {"type": "dropdown", "config_key": "主帅主城_空军", "label": "空军:", "value": "03", "options": 等级选项, "width": 下拉框宽度},
                {"type": "dropdown", "config_key": "主帅主城_商业", "label": "商业:", "value": "04", "options": 等级选项, "width": 下拉框宽度},
                {"type": "dropdown", "config_key": "主帅主城_补给", "label": "补给:", "value": "03", "options": 等级选项, "width": 下拉框宽度},
                {"type": "dropdown", "config_key": "主帅主城_内塔", "label": "内塔:", "value": "04", "options": 等级选项, "width": 下拉框宽度},
                {"type": "dropdown", "config_key": "主帅主城_村庄", "label": "村庄:", "value": "03", "options": 等级选项, "width": 下拉框宽度},
                {"type": "dropdown", "config_key": "主帅主城_资源", "label": "资源:", "value": "03", "options": 等级选项, "width": 下拉框宽度},
                {"type": "dropdown", "config_key": "主帅主城_军工", "label": "军工:", "value": "03", "options": 等级选项, "width": 下拉框宽度},
                {"type": "dropdown", "config_key": "主帅主城_港口", "label": "港口:", "value": "03", "options": 等级选项, "width": 下拉框宽度},
                {"type": "dropdown", "config_key": "主帅主城_外塔", "label": "外塔:", "value": "03", "options": 等级选项, "width": 下拉框宽度},
            ],
            每行控件数=6,
        )
        
        创建卡片(
            卡片ID="vice_main_city",
            标题="付帅主城",
            图标="APARTMENT",
            副标题="设置付帅主城建筑等级",
            控件配置=[
                {"type": "dropdown", "config_key": "付帅主城_城市", "label": "城市:", "value": "15", "options": 等级选项, "width": 下拉框宽度},
                {"type": "dropdown", "config_key": "付帅主城_兵工", "label": "兵工:", "value": "10", "options": 等级选项, "width": 下拉框宽度},
                {"type": "dropdown", "config_key": "付帅主城_陆军", "label": "陆军:", "value": "10", "options": 等级选项, "width": 下拉框宽度},
                {"type": "dropdown", "config_key": "付帅主城_空军", "label": "空军:", "value": "03", "options": 等级选项, "width": 下拉框宽度},
                {"type": "dropdown", "config_key": "付帅主城_商业", "label": "商业:", "value": "04", "options": 等级选项, "width": 下拉框宽度},
                {"type": "dropdown", "config_key": "付帅主城_补给", "label": "补给:", "value": "03", "options": 等级选项, "width": 下拉框宽度},
                {"type": "dropdown", "config_key": "付帅主城_内塔", "label": "内塔:", "value": "03", "options": 等级选项, "width": 下拉框宽度},
                {"type": "dropdown", "config_key": "付帅主城_村庄", "label": "村庄:", "value": "03", "options": 等级选项, "width": 下拉框宽度},
                {"type": "dropdown", "config_key": "付帅主城_资源", "label": "资源:", "value": "03", "options": 等级选项, "width": 下拉框宽度},
                {"type": "dropdown", "config_key": "付帅主城_军工", "label": "军工:", "value": "03", "options": 等级选项, "width": 下拉框宽度},
                {"type": "dropdown", "config_key": "付帅主城_港口", "label": "港口:", "value": "03", "options": 等级选项, "width": 下拉框宽度},
                {"type": "dropdown", "config_key": "付帅主城_外塔", "label": "外塔:", "value": "03", "options": 等级选项, "width": 下拉框宽度},
            ],
            每行控件数=6,
        )
        
        创建卡片(
            卡片ID="sub_city",
            标题="所有分城",
            图标="LOCATION_CITY",
            副标题="设置所有分城建筑等级",
            控件配置=[
                {"type": "dropdown", "config_key": "所有分城_城市", "label": "城市:", "value": "15", "options": 等级选项, "width": 下拉框宽度},
                {"type": "dropdown", "config_key": "所有分城_兵工", "label": "兵工:", "value": "10", "options": 等级选项, "width": 下拉框宽度},
                {"type": "dropdown", "config_key": "所有分城_陆军", "label": "陆军:", "value": "10", "options": 等级选项, "width": 下拉框宽度},
                {"type": "dropdown", "config_key": "所有分城_空军", "label": "空军:", "value": "03", "options": 等级选项, "width": 下拉框宽度},
                {"type": "dropdown", "config_key": "所有分城_商业", "label": "商业:", "value": "04", "options": 等级选项, "width": 下拉框宽度},
                {"type": "dropdown", "config_key": "所有分城_补给", "label": "补给:", "value": "03", "options": 等级选项, "width": 下拉框宽度},
                {"type": "dropdown", "config_key": "所有分城_内塔", "label": "内塔:", "value": "03", "options": 等级选项, "width": 下拉框宽度},
                {"type": "dropdown", "config_key": "所有分城_村庄", "label": "村庄:", "value": "03", "options": 等级选项, "width": 下拉框宽度},
                {"type": "dropdown", "config_key": "所有分城_资源", "label": "资源:", "value": "03", "options": 等级选项, "width": 下拉框宽度},
                {"type": "dropdown", "config_key": "所有分城_军工", "label": "军工:", "value": "03", "options": 等级选项, "width": 下拉框宽度},
                {"type": "dropdown", "config_key": "所有分城_港口", "label": "港口:", "value": "03", "options": 等级选项, "width": 下拉框宽度},
                {"type": "dropdown", "config_key": "所有分城_外塔", "label": "外塔:", "value": "03", "options": 等级选项, "width": 下拉框宽度},
            ],
            每行控件数=6,
        )
        
        创建卡片(
            卡片ID="legion_city",
            标题="军团城市",
            图标="ACCOUNT_BALANCE",
            副标题="设置军团城市建筑等级",
            控件配置=[
                {"type": "dropdown", "config_key": "军团城市_城市", "label": "城市:", "value": "05", "options": 等级选项, "width": 下拉框宽度},
                {"type": "dropdown", "config_key": "军团城市_兵工", "label": "兵工:", "value": "05", "options": 等级选项, "width": 下拉框宽度},
                {"type": "dropdown", "config_key": "军团城市_军需", "label": "军需:", "value": "05", "options": 等级选项, "width": 下拉框宽度},
                {"type": "dropdown", "config_key": "军团城市_陆军", "label": "陆军:", "value": "00", "options": 等级选项_含0, "width": 下拉框宽度},
                {"type": "dropdown", "config_key": "军团城市_空军", "label": "空军:", "value": "00", "options": 等级选项_含0, "width": 下拉框宽度},
                {"type": "dropdown", "config_key": "军团城市_炮塔", "label": "炮塔:", "value": "00", "options": 等级选项_含0, "width": 下拉框宽度},
                {"type": "dropdown", "config_key": "军团城市_编号", "label": "编号:", "value": "01", "options": 等级选项, "width": 下拉框宽度},
            ],
            每行控件数=6,
        )
        
        创建卡片(
            卡片ID="priority",
            标题="建筑优先级",
            图标="HOME_WORK",
            副标题="按选择顺序建设建筑",
            控件配置=[
                {"type": "dropdown", "config_key": "资源建筑", "label": "资源:", "value": "自动平衡", "options": ["自动平衡", "钢铁优先", "橡胶优先", "石油优先"]},
                {"type": "dropdown", "config_key": "塔防建筑", "label": "塔防:", "value": "炮塔优先", "options": ["炮塔优先", "岸防优先"]},
            ],
            每行控件数=6,
        )
        
        标题栏 = ft.Row([
            ft.Icon(ft.Icons.DOMAIN, size=20, color=主题颜色.get("accent")),
            ft.Container(width=6),
            ft.Text("建筑设置", size=16, weight=ft.FontWeight.BOLD, color=主题颜色.get("text_primary")),
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
        
        return ft.Container(
            content=内容列,
            expand=True,
        )


# *** 调试逻辑 ***
if __name__ == "__main__":
    ft.run(lambda page: page.add(建筑界面.创建()))
