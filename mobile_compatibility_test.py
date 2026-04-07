# -*- coding: utf-8 -*-
"""
移动设备兼容性测试脚本
用于测试应用在移动设备上的UI适配性
"""

import flet as ft
from 设置界面.层级1_主入口.主入口 import MainEntry
from 设置界面.层级0_数据管理.配置管理 import ConfigManager


def test_mobile_layout(page: ft.Page):
    """测试移动设备布局兼容性"""
    
    # 模拟不同移动设备分辨率
    mobile_resolutions = [
        {"name": "iPhone 12", "width": 390, "height": 844},
        {"name": "Galaxy S21", "width": 411, "height": 914},
        {"name": "Pixel 6", "width": 393, "height": 851},
        {"name": "iPad Pro", "width": 1024, "height": 1366},
        {"name": "Galaxy Tab S7", "width": 1080, "height": 1920},
    ]
    
    results = []
    
    for device in mobile_resolutions:
        print(f"\n=== 测试设备: {device['name']} ({device['width']}x{device['height']}) ===")
        
        # 创建模拟页面
        test_page = ft.Page()
        test_page.window.width = device["width"]
        test_page.window.height = device["height"]
        
        try:
            # 测试主入口初始化
            main_entry = MainEntry(test_page)
            
            # 检查UI组件是否渲染正常
            if hasattr(main_entry, '_main_column'):
                results.append({
                    "device": device["name"],
                    "resolution": f"{device['width']}x{device['height']}",
                    "status": "✅ 通过",
                    "issues": []
                })
                print(f"✅ {device['name']}: 界面初始化成功")
            else:
                results.append({
                    "device": device["name"],
                    "resolution": f"{device['width']}x{device['height']}",
                    "status": "❌ 失败",
                    "issues": ["主列未创建"]
                })
                print(f"❌ {device['name']}: 主列未创建")
                
        except Exception as e:
            results.append({
                "device": device["name"],
                "resolution": f"{device['width']}x{device['height']}",
                "status": "❌ 异常",
                "issues": [str(e)]
            })
            print(f"❌ {device['name']}: 异常 - {e}")
    
    return results


def check_mobile_issues():
    """检查移动设备潜在问题"""
    print("\n=== 移动设备兼容性检查 ===")
    
    issues = []
    
    # 1. 检查UI固定尺寸问题
    print("1. 检查UI固定尺寸问题...")
    from 设置界面.层级1_主入口.主入口 import MainEntry
    
    # 分析主入口的_setup_page方法中的固定尺寸
    try:
        import inspect
        source = inspect.getsource(MainEntry._setup_page)
        if "self._page.width = 1200" in source or "self._page.height = 540" in source:
            issues.append("发现固定尺寸设置：主入口设置了固定宽高1200x540，需要调整为响应式设计")
            print("⚠️ 发现固定宽高设置：1200x540")
    except:
        pass
    
    # 2. 检查导航栏尺寸
    print("2. 检查导航栏尺寸...")
    config_manager = ConfigManager()
    nav_width = config_manager.get_ui_config("导航", "宽度")
    if nav_width and nav_width > 300:
        issues.append(f"导航栏宽度({nav_width})较大，可能影响移动设备显示")
        print(f"⚠️ 导航栏宽度可能过大: {nav_width}")
    
    # 3. 检查字体大小配置
    print("3. 检查字体大小配置...")
    font_size = config_manager.get_nav_config("字体大小", 14)
    if font_size > 16:
        issues.append(f"导航字体大小({font_size})较大，建议调整为14-16")
        print(f"⚠️ 导航字体大小: {font_size}")
    
    icon_size = config_manager.get_nav_config("图标大小", 20)
    if icon_size > 24:
        issues.append(f"图标大小({icon_size})较大，建议调整为18-24")
        print(f"⚠️ 图标大小: {icon_size}")
    
    # 4. 检查界面配置
    print("4. 检查界面配置...")
    interface_names = config_manager.get_interface_names()
    if len(interface_names) > 8:
        issues.append(f"界面数量较多({len(interface_names)})，移动设备导航栏可能过长")
        print(f"⚠️ 界面数量: {len(interface_names)}")
    
    return issues


def main(page: ft.Page):
    """主测试函数"""
    page.title = "移动设备兼容性测试"
    page.theme_mode = ft.ThemeMode.DARK
    
    results = test_mobile_layout(page)
    
    # 显示测试结果
    result_texts = []
    for result in results:
        result_texts.append(f"{result['device']} ({result['resolution']}): {result['status']}")
        if result['issues']:
            for issue in result['issues']:
                result_texts.append(f"  - {issue}")
    
    # 检查潜在问题
    issues = check_mobile_issues()
    
    # 创建UI显示结果
    content = ft.Column([
        ft.Text("移动设备兼容性测试结果", size=24, weight=ft.FontWeight.BOLD),
        ft.Divider(height=20),
        ft.Text("设备测试结果:", size=18, weight=ft.FontWeight.BOLD),
        ft.Column([
            ft.Text(text, size=14) for text in result_texts
        ], spacing=5),
        ft.Divider(height=20),
        ft.Text("潜在兼容性问题:", size=18, weight=ft.FontWeight.BOLD),
    ])
    
    if issues:
        for issue in issues:
            content.controls.append(ft.Text(f"• {issue}", size=14, color=ft.Colors.ORANGE))
    else:
        content.controls.append(ft.Text("✅ 未发现明显兼容性问题", size=14, color=ft.Colors.GREEN))
    
    page.add(ft.Container(
        content=content,
        padding=20,
        expand=True,
    ))
    
    # 打印详细结果
    print("\n" + "="*50)
    print("移动设备兼容性测试总结:")
    print("="*50)
    for result in results:
        print(f"{result['device']} ({result['resolution']}): {result['status']}")
    
    if issues:
        print(f"\n发现 {len(issues)} 个潜在问题:")
        for issue in issues:
            print(f"  • {issue}")
    else:
        print("\n✅ 所有测试通过，未发现兼容性问题")
    
    # 建议修复
    print("\n" + "="*50)
    print("建议修复方案:")
    print("="*50)
    print("1. 修改主入口_setup_page方法，移除固定尺寸设置")
    print("2. 使用ft.ResponsiveRow和ft.ResponsiveColumn代替固定布局")
    print("3. 为移动设备添加媒体查询或平台检测")
    print("4. 调整导航栏宽度为相对值（如百分比）")
    print("5. 考虑使用ft.View实现多页面导航")
    print("6. 为小屏幕设备调整字体和图标大小")


if __name__ == "__main__":
    ft.run(main)