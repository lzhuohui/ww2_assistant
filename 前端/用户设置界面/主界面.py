import flet as ft
from typing import Callable

from 前端.用户设置界面.配置.界面配置 import 界面配置
from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider
from 前端.用户设置界面.界面模块.用户界面 import UserInfoCard
from 前端.用户设置界面.界面模块.导航界面 import NavBar
from 前端.用户设置界面.界面模块.系统界面 import SystemInterface
from 前端.用户设置界面.界面模块.策略界面 import StrategyInterface
from 前端.用户设置界面.界面模块.任务界面 import TaskInterface
from 前端.用户设置界面.界面模块.建筑界面 import BuildingInterface
from 前端.用户设置界面.界面模块.集资界面 import FundraisingInterface
from 前端.用户设置界面.界面模块.账号界面 import AccountInterface
from 前端.用户设置界面.界面模块.打扫界面 import CleaningInterface
from 前端.用户设置界面.界面模块.打野界面 import WildInterface
from 前端.用户设置界面.界面模块.个性化界面 import PersonalizationInterface
from 前端.用户设置界面.界面模块.关于界面 import AboutInterface
from 前端.用户设置界面.单元模块.文本标签 import LabelText


DEFAULT_WIDTH = 1200
DEFAULT_HEIGHT = 540
DEFAULT_SPACING = 10


class MainInterface:
    """主界面 - 页面层"""
    
    current_nav = "系统"
    content_area = None
    
    @staticmethod
    def setup_window(page: ft.Page) -> None:
        """
        设置主窗口属性
        
        参数:
            page: Flet页面对象
        """
        page.title = "用户设置"
        page.window.width = DEFAULT_WIDTH
        page.window.height = DEFAULT_HEIGHT
        page.window.resizable = False
        page.bgcolor = ThemeProvider.get_color("bg_primary")
        page.padding = 0
    
    @staticmethod
    def get_page_content(nav_name: str) -> ft.Control:
        """获取页面内容"""
        if nav_name == "系统":
            return SystemInterface.create()
        elif nav_name == "策略":
            return StrategyInterface.create()
        elif nav_name == "任务":
            return TaskInterface.create()
        elif nav_name == "建筑":
            return BuildingInterface.create()
        elif nav_name == "集资":
            return FundraisingInterface.create()
        elif nav_name == "账号":
            return AccountInterface.create()
        elif nav_name == "打扫":
            return CleaningInterface.create()
        elif nav_name == "打野":
            return WildInterface.create()
        elif nav_name == "个性化":
            return PersonalizationInterface.create()
        elif nav_name == "关于":
            return AboutInterface.create()
        else:
            return ft.Column(
                [
                    LabelText.create(
                        text=nav_name,
                        role="h1",
                        win11_style=True
                    ),
                    ft.Container(height=24),
                    LabelText.create(
                        text=f"{nav_name}页面开发中...",
                        role="body",
                        win11_style=True
                    ),
                ],
                spacing=0,
                expand=True,
            )
    
    @staticmethod
    def handle_nav_change(nav_name: str):
        """处理导航切换"""
        MainInterface.current_nav = nav_name
        if MainInterface.content_area:
            MainInterface.content_area.content = MainInterface.get_page_content(nav_name)
            try:
                MainInterface.content_area.update()
            except:
                pass
    
    @staticmethod
    def create() -> ft.Container:
        """
        创建主界面内容
        
        布局规则（按顺序实现）:
        1. 用户界面的左/上侧边缘和基准通用容器左/上侧边缘1个间距
        2. 导航界面上部边缘与用户界面下部边缘1个间距
        3. 导航界面左/右侧边缘与用户界面左/右侧边缘对应对齐
        4. 导航界面的下部边缘与和基准通用容器下部边缘1个间距
        5. 功能界面左侧边缘与用户界面右侧边缘一个间距
        6. 功能界面上侧边缘与用户界面上侧边缘对齐
        7. 功能界面下侧边缘与导航界面下侧边缘对齐
        8. 功能界面的右侧边缘和基准通用容器右侧边缘1个间距
        
        联动效果:
        - 改变用户界面宽/高 → 导航界面和功能界面自动联动调整
        
        返回:
            ft.Container: 主界面容器
        """
        bg_color = ThemeProvider.get_color("bg_primary")
        
        配置 = 界面配置()
        
        user_left = DEFAULT_SPACING
        user_top = DEFAULT_SPACING
        
        user_interface = UserInfoCard.create()
        user_interface.left = user_left
        user_interface.top = user_top
        
        user_width = user_interface.width
        user_height = user_interface.height
        user_right = user_left + user_width
        user_bottom = user_top + user_height
        
        nav_top = user_bottom + DEFAULT_SPACING
        nav_left = user_left
        nav_width = user_width
        nav_bottom = DEFAULT_SPACING
        
        content_left = user_right + DEFAULT_SPACING
        content_top = user_top
        content_bottom = DEFAULT_SPACING
        content_right = DEFAULT_SPACING
        
        nav_interface = NavBar.create(
            width=nav_width,
            on_select=lambda idx, names=["系统", "策略", "任务", "建筑", "集资", "账号", "打扫", "打野", "个性化", "关于"]: MainInterface.handle_nav_change(names[idx]),
        )
        nav_interface.left = nav_left
        nav_interface.top = nav_top
        nav_interface.bottom = nav_bottom
        
        content_container = ft.Container(
            content=MainInterface.get_page_content(MainInterface.current_nav),
            left=content_left,
            top=content_top,
            right=content_right,
            bottom=content_bottom,
        )
        MainInterface.content_area = content_container
        
        layout_stack = ft.Stack(
            controls=[
                user_interface,
                nav_interface,
                content_container,
            ],
            expand=True,
        )
        
        base_container = ft.Container(
            content=layout_stack,
            expand=True,
        )
        
        return ft.Container(
            content=base_container,
            bgcolor=bg_color,
            expand=True,
            padding=DEFAULT_SPACING,
        )


if __name__ == "__main__":
    配置 = 界面配置()
    ThemeProvider.initialize(配置)
    def main(page: ft.Page):
        MainInterface.setup_window(page)
        page.add(MainInterface.create())
    ft.run(main)