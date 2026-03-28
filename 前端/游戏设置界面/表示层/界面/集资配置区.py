# -*- coding: utf-8 -*-
"""
模块名称：FundingConfigSection
模块功能：集资配置区，包含小号上贡、分城纳租配置
实现步骤：
- 创建小号上贡配置卡片
- 创建分城纳租配置卡片
- 使用CardGroupManager管理卡片状态
- 支持配置保存和加载
"""

from typing import Callable, List, Optional
import flet as ft

# 导入项目模块
try:
    from 核心层.配置.界面配置 import UIConfig
    from 表示层.组件.复合.卡片组管理器 import CardGroupManager, create_managed_card
    from 表示层.组件.基础.下拉框 import create_dropdown
    from 业务层.服务.配置服务 import ConfigService
    from 核心层.常量.共享选项 import get_options_for_control
except ImportError:
    # 备用导入路径（用于测试）
    import sys
    import os
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    sys.path.insert(0, project_root)
    
    from 核心层.配置.界面配置 import UIConfig
    from 表示层.组件.复合.卡片组管理器 import CardGroupManager, create_managed_card
    from 表示层.组件.基础.下拉框 import create_dropdown
    from 业务层.服务.配置服务 import ConfigService
    from 核心层.常量.共享选项 import get_options_for_control


# *** 用户指定变量: 变量值必须生效,AI不得更改数据 ***
USER_CARD_SPACING = 10  # 卡片间距
USER_DROPDOWN_WIDTH = 120  # 下拉框宽度
USER_PLACEHOLDER = "请选统帅"  # 统帅选择占位符
# *********************************


