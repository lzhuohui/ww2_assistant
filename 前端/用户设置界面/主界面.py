import flet as ft
from typing import Callable

from 前端.配置.界面配置 import 界面配置
from 前端.用户设置界面.核心接口.主题提供者 import ThemeProvider
from 前端.用户设置界面.界面模块.用户界面 import UserInfoCard
from 前端.用户设置界面.界面模块.导航界面 import NavBar
from 前端.用户设置界面.界面模块.功能通用界面 import ContentArea
from 前端.用户设置界面.界面模块.系统界面 import SystemInterface
from 前端.用户设置界面.界面模块.策略界面 import StrategyInterface
from 前端.用户设置界面.界面模块.任务界面 import TaskInterface
from 前端.用户设置界面.界面模块.建筑界面 import BuildingInterface
from 前端.用户设置界面.界面模块.集资界面 import FundraisingInterface
from 前端.用户设置界面.界面模块.账号界面 import AccountInterface


# *** 用户指定变量 - AI不得修改 ***
DEFAULT_WIDTH = 1200
DEFAULT_HEIGHT = 540
DEFAULT_SPACING = 5  # 主窗口周边与各界面之间的间距
# *********************************


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
        page.window.height = DEFAULT_HEIGHT  # 直接使用内容区域高度
        page.window.resizable = False
        page.bgcolor = ThemeProvider.get_color("bg_primary")
        page.padding = 0  # 不使用page.padding，由Stack布局自己管理间距
    
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
        else:
            return ft.Column(
                [
                    ft.Text(
                        nav_name,
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color=ThemeProvider.get_color("text_primary"),
                    ),
                    ft.Container(height=24),
                    ft.Text(
                        f"{nav_name}页面开发中...",
                        size=14,
                        color=ThemeProvider.get_color("text_secondary"),
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
        
        # ========== 第1步：用户界面定位 ==========
        # 用户界面的左/上侧边缘和基准通用容器左/上侧边缘1个间距
        # 用户界面自己管理尺寸，主界面只负责定位
        user_left = DEFAULT_SPACING
        user_top = DEFAULT_SPACING
        
        # ========== 创建用户界面（不覆盖被调模块数据） ==========
        user_interface = UserInfoCard.create()
        user_interface.left = user_left
        user_interface.top = user_top
        
        # 获取用户界面实际尺寸（用于其他组件定位参考）
        user_width = user_interface.width
        user_height = user_interface.height
        user_right = user_left + user_width
        user_bottom = user_top + user_height
        
        # ========== 第2步：导航界面上边缘定位 ==========
        # 导航界面上部边缘与用户界面下部边缘1个间距
        nav_top = user_bottom + DEFAULT_SPACING
        
        # ========== 第3步：导航界面左/右边缘定位 ==========
        # 导航界面左/右侧边缘与用户界面左/右侧边缘对应对齐
        nav_left = user_left
        nav_width = user_width  # 与用户界面同宽
        
        # ========== 第4步：导航界面下边缘定位 ==========
        # 导航界面的下部边缘与和基准通用容器下部边缘1个间距
        nav_bottom = DEFAULT_SPACING
        
        # ========== 第5步：功能界面左边缘定位 ==========
        # 功能界面左侧边缘与用户界面右侧边缘一个间距
        content_left = user_right + DEFAULT_SPACING
        
        # ========== 第6步：功能界面上边缘定位 ==========
        # 功能界面上侧边缘与用户界面上侧边缘对齐
        content_top = user_top
        
        # ========== 第7步：功能界面下边缘定位 ==========
        # 功能界面下侧边缘与导航界面下侧边缘对齐
        content_bottom = DEFAULT_SPACING
        
        # ========== 第8步：功能界面右边缘定位 ==========
        # 功能界面的右侧边缘和基准通用容器右侧边缘1个间距
        content_right = DEFAULT_SPACING
        
        # ========== 创建导航界面 ==========
        nav_interface = NavBar.create(
            width=nav_width,
            on_select=lambda idx, names=["系统", "策略", "任务", "建筑", "集资", "账号", "打扫", "打野", "个性化", "关于"]: MainInterface.handle_nav_change(names[idx]),
        )
        nav_interface.left = nav_left
        nav_interface.top = nav_top
        nav_interface.bottom = nav_bottom
        
        # ========== 创建功能界面容器 ==========
        # 直接创建一个容器来容纳功能页面内容，不使用ContentArea的通用容器
        content_container = ft.Container(
            content=MainInterface.get_page_content(MainInterface.current_nav),
            left=content_left,
            top=content_top,
            right=content_right,
            bottom=content_bottom,
            width=None,  # 必须清除默认宽度，以实现自适应
            height=None,  # 必须清除默认高度，以实现自适应
            expand=True,
        )
        MainInterface.content_area = content_container
        
        # ========== 使用 Stack 进行绝对定位 ==========
        layout_stack = ft.Stack(
            controls=[
                user_interface,
                nav_interface,
                content_container,
            ],
            expand=True,
        )
        
        # 基准容器：自适应主窗口
        base_container = ft.Container(
            content=layout_stack,
            expand=True,
        )
        
        # 返回主界面容器：填充整个页面
        return ft.Container(
            content=base_container,
            bgcolor=bg_color,
            expand=True,
            padding=DEFAULT_SPACING,  # 主窗口周边间距
        )


# *** 调试逻辑 ***
if __name__ == "__main__":
    配置 = 界面配置()
    ThemeProvider.initialize(配置)
    def main(page: ft.Page):
        MainInterface.setup_window(page)
        page.add(MainInterface.create())
    ft.run(main)
