#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
监控Gitee/GitHub Actions构建状态
"""

import os
import time
import webbrowser
import sys

def open_gitee_actions():
    """打开Gitee Actions页面"""
    gitee_url = "https://gitee.com/lzhuohui/ww2_assistant/actions"
    print(f"打开Gitee Actions页面: {gitee_url}")
    webbrowser.open(gitee_url)
    
def open_github_actions():
    """打开GitHub Actions页面"""
    github_url = "https://github.com/lzhuohui/ww2_assistant/actions"
    print(f"打开GitHub Actions页面: {github_url}")
    webbrowser.open(github_url)

def check_build_status():
    """检查构建状态"""
    print("=" * 60)
    print("APK自动构建监控")
    print("=" * 60)
    print()
    print("✅ 已完成以下步骤：")
    print("1. 创建了GitHub Actions工作流文件 (.github/workflows/build-apk.yml)")
    print("2. 提交了更改到Git仓库")
    print("3. 推送到Gitee镜像 (lzhuohui/ww2_assistant)")
    print()
    print("📱 现在你需要：")
    print("1. 打开浏览器访问 https://gitee.com/lzhuohui/ww2_assistant")
    print("2. 点击 'Actions' 标签页")
    print("3. 找到 'Build APK' 工作流")
    print("4. 点击 'Run workflow' 按钮（手动触发构建）")
    print()
    print("🔧 GitHub Actions工作流配置：")
    print("- 触发条件: push到main/master分支 或 手动触发")
    print("- 构建环境: Ubuntu最新版")
    print("- 构建步骤:")
    print("  1. 检出代码")
    print("  2. 设置Python环境 (3.11)")
    print("  3. 安装依赖")
    print("  4. 设置Flutter环境")
    print("  5. 接受Android许可")
    print("  6. 安装Android SDK和JDK")
    print("  7. 构建APK")
    print("  8. 上传APK作为构建产物")
    print()
    print("📦 构建产物：")
    print("- APK文件将作为构建产物提供下载")
    print("- 在Actions页面点击构建完成后的工作流")
    print("- 在 'Artifacts' 部分下载 ww2-assistant-apk")
    print()
    print("⏱️ 构建时间：")
    print("- 预计构建时间: 15-30分钟（首次构建可能需要更长时间）")
    print()

def create_gitee_workflow():
    """为Gitee创建专用的工作流文件"""
    gitee_workflow = """name: Build APK (Gitee)

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]
  workflow_dispatch:  # 允许手动触发

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout repository
      uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
    
    - name: Install Python dependencies
      run: |
        python -m pip install --upgrade pip
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
        pip install flet==0.82.0
    
    - name: Set up Flutter
      uses: subosito/flutter-action@v2
      with:
        flutter-version: '3.19.5'
        channel: 'stable'
    
    - name: Accept Android licenses
      run: |
        yes | sdkmanager --licenses || true
        flutter doctor --android-licenses
    
    - name: Install Android SDK
      uses: android-actions/setup-android@v3
    
    - name: Set up JDK
      uses: actions/setup-java@v4
      with:
        distribution: 'temurin'
        java-version: '17'
    
    - name: Check Flutter environment
      run: |
        flutter doctor -v
    
    - name: Build APK
      env:
        FLET_CLI_NO_RICH_OUTPUT: 1
        PYTHONIOENCODING: utf-8
      run: |
        # 清理之前的构建目录
        rm -rf build/
        
        # 构建APK
        echo "开始构建APK..."
        python -m flet.cli build apk --verbose --project "WW2Assistant"
        
        # 检查构建结果
        echo "检查构建结果..."
        if [ -d "build/apk" ]; then
          echo "APK构建成功！"
          ls -la build/apk/
        else
          echo "APK构建失败！"
          exit 1
        fi
    
    - name: Upload APK as artifact
      if: success()
      uses: actions/upload-artifact@v4
      with:
        name: ww2-assistant-apk
        path: build/apk/*.apk
        retention-days: 7
"""
    
    workflow_dir = ".github/workflows"
    workflow_file = os.path.join(workflow_dir, "build-apk-gitee.yml")
    
    # 确保目录存在
    os.makedirs(workflow_dir, exist_ok=True)
    
    with open(workflow_file, 'w', encoding='utf-8') as f:
        f.write(gitee_workflow)
    
    print(f"✅ 已创建Gitee专用工作流文件: {workflow_file}")
    return workflow_file

def main():
    """主函数"""
    check_build_status()
    
    # 询问用户是否要打开网页
    print("是否要打开Gitee Actions页面？ (y/n): ", end="")
    choice = input().strip().lower()
    
    if choice in ['y', 'yes', '是']:
        open_gitee_actions()
    
    # 询问是否创建Gitee专用工作流
    print("\n是否要为Gitee创建专用工作流文件？ (y/n): ", end="")
    gitee_choice = input().strip().lower()
    
    if gitee_choice in ['y', 'yes', '是']:
        create_gitee_workflow()
        print("\n✅ Gitee专用工作流已创建")
        print("请提交并推送这个新文件到仓库")
    
    print("\n🎯 下一步操作：")
    print("1. 访问 https://gitee.com/lzhuohui/ww2_assistant")
    print("2. 手动触发构建")
    print("3. 等待构建完成")
    print("4. 下载生成的APK文件")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())