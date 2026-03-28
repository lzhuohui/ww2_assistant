# -*- coding: utf-8 -*-
"""
模块名称：AccountConfigSection
模块功能：账号配置区，管理多个游戏账号
实现步骤：
- 创建账号卡片列表
- 支持账号的增删改查
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
    from 表示层.组件.基础.输入框 import InputBox
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
    from 表示层.组件.基础.输入框 import InputBox
    from 业务层.服务.配置服务 import ConfigService
    from 核心层.常量.共享选项 import get_options_for_control


# *** 用户指定变量: 变量值必须生效,AI不得更改数据 ***
USER_MAX_ACCOUNTS = 15  # 最大账号数量
USER_DROPDOWN_WIDTH = 68  # 下拉框宽度
USER_INPUT_WIDTH = 166  # 输入框宽度
USER_SCHEME_WIDTH = 100  # 配置方案下拉框宽度
USER_AUTHORIZED_COUNT = 15  # 授权账号数量
# *********************************


class AccountConfigSection:
    """账号配置区"""
    
    @staticmethod
    def create(
        config: UIConfig = None,
        config_service: ConfigService = None,
        save_callback: Optional[Callable[[str, str, str], None]] = None,
        on_count_change: Optional[Callable[[int], None]] = None,
    ) -> tuple:
        """创建账号配置区
        
        Args:
            config: 界面配置
            config_service: 配置服务
            save_callback: 保存回调函数
            on_count_change: 账号数量变化回调
            
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
        
        # 统计启用的账号数量
        enabled_count = [0]
        
        # ========== 创建账号卡片 ==========
        for i in range(1, USER_MAX_ACCOUNTS + 1):
            card_id = f"account_{i}"
            
            # 获取保存的配置
            saved_enabled = config_service.get_value(card_id, "启用") == "true"
            saved_type = config_service.get_value(card_id, "类型") or "主帅"
            saved_platform = config_service.get_value(card_id, "平台") or "安卓"
            saved_name = config_service.get_value(card_id, "名称") or f"统帅{i}"
            saved_account = config_service.get_value(card_id, "账号") or ""
            saved_password = config_service.get_value(card_id, "密码") or ""
            saved_scheme = config_service.get_value(card_id, "配置方案") or "默认配置"
            
            # 更新启用计数
            if saved_enabled:
                enabled_count[0] += 1
            
            # 创建卡片
            def create_account_card(card_id: str, saved_enabled: bool, saved_type: str, 
                                   saved_platform: str, saved_name: str, saved_account: str,
                                   saved_password: str, saved_scheme: str) -> ft.Control:
                """创建单个账号卡片"""
                
                # 获取选项
                scheme_options = get_options_for_control("配置方案")
                
                # 创建控件
                type_dropdown = create_dropdown(
                    options=get_options_for_control("统帅1"),  # 主帅/副帅
                    current_value=saved_type,
                    width=USER_DROPDOWN_WIDTH,
                    enabled=True,
                    config=config,
                    on_change=lambda v: handle_save(card_id, "类型", v),
                )
                
                platform_dropdown = create_dropdown(
                    options=get_options_for_control("控制22"),  # 平台选项
                    current_value=saved_platform,
                    width=USER_DROPDOWN_WIDTH,
                    enabled=True,
                    config=config,
                    on_change=lambda v: handle_save(card_id, "平台", v),
                )
                
                name_input = InputBox.create(
                    config=config,
                    hint_text="输入统帅名称",
                    width=USER_INPUT_WIDTH,
                    enabled=True,
                    on_change=lambda v: handle_save(card_id, "名称", v),
                )
                name_input.set_value(saved_name)
                
                account_input = InputBox.create(
                    config=config,
                    hint_text="输入游戏账号",
                    width=USER_INPUT_WIDTH,
                    enabled=True,
                    on_change=lambda v: handle_save(card_id, "账号", v),
                )
                account_input.set_value(saved_account)
                
                password_input = InputBox.create(
                    config=config,
                    hint_text="输入游戏密码",
                    width=USER_INPUT_WIDTH,
                    enabled=True,
                    is_password=True,
                    on_change=lambda v: handle_save(card_id, "密码", v),
                )
                password_input.set_value(saved_password)
                
                scheme_display = saved_scheme if saved_scheme in scheme_options else "默认配置"
                scheme_dropdown = create_dropdown(
                    options=scheme_options,
                    current_value=scheme_display,
                    width=USER_SCHEME_WIDTH,
                    enabled=True,
                    config=config,
                    on_change=lambda v: handle_save(card_id, "配置方案", v),
                )
                
                # 创建卡片
                card = create_managed_card(
                    card_id=card_id,
                    title=f"账号 {card_id.split('_')[1]}",
                    icon="person",
                    subtitle="配置游戏账号信息",
                    controls=[
                        ft.Row([
                            ft.Column([
                                ft.Text("类型", size=12, color=theme_colors.get("text_secondary")),
                                type_dropdown,
                            ], spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            ft.Column([
                                ft.Text("平台", size=12, color=theme_colors.get("text_secondary")),
                                platform_dropdown,
                            ], spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            ft.Column([
                                ft.Text("名称", size=12, color=theme_colors.get("text_secondary")),
                                name_input,
                            ], spacing=2),
                        ], spacing=10, alignment=ft.MainAxisAlignment.START),
                        ft.Row([
                            ft.Column([
                                ft.Text("账号", size=12, color=theme_colors.get("text_secondary")),
                                account_input,
                            ], spacing=2),
                            ft.Column([
                                ft.Text("密码", size=12, color=theme_colors.get("text_secondary")),
                                password_input,
                            ], spacing=2),
                        ], spacing=10, alignment=ft.MainAxisAlignment.START),
                        ft.Row([
                            ft.Column([
                                ft.Text("配置方案", size=12, color=theme_colors.get("text_secondary")),
                                scheme_dropdown,
                            ], spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        ], spacing=10, alignment=ft.MainAxisAlignment.START),
                    ],
                    config=config,
                    config_service=config_service,
                    save_callback=save_callback,
                    manager=manager,
                    initially_enabled=saved_enabled,
                )
                
                return card
            
            # 创建并添加卡片
            card = create_account_card(card_id, saved_enabled, saved_type, saved_platform,
                                      saved_name, saved_account, saved_password, saved_scheme)
            card_list.append(card)
        
        # ========== 回调函数 ==========
        def handle_save(card_id: str, config_key: str, value: str):
            """处理保存"""
            config_service.set_value(card_id, config_key, value)
            if save_callback:
                save_callback(card_id, config_key, value)
            
            # 如果是启用状态变化，更新计数
            if config_key == "启用":
                if value == "true":
                    enabled_count[0] += 1
                else:
                    enabled_count[0] -= 1
                
                if on_count_change:
                    on_count_change(enabled_count[0])
            
            print(f"[账号配置] {card_id}.{config_key} = {value}")
        
        # ========== 组装主容器 ==========
        title = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon("people", size=24, color=theme_colors.get("accent")),
                    ft.Text("账号配置", size=20, weight=ft.FontWeight.BOLD),
                ], spacing=10),
                ft.Text(f"管理最多 {USER_MAX_ACCOUNTS} 个游戏账号，当前已启用 {enabled_count[0]} 个", 
                       size=14, color=theme_colors.get("text_secondary")),
                ft.Divider(height=20),
            ], spacing=5),
            padding=ft.padding.only(bottom=10),
        )
        
        main_container = ft.Column([
            title,
            *card_list,
        ], spacing=10)
        
        # 添加销毁方法
        def destroy_controls():
            """销毁所有控件的选项列表"""
            manager.destroy_controls()
        
        main_container.destroy_controls = destroy_controls
        
        return main_container, manager


# ========== 测试函数 ==========
def test_account_config():
    """测试账号配置区"""
    
    def save_callback(card_id: str, config_key: str, value: str):
        """保存回调测试"""
        print(f"[测试] 保存: {card_id}.{config_key} = {value}")
    
    def count_change_callback(count: int):
        """账号数量变化回调测试"""
        print(f"[测试] 启用账号数量: {count}")
    
    def main(page: ft.Page):
        page.title = "账号配置区测试"
        page.window_width = 800
        page.window_height = 600
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 20
        
        # 创建配置
        config = UIConfig()
        
        # 创建配置服务
        config_service = ConfigService()
        
        # 创建账号配置区
        account_section, manager = AccountConfigSection.create(
            config=config,
            config_service=config_service,
            save_callback=save_callback,
            on_count_change=count_change_callback,
        )
        
        # 主布局
        page.add(
            ft.Column([
                ft.Text("✅ 账号配置区测试", size=24, weight=ft.FontWeight.BOLD),
                ft.Text("使用新的下拉框系统", size=14, color="#666666"),
                ft.Divider(height=20),
                account_section,
            ], spacing=15, scroll=ft.ScrollMode.AUTO)
        )
    
    ft.app(target=main)


if __name__ == "__main__":
    test_account_config()