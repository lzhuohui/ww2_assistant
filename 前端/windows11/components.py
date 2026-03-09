#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows 11风格 - 组件库

创建日期: 2026-03-08
作者: AI
版本: v1.0.0

说明：Windows 11风格的UI组件，支持主题切换和响应式布局
"""

import flet as ft
from windows11.styles import get_color, get_theme_name, set_theme, register_theme_callback, SPACING, BORDER_RADIUS
from windows11.navigation import NavigationBar, TopNavigationBar


def create_card(title, subtitle, items, width=None):
    """创建卡片组件"""
    return ft.Container(
        content=ft.Column([
            ft.Text(
                title, 
                size=18, 
                weight=ft.FontWeight.BOLD, 
                color=get_color("text_primary")
            ),
            ft.Text(
                subtitle, 
                size=12, 
                color=get_color("text_secondary")
            ),
            ft.Divider(height=SPACING["sm"], color="transparent"),
            ft.Column(items, spacing=SPACING["sm"])
        ], spacing=SPACING["xs"]),
        padding=SPACING["lg"],
        bgcolor=get_color("bg_secondary"),
        border_radius=BORDER_RADIUS["md"],
        width=width
    )


def create_button(text, on_click=None, primary=False):
    """创建按钮组件"""
    return ft.Button(
        text,
        on_click=on_click,
        style=ft.ButtonStyle(
            bgcolor=get_color("accent") if primary else get_color("bg_secondary"),
            color="white" if primary else get_color("text_primary"),
            elevation=0
        ),
        height=36
    )


def create_text_button(text, on_click=None):
    """创建文本按钮组件"""
    return ft.TextButton(
        text,
        on_click=on_click,
        style=ft.ButtonStyle(
            color=get_color("accent")
        )
    )


def create_navigation_item(text, on_click=None, active=False):
    """创建导航项"""
    return ft.Container(
        content=ft.TextButton(
            text,
            on_click=on_click,
            style=ft.ButtonStyle(
                color=get_color("accent") if active else get_color("text_primary")
            )
        ),
        bgcolor=get_color("accent_light") if active else "transparent",
        padding=SPACING["md"],
        border_radius=BORDER_RADIUS["sm"],
        on_click=on_click
    )


def create_main_layout(page):
    """创建主布局"""
    # 导航数据
    navigation_data = {
        "系统": {
            "items": [
                {"id": "system_device", "text": "设备管理", "subitems": [
                    {"id": "system_device_list", "text": "设备列表"},
                    {"id": "system_device_connect", "text": "连接设备"},
                    {"id": "system_device_config", "text": "设备配置"}
                ]},
                {"id": "system_info", "text": "系统信息", "subitems": [
                    {"id": "system_info_basic", "text": "基本信息"},
                    {"id": "system_info_performance", "text": "性能信息"},
                    {"id": "system_info_network", "text": "网络信息"}
                ]},
                {"id": "system_activation", "text": "授权管理", "subitems": [
                    {"id": "system_activation_status", "text": "授权状态"},
                    {"id": "system_activation_bind", "text": "设备绑定"},
                    {"id": "system_activation_verify", "text": "授权验证"}
                ]}
            ]
        },
        "通用设置": {
            "items": [
                {"id": "general_settings", "text": "基本参数", "subitems": [
                    {"id": "general_settings_basic", "text": "基本设置"},
                    {"id": "general_settings_speed", "text": "速度设置"},
                    {"id": "general_settings_attempts", "text": "尝试次数"}
                ]}
            ]
        },
        "策略设置": {
            "items": [
                {"id": "strategy_settings", "text": "策略配置", "subitems": [
                    {"id": "strategy_settings_build", "text": "建筑速建"},
                    {"id": "strategy_settings_resource", "text": "资源速产"},
                    {"id": "strategy_settings_points", "text": "策点保留"}
                ]}
            ]
        },
        "任务设置": {
            "items": [
                {"id": "task_settings", "text": "任务配置", "subitems": [
                    {"id": "task_settings_main", "text": "主线任务"},
                    {"id": "task_settings_branch", "text": "支线任务"},
                    {"id": "task_settings_daily", "text": "日常任务"}
                ]}
            ]
        },
        "建筑设置": {
            "items": [
                {"id": "building_settings", "text": "建筑等级与优先级", "subitems": [
                    {"id": "building_settings_main", "text": "主帅主城"},
                    {"id": "building_settings_vice", "text": "付帅主城"},
                    {"id": "building_settings_priority", "text": "建筑优先级"}
                ]}
            ]
        },
        "集资设置": {
            "items": [
                {"id": "fundraising_settings", "text": "集资策略", "subitems": [
                    {"id": "fundraising_settings_sub", "text": "小号上贡"},
                    {"id": "fundraising_settings_city", "text": "分城纳租"},
                    {"id": "fundraising_settings_limit", "text": "上贡限量"}
                ]}
            ]
        },
        "打扫设置": {
            "items": [
                {"id": "cleaning_settings", "text": "战场打扫", "subitems": [
                    {"id": "cleaning_settings_city", "text": "城区战场"},
                    {"id": "cleaning_settings_political", "text": "政区战场"},
                    {"id": "cleaning_settings_strategy", "text": "打扫策略"}
                ]}
            ]
        },
        "账号设置": {
            "items": [
                {"id": "account_settings", "text": "账号管理", "subitems": [
                    {"id": "account_settings_list", "text": "账号列表"},
                    {"id": "account_settings_add", "text": "添加账号"},
                    {"id": "account_settings_edit", "text": "编辑账号"}
                ]}
            ]
        },
        "个性化": {
            "items": [
                {"id": "personalization_theme", "text": "主题设置", "subitems": [
                    {"id": "personalization_theme_color", "text": "主题颜色"},
                    {"id": "personalization_theme_mode", "text": "主题模式"}
                ]},
                {"id": "personalization_appearance", "text": "外观设置", "subitems": [
                    {"id": "personalization_appearance_font", "text": "字体设置"},
                    {"id": "personalization_appearance_effect", "text": "透明效果"}
                ]}
            ]
        },
        "关于": {
            "items": [
                {"id": "about_info", "text": "关于应用", "subitems": [
                    {"id": "about_info_version", "text": "版本信息"},
                    {"id": "about_info_help", "text": "帮助中心"},
                    {"id": "about_info_feedback", "text": "意见反馈"}
                ]}
            ]
        }
    }
    
    active_item = "system_device"
    active_group = "系统"
    is_narrow_screen = page.width < 1024
    
    # 初始展开系统分组
    expanded_groups = set()
    expanded_groups.add("系统")
    
    # 内容区域
    def get_content_for_nav(item_id):
        # 系统
        if item_id == "system_device":
            return create_device_adb_settings()
        elif item_id == "system_device_list":
            return create_device_list_settings()
        elif item_id == "system_device_connect":
            return create_device_connect_settings()
        elif item_id == "system_device_config":
            return create_device_config_settings()
        elif item_id == "system_info":
            return create_device_info_settings()
        elif item_id == "system_info_basic":
            return create_system_info_basic_settings()
        elif item_id == "system_info_performance":
            return create_system_info_performance_settings()
        elif item_id == "system_info_network":
            return create_system_info_network_settings()
        elif item_id == "system_activation":
            return create_activation_settings()
        elif item_id == "system_activation_status":
            return create_system_activation_status_settings()
        elif item_id == "system_activation_bind":
            return create_system_activation_bind_settings()
        elif item_id == "system_activation_verify":
            return create_system_activation_verify_settings()
        # 通用设置
        elif item_id == "general_settings":
            return create_general_settings()
        elif item_id == "general_settings_basic":
            return create_general_settings_basic_settings()
        elif item_id == "general_settings_speed":
            return create_general_settings_speed_settings()
        elif item_id == "general_settings_attempts":
            return create_general_settings_attempts_settings()
        # 策略设置
        elif item_id == "strategy_settings":
            return create_strategy_settings()
        elif item_id == "strategy_settings_build":
            return create_strategy_settings_build_settings()
        elif item_id == "strategy_settings_resource":
            return create_strategy_settings_resource_settings()
        elif item_id == "strategy_settings_points":
            return create_strategy_settings_points_settings()
        # 任务设置
        elif item_id == "task_settings":
            return create_task_settings()
        elif item_id == "task_settings_main":
            return create_task_settings_main()
        elif item_id == "task_settings_branch":
            return create_task_settings_branch()
        elif item_id == "task_settings_daily":
            return create_task_settings_daily()
        # 建筑设置
        elif item_id == "building_settings":
            return create_building_settings()
        elif item_id == "building_settings_main":
            return create_building_settings_main()
        elif item_id == "building_settings_vice":
            return create_building_settings_vice()
        elif item_id == "building_settings_priority":
            return create_building_settings_priority()
        # 集资设置
        elif item_id == "fundraising_settings":
            return create_fundraising_settings()
        elif item_id == "fundraising_settings_sub":
            return create_fundraising_settings_sub()
        elif item_id == "fundraising_settings_city":
            return create_fundraising_settings_city()
        elif item_id == "fundraising_settings_limit":
            return create_fundraising_settings_limit()
        # 打扫设置
        elif item_id == "cleaning_settings":
            return create_cleaning_settings()
        elif item_id == "cleaning_settings_city":
            return create_cleaning_settings_city()
        elif item_id == "cleaning_settings_political":
            return create_cleaning_settings_political()
        elif item_id == "cleaning_settings_strategy":
            return create_cleaning_settings_strategy()
        # 账号设置
        elif item_id == "account_settings":
            return create_account_settings()
        elif item_id == "account_settings_list":
            return create_account_settings_list()
        elif item_id == "account_settings_add":
            return create_account_settings_add()
        elif item_id == "account_settings_edit":
            return create_account_settings_edit()
        # 个性化
        elif item_id == "personalization_theme":
            return create_theme_settings()
        elif item_id == "personalization_appearance":
            return create_appearance_settings()
        # 关于
        elif item_id == "about_info":
            return create_about_settings()
        else:
            return ft.Text("内容正在开发中...")
    
    # 系统设置 - 主题
    def create_theme_settings():
        """创建主题设置"""
        return create_card(
            "主题设置",
            "选择界面主题",
            [
                ft.Row([
                        ft.Text("主题"),
                        ft.Dropdown(
                            options=[
                                ft.dropdown.Option("dark", "深色"),
                                ft.dropdown.Option("light", "浅色")
                            ],
                            value=get_theme_name()
                        )
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Text("主题更改将立即应用到整个界面", size=12, color=get_color("text_secondary"))
            ]
        )
    
    # 设备设置 - ADB设备
    def create_device_adb_settings():
        return create_card(
            "ADB设备",
            "管理连接的设备",
            [
                ft.Text("已连接设备:"),
                ft.Text("127.0.0.1:5555 (蓝叠模拟器)", size=14),
                ft.Divider(height=SPACING["sm"]),
                create_button("刷新设备列表", on_click=lambda e: print("刷新设备")),
                create_button("连接新设备", on_click=lambda e: print("连接新设备"))
            ]
        )
    
    # 设备设置 - 设备列表
    def create_device_list_settings():
        return create_card(
            "设备列表",
            "查看和管理已连接的设备",
            [
                ft.Text("已连接设备:"),
                ft.ListView(
                    controls=[
                        ft.ListTile(
                            title=ft.Text("127.0.0.1:5555"),
                            subtitle=ft.Text("蓝叠模拟器"),
                            trailing=ft.Row([
                                create_text_button("连接", on_click=lambda e: print("连接设备")),
                                create_text_button("断开", on_click=lambda e: print("断开设备"))
                            ])
                        ),
                        ft.ListTile(
                            title=ft.Text("127.0.0.1:5556"),
                            subtitle=ft.Text("MuMu模拟器"),
                            trailing=ft.Row([
                                create_text_button("连接", on_click=lambda e: print("连接设备")),
                                create_text_button("断开", on_click=lambda e: print("断开设备"))
                            ])
                        )
                    ],
                    expand=True,
                    height=200
                ),
                ft.Divider(height=SPACING["sm"]),
                create_button("刷新设备列表", on_click=lambda e: print("刷新设备列表")),
                create_button("移除离线设备", on_click=lambda e: print("移除离线设备"))
            ]
        )
    
    # 设备设置 - 连接设备
    def create_device_connect_settings():
        return create_card(
            "连接新设备",
            "连接新的ADB设备",
            [
                ft.Row([
                    ft.Text("连接方式:"),
                    ft.Dropdown(
                        options=[
                            ft.dropdown.Option("usb", "USB连接"),
                            ft.dropdown.Option("wifi", "WiFi连接")
                        ],
                        value="usb"
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("设备地址:"),
                    ft.TextField(
                        value="127.0.0.1:5555",
                        width=200
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("ADB路径:"),
                    ft.TextField(
                        value="adb",
                        width=200
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(height=SPACING["sm"]),
                create_button("连接设备", primary=True, on_click=lambda e: print("连接设备")),
                create_button("测试连接", on_click=lambda e: print("测试连接"))
            ]
        )
    
    # 设备设置 - 设备配置
    def create_device_config_settings():
        return create_card(
            "设备配置",
            "配置设备的参数",
            [
                ft.Text("设备选择:"),
                ft.Dropdown(
                    options=[
                        ft.dropdown.Option("127.0.0.1:5555", "127.0.0.1:5555 (蓝叠模拟器)"),
                        ft.dropdown.Option("127.0.0.1:5556", "127.0.0.1:5556 (MuMu模拟器)")
                    ],
                    value="127.0.0.1:5555"
                ),
                ft.Divider(height=SPACING["sm"]),
                ft.Text("屏幕校准:"),
                ft.Row([
                    ft.Text("屏幕宽度:"),
                    ft.TextField(
                        value="1920",
                        width=80,
                        keyboard_type=ft.KeyboardType.NUMBER
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("屏幕高度:"),
                    ft.TextField(
                        value="1080",
                        width=80,
                        keyboard_type=ft.KeyboardType.NUMBER
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(height=SPACING["sm"]),
                ft.Text("性能设置:"),
                ft.Row([
                    ft.Text("操作延迟:"),
                    ft.Slider(min=0.1, max=5, value=1.5, width=200)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("随机化程度:"),
                    ft.Slider(min=0, max=100, value=70, width=200)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(height=SPACING["sm"]),
                create_button("保存配置", primary=True, on_click=lambda e: print("保存配置")),
                create_button("恢复默认", on_click=lambda e: print("恢复默认"))
            ]
        )
    
    # 设备设置 - 设备信息
    def create_device_info_settings():
        return create_card(
            "设备信息",
            "设备详细信息",
            [
                ft.Row([ft.Text("设备型号:"), ft.Text("BlueStacks"), ft.TextButton("查看详情")]),
                ft.Row([ft.Text("系统版本:"), ft.Text("Android 11")]),
                ft.Row([ft.Text("屏幕分辨率:"), ft.Text("1920x1080")])
            ]
        )
    
    # 系统信息 - 基本信息
    def create_system_info_basic_settings():
        return create_card(
            "基本信息",
            "设备的基本信息",
            [
                ft.Text("设备信息:"),
                ft.Row([ft.Text("设备型号:"), ft.Text("BlueStacks")]),
                ft.Row([ft.Text("系统版本:"), ft.Text("Android 11")]),
                ft.Row([ft.Text("屏幕分辨率:"), ft.Text("1920x1080")]),
                ft.Row([ft.Text("屏幕密度:"), ft.Text("320 dpi")]),
                ft.Divider(height=SPACING["sm"]),
                ft.Text("应用信息:"),
                ft.Row([ft.Text("应用版本:"), ft.Text("v1.0.0")]),
                ft.Row([ft.Text("ADB版本:"), ft.Text("1.0.41")]),
                ft.Divider(height=SPACING["sm"]),
                create_button("刷新信息", on_click=lambda e: print("刷新信息"))
            ]
        )
    
    # 系统信息 - 性能信息
    def create_system_info_performance_settings():
        return create_card(
            "性能信息",
            "设备的性能信息",
            [
                ft.Text("CPU信息:"),
                ft.Row([ft.Text("CPU型号:"), ft.Text("Intel Core i7")]),
                ft.Row([ft.Text("CPU核心:"), ft.Text("4核心")]),
                ft.Divider(height=SPACING["sm"]),
                ft.Text("内存信息:"),
                ft.Row([ft.Text("总内存:"), ft.Text("8GB")]),
                ft.Row([ft.Text("可用内存:"), ft.Text("4.5GB")]),
                ft.Divider(height=SPACING["sm"]),
                ft.Text("存储信息:"),
                ft.Row([ft.Text("总存储:"), ft.Text("64GB")]),
                ft.Row([ft.Text("可用存储:"), ft.Text("32GB")]),
                ft.Divider(height=SPACING["sm"]),
                create_button("刷新性能数据", on_click=lambda e: print("刷新性能数据"))
            ]
        )
    
    # 系统信息 - 网络信息
    def create_system_info_network_settings():
        return create_card(
            "网络信息",
            "设备的网络信息",
            [
                ft.Text("网络状态:"),
                ft.Row([ft.Text("网络类型:"), ft.Text("WiFi")]),
                ft.Row([ft.Text("IP地址:"), ft.Text("192.168.1.100")]),
                ft.Row([ft.Text("MAC地址:"), ft.Text("00:11:22:33:44:55")]),
                ft.Divider(height=SPACING["sm"]),
                ft.Text("网络延迟:"),
                ft.Row([ft.Text("Ping值:"), ft.Text("25ms")]),
                ft.Row([ft.Text("下载速度:"), ft.Text("10Mbps")]),
                ft.Row([ft.Text("上传速度:"), ft.Text("2Mbps")]),
                ft.Divider(height=SPACING["sm"]),
                create_button("测试网络", on_click=lambda e: print("测试网络")),
                create_button("刷新网络信息", on_click=lambda e: print("刷新网络信息"))
            ]
        )
    
    # 游戏设置 - 游戏相关设置
    def create_game_related_settings():
        return create_card(
            "游戏设置",
            "调整游戏相关设置",
            [
                ft.Row([
                    ft.Text("自动登录"),
                    ft.Switch(value=True)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("自动开始游戏"),
                    ft.Switch(value=False)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            ]
        )
    
    # 脚本设置 - 脚本运行参数
    def create_script_params_settings():
        return create_card(
            "脚本设置",
            "调整脚本运行参数",
            [
                ft.Row([
                    ft.Text("脚本延迟"),
                    ft.Slider(min=0.1, max=5, value=1.5, width=200)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("最大运行时长"),
                    ft.TextField(
                        value="12",
                        width=50,
                        keyboard_type=ft.KeyboardType.NUMBER
                    ),
                    ft.Text("小时")
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("随机化程度"),
                    ft.Slider(min=0, max=100, value=70, width=200)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            ]
        )
    
    # 脚本设置 - 安全设置
    def create_script_security_settings():
        return create_card(
            "安全设置",
            "防封设置",
            [
                ft.Row([
                    ft.Text("坐标偏移"),
                    ft.Switch(value=True)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("时间间隔随机"),
                    ft.Switch(value=True)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("模拟真实行为"),
                    ft.Switch(value=True)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            ]
        )
    
    # 监控面板 - 运行状态
    def create_monitor_status():
        return create_card(
            "运行状态",
            "当前运行状态",
            [
                ft.Row([
                    ft.Text("状态:"),
                    ft.Text("就绪", color=get_color("success"))
                ]),
                ft.Row([
                    ft.Text("运行时间:"),
                    ft.Text("00:00:00")
                ]),
                ft.Row([
                    ft.Text("点击次数:"),
                    ft.Text("0")
                ]),
                ft.Row([
                    create_button("开始", primary=True),
                    create_button("停止")
                ], spacing=SPACING["sm"])
            ]
        )
    
    # 系统 - 授权管理
    def create_activation_settings():
        return create_card(
            "授权管理",
            "管理软件授权",
            [
                ft.Text("当前状态: 未授权"),
                ft.Divider(height=SPACING["sm"]),
                create_button("申请授权", primary=True),
                create_button("验证授权")
            ]
        )
    
    # 授权管理 - 授权状态
    def create_system_activation_status_settings():
        return create_card(
            "授权状态",
            "查看当前授权状态",
            [
                ft.Row([ft.Text("授权状态:"), ft.Text("未授权", color="red")]),
                ft.Row([ft.Text("授权类型:"), ft.Text("试用版")]),
                ft.Row([ft.Text("有效期:"), ft.Text("30天")]),
                ft.Row([ft.Text("剩余天数:"), ft.Text("25天")]),
                ft.Divider(height=SPACING["sm"]),
                ft.Text("授权设备:"),
                ft.Row([ft.Text("设备ID:"), ft.Text("1234567890")]),
                ft.Row([ft.Text("设备名称:"), ft.Text("BlueStacks")]),
                ft.Divider(height=SPACING["sm"]),
                create_button("刷新状态", on_click=lambda e: print("刷新状态")),
                create_button("查看详情", on_click=lambda e: print("查看详情"))
            ]
        )
    
    # 授权管理 - 设备绑定
    def create_system_activation_bind_settings():
        return create_card(
            "设备绑定",
            "绑定设备到授权",
            [
                ft.Text("设备信息:"),
                ft.Row([ft.Text("设备ID:"), ft.Text("1234567890")]),
                ft.Row([ft.Text("设备名称:"), ft.Text("BlueStacks")]),
                ft.Divider(height=SPACING["sm"]),
                ft.Text("绑定设置:"),
                ft.Row([
                    ft.Text("自动绑定设备"),
                    ft.Switch(value=True)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("允许多设备"),
                    ft.Switch(value=False)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(height=SPACING["sm"]),
                create_button("绑定当前设备", primary=True, on_click=lambda e: print("绑定当前设备")),
                create_button("解绑设备", on_click=lambda e: print("解绑设备"))
            ]
        )
    
    # 授权管理 - 授权验证
    def create_system_activation_verify_settings():
        return create_card(
            "授权验证",
            "验证授权码",
            [
                ft.Text("授权码:"),
                ft.TextField(
                    hint_text="请输入授权码",
                    width=300
                ),
                ft.Divider(height=SPACING["sm"]),
                ft.Text("验证方式:"),
                ft.Dropdown(
                    options=[
                        ft.dropdown.Option("online", "在线验证"),
                        ft.dropdown.Option("offline", "离线验证")
                    ],
                    value="online"
                ),
                ft.Divider(height=SPACING["sm"]),
                create_button("验证授权", primary=True, on_click=lambda e: print("验证授权")),
                create_button("申请授权", on_click=lambda e: print("申请授权")),
                create_button("恢复授权", on_click=lambda e: print("恢复授权"))
            ]
        )
    
    # 通用设置
    def create_general_settings():
        return create_card(
            "通用设置",
            "配置脚本通用参数",
            [
                ft.Row([
                    ft.Text("挂机模式:"),
                    ft.Dropdown(
                        options=["全自动", "半自动"],
                        value="全自动",
                        width=100
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("指令速度:"),
                    ft.Dropdown(
                        options=["100", "150", "200", "250", "300"],
                        value="100",
                        width=80
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("尝试次数:"),
                    ft.Dropdown(
                        options=["10", "15", "20", "25", "30"],
                        value="15",
                        width=80
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("清缓限量:"),
                    ft.Dropdown(
                        options=["1.0", "1.5", "2.0", "2.5", "3.0"],
                        value="1.0",
                        width=80
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            ]
        )
    
    # 通用设置 - 基本设置
    def create_general_settings_basic_settings():
        return create_card(
            "基本设置",
            "配置脚本的基本参数",
            [
                ft.Row([
                    ft.Text("挂机模式:"),
                    ft.Dropdown(
                        options=["全自动", "半自动"],
                        value="全自动",
                        width=100
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("清缓限量:"),
                    ft.Dropdown(
                        options=["1.0", "1.5", "2.0", "2.5", "3.0"],
                        value="1.0",
                        width=80
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("自动重试"),
                    ft.Switch(value=True)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("自动清理缓存"),
                    ft.Switch(value=True)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(height=SPACING["sm"]),
                create_button("保存设置", primary=True, on_click=lambda e: print("保存设置")),
                create_button("恢复默认", on_click=lambda e: print("恢复默认"))
            ]
        )
    
    # 通用设置 - 速度设置
    def create_general_settings_speed_settings():
        return create_card(
            "速度设置",
            "配置脚本的运行速度",
            [
                ft.Row([
                    ft.Text("指令速度:"),
                    ft.Dropdown(
                        options=["50", "100", "150", "200", "250", "300"],
                        value="100",
                        width=80
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("操作间隔:"),
                    ft.Slider(min=0.1, max=5, value=1.0, width=200)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("响应超时:"),
                    ft.Slider(min=1, max=30, value=10, width=200)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(height=SPACING["sm"]),
                create_button("保存设置", primary=True, on_click=lambda e: print("保存设置")),
                create_button("恢复默认", on_click=lambda e: print("恢复默认"))
            ]
        )
    
    # 通用设置 - 尝试次数
    def create_general_settings_attempts_settings():
        return create_card(
            "尝试次数",
            "配置脚本的尝试次数",
            [
                ft.Row([
                    ft.Text("尝试次数:"),
                    ft.Dropdown(
                        options=["5", "10", "15", "20", "25", "30"],
                        value="15",
                        width=80
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("失败重试次数:"),
                    ft.Dropdown(
                        options=["3", "5", "7", "10"],
                        value="5",
                        width=80
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("网络错误重试:"),
                    ft.Switch(value=True)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("超时重试"),
                    ft.Switch(value=True)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(height=SPACING["sm"]),
                create_button("保存设置", primary=True, on_click=lambda e: print("保存设置")),
                create_button("恢复默认", on_click=lambda e: print("恢复默认"))
            ]
        )
    
    # 策略设置
    def create_strategy_settings():
        return create_card(
            "策略设置",
            "配置游戏策略",
            [
                ft.Text("建筑速建"),
                ft.Row([
                    ft.Text("开启速建"),
                    ft.Switch(value=True)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("速建限级:"),
                    ft.Dropdown(
                        options=[f"{i:02d}" for i in range(5, 16)],
                        value="08",
                        width=80
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("建筑类型:"),
                    ft.Dropdown(
                        options=["城资建筑", "城市建筑", "资源建筑"],
                        value="城资建筑",
                        width=120
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(height=SPACING["sm"]),
                ft.Text("资源速产"),
                ft.Row([
                    ft.Text("开启速产"),
                    ft.Switch(value=True)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("速产限级:"),
                    ft.Dropdown(
                        options=[f"{i:02d}" for i in range(5, 16)],
                        value="07",
                        width=80
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("策略类型:"),
                    ft.Dropdown(
                        options=["平衡资源", "战时经济", "钢铁熔炉", "橡胶采集", "石油开采"],
                        value="平衡资源",
                        width=120
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(height=SPACING["sm"]),
                ft.Text("策点保留"),
                ft.Row([
                    ft.Text("保留点数:"),
                    ft.Dropdown(
                        options=["30", "60", "90", "120", "150"],
                        value="60",
                        width=80
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("保留开关"),
                    ft.Switch(value=True)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            ]
        )
    
    # 策略设置 - 建筑速建
    def create_strategy_settings_build_settings():
        return create_card(
            "建筑速建",
            "配置建筑速建策略",
            [
                ft.Row([
                    ft.Text("开启速建"),
                    ft.Switch(value=True)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("速建限级:"),
                    ft.Dropdown(
                        options=[f"{i:02d}" for i in range(5, 16)],
                        value="08",
                        width=80
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("建筑类型:"),
                    ft.Dropdown(
                        options=["城资建筑", "城市建筑", "资源建筑"],
                        value="城资建筑",
                        width=120
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("优先顺序:"),
                    ft.Dropdown(
                        options=["城市中心", "兵工厂", "资源建筑", "防御建筑"],
                        value="城市中心",
                        width=120
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(height=SPACING["sm"]),
                create_button("保存设置", primary=True, on_click=lambda e: print("保存设置")),
                create_button("恢复默认", on_click=lambda e: print("恢复默认"))
            ]
        )
    
    # 策略设置 - 资源速产
    def create_strategy_settings_resource_settings():
        return create_card(
            "资源速产",
            "配置资源速产策略",
            [
                ft.Row([
                    ft.Text("开启速产"),
                    ft.Switch(value=True)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("速产限级:"),
                    ft.Dropdown(
                        options=[f"{i:02d}" for i in range(5, 16)],
                        value="07",
                        width=80
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("策略类型:"),
                    ft.Dropdown(
                        options=["平衡资源", "战时经济", "钢铁熔炉", "橡胶采集", "石油开采"],
                        value="平衡资源",
                        width=120
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("资源优先级:"),
                    ft.Dropdown(
                        options=["钢铁", "橡胶", "石油", "粮食"],
                        value="钢铁",
                        width=120
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(height=SPACING["sm"]),
                create_button("保存设置", primary=True, on_click=lambda e: print("保存设置")),
                create_button("恢复默认", on_click=lambda e: print("恢复默认"))
            ]
        )
    
    # 策略设置 - 策点保留
    def create_strategy_settings_points_settings():
        return create_card(
            "策点保留",
            "配置策点保留策略",
            [
                ft.Row([
                    ft.Text("保留开关"),
                    ft.Switch(value=True)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("保留点数:"),
                    ft.Dropdown(
                        options=["30", "60", "90", "120", "150"],
                        value="60",
                        width=80
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("自动分配"),
                    ft.Switch(value=True)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("分配比例:"),
                    ft.Dropdown(
                        options=["平衡分配", "攻击优先", "防御优先", "资源优先"],
                        value="平衡分配",
                        width=120
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(height=SPACING["sm"]),
                create_button("保存设置", primary=True, on_click=lambda e: print("保存设置")),
                create_button("恢复默认", on_click=lambda e: print("恢复默认"))
            ]
        )
    
    # 任务设置 - 主线任务
    def create_task_settings_main():
        return create_card(
            "主线任务",
            "配置主线任务执行策略",
            [
                ft.Row([
                    ft.Text("开启主线任务"),
                    ft.Switch(value=True)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("主线限级:"),
                    ft.Dropdown(
                        options=[f"{i:02d}" for i in range(1, 16)],
                        value="05",
                        width=80
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("任务优先级:"),
                    ft.Dropdown(
                        options=["军事任务", "经济任务", "科技任务", "外交任务"],
                        value="军事任务",
                        width=120
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(height=SPACING["sm"]),
                create_button("保存设置", primary=True, on_click=lambda e: print("保存主线任务设置")),
                create_button("恢复默认", on_click=lambda e: print("恢复主线任务默认"))
            ]
        )
    
    # 任务设置 - 支线任务
    def create_task_settings_branch():
        return create_card(
            "支线任务",
            "配置支线任务执行策略",
            [
                ft.Row([
                    ft.Text("开启支线任务"),
                    ft.Switch(value=True)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("支线限级:"),
                    ft.Dropdown(
                        options=[f"{i:02d}" for i in range(5, 16)],
                        value="10",
                        width=80
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("任务类型:"),
                    ft.Dropdown(
                        options=["资源任务", "军事任务", "科技任务", "探索任务"],
                        value="资源任务",
                        width=120
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(height=SPACING["sm"]),
                create_button("保存设置", primary=True, on_click=lambda e: print("保存支线任务设置")),
                create_button("恢复默认", on_click=lambda e: print("恢复支线任务默认"))
            ]
        )
    
    # 任务设置 - 日常任务
    def create_task_settings_daily():
        return create_card(
            "日常任务",
            "配置日常任务执行策略",
            [
                ft.Row([
                    ft.Text("开启日常任务"),
                    ft.Switch(value=True)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("任务频率:"),
                    ft.Dropdown(
                        options=["每小时", "每2小时", "每4小时", "每天"],
                        value="每4小时",
                        width=120
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("任务优先级:"),
                    ft.Dropdown(
                        options=["经验任务", "资源任务", "军事任务", "社交任务"],
                        value="经验任务",
                        width=120
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(height=SPACING["sm"]),
                create_button("保存设置", primary=True, on_click=lambda e: print("保存日常任务设置")),
                create_button("恢复默认", on_click=lambda e: print("恢复日常任务默认"))
            ]
        )
    
    # 建筑设置 - 主帅主城
    def create_building_settings_main():
        return create_card(
            "主帅主城",
            "配置主帅主城建筑等级",
            [
                ft.Row([
                    ft.Text("城市等级:"),
                    ft.Dropdown(
                        options=[f"{i:02d}" for i in range(1, 21)],
                        value="17",
                        width=80
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("兵工厂等级:"),
                    ft.Dropdown(
                        options=[f"{i:02d}" for i in range(1, 21)],
                        value="17",
                        width=80
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("陆军基地等级:"),
                    ft.Dropdown(
                        options=[f"{i:02d}" for i in range(1, 21)],
                        value="14",
                        width=80
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("空军基地等级:"),
                    ft.Dropdown(
                        options=[f"{i:02d}" for i in range(1, 21)],
                        value="12",
                        width=80
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("海军基地等级:"),
                    ft.Dropdown(
                        options=[f"{i:02d}" for i in range(1, 21)],
                        value="10",
                        width=80
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(height=SPACING["sm"]),
                create_button("保存设置", primary=True, on_click=lambda e: print("保存主帅主城设置")),
                create_button("恢复默认", on_click=lambda e: print("恢复主帅主城默认"))
            ]
        )
    
    # 建筑设置 - 付帅主城
    def create_building_settings_vice():
        return create_card(
            "付帅主城",
            "配置付帅主城建筑等级",
            [
                ft.Row([
                    ft.Text("城市等级:"),
                    ft.Dropdown(
                        options=[f"{i:02d}" for i in range(1, 21)],
                        value="15",
                        width=80
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("兵工厂等级:"),
                    ft.Dropdown(
                        options=[f"{i:02d}" for i in range(1, 21)],
                        value="10",
                        width=80
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("陆军基地等级:"),
                    ft.Dropdown(
                        options=[f"{i:02d}" for i in range(1, 21)],
                        value="08",
                        width=80
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("资源建筑等级:"),
                    ft.Dropdown(
                        options=[f"{i:02d}" for i in range(1, 21)],
                        value="12",
                        width=80
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(height=SPACING["sm"]),
                create_button("保存设置", primary=True, on_click=lambda e: print("保存付帅主城设置")),
                create_button("恢复默认", on_click=lambda e: print("恢复付帅主城默认"))
            ]
        )
    
    # 建筑设置 - 建筑优先级
    def create_building_settings_priority():
        return create_card(
            "建筑优先级",
            "配置建筑升级优先级",
            [
                ft.Row([
                    ft.Text("资源建筑:"),
                    ft.Dropdown(
                        options=["自动平衡", "钢铁优先", "橡胶优先", "石油优先"],
                        value="自动平衡",
                        width=120
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("军事建筑:"),
                    ft.Dropdown(
                        options=["陆军优先", "空军优先", "海军优先", "平衡发展"],
                        value="陆军优先",
                        width=120
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("塔防建筑:"),
                    ft.Dropdown(
                        options=["炮塔优先", "岸防优先", "防空优先"],
                        value="炮塔优先",
                        width=120
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("基础设施:"),
                    ft.Dropdown(
                        options=["城市中心", "仓库", "科研中心", "医院"],
                        value="城市中心",
                        width=120
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(height=SPACING["sm"]),
                create_button("保存设置", primary=True, on_click=lambda e: print("保存建筑优先级设置")),
                create_button("恢复默认", on_click=lambda e: print("恢复建筑优先级默认"))
            ]
        )
    
    # 建筑设置
    def create_building_settings():
        return create_card(
            "建筑管理",
            "管理建筑设置",
            [
                ft.Text("选择建筑设置功能"),
                ft.Divider(height=SPACING["sm"]),
                create_button("主帅主城设置", on_click=lambda e: print("主帅主城设置")),
                create_button("付帅主城设置", on_click=lambda e: print("付帅主城设置")),
                create_button("建筑优先级设置", on_click=lambda e: print("建筑优先级设置"))
            ]
        )
    
    # 集资设置 - 小号上贡
    def create_fundraising_settings_sub():
        return create_card(
            "小号上贡",
            "配置小号上贡策略",
            [
                ft.Row([
                    ft.Text("开启上贡"),
                    ft.Switch(value=True)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("上贡限级:"),
                    ft.Dropdown(
                        options=[f"{i:02d}" for i in range(5, 16)],
                        value="05",
                        width=80
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("上贡限量:"),
                    ft.Dropdown(
                        options=[str(i) for i in range(2, 21)],
                        value="2",
                        width=80
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("上贡频率:"),
                    ft.Dropdown(
                        options=["每小时", "每2小时", "每4小时", "每天"],
                        value="每4小时",
                        width=120
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(height=SPACING["sm"]),
                create_button("保存设置", primary=True, on_click=lambda e: print("保存小号上贡设置")),
                create_button("恢复默认", on_click=lambda e: print("恢复小号上贡默认"))
            ]
        )
    
    # 集资设置 - 分城纳租
    def create_fundraising_settings_city():
        return create_card(
            "分城纳租",
            "配置分城纳租策略",
            [
                ft.Row([
                    ft.Text("开启纳租"),
                    ft.Switch(value=False)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("分城等级:"),
                    ft.Dropdown(
                        options=[f"{i:02d}" for i in range(5, 16)],
                        value="05",
                        width=80
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("纳租限量:"),
                    ft.Dropdown(
                        options=[str(i) for i in range(2, 21)],
                        value="2",
                        width=80
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("纳租频率:"),
                    ft.Dropdown(
                        options=["每小时", "每2小时", "每4小时", "每天"],
                        value="每4小时",
                        width=120
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(height=SPACING["sm"]),
                create_button("保存设置", primary=True, on_click=lambda e: print("保存分城纳租设置")),
                create_button("恢复默认", on_click=lambda e: print("恢复分城纳租默认"))
            ]
        )
    
    # 集资设置 - 上贡限量
    def create_fundraising_settings_limit():
        return create_card(
            "上贡限量",
            "配置上贡限量策略",
            [
                ft.Row([
                    ft.Text("资源类型:"),
                    ft.Dropdown(
                        options=["钢铁", "橡胶", "石油", "粮食"],
                        value="钢铁",
                        width=120
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("单次上贡量:"),
                    ft.Dropdown(
                        options=["1000", "5000", "10000", "20000"],
                        value="5000",
                        width=120
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("每日上限:"),
                    ft.Dropdown(
                        options=["10000", "50000", "100000", "无上限"],
                        value="50000",
                        width=120
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("自动调整"),
                    ft.Switch(value=True)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(height=SPACING["sm"]),
                create_button("保存设置", primary=True, on_click=lambda e: print("保存上贡限量设置")),
                create_button("恢复默认", on_click=lambda e: print("恢复上贡限量默认"))
            ]
        )
    
    # 集资设置
    def create_fundraising_settings():
        return create_card(
            "集资管理",
            "管理集资策略",
            [
                ft.Text("选择集资设置功能"),
                ft.Divider(height=SPACING["sm"]),
                create_button("小号上贡设置", on_click=lambda e: print("小号上贡设置")),
                create_button("分城纳租设置", on_click=lambda e: print("分城纳租设置")),
                create_button("上贡限量设置", on_click=lambda e: print("上贡限量设置"))
            ]
        )
    
    # 打扫设置 - 城区战场
    def create_cleaning_settings_city():
        return create_card(
            "城区战场",
            "配置城区战场打扫策略",
            [
                ft.Row([
                    ft.Text("打扫城区战场"),
                    ft.Switch(value=True)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("打扫频率:"),
                    ft.Dropdown(
                        options=["每小时", "每2小时", "每4小时", "每天"],
                        value="每4小时",
                        width=120
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("打扫范围:"),
                    ft.Dropdown(
                        options=["全城区", "仅主城", "指定区域"],
                        value="全城区",
                        width=120
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("资源优先级:"),
                    ft.Dropdown(
                        options=["钢铁", "橡胶", "石油", "粮食"],
                        value="钢铁",
                        width=120
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(height=SPACING["sm"]),
                create_button("保存设置", primary=True, on_click=lambda e: print("保存城区战场设置")),
                create_button("恢复默认", on_click=lambda e: print("恢复城区战场默认"))
            ]
        )
    
    # 打扫设置 - 政区战场
    def create_cleaning_settings_political():
        return create_card(
            "政区战场",
            "配置政区战场打扫策略",
            [
                ft.Row([
                    ft.Text("打扫政区战场"),
                    ft.Switch(value=False)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("打扫频率:"),
                    ft.Dropdown(
                        options=["每小时", "每2小时", "每4小时", "每天"],
                        value="每4小时",
                        width=120
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("打扫范围:"),
                    ft.Dropdown(
                        options=["全政区", "仅附近", "指定区域"],
                        value="全政区",
                        width=120
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("敌人等级:"),
                    ft.Dropdown(
                        options=["所有等级", "1-10级", "11-20级", "21级以上"],
                        value="所有等级",
                        width=120
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(height=SPACING["sm"]),
                create_button("保存设置", primary=True, on_click=lambda e: print("保存政区战场设置")),
                create_button("恢复默认", on_click=lambda e: print("恢复政区战场默认"))
            ]
        )
    
    # 打扫设置 - 打扫策略
    def create_cleaning_settings_strategy():
        return create_card(
            "打扫策略",
            "配置打扫策略",
            [
                ft.Row([
                    ft.Text("自动打扫"),
                    ft.Switch(value=True)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("打扫模式:"),
                    ft.Dropdown(
                        options=["资源优先", "经验优先", "荣誉优先", "平衡模式"],
                        value="资源优先",
                        width=120
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("打扫时间:"),
                    ft.Dropdown(
                        options=["全天", "白天", "夜间", "自定义"],
                        value="全天",
                        width=120
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("最大连续次数:"),
                    ft.Dropdown(
                        options=["5次", "10次", "20次", "无限制"],
                        value="10次",
                        width=120
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(height=SPACING["sm"]),
                create_button("保存设置", primary=True, on_click=lambda e: print("保存打扫策略设置")),
                create_button("恢复默认", on_click=lambda e: print("恢复打扫策略默认"))
            ]
        )
    
    # 打扫设置
    def create_cleaning_settings():
        return create_card(
            "打扫管理",
            "管理战场打扫设置",
            [
                ft.Text("选择打扫设置功能"),
                ft.Divider(height=SPACING["sm"]),
                create_button("城区战场设置", on_click=lambda e: print("城区战场设置")),
                create_button("政区战场设置", on_click=lambda e: print("政区战场设置")),
                create_button("打扫策略设置", on_click=lambda e: print("打扫策略设置"))
            ]
        )
    
    # 账号设置 - 账号列表
    def create_account_settings_list():
        return create_card(
            "账号列表",
            "管理已添加的游戏账号",
            [
                ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("账号名称")),
                        ft.DataColumn(ft.Text("状态")),
                        ft.DataColumn(ft.Text("类型")),
                        ft.DataColumn(ft.Text("平台")),
                        ft.DataColumn(ft.Text("操作"))
                    ],
                    rows=[
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text("账号1")),
                                ft.DataCell(ft.Text("在线")),
                                ft.DataCell(ft.Text("主帅")),
                                ft.DataCell(ft.Text("Tap")),
                                ft.DataCell(
                                    ft.Row([
                                        create_text_button("编辑"),
                                        create_text_button("删除")
                                    ])
                                )
                            ]
                        ),
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text("账号2")),
                                ft.DataCell(ft.Text("离线")),
                                ft.DataCell(ft.Text("付帅")),
                                ft.DataCell(ft.Text("官方")),
                                ft.DataCell(
                                    ft.Row([
                                        create_text_button("编辑"),
                                        create_text_button("删除")
                                    ])
                                )
                            ]
                        )
                    ]
                ),
                ft.Divider(height=SPACING["sm"]),
                create_button("添加账号", primary=True, on_click=lambda e: print("添加账号")),
                create_button("刷新列表", on_click=lambda e: print("刷新列表"))
            ]
        )
    
    # 账号设置 - 添加账号
    def create_account_settings_add():
        return create_card(
            "添加账号",
            "添加新的游戏账号",
            [
                ft.Row([
                    ft.Text("账号名称:"),
                    ft.TextField(value="", hint_text="请输入账号名称")
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("账号信息:"),
                    ft.TextField(value="", hint_text="输入账号信息,格式: 统帅名称/登录账号/登录密码")
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("账号类型:"),
                    ft.Dropdown(
                        options=["主帅", "付帅"],
                        value="主帅",
                        width=100
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("平台:"),
                    ft.Dropdown(
                        options=["Tap", "官方", "其他"],
                        value="Tap",
                        width=100
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(height=SPACING["sm"]),
                create_button("保存账号", primary=True, on_click=lambda e: print("保存账号")),
                create_button("取消", on_click=lambda e: print("取消"))
            ]
        )
    
    # 账号设置 - 编辑账号
    def create_account_settings_edit():
        return create_card(
            "编辑账号",
            "修改账号信息",
            [
                ft.Row([
                    ft.Text("账号名称:"),
                    ft.TextField(value="账号1")
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("账号信息:"),
                    ft.TextField(value="统帅1/account1/password1")
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("账号类型:"),
                    ft.Dropdown(
                        options=["主帅", "付帅"],
                        value="主帅",
                        width=100
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("平台:"),
                    ft.Dropdown(
                        options=["Tap", "官方", "其他"],
                        value="Tap",
                        width=100
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(height=SPACING["sm"]),
                create_button("更新账号", primary=True, on_click=lambda e: print("更新账号")),
                create_button("取消", on_click=lambda e: print("取消"))
            ]
        )
    
    # 账号设置
    def create_account_settings():
        return create_card(
            "账号管理",
            "管理游戏账号",
            [
                ft.Text("选择账号管理功能"),
                ft.Divider(height=SPACING["sm"]),
                create_button("查看账号列表", on_click=lambda e: print("查看账号列表")),
                create_button("添加新账号", on_click=lambda e: print("添加新账号"))
            ]
        )
    
    # 个性化 - 外观设置
    def create_appearance_settings():
        return create_card(
            "外观设置",
            "调整界面外观",
            [
                ft.Row([
                    ft.Text("透明效果"),
                    ft.Switch(value=False)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("字体:"),
                    ft.Dropdown(
                        options=["微软雅黑", "宋体", "Arial"],
                        value="微软雅黑",
                        width=120
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("导航展开"),
                    ft.Switch(value=False)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            ]
        )
    
    # 关于 - 关于应用
    def create_about_settings():
        return create_card(
            "关于应用",
            "二战风云辅助工具",
            [
                ft.Text("当前版本: v1.0.0"),
                ft.Divider(height=SPACING["sm"]),
                create_text_button("访问主页", on_click=lambda e: print("访问主页")),
                create_text_button("提交问题", on_click=lambda e: print("提交问题")),
                create_text_button("申请授权", on_click=lambda e: print("申请授权"))
            ]
        )
    
    # 导航点击事件
    def on_nav_change(item_data):
        nonlocal active_item, active_group
        active_item = item_data["id"]
        # 找到包含该item_id的分组
        for group_name, group_data in navigation_data.items():
            for item in group_data["items"]:
                if item["id"] == item_data["id"]:
                    active_group = group_name
                    break
                # 检查子项
                if "subitems" in item:
                    for subitem in item["subitems"]:
                        if subitem["id"] == item_data["id"]:
                            active_group = group_name
                            break
                    if active_group:
                        break
            if active_group:
                break
        update_layout()
    
    # 窗口大小变化事件
    def on_window_resize(e):
        nonlocal is_narrow_screen
        is_narrow_screen = page.width < 1024
        update_layout()
    
    # 更新布局
    content = get_content_for_nav(active_item)
    
    # 创建导航栏实例（只创建一次）
    nav_bar = NavigationBar(navigation_data, on_nav_change)
    
    def update_layout():
        nonlocal content
        content = get_content_for_nav(active_item)
        layout.content = create_layout()
        page.update()
    
    # 创建布局
    def create_layout():
        if is_narrow_screen:
            # 窄屏模式：顶部导航
            return ft.Column([
                TopNavigationBar(navigation_data, on_nav_change),
                ft.Container(
                    content=content,
                    expand=True
                )
            ], expand=True)
        else:
            # 宽屏模式：左侧导航
            # 完全重新设计，使用最基本的结构
            return ft.Container(
                content=ft.Row([
                    # 导航栏 - 固定宽度，直接使用NavigationBar
                    nav_bar,
                    # 分隔线
                    ft.VerticalDivider(width=1, color=get_color("border")),
                    # 内容区域 - 直接显示内容，不使用额外容器
                    ft.Container(
                        content=content,
                        expand=True
                    )
                ], spacing=0),
                expand=True,
                bgcolor=get_color("bg_primary")
            )
    
    # 注册窗口大小变化事件
    page.on_resize = on_window_resize
    
    layout = ft.Container(
        content=create_layout(),
        expand=True
    )
    
    return layout