#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单布局测试 - 导航栏功能测试

创建日期: 2026-03-08
作者: AI
版本: v1.0.0

说明：测试导航栏功能，包括展开、折叠和三级导航
"""

import flet as ft


def main(page: ft.Page):
    """主函数"""
    # 设置页面
    page.title = "二战风云 - 导航栏功能测试"
    page.window_width = 1200
    page.window_height = 540
    page.bgcolor = "#1C1C1C"  # 深色背景
    page.padding = 20
    
    # 清空页面
    page.clean()
    
    # 导航数据
    navigation_data = {
        "系统": {
            "items": [
                {
                    "id": "system_device", 
                    "text": "设备管理",
                    "subitems": [
                        {"id": "system_device_list", "text": "设备列表"},
                        {"id": "system_device_connect", "text": "连接设备"},
                        {"id": "system_device_config", "text": "设备配置"}
                    ]
                },
                {
                    "id": "system_info", 
                    "text": "系统信息",
                    "subitems": [
                        {"id": "system_info_basic", "text": "基本信息"},
                        {"id": "system_info_performance", "text": "性能信息"},
                        {"id": "system_info_network", "text": "网络信息"}
                    ]
                },
                {
                    "id": "system_activation", 
                    "text": "授权管理",
                    "subitems": [
                        {"id": "system_activation_status", "text": "授权状态"},
                        {"id": "system_activation_bind", "text": "设备绑定"},
                        {"id": "system_activation_verify", "text": "授权验证"}
                    ]
                }
            ]
        },
        "通用设置": {
            "items": [
                {
                    "id": "general_settings", 
                    "text": "基本参数",
                    "subitems": [
                        {"id": "general_settings_basic", "text": "基本设置"},
                        {"id": "general_settings_speed", "text": "速度设置"},
                        {"id": "general_settings_attempts", "text": "尝试次数"}
                    ]
                }
            ]
        },
        "策略设置": {
            "items": [
                {
                    "id": "strategy_settings", 
                    "text": "策略配置",
                    "subitems": [
                        {"id": "strategy_settings_build", "text": "建筑速建"},
                        {"id": "strategy_settings_resource", "text": "资源速产"},
                        {"id": "strategy_settings_points", "text": "策点保留"}
                    ]
                }
            ]
        }
    }
    
    # 当前状态
    expanded_groups = set()  # 展开的分组
    active_item = None  # 激活的主项
    active_subitem = None  # 激活的子项
    
    # 内容区域容器
    content_container = ft.Container(
        content=ft.Column([
            ft.Text("请选择导航项", size=18, weight=ft.FontWeight.BOLD, color="#F2F2F2"),
            ft.Text("点击左侧导航栏查看详细内容", size=12, color="#CCCCCC")
        ]),
        padding=20,
        bgcolor="#2D2D2D",
        border_radius=8,
        expand=True
    )
    
    # 导航栏容器
    nav_container = ft.Container(
        width=240,
        padding=20,
        bgcolor="#1C1C1C"
    )
    
    # 获取内容
    def get_content(item_id):
        """根据导航项ID返回对应的内容"""
        contents = {
            # 设备管理
            "system_device_list": ft.Column([
                ft.Text("设备列表", size=18, weight=ft.FontWeight.BOLD, color="#F2F2F2"),
                ft.Text("管理已连接的设备", size=12, color="#CCCCCC"),
                ft.Divider(height=16, color="transparent"),
                ft.Text("已连接设备:", color="#F2F2F2"),
                ft.Text("127.0.0.1:5555 (蓝叠模拟器)", size=14, color="#F2F2F2"),
                ft.Divider(height=16, color="transparent"),
                ft.Row([
                    ft.Button("刷新列表", style=ft.ButtonStyle(bgcolor="#0078D4", color="white", elevation=0)),
                    ft.Button("断开连接", style=ft.ButtonStyle(bgcolor="#2D2D2D", color="#F2F2F2", elevation=0))
                ])
            ]),
            "system_device_connect": ft.Column([
                ft.Text("连接设备", size=18, weight=ft.FontWeight.BOLD, color="#F2F2F2"),
                ft.Text("连接新的设备", size=12, color="#CCCCCC"),
                ft.Divider(height=16, color="transparent"),
                ft.TextField(label="设备地址", value="127.0.0.1:5555", color="#F2F2F2"),
                ft.Divider(height=16, color="transparent"),
                ft.Button("连接", style=ft.ButtonStyle(bgcolor="#0078D4", color="white", elevation=0))
            ]),
            "system_device_config": ft.Column([
                ft.Text("设备配置", size=18, weight=ft.FontWeight.BOLD, color="#F2F2F2"),
                ft.Text("配置设备参数", size=12, color="#CCCCCC"),
                ft.Divider(height=16, color="transparent"),
                ft.Text("配置选项:", color="#F2F2F2"),
                ft.Switch(label="自动重连", value=True),
                ft.Switch(label="调试模式", value=False)
            ]),
            # 系统信息
            "system_info_basic": ft.Column([
                ft.Text("基本信息", size=18, weight=ft.FontWeight.BOLD, color="#F2F2F2"),
                ft.Text("系统基本信息", size=12, color="#CCCCCC"),
                ft.Divider(height=16, color="transparent"),
                ft.Text("系统版本: v1.0.0", color="#F2F2F2"),
                ft.Text("Python版本: 3.11.0", color="#F2F2F2"),
                ft.Text("Flet版本: 0.21.0", color="#F2F2F2")
            ]),
            "system_info_performance": ft.Column([
                ft.Text("性能信息", size=18, weight=ft.FontWeight.BOLD, color="#F2F2F2"),
                ft.Text("系统性能信息", size=12, color="#CCCCCC"),
                ft.Divider(height=16, color="transparent"),
                ft.Text("CPU使用率: 25%", color="#F2F2F2"),
                ft.Text("内存使用率: 45%", color="#F2F2F2"),
                ft.Text("磁盘使用率: 60%", color="#F2F2F2")
            ]),
            "system_info_network": ft.Column([
                ft.Text("网络信息", size=18, weight=ft.FontWeight.BOLD, color="#F2F2F2"),
                ft.Text("网络连接信息", size=12, color="#CCCCCC"),
                ft.Divider(height=16, color="transparent"),
                ft.Text("网络状态: 已连接", color="#F2F2F2"),
                ft.Text("IP地址: 192.168.1.100", color="#F2F2F2"),
                ft.Text("延迟: 15ms", color="#F2F2F2")
            ]),
            # 授权管理
            "system_activation_status": ft.Column([
                ft.Text("授权状态", size=18, weight=ft.FontWeight.BOLD, color="#F2F2F2"),
                ft.Text("查看授权状态", size=12, color="#CCCCCC"),
                ft.Divider(height=16, color="transparent"),
                ft.Text("授权状态: 已授权", color="#4CAF50"),
                ft.Text("授权类型: 专业版", color="#F2F2F2"),
                ft.Text("到期时间: 2026-12-31", color="#F2F2F2")
            ]),
            "system_activation_bind": ft.Column([
                ft.Text("设备绑定", size=18, weight=ft.FontWeight.BOLD, color="#F2F2F2"),
                ft.Text("绑定设备信息", size=12, color="#CCCCCC"),
                ft.Divider(height=16, color="transparent"),
                ft.Text("已绑定设备: 1台", color="#F2F2F2"),
                ft.Text("设备ID: ABC123DEF456", color="#F2F2F2"),
                ft.Button("解绑设备", style=ft.ButtonStyle(bgcolor="#FF5722", color="white", elevation=0))
            ]),
            "system_activation_verify": ft.Column([
                ft.Text("授权验证", size=18, weight=ft.FontWeight.BOLD, color="#F2F2F2"),
                ft.Text("验证授权信息", size=12, color="#CCCCCC"),
                ft.Divider(height=16, color="transparent"),
                ft.TextField(label="授权码", password=True, can_reveal_password=True, color="#F2F2F2"),
                ft.Divider(height=16, color="transparent"),
                ft.Button("验证授权", style=ft.ButtonStyle(bgcolor="#0078D4", color="white", elevation=0))
            ]),
            # 通用设置
            "general_settings_basic": ft.Column([
                ft.Text("基本设置", size=18, weight=ft.FontWeight.BOLD, color="#F2F2F2"),
                ft.Text("配置基本参数", size=12, color="#CCCCCC"),
                ft.Divider(height=16, color="transparent"),
                ft.Text("运行模式:", color="#F2F2F2"),
                ft.Dropdown(options=["标准模式", "快速模式", "安全模式"], value="标准模式", width=200),
                ft.Switch(label="开机自启", value=False)
            ]),
            "general_settings_speed": ft.Column([
                ft.Text("速度设置", size=18, weight=ft.FontWeight.BOLD, color="#F2F2F2"),
                ft.Text("配置运行速度", size=12, color="#CCCCCC"),
                ft.Divider(height=16, color="transparent"),
                ft.Text("操作速度:", color="#F2F2F2"),
                ft.Slider(min=1, max=10, value=5, label="{value}"),
                ft.Text("延迟时间:", color="#F2F2F2"),
                ft.Dropdown(options=["0.5秒", "1秒", "2秒", "3秒"], value="1秒", width=200)
            ]),
            "general_settings_attempts": ft.Column([
                ft.Text("尝试次数", size=18, weight=ft.FontWeight.BOLD, color="#F2F2F2"),
                ft.Text("配置重试次数", size=12, color="#CCCCCC"),
                ft.Divider(height=16, color="transparent"),
                ft.Text("最大重试次数:", color="#F2F2F2"),
                ft.Dropdown(options=["1次", "3次", "5次", "10次"], value="3次", width=200),
                ft.Text("重试间隔:", color="#F2F2F2"),
                ft.Dropdown(options=["1秒", "2秒", "5秒", "10秒"], value="2秒", width=200)
            ]),
            # 策略设置
            "strategy_settings_build": ft.Column([
                ft.Text("建筑速建", size=18, weight=ft.FontWeight.BOLD, color="#F2F2F2"),
                ft.Text("配置建筑速建策略", size=12, color="#CCCCCC"),
                ft.Divider(height=16, color="transparent"),
                ft.Switch(label="开启速建", value=True),
                ft.Text("速建等级限制:", color="#F2F2F2"),
                ft.Dropdown(options=["5级", "10级", "15级", "20级"], value="10级", width=200)
            ]),
            "strategy_settings_resource": ft.Column([
                ft.Text("资源速产", size=18, weight=ft.FontWeight.BOLD, color="#F2F2F2"),
                ft.Text("配置资源速产策略", size=12, color="#CCCCCC"),
                ft.Divider(height=16, color="transparent"),
                ft.Switch(label="开启速产", value=True),
                ft.Text("速产等级限制:", color="#F2F2F2"),
                ft.Dropdown(options=["5级", "10级", "15级", "20级"], value="10级", width=200)
            ]),
            "strategy_settings_points": ft.Column([
                ft.Text("策点保留", size=18, weight=ft.FontWeight.BOLD, color="#F2F2F2"),
                ft.Text("配置策略点保留", size=12, color="#CCCCCC"),
                ft.Divider(height=16, color="transparent"),
                ft.Switch(label="保留策点", value=False),
                ft.Text("保留数量:", color="#F2F2F2"),
                ft.Dropdown(options=["100", "500", "1000", "5000"], value="500", width=200)
            ])
        }
        return contents.get(item_id, ft.Column([
            ft.Text("未知内容", size=18, weight=ft.FontWeight.BOLD, color="#F2F2F2"),
            ft.Text(f"ID: {item_id}", size=12, color="#CCCCCC")
        ]))
    
    # 更新导航栏
    def update_navigation():
        """更新导航栏"""
        nonlocal expanded_groups, active_item, active_subitem
        
        controls = [
            ft.Text(
                "设置",
                size=20,
                weight=ft.FontWeight.BOLD,
                color="#F2F2F2"
            ),
            ft.Divider(height=16)
        ]
        
        for group_name, group_data in navigation_data.items():
            # 分组标题
            is_expanded = group_name in expanded_groups
            group_title = ft.Container(
                content=ft.Row([
                    ft.Text(
                        group_name,
                        color="#0078D4",
                        size=14,
                        weight=ft.FontWeight.BOLD
                    ),
                    ft.Icon(
                        "expand_more" if is_expanded else "chevron_right",
                        size=16,
                        color="#CCCCCC"
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=ft.Padding(left=16, right=16, top=8, bottom=8),
                on_click=lambda e, group=group_name: on_group_click(group)
            )
            controls.append(group_title)
            
            # 子项
            if is_expanded:
                for item_data in group_data["items"]:
                    # 主项
                    is_active = item_data["id"] == active_item
                    main_item = ft.Container(
                        content=ft.Row([
                            ft.Text(
                                item_data["text"],
                                color="#0078D4" if is_active else "#F2F2F2",
                                size=14,
                                weight=ft.FontWeight.BOLD if is_active else ft.FontWeight.NORMAL
                            )
                        ]),
                        padding=ft.Padding(left=40, right=16, top=8, bottom=8),
                        bgcolor="#2D2D2D" if is_active else "transparent",
                        border_radius=4,
                        on_click=lambda e, data=item_data: on_item_click(data)
                    )
                    controls.append(main_item)
                    
                    # 子项的子项
                    if is_active and "subitems" in item_data:
                        for subitem_data in item_data["subitems"]:
                            is_subactive = subitem_data["id"] == active_subitem
                            subitem = ft.Container(
                                content=ft.Row([
                                    ft.Text(
                                        subitem_data["text"],
                                        color="#0078D4" if is_subactive else "#F2F2F2",
                                        size=13
                                    )
                                ]),
                                padding=ft.Padding(left=64, right=16, top=4, bottom=4),
                                bgcolor="#2D2D2D" if is_subactive else "transparent",
                                border_radius=4,
                                on_click=lambda e, data=subitem_data: on_subitem_click(data)
                            )
                            controls.append(subitem)
        
        nav_container.content = ft.Column(controls, spacing=0)
        page.update()
    
    # 分组点击事件
    def on_group_click(group_name):
        """分组点击事件"""
        nonlocal expanded_groups
        if group_name in expanded_groups:
            expanded_groups.remove(group_name)
        else:
            expanded_groups.add(group_name)
        update_navigation()
    
    # 主项点击事件
    def on_item_click(item_data):
        """主项点击事件"""
        nonlocal active_item, active_subitem
        active_item = item_data["id"]
        active_subitem = None
        update_navigation()
        
        # 如果有子项，显示第一个子项的内容
        if "subitems" in item_data and item_data["subitems"]:
            on_subitem_click(item_data["subitems"][0])
    
    # 子项点击事件
    def on_subitem_click(subitem_data):
        """子项点击事件"""
        nonlocal active_subitem
        active_subitem = subitem_data["id"]
        update_navigation()
        
        # 更新内容区域
        content_container.content = get_content(active_subitem)
        page.update()
    
    # 创建主布局
    main_layout = ft.Row([
        # 导航栏
        nav_container,
        # 分隔线
        ft.VerticalDivider(width=1, color="#404040"),
        # 内容区域
        ft.Container(
            content=content_container,
            expand=True,
            bgcolor="#1C1C1C"
        )
    ], spacing=0, expand=True)
    
    # 初始化导航栏
    update_navigation()
    
    # 添加到页面
    page.add(main_layout)


if __name__ == "__main__":
    print("正在启动导航栏功能测试...")
    print("测试步骤:")
    print("1. 点击'系统'分组，展开二级导航")
    print("2. 点击'设备管理'，展开三级导航")
    print("3. 点击'设备列表'，查看内容")
    print("4. 测试其他导航项")
    print("请稍候，界面即将出现...")
    ft.run(main)