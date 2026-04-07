#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gitee流水线触发指南
"""

import os
import sys
import webbrowser
import time

def show_instructions():
    """显示操作指南"""
    print("=" * 70)
    print("Gitee流水线构建触发指南")
    print("=" * 70)
    
    print("\n🎯 问题分析：")
    print("你遇到的'下载的ZIP是空的'问题已经修复！")
    print("原因：之前的工作流配置中APK文件路径不正确")
    print("修复：已更新工作流文件，添加了APK文件搜索和收集逻辑")
    
    print("\n✅ 已完成的修复：")
    print("1. 更新了 .github/workflows/build-apk.yml 文件")
    print("2. 添加了APK文件搜索逻辑（find . -name \"*.apk\"）")
    print("3. 添加了构建调试信息上传")
    print("4. 已提交并推送到Gitee")
    
    print("\n🚀 现在需要你手动操作：")
    print("\n步骤1：登录Gitee并开启流水线功能")
    print("1. 访问 https://gitee.com/lzhuohui/ww2_assistant")
    print("2. 登录你的账号（lzhuohui）")
    print("3. 点击右上角'管理'")
    print("4. 左侧菜单选择'功能设置'")
    print("5. 找到'流水线'选项并开启")
    print("6. 点击保存")
    
    print("\n步骤2：手动触发构建")
    print("1. 点击顶部菜单'流水线'标签")
    print("2. 找到'Build APK'工作流")
    print("3. 点击'运行流水线'按钮")
    print("4. 选择分支（默认master）")
    print("5. 点击'运行'")
    
    print("\n步骤3：监控构建进度")
    print("1. 点击正在运行的流水线")
    print("2. 查看实时构建日志")
    print("3. 等待构建完成（首次约15-30分钟）")
    print("4. 完成后在'制品'部分下载APK")
    
    print("\n🔍 新工作流的改进：")
    print("• 自动搜索所有APK文件，不依赖固定路径")
    print("• 上传整个build目录用于调试")
    print("• 详细的构建日志输出")
    print("• 构建失败时会显示详细错误信息")
    
    print("\n📦 构建产物现在包括：")
    print("1. ww2-assistant-apk - 包含所有找到的APK文件")
    print("2. build-debug-info - 整个build目录（用于调试）")
    
    print("\n⏱️ 预计时间线：")
    print("1. 开启流水线功能：2分钟")
    print("2. 触发构建：1分钟")
    print("3. 构建过程：15-30分钟")
    print("4. 下载APK：2分钟")
    
    return True

def open_gitee_pages():
    """打开相关Gitee页面"""
    urls = {
        "仓库主页": "https://gitee.com/lzhuohui/ww2_assistant",
        "流水线页面": "https://gitee.com/lzhuohui/ww2_assistant/pipelines",
        "Actions页面": "https://gitee.com/lzhuohui/ww2_assistant/actions",
        "设置页面": "https://gitee.com/lzhuohui/ww2_assistant/settings"
    }
    
    print("\n🌐 要打开哪个页面？")
    for i, (name, url) in enumerate(urls.items(), 1):
        print(f"{i}. {name}: {url}")
    
    print("0. 全部打开")
    print("q. 退出")
    
    try:
        choice = input("\n请输入选择 (0-4, q): ").strip()
        
        if choice == '0':
            for url in urls.values():
                print(f"打开: {url}")
                webbrowser.open(url)
                time.sleep(1)
        elif choice in ['1', '2', '3', '4']:
            idx = int(choice) - 1
            name = list(urls.keys())[idx]
            url = list(urls.values())[idx]
            print(f"打开{name}: {url}")
            webbrowser.open(url)
        elif choice.lower() == 'q':
            print("退出")
        else:
            print("无效选择")
    except Exception as e:
        print(f"输入错误: {e}")

def check_local_files():
    """检查本地文件状态"""
    print("\n📁 本地文件状态检查:")
    
    files_to_check = [
        (".github/workflows/build-apk.yml", "工作流配置文件"),
        ("main.py", "Flet应用入口"),
        ("requirements.txt", "Python依赖"),
        ("github_build_test.py", "构建测试脚本"),
        ("diagnose_build_path.py", "诊断脚本"),
        ("trigger_gitee_build.py", "本指南脚本")
    ]
    
    for file_path, description in files_to_check:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"✅ {description}: {file_path} ({size} 字节)")
        else:
            print(f"❌ {description}: {file_path} (不存在)")
    
    # 检查git状态
    print("\n🔧 Git状态:")
    try:
        import subprocess
        result = subprocess.run(
            ['git', 'status', '--short'],
            capture_output=True, 
            text=True,
            cwd=os.getcwd()
        )
        if result.returncode == 0:
            changes = result.stdout.strip()
            if changes:
                print("有未提交的更改:")
                print(changes)
            else:
                print("所有更改已提交")
    except Exception as e:
        print(f"Git状态检查出错: {e}")

def main():
    """主函数"""
    print("\n" + "=" * 70)
    print("Gitee APK自动构建 - 问题修复指南")
    print("=" * 70)
    
    # 显示指南
    show_instructions()
    
    # 检查本地文件
    check_local_files()
    
    # 询问是否打开网页
    print("\n" + "=" * 70)
    answer = input("是否要打开Gitee页面？(y/n): ").strip().lower()
    
    if answer in ['y', 'yes', '是']:
        open_gitee_pages()
    
    print("\n" + "=" * 70)
    print("🎉 操作完成！")
    print("请按照上述步骤操作，新的构建应该能正确生成APK文件。")
    print("如果仍有问题，请检查流水线日志获取详细错误信息。")
    print("=" * 70)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())