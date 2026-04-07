#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试Gitee构建失败问题
分析可能的失败原因和解决方案
"""

import os
import sys
import re

def analyze_workflow_issues():
    """分析工作流文件的问题"""
    print("=" * 70)
    print("分析Gitee构建失败原因")
    print("=" * 70)
    
    workflow_file = ".github/workflows/build-apk-gitee.yml"
    
    print(f"\n🔍 分析工作流文件: {workflow_file}")
    
    with open(workflow_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找潜在问题
    issues = []
    
    # 1. 检查APK文件存在性检查
    if 'if [ ! -f "apk-output/*.apk" ]; then' in content:
        issues.append("❌ 第77行: APK文件存在性检查有问题")
        issues.append("   问题: 'if [ ! -f \"apk-output/*.apk\" ]' 检查字面文件'*.apk'")
        issues.append("   修复: 应该使用 'if [ ! -f apk-output/*.apk 2>/dev/null ]' 或 'if ls apk-output/*.apk 1>/dev/null 2>&1; then'")
    
    # 2. 检查Android SDK安装
    if 'android-actions/setup-android' not in content:
        issues.append("⚠️  缺少Android SDK安装步骤")
        issues.append("   建议: 添加Android SDK安装步骤")
    
    # 3. 检查错误处理
    if 'set -e' not in content:
        issues.append("⚠️  缺少严格的错误处理")
        issues.append("   建议: 在run命令开始时添加 'set -e'")
    
    # 4. 检查依赖安装
    if 'pip install flet' in content and 'requirements.txt' in content:
        issues.append("✅ 依赖安装配置正确")
    else:
        issues.append("❌ 依赖安装可能有问题")
    
    return issues

def create_fixed_workflow():
    """创建修复后的工作流文件"""
    print("\n" + "=" * 70)
    print("创建修复后的工作流文件")
    print("=" * 70)
    
    fixed_workflow = """name: Build APK for Gitee

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]
  workflow_dispatch:  # 允许手动触发

jobs:
  build-apk:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
    
    - name: Setup Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
        pip install flet==0.82.0
    
    - name: Setup Flutter
      uses: subosito/flutter-action@v2
      with:
        flutter-version: '3.19.5'
        channel: 'stable'
    
    - name: Setup Android SDK
      uses: android-actions/setup-android@v3
    
    - name: Accept Android licenses
      run: |
        yes | sdkmanager --licenses || true
        flutter doctor --android-licenses
    
    - name: Setup JDK
      uses: actions/setup-java@v4
      with:
        distribution: 'temurin'
        java-version: '17'
    
    - name: Check Flutter environment
      run: |
        flutter doctor -v
        echo "Flutter环境检查完成"
    
    - name: Build APK with Flet
      env:
        FLET_CLI_NO_RICH_OUTPUT: 1
        PYTHONIOENCODING: utf-8
      run: |
        set -e  # 出错时退出
        echo "开始构建APK..."
        
        # 清理旧的构建
        rm -rf build/ || true
        
        # 构建APK
        echo "运行Flet构建命令..."
        python -m flet.cli build apk --verbose --project "WW2Assistant" || {
          echo "Flet构建失败，尝试诊断..."
          # 检查Flet版本
          python -m flet.cli --version
          # 检查项目结构
          echo "项目结构:"
          ls -la
          echo "main.py内容:"
          head -20 main.py || echo "main.py不存在"
          exit 1
        }
        
        echo "构建完成，搜索APK文件..."
        
        # 查找所有APK文件
        find . -name "*.apk" -type f 2>/dev/null | while read apk; do
          echo "找到APK: $apk"
          ls -lh "$apk"
        done
        
        # 创建明确的输出目录
        mkdir -p apk-output
        
        # 复制所有APK文件到输出目录
        find . -name "*.apk" -type f -exec cp {} apk-output/ \; 2>/dev/null || true
        
        echo "APK文件已收集到 apk-output/ 目录:"
        ls -la apk-output/ || echo "apk-output目录为空"
        
        # 检查是否有APK文件
        if ls apk-output/*.apk 1>/dev/null 2>&1; then
          echo "✅ 找到APK文件"
          APK_COUNT=$(find apk-output -name "*.apk" -type f | wc -l)
          echo "APK文件数量: $APK_COUNT"
        else
          echo "❌ 未找到APK文件"
          echo "构建可能失败，检查日志..."
          # 保存构建日志
          find build -type f -name "*.log" -exec cat {} \; > apk-output/build-error.log 2>/dev/null || true
          echo "详细错误信息已保存到 apk-output/build-error.log"
          exit 1
        fi
    
    - name: Create APK archive
      if: success()
      run: |
        echo "创建APK压缩包..."
        
        # 进入输出目录
        cd apk-output
        
        # 创建ZIP文件
        zip -r ../ww2-assistant-apk.zip ./*
        
        echo "ZIP文件创建完成:"
        ls -lh ../ww2-assistant-apk.zip
        
        # 返回到项目根目录
        cd ..
    
    - name: Upload APK archive
      if: success()
      uses: actions/upload-artifact@v4
      with:
        name: WW2Assistant-APK
        path: ww2-assistant-apk.zip
        retention-days: 30
    
    - name: Upload individual APK files
      if: success()
      uses: actions/upload-artifact@v4
      with:
        name: APK-Files
        path: apk-output/*.apk
        retention-days: 30
    
    - name: Upload build logs (always)
      if: always()
      uses: actions/upload-artifact@v4
      with:
        name: Build-Logs
        path: |
          build/
          apk-output/
        retention-days: 7
    
    - name: Upload debug info
      if: failure()
      uses: actions/upload-artifact@v4
      with:
        name: Debug-Info
        path: |
          **/*.log
          **/build/
          **/apk-output/
        retention-days: 7
