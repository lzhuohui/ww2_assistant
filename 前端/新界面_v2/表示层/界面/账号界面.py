# -*- coding: utf-8 -*-
"""
模块名称：AccountPage
设计思路: 账号配置界面，使用折叠卡片和输入框组件
模块隔离: 界面层依赖组件层和业务层

功能设计:
    1. 显示15个账号卡片
    2. 开关控制参与挂机状态
    3. 开关状态不影响控件操作
    4. 计数机制：开关打开且输入有效时计数+1
    5. 授权限制：超过授权数量禁止打开开关
    6. 输入验证：名称/账号/密码都不为空时才有效
    7. 计数显示：页面顶部显示"已启用: X/Y"

副标题逻辑:
    - 开关关闭: "未参与挂机"
    - 开关打开但信息不完整: "请填写完整的账号信息"
    - 开关打开且信息完整: "参与挂机"

折叠卡片副标题设计规范:
    采用动态副标题方案，折叠/展开显示不同内容:
    
    | 状态 | 折叠时副标题 | 展开时副标题 |
    |------|-------------|-------------|
    | 开关关闭 | "未参与挂机" | "未参与挂机" |
    | 开关打开但信息不完整 | "请填写完整信息 >>" | "缺少: 名称/账号/密码" |
    | 开关打开且信息完整 | "参与挂机" | "已配置: {名称}" |
    
    设计依据:
    - 折叠状态: 显示状态摘要，快速了解配置状态
    - 展开状态: 显示详细信息，方便用户确认具体配置

实时更新流程:
    输入框输入 → on_change → handle_save → update_subtitle_and_count → 更新副标题 + 更新计数

依赖模块:
    - CollapsibleCard: 折叠卡片组件
    - Dropdown: 下拉框组件
    - InputBox: 输入框组件
    - UIConfig: 界面配置

对外接口:
    - create(config, save_callback): 创建账号界面
"""

import flet as ft
from typing import Dict, Any, List, Callable

from 前端.新界面_v2.核心.配置.界面配置 import UIConfig
from 前端.新界面_v2.表示层.组件.复合.折叠卡片 import CollapsibleCard
from 前端.新界面_v2.表示层.组件.基础.下拉框 import Dropdown, USER_WIDTH as DROPDOWN_WIDTH
from 前端.新界面_v2.表示层.组件.基础.输入框 import InputBox, USER_WIDTH as INPUT_WIDTH
from 前端.新界面_v2.核心.常量.全局常量 import USER_SPACING, USER_CARD_SPACING


# *** 用户指定变量: 变量值必须生效,AI不得更改数据 ***
USER_MAX_ACCOUNTS = 15        # 最大账号数量
USER_DROPDOWN_WIDTH = 70      # 下拉框宽度
USER_INPUT_WIDTH = 190        # 输入框宽度
USER_AUTHORIZED_COUNT = 15    # 授权账号数量
# *********************************


