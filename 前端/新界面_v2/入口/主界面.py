# -*- coding: utf-8 -*-
"""
模块名称：主界面
设计思路: 应用入口，组装各层模块
模块隔离: 入口层依赖所有层，不被任何层依赖
"""

import flet as ft
from typing import Dict, Any, Callable, Optional

from 前端.新界面_v2.核心.配置.界面配置 import 界面配置
from 前端.新界面_v2.核心.常量.全局常量 import 全局常量
from 前端.新界面_v2.业务层.服务.配置服务 import 配置服务
from 前端.新界面_v2.业务层.事件.事件总线 import 事件总线
from 前端.新界面_v2.表示层.界面.系统界面 import 系统界面
from 前端.新界面_v2.表示层.界面.策略界面 import 策略界面
from 前端.新界面_v2.表示层.界面.任务界面 import 任务界面
from 前端.新界面_v2.表示层.界面.建筑界面 import 建筑界面
from 前端.新界面_v2.表示层.界面.集资界面 import 集资界面
from 前端.新界面_v2.表示层.界面.账号界面 import 账号界面
from 前端.新界面_v2.表示层.界面.打扫界面 import 打扫界面
from 前端.新界面_v2.表示层.界面.打野界面 import 打野界面
from 前端.新界面_v2.表示层.界面.个性化界面 import 个性化界面
from 前端.新界面_v2.表示层.界面.关于界面 import 关于界面
from 前端.新界面_v2.表示层.组件.基础.卡片容器 import 卡片容器, USER_PADDING, USER_HEIGHT
from 前端.新界面_v2.表示层.组件.复合.用户信息卡片 import 用户信息卡片
from 前端.新界面_v2.表示层.组件.复合.导航按钮 import 导航按钮


# *** 用户指定变量 - AI不得修改 ***
USER_WINDOW_WIDTH = 1200
USER_WINDOW_HEIGHT = 540
USER_NAV_WIDTH = 280
USER_SPACING = 10
# *********************************


