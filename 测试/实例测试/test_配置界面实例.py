#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置界面实例测试

创建日期: 2026-03-08
作者: AI
版本: v1.0.0

说明：模拟游戏辅助工具的配置界面
"""

import flet as ft


def main(page: ft.Page):
    """主函数 - 创建配置界面"""
    
    page.title = "游戏辅助工具 - 配置界面"
    page.window_width = 900
    page.window_height = 700
    page.padding = 20
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # 状态栏
    status_bar = ft.Text(
        "状态: 就绪",
        size=14,
        color=ft.colors.GREEN,
        weight=ft.FontWeight.BOLD
    )
    
    def update_status(message, color=ft.colors.GREEN):
        """更新状态栏"""
        status_bar.value = f"状态: {message}"
        status_bar.color = color
        page.update()
    
    # ========== 游戏设置区域 ==========
    game_path_input = ft.TextField(
        label="游戏路径",
        hint_text="选择游戏可执行文件...",
        width=500,
        prefix_icon=ft.icons.FOLDER_OPEN,
        read_only=True
    )
    
    def on_browse_game(e):
        """浏览游戏文件"""
        file_picker = ft.FilePicker()
        page.overlay.append(file_picker)
        page.update()
        # 模拟选择文件
        game_path_input.value = "C:/Games/二战风云/game.exe"
        update_status("游戏路径已设置")
        page.update()
    
    browse_game_btn = ft.IconButton(
        icon=ft.icons.FOLDER_OPEN,
        tooltip="浏览",
        on_click=on_browse_game
    )
    
    device_id_input = ft.TextField(
        label="设备ID",
        value="emulator-5554",
        width=300,
        prefix_icon=ft.icons.DEVICES
    )
    
    timeout_input = ft.TextField(
        label="连接超时(秒)",
        value="30",
        width=150,
        prefix_icon=ft.icons.TIMER,
        keyboard_type=ft.KeyboardType.NUMBER
    )
    
    # ========== 脚本设置区域 ==========
    delay_slider = ft.Slider(
        min=0.5,
        max=5.0,
        divisions=9,
        value=1.5,
        label="{value}秒",
        width=400
    )
    
    delay_value_text = ft.Text("1.5秒", size=16, weight=ft.FontWeight.BOLD)
    
    def on_delay_change(e):
        """延迟滑块变化"""
        delay_value_text.value = f"{delay_slider.value}秒"
        page.update()
    
    delay_slider.on_change = on_delay_change
    
    auto_run_switch = ft.Switch(
        label="自动运行",
        value=False
    )
    
    run_mode_dropdown = ft.Dropdown(
        label="运行模式",
        width=200,
        options=[
            ft.dropdown.Option("手动", "手动模式"),
            ft.dropdown.Option("自动", "自动模式"),
            ft.dropdown.Option("定时", "定时模式"),
        ],
        value="手动"
    )
    
    max_duration_input = ft.TextField(
        label="最大运行时长(小时)",
        value="12",
        width=200,
        prefix_icon=ft.icons.TIMELAPSE,
        keyboard_type=ft.KeyboardType.NUMBER
    )
    
    # ========== 界面设置区域 ==========
    theme_dropdown = ft.Dropdown(
        label="主题",
        width=200,
        options=[
            ft.dropdown.Option("浅色", "浅色主题"),
            ft.dropdown.Option("深色", "深色主题"),
            ft.dropdown.Option("自动", "跟随系统"),
        ],
        value="浅色"
    )
    
    language_dropdown = ft.Dropdown(
        label="语言",
        width=200,
        options=[
            ft.dropdown.Option("中文", "简体中文"),
            ft.dropdown.Option("英文", "English"),
        ],
        value="中文"
    )
    
    # ========== 按钮 ==========
    def on_save(e):
        """保存配置"""
        update_status("配置保存成功！", ft.colors.GREEN)
        # 显示成功提示
        page.show_snack_bar(
            ft.SnackBar(
                content=ft.Text("✅ 配置已保存"),
                action="确定",
                bgcolor=ft.colors.GREEN
            )
        )
    
    def on_reset(e):
        """重置配置"""
        game_path_input.value = ""
        device_id_input.value = "emulator-5554"
        timeout_input.value = "30"
        delay_slider.value = 1.5
        delay_value_text.value = "1.5秒"
        auto_run_switch.value = False
        run_mode_dropdown.value = "手动"
        max_duration_input.value = "12"
        theme_dropdown.value = "浅色"
        language_dropdown.value = "中文"
        update_status("配置已重置", ft.colors.ORANGE)
        page.update()
    
    def on_test(e):
        """测试连接"""
        update_status("正在测试连接...", ft.colors.BLUE)
        # 模拟测试过程
        import time
        time.sleep(1)
        update_status("连接测试成功！", ft.colors.GREEN)
        page.show_snack_bar(
            ft.SnackBar(
                content=ft.Text("✅ 连接测试成功"),
                bgcolor=ft.colors.GREEN
            )
        )
    
    save_btn = ft.ElevatedButton(
        "保存配置",
        icon=ft.icons.SAVE,
        on_click=on_save,
        style=ft.ButtonStyle(
            bgcolor=ft.colors.GREEN,
            color=ft.colors.WHITE
        ),
        width=150,
        height=45
    )
    
    reset_btn = ft.ElevatedButton(
        "重置",
        icon=ft.icons.REFRESH,
        on_click=on_reset,
        width=120,
        height=45
    )
    
    test_btn = ft.ElevatedButton(
        "测试连接",
        icon=ft.icons.NETWORK_CHECK,
        on_click=on_test,
        style=ft.ButtonStyle(
            bgcolor=ft.colors.BLUE,
            color=ft.colors.WHITE
        ),
        width=150,
        height=45
    )
    
    # ========== 布局 ==========
    page.add(
        ft.Column(
            [
                # 标题
                ft.Row(
                    [
                        ft.Icon(ft.icons.SETTINGS_APPLICATIONS, size=40, color=ft.colors.BLUE),
                        ft.Text("游戏辅助工具配置", size=28, weight=ft.FontWeight.BOLD),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10
                ),
                
                ft.Divider(),
                
                # 游戏设置卡片
                ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.Icon(ft.icons.GAMEPAD, color=ft.colors.BLUE),
                                        ft.Text("游戏设置", size=20, weight=ft.FontWeight.BOLD),
                                    ],
                                    spacing=10
                                ),
                                ft.Row([game_path_input, browse_game_btn]),
                                ft.Row([device_id_input, timeout_input]),
                            ],
                            spacing=15
                        ),
                        padding=20
                    ),
                    width=800
                ),
                
                # 脚本设置卡片
                ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.Icon(ft.icons.CODE, color=ft.colors.ORANGE),
                                        ft.Text("脚本设置", size=20, weight=ft.FontWeight.BOLD),
                                    ],
                                    spacing=10
                                ),
                                ft.Row(
                                    [
                                        ft.Text("脚本延迟:"),
                                        delay_slider,
                                        delay_value_text
                                    ],
                                    spacing=10
                                ),
                                ft.Row([auto_run_switch, run_mode_dropdown, max_duration_input]),
                            ],
                            spacing=15
                        ),
                        padding=20
                    ),
                    width=800
                ),
                
                # 界面设置卡片
                ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.Icon(ft.icons.PALETTE, color=ft.colors.PURPLE),
                                        ft.Text("界面设置", size=20, weight=ft.FontWeight.BOLD),
                                    ],
                                    spacing=10
                                ),
                                ft.Row([theme_dropdown, language_dropdown]),
                            ],
                            spacing=15
                        ),
                        padding=20
                    ),
                    width=800
                ),
                
                ft.Divider(),
                
                # 按钮区域
                ft.Row(
                    [save_btn, reset_btn, test_btn],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20
                ),
                
                # 状态栏
                ft.Container(
                    content=status_bar,
                    bgcolor=ft.colors.BLACK12,
                    padding=10,
                    border_radius=5,
                    width=800
                ),
            ],
            spacing=15,
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )
    )


if __name__ == "__main__":
    print("正在启动配置界面测试...")
    print("请稍候，界面即将出现...")
    ft.app(target=main)