class AccountPage:
    """账号配置界面"""
    
    授权数量 = USER_AUTHORIZED_COUNT
    当前参与数量 = 0
    账号开关状态 = {}
    
    @staticmethod
    def create(
        config: UIConfig = None,
        save_callback: Callable[[str, str, str], None] = None,
    ) -> ft.Container:
        if config is None:
            config = UIConfig()
        
        theme_colors = config.当前主题颜色
        card_list: List[ft.Control] = []
        card_data: Dict[str, Dict[str, Any]] = {}
        card_refs: Dict[str, ft.Container] = {}
        
        AccountPage.授权数量 = USER_AUTHORIZED_COUNT
        AccountPage.当前参与数量 = 0
        AccountPage.账号开关状态 = {}
        
        # 从配置服务获取已保存的配置
        from 前端.新界面_v2.业务层.服务.配置服务 import ConfigService
        config_service = ConfigService()
        
        count_text = ft.Text(
            f"已启用: {AccountPage.当前参与数量}/{AccountPage.授权数量}",
            size=14,
            color=theme_colors.get("text_secondary"),
        )
        
        def get_subtitle(enabled: bool, name: str, account: str, password: str, is_expanded: bool = False) -> str:
            """获取副标题（支持折叠/展开不同内容）"""
            if not enabled:
                if is_expanded:
                    return "未参与挂机"
                else:
                    display_name = name if name else "未设置"
                    return f"{display_name} (未参与), 设置请进入 >>"
            
            if not name or not account or not password:
                if is_expanded:
                    missing = []
                    if not name:
                        missing.append("名称")
                    if not account:
                        missing.append("账号")
                    if not password:
                        missing.append("密码")
                    return f"缺少: {'/'.join(missing)}"
                else:
                    display_name = name if name else "未设置"
                    return f"{display_name} (信息不完整), 设置请进入 >>"
            
            if is_expanded:
                return f"已配置: {name}"
            else:
                return f"{name} (参与挂机), 设置请进入 >>"
        
        def can_participate(enabled: bool, name: str, account: str, password: str) -> bool:
            """判断是否可以参与挂机"""
            return enabled and bool(name) and bool(account) and bool(password)
        
        def update_subtitle_and_count(card_name: str, card: ft.Container, enabled: bool, name: str, account: str, password: str, is_expanded: bool = False) -> bool:
            """更新副标题和计数"""
            old_can = can_participate(
                AccountPage.账号开关状态.get(card_name, False),
                card_data.get(card_name, {}).get("名称", ""),
                card_data.get(card_name, {}).get("账号", ""),
                card_data.get(card_name, {}).get("密码", ""),
            )
            
            new_can = can_participate(enabled, name, account, password)
            
            if new_can and not old_can:
                if AccountPage.当前参与数量 >= AccountPage.授权数量:
                    return False
                AccountPage.当前参与数量 += 1
            elif not new_can and old_can:
                AccountPage.当前参与数量 -= 1
            
            AccountPage.账号开关状态[card_name] = enabled
            
            subtitle = get_subtitle(enabled, name, account, password, is_expanded)
            if card and hasattr(card, 'set_subtitle'):
                card.set_subtitle(subtitle, is_expanded)
            
            count_text.value = f"已启用: {AccountPage.当前参与数量}/{AccountPage.授权数量}"
            try:
                if count_text.page:
                    count_text.update()
            except:
                pass
            
            return True
        
        def handle_save(card_id: str, config_key: str, value: str):
            if card_id not in card_data:
                card_data[card_id] = {}
            card_data[card_id][config_key] = value
            if save_callback:
                save_callback(card_id, config_key, value)
            
            # 更新副标题和计数
            if card_id in card_refs:
                card = card_refs[card_id]
                current_enabled = AccountPage.账号开关状态.get(card_id, False)
                current_name = card_data.get(card_id, {}).get("名称", "")
                current_account = card_data.get(card_id, {}).get("账号", "")
                current_password = card_data.get(card_id, {}).get("密码", "")
                is_expanded = card.is_loaded() if hasattr(card, 'is_loaded') else False
                
                update_subtitle_and_count(card_id, card, current_enabled, current_name, current_account, current_password, is_expanded)
        
        def create_card(
            card_id: str,
            title: str,
            icon: str,
            default_type: str = "付帅",
            enabled: bool = False,
        ) -> ft.Container:
            # 加载已保存的配置值，如果没有则保存默认值
            current_name = config_service.get_value(card_id, "名称")
            if current_name is None:
                current_name = ""
                if save_callback:
                    save_callback(card_id, "名称", "")
            
            current_account = config_service.get_value(card_id, "账号")
            if current_account is None:
                current_account = ""
                if save_callback:
                    save_callback(card_id, "账号", "")
            
            current_password = config_service.get_value(card_id, "密码")
            if current_password is None:
                current_password = ""
                if save_callback:
                    save_callback(card_id, "密码", "")
            
            saved_enabled = config_service.get_value(card_id, "enabled")
            if saved_enabled is None:
                saved_enabled = enabled
                if save_callback:
                    save_callback(card_id, "enabled", enabled)
            
            saved_type = config_service.get_value(card_id, "类型")
            if saved_type is None:
                saved_type = default_type
                if save_callback:
                    save_callback(card_id, "类型", default_type)
            
            saved_platform = config_service.get_value(card_id, "平台")
            if saved_platform is None:
                saved_platform = "Tap"
                if save_callback:
                    save_callback(card_id, "平台", "Tap")
            
            # 更新卡片数据
            card_data[card_id] = {
                "名称": current_name,
                "账号": current_account,
                "密码": current_password,
                "enabled": saved_enabled,
                "类型": saved_type,
                "平台": saved_platform
            }
            
            # 更新开关状态
            AccountPage.账号开关状态[card_id] = saved_enabled
            
            # 计算参与数量
            if saved_enabled and current_name and current_account and current_password:
                AccountPage.当前参与数量 += 1
            
            subtitle = get_subtitle(saved_enabled, current_name, current_account, current_password, False)
            
            def handle_state_change(new_enabled: bool):
                current_name = card_data.get(card_id, {}).get("名称", "")
                current_account = card_data.get(card_id, {}).get("账号", "")
                current_password = card_data.get(card_id, {}).get("密码", "")
                is_expanded = card.is_loaded() if hasattr(card, 'is_loaded') else False
                
                if new_enabled:
                    if not update_subtitle_and_count(card_id, card, new_enabled, current_name, current_account, current_password, is_expanded):
                        AccountPage.账号开关状态[card_id] = False
                        if hasattr(card, 'set_state'):
                            card.set_state(False)
                        return
                else:
                    update_subtitle_and_count(card_id, card, new_enabled, current_name, current_account, current_password, is_expanded)
                
                handle_save(card_id, "enabled", str(new_enabled))
            
            def handle_expand():
                current_enabled = AccountPage.账号开关状态.get(card_id, False)
                current_name = card_data.get(card_id, {}).get("名称", "")
                current_account = card_data.get(card_id, {}).get("账号", "")
                current_password = card_data.get(card_id, {}).get("密码", "")
                update_subtitle_and_count(card_id, card, current_enabled, current_name, current_account, current_password, True)
            
            def handle_collapse():
                current_enabled = AccountPage.账号开关状态.get(card_id, False)
                current_name = card_data.get(card_id, {}).get("名称", "")
                current_account = card_data.get(card_id, {}).get("账号", "")
                current_password = card_data.get(card_id, {}).get("密码", "")
                update_subtitle_and_count(card_id, card, current_enabled, current_name, current_account, current_password, False)
            
            type_dropdown = Dropdown.create(
                options=["主帅", "副帅"],
                current_value=saved_type,
                width=USER_DROPDOWN_WIDTH,
                enabled=True,
                on_change=lambda v: handle_save(card_id, "类型", v),
                config=config,
            )
            
            platform_dropdown = Dropdown.create(
                options=["Tap", "九游", "Fan", "小7", "Vivo", "Opop"],
                current_value=saved_platform,
                width=USER_DROPDOWN_WIDTH,
                enabled=True,
                on_change=lambda v: handle_save(card_id, "平台", v),
                config=config,
            )
            
            name_input = InputBox.create(
                config=config,
                hint_text="输入统帅名称",
                width=USER_INPUT_WIDTH,
                enabled=True,
                on_change=lambda v: handle_save(card_id, "名称", v),
                value=current_name,
            )
            
            account_input = InputBox.create(
                config=config,
                hint_text="输入统帅账号",
                width=USER_INPUT_WIDTH,
                enabled=True,
                on_change=lambda v: handle_save(card_id, "账号", v),
                value=current_account,
            )
            
            password_input = InputBox.create(
                config=config,
                hint_text="输入统帅密码",
                width=USER_INPUT_WIDTH,
                password_mode=True,
                enabled=True,
                on_change=lambda v: handle_save(card_id, "密码", v),
                value=current_password,
            )
            
            controls = [
                type_dropdown,
                name_input,
                account_input,
                password_input,
                platform_dropdown,
            ]
            
            card = CollapsibleCard.create(
                title=title,
                icon=icon,
                subtitle=subtitle,
                enabled=saved_enabled,
                controls=controls,
                controls_per_row=5,
                on_expand=handle_expand,
                on_collapse=handle_collapse,
                on_save=lambda key, value: handle_save(card_id, key, value),
                config=config,
            )
            
            card_list.append(card)
            card_refs[card_id] = card
            return card
        
        for i in range(1, USER_MAX_ACCOUNTS + 1):
            card_id = f"account_{i:02d}"
            title = f"{i:02d}账号"
            default_type = "主帅" if i == 1 else "副帅"
            
            create_card(
                card_id=card_id,
                title=title,
                icon="ACCOUNT_CIRCLE",
                default_type=default_type,
            )
        
        title_bar = ft.Row([
            ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=20, color=theme_colors.get("accent")),
            ft.Container(width=6),
            ft.Text("账号设置", size=16, weight=ft.FontWeight.BOLD, color=theme_colors.get("text_primary")),
            ft.Container(width=20),
            count_text,
        ], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER)
        
        divider = ft.Container(
            content=ft.Divider(
                height=1,
                thickness=1,
                color=theme_colors.get("border"),
            ),
            opacity=0.5,
        )
        
        card_column = ft.Column(
            controls=card_list,
            spacing=USER_CARD_SPACING,
            scroll=ft.ScrollMode.HIDDEN,
            expand=True,
        )
        
        content_column = ft.Column(
            controls=[
                title_bar,
                divider,
                ft.Container(height=USER_SPACING),
                card_column,
            ],
            spacing=0,
            expand=True,
        )
        
        return ft.Container(
            content=content_column,
            expand=True,
        )


# *** 标准测试格式: 仅调用被测模块,AI不得添加数据 ***
if __name__ == "__main__":
    def main(page: ft.Page):
        page.add(AccountPage.create())
    
    ft.app(target=main)