class 主界面:
    """主界面 - 应用入口"""
    
    当前导航 = "系统"
    内容区域 = None
    配置服务实例: Optional[配置服务] = None
    事件总线实例: Optional[事件总线] = None
    
    @staticmethod
    def 设置窗口(页面: ft.Page, 配置: 界面配置=None) -> None:
        if 配置 is None:
            配置 = 界面配置()
        
        主题颜色 = 配置.当前主题颜色
        
        页面.title = 全局常量.APP_NAME
        页面.window.width = USER_WINDOW_WIDTH
        页面.window.height = USER_WINDOW_HEIGHT
        页面.window.resizable = False
        页面.bgcolor = 主题颜色.get("bg_primary")
        页面.padding = 0
    
    @staticmethod
    def 获取页面内容(导航名称: str, 配置: 界面配置, 配置服务实例: 配置服务) -> ft.Control:
        """获取页面内容"""
        主题颜色 = 配置.当前主题颜色
        
        def 保存回调(卡片ID: str, 配置键: str, 值: str):
            配置服务实例.设置值(导航名称, 卡片ID, 配置键, 值)
        
        if 导航名称 == "系统":
            return 系统界面.创建(配置=配置, 保存回调=保存回调)
        elif 导航名称 == "策略":
            return 策略界面.创建(配置=配置, 保存回调=保存回调)
        elif 导航名称 == "任务":
            return 任务界面.创建(配置=配置, 保存回调=保存回调)
        elif 导航名称 == "建筑":
            return 建筑界面.创建(配置=配置, 保存回调=保存回调)
        elif 导航名称 == "集资":
            return 集资界面.创建(配置=配置, 保存回调=保存回调)
        elif 导航名称 == "账号":
            return 账号界面.创建(配置=配置, 保存回调=保存回调)
        elif 导航名称 == "打扫":
            return 打扫界面.创建(配置=配置, 保存回调=保存回调)
        elif 导航名称 == "打野":
            return 打野界面.创建(配置=配置, 保存回调=保存回调)
        elif 导航名称 == "个性化":
            return 个性化界面.创建(配置=配置, 保存回调=保存回调)
        elif 导航名称 == "关于":
            return 关于界面.创建(配置=配置, 保存回调=保存回调)
        else:
            return ft.Column([
                ft.Text(导航名称, size=20, weight=ft.FontWeight.BOLD, color=主题颜色.get("text_primary")),
                ft.Container(height=24),
                ft.Text(f"{导航名称}页面开发中...", size=14, color=主题颜色.get("text_secondary")),
            ], spacing=0, expand=True)
    
    @staticmethod
    def 处理功能点击(功能ID: str, 配置: 界面配置, 配置服务实例: 配置服务, 容器: ft.Container):
        """处理功能按钮点击"""
        主题颜色 = 配置.当前主题颜色
        页面 = 容器.page if 容器 else None
        
        if 功能ID == "导出配置":
            try:
                文件路径 = 配置服务实例.保存游戏配置()
                提示 = ft.SnackBar(
                    content=ft.Text(f"配置已导出: {文件路径}", color=主题颜色.get("text_primary")),
                    bgcolor=主题颜色.get("success"),
                )
                if 页面:
                    页面.snack_bar = 提示
                    提示.open = True
                    页面.update()
            except Exception as 异常:
                提示 = ft.SnackBar(
                    content=ft.Text(f"导出失败: {str(异常)}", color=主题颜色.get("text_primary")),
                    bgcolor=主题颜色.get("error"),
                )
                if 页面:
                    页面.snack_bar = 提示
                    提示.open = True
                    页面.update()
        elif 功能ID == "恢复默认":
            pass
        elif 功能ID == "配置方案":
            pass
    
    @staticmethod
    def 创建(
        配置: 界面配置=None,
    ) -> ft.Container:
        if 配置 is None:
            配置 = 界面配置()
        
        主题颜色 = 配置.当前主题颜色
        
        主界面.配置服务实例 = 配置服务()
        主界面.事件总线实例 = 事件总线()
        
        导航项列表 = 全局常量.NAV_ITEMS
        
        导航按钮列表 = []
        当前选中 = [0]
        
        def 处理导航点击(索引: int):
            当前选中[0] = 索引
            导航名称 = 导航项列表[索引]["id"]
            主界面.当前导航 = 导航名称
            
            for i, 按钮 in enumerate(导航按钮列表):
                导航按钮.更新选中状态(按钮, i == 索引, 配置)
            
            if 主界面.内容区域:
                内容 = 主界面.获取页面内容(导航名称, 配置, 主界面.配置服务实例)
                主界面.内容区域.content = 内容
                
                try:
                    主界面.内容区域.update()
                except Exception as e:
                    print(f"更新内容区域失败: {e}")
            
            主界面.事件总线实例.发布界面切换(导航名称)
        
        for i, 项 in enumerate(导航项列表):
            按钮 = 导航按钮.创建(
                配置=配置,
                项=项,
                索引=i,
                当前选中=当前选中,
                处理导航点击=处理导航点击,
                选中状态=(i == 0),
                自适应高度=True,
            )
            导航按钮列表.append(按钮)
        
        用户信息 = 用户信息卡片.创建(配置=配置)
        
        功能项列表 = [
            {"id": "导出配置", "icon": "SAVE"},
        ]
        
        功能按钮列表 = []
        for 功能项 in 功能项列表:
            def 创建功能点击回调(fid=功能项.get("id")):
                def 回调(idx):
                    主界面.处理功能点击(fid, 配置, 主界面.配置服务实例, 容器)
                return 回调
            
            按钮 = 导航按钮.创建(
                配置=配置,
                项=功能项,
                索引=-1,
                处理导航点击=创建功能点击回调(),
                选中状态=False,
                自适应高度=True,
            )
            功能按钮列表.append(按钮)
        
        所有按钮列表 = 导航按钮列表 + 功能按钮列表
        
        导航列 = ft.Column(
            controls=所有按钮列表,
            spacing=USER_SPACING // 4,
            expand=True,
        )
        
        导航面板 = ft.Container(
            content=ft.Column([
                用户信息,
                ft.Container(height=USER_SPACING),
                导航列,
            ], spacing=0),
            width=USER_NAV_WIDTH,
            padding=ft.Padding(
                left=USER_SPACING,
                top=USER_SPACING,
                right=USER_SPACING * 2,
                bottom=USER_SPACING,
            ),
            bgcolor=主题颜色.get("bg_primary"),
        )
        
        右侧内容 = 主界面.获取页面内容(主界面.当前导航, 配置, 主界面.配置服务实例)
        
        内容列 = ft.Column(
            controls=[右侧内容],
            spacing=0,
            expand=True,
        )
        
        内容容器 = ft.Container(
            content=内容列,
            padding=ft.Padding(
                left=USER_SPACING * 2,
                top=USER_SPACING + USER_PADDING,
                right=USER_SPACING,
                bottom=USER_SPACING * 2,
            ),
            expand=True,
        )
        
        主界面.内容区域 = 内容容器
        
        主行 = ft.Row([
            导航面板,
            ft.VerticalDivider(width=1, color=主题颜色.get("border")),
            内容容器,
        ], expand=True, spacing=0)
        
        容器 = ft.Container(
            content=主行,
            bgcolor=主题颜色.get("bg_primary"),
            expand=True,
        )
        
        def 处理挂载(e):
            if 容器.page:
                主界面.设置窗口(容器.page, 配置)
        
        容器.on_mount = 处理挂载
        
        return 容器
    
    @staticmethod
    def 获取游戏配置() -> Dict[str, Any]:
        """获取游戏控制配置（供外部调用）"""
        if 主界面.配置服务实例:
            return 主界面.配置服务实例.导出游戏配置()
        return {}
    
    @staticmethod
    def 保存游戏配置() -> str:
        """保存游戏控制配置（供外部调用）"""
        if 主界面.配置服务实例:
            return 主界面.配置服务实例.保存游戏配置()
        return ""


# *** 调试逻辑 ***
if __name__ == "__main__":
    ft.run(lambda page: page.add(主界面.创建()))