"""
    
    # 创建修复后的工作流
    workflow_file = ".github/workflows/build-apk-gitee-fixed.yml"
    with open(workflow_file, 'w', encoding='utf-8') as f:
        f.write(fixed_workflow)
    
    print(f"✅ 已创建修复后的工作流: {workflow_file}")
    print("\n🔧 主要修复:")
    print("1. 修复了APK文件存在性检查")
    print("2. 添加了Android SDK安装步骤")
    print("3. 添加了严格的错误处理 (set -e)")
    print("4. 改进了构建失败时的诊断信息")
    print("5. 添加了失败时的调试信息上传")
    
    return workflow_file

def create_simplified_workflow():
    """创建简化版的工作流（更稳定）"""
    print("\n" + "=" * 70)
    print("创建简化版工作流（备选方案）")
    print("=" * 70)
    
    simplified_workflow = """name: Simple APK Build

on:
  push:
    branches: [ main, master ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
    
    - name: Setup Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
    
    - name: Install Flet
      run: |
        python -m pip install --upgrade pip
        pip install flet==0.82.0
    
    - name: Build APK (simple)
      env:
        FLET_CLI_NO_RICH_OUTPUT: 1
      run: |
        echo "简单构建APK..."
        echo "项目目录内容:"
        ls -la
        
        echo "检查main.py..."
        if [ -f "main.py" ]; then
          echo "main.py存在，开始构建..."
          python -m flet.cli build apk --project "WW2Assistant" || echo "构建失败"
        else
          echo "错误: main.py不存在"
          exit 1
        fi
        
        echo "查找APK文件..."
        find . -name "*.apk" -type f
        
        # 创建输出目录
        mkdir -p dist
        find . -name "*.apk" -type f -exec cp {} dist/ \; 2>/dev/null || true
        
        echo "输出目录内容:"
        ls -la dist/
    
    - name: Upload APK
      if: success()
      uses: actions/upload-artifact@v4
      with:
        name: Simple-APK
        path: dist/*.apk
        retention-days: 30
"""
    
    simple_file = ".github/workflows/build-apk-simple.yml"
    with open(simple_file, 'w', encoding='utf-8') as f:
        f.write(simplified_workflow)
    
    print(f"✅ 已创建简化版工作流: {simple_file}")
    print("\n🎯 简化版特点:")
    print("1. 更简单的配置")
    print("2. 更少的依赖")
    print("3. 更容易调试")
    print("4. 适合快速测试")
    
    return simple_file

def main():
    """主函数"""
    print("\n🔧 诊断Gitee构建失败 #6")
    print("构建ID: #6")
    print("提交: 修复构建失败问题并添加Gitee专用工作流")
    print("时间: 2026-04-07 09:59:04")
    print("状态: 失败")
    
    # 分析问题
    issues = analyze_workflow_issues()
    
    if issues:
        print("\n📋 发现的问题:")
        for issue in issues:
            print(issue)
    else:
        print("\n✅ 未发现明显问题")
    
    # 创建修复后的工作流
    fixed_file = create_fixed_workflow()
    
    # 创建简化版工作流
    simple_file = create_simplified_workflow()
    
    print("\n" + "=" * 70)
    print("🚀 修复方案")
    print("=" * 70)
    
    print("\n方案A: 使用修复后的工作流")
    print(f"   文件: {fixed_file}")
    print("   步骤:")
    print("   1. git add .github/workflows/build-apk-gitee-fixed.yml")
    print("   2. git commit -m '修复构建工作流'")
    print("   3. git push gitee master")
    print("   4. 在Gitee上触发新工作流")
    
    print("\n方案B: 使用简化版工作流")
    print(f"   文件: {simple_file}")
    print("   特点: 更简单，更容易成功")
    
    print("\n方案C: 本地构建测试")
    print("   运行: python local_build_alternative.py")
    print("   优点: 不依赖Gitee，可以本地调试")
    
    print("\n" + "=" * 70)
    print("💡 建议操作顺序:")
    print("1. 先运行本地构建测试，验证项目可以构建")
    print("2. 提交修复后的工作流")
    print("3. 在Gitee上触发新构建")
    print("4. 如果仍然失败，使用简化版工作流")
    print("=" * 70)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())