class FundingConfigSection:
    """集资配置区"""
    
    @staticmethod
    def create(
        config: UIConfig = None,
        config_service: ConfigService = None,
        save_callback: Optional[Callable[[str, str, str], None]] = None,
    ) -> tuple:
        """创建集资配置区
        
        Args:
            config: 界面配置
            config_service: 配置服务
            save_callback: 保存回调函数
            
        Returns:
            (配置区容器, 管理器)
        """
        if config is None:
            config = UIConfig()
        if config_service is None:
            config_service = ConfigService()
        
        theme_colors = config.当前主题颜色
        
        manager = CardGroupManager()
        card_list: List[ft.Control] = []
        
        # ========== 小号上贡配置卡片 ==========
        def create_tribute_card() -> ft.Control:
            """创建小号上贡配置卡片"""
            card_id = "tribute_card"
            
            # 获取保存的配置
            saved_level = config_service.get_value(card_id, "上贡等级") or "1"
            saved_amount = config_service.get_value(card_id, "上贡限量") or "2"
            
            # 获取选项
            level_options = get_options_for_control("控制1")  # 1-10级
            amount_options = get_options_for_control("控制2")  # 1-10个
            
            # 创建下拉框
            level_dropdown = create_dropdown(
                options=level_options,
                current_value=saved_level,
                width=USER_DROPDOWN_WIDTH,
                enabled=True,
                config=config,
                on_change=lambda v: handle_value_change(card_id, "上贡等级", v),
            )
            
            amount_dropdown = create_dropdown(
                options=amount_options,
                current_value=saved_amount,
                width=USER_DROPDOWN_WIDTH,
                enabled=True,
                config=config,
                on_change=lambda v: handle_value_change(card_id, "上贡限量", v),
            )
            
            # 创建卡片
            card = create_managed_card(
                card_id=card_id,
                title="小号上贡",
                icon="account_balance",
                subtitle="配置小号上贡等级和数量",
                controls=[
                    ft.Row([
                        ft.Column([
                            ft.Text("上贡等级", size=12, color=theme_colors.get("text_secondary")),
                            level_dropdown,
                        ], spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        ft.Column([
                            ft.Text("上贡限量", size=12, color=theme_colors.get("text_secondary")),
                            amount_dropdown,
                        ], spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    ], spacing=20, alignment=ft.MainAxisAlignment.CENTER),
                ],
                config=config,
                config_service=config_service,
                save_callback=save_callback,
                manager=manager,
            )
            
            return card
        
        # ========== 分城纳租配置卡片 ==========
        def create_rent_card() -> ft.Control:
            """创建分城纳租配置卡片"""
            card_id = "rent_card"
            
            # 获取保存的配置
            saved_primary = config_service.get_value(card_id, "主统帅") or ""
            saved_secondary = config_service.get_value(card_id, "副统帅") or ""
            
            # 获取统帅选项
            commander_options = get_options_for_control("统帅1")  # 统帅列表
            
            # 创建下拉框
            primary_display = saved_primary if saved_primary in commander_options else (commander_options[0] if commander_options else USER_PLACEHOLDER)
            primary_options = commander_options if commander_options else [USER_PLACEHOLDER]
            
            primary_dropdown = create_dropdown(
                options=primary_options,
                current_value=primary_display,
                width=USER_DROPDOWN_WIDTH,
                enabled=True,
                config=config,
                on_change=lambda v: handle_value_change(card_id, "主统帅", v),
            )
            
            secondary_display = saved_secondary if saved_secondary in commander_options else USER_PLACEHOLDER
            secondary_initial_options = commander_options if commander_options else [USER_PLACEHOLDER]
            
            secondary_dropdown = create_dropdown(
                options=secondary_initial_options,
                current_value=secondary_display,
                width=USER_DROPDOWN_WIDTH,
                enabled=True,
                config=config,
                on_change=lambda v: handle_value_change(card_id, "副统帅", v),
            )
            
            # 创建卡片
            card = create_managed_card(
                card_id=card_id,
                title="分城纳租",
                icon="home_work",
                subtitle="配置分城纳租的主副统帅",
                controls=[
                    ft.Row([
                        ft.Column([
                            ft.Text("主统帅", size=12, color=theme_colors.get("text_secondary")),
                            primary_dropdown,
                        ], spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        ft.Column([
                            ft.Text("副统帅", size=12, color=theme_colors.get("text_secondary")),
                            secondary_dropdown,
                        ], spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    ], spacing=20, alignment=ft.MainAxisAlignment.CENTER),
                ],
                config=config,
                config_service=config_service,
                save_callback=save_callback,
                manager=manager,
            )
            
            return card
        
        # ========== 回调函数 ==========
        def handle_value_change(card_id: str, config_key: str, value: str):
            """处理值变化"""
            config_service.set_value(card_id, config_key, value)
            if save_callback:
                save_callback(card_id, config_key, value)
            print(f"[集资配置] {card_id}.{config_key} = {value}")
        
        # ========== 创建卡片 ==========
        tribute_card = create_tribute_card()
        rent_card = create_rent_card()
        
        card_list.append(tribute_card)
        card_list.append(rent_card)
        
        # ========== 组装主容器 ==========
        title = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon("account_balance_wallet", size=24, color=theme_colors.get("accent")),
                    ft.Text("集资配置", size=20, weight=ft.FontWeight.BOLD),
                ], spacing=10),
                ft.Text("配置小号上贡和分城纳租的相关参数", 
                       size=14, color=theme_colors.get("text_secondary")),
                ft.Divider(height=20),
            ], spacing=5),
            padding=ft.padding.only(bottom=10),
        )
        
        main_container = ft.Column([
            title,
            *card_list,
        ], spacing=USER_CARD_SPACING)
        
        # 添加销毁方法
        def destroy_controls():
            """销毁所有控件的选项列表"""
            manager.destroy_controls()
        
        main_container.destroy_controls = destroy_controls
        
        return main_container, manager


# ========== 测试函数 ==========
def test_funding_config():
    """测试集资配置区"""
    
    def save_callback(card_id: str, config_key: str, value: str):
        """保存回调测试"""
        print(f"[测试] 保存: {card_id}.{config_key} = {value}")
    
    def main(page: ft.Page):
        page.title = "集资配置区测试"
        page.window_width = 600
        page.window_height = 500
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 20
        
        # 创建配置
        config = UIConfig()
        
        # 创建配置服务
        config_service = ConfigService()
        
        # 创建集资配置区
        funding_section, manager = FundingConfigSection.create(
            config=config,
            config_service=config_service,
            save_callback=save_callback,
        )
        
        # 主布局
        page.add(
            ft.Column([
                ft.Text("✅ 集资配置区测试", size=24, weight=ft.FontWeight.BOLD),
                ft.Text("使用新的下拉框系统", size=14, color="#666666"),
                ft.Divider(height=20),
                funding_section,
            ], spacing=15, scroll=ft.ScrollMode.AUTO)
        )
    
    ft.app(target=main)


if __name__ == "__main__":
    test_funding_config()