#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查Gitee流水线构建产物问题
解决"备份"而不是APK的问题
"""

import os
import sys
import re

def analyze_gitee_workflow():
    """分析Gitee工作流配置"""
    print("=" * 70)
    print("分析Gitee流水线构建产物问题")
    print("=" * 70)
    
    workflow_file = ".github/workflows/build-apk.yml"
    
    if not os.path.exists(workflow_file):
        print(f"❌ 工作流文件不存在: {workflow_file}")
        return False
    
    print(f"\n📋 分析工作流文件: {workflow_file}")
    
    with open(workflow_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查上传artifact的配置
    print("\n🔍 检查构建产物上传配置:")
    
    # 查找所有upload-artifact步骤
    upload_pattern = r'- name: [^\n]*upload[^\n]*artifact[^\n]*\n(?:[ \t]+[^\n]*\n)*'
    upload_matches = re.findall(upload_pattern, content, re.IGNORECASE)
    
    if not upload_matches:
        print("❌ 未找到upload-artifact配置")
    else:
        for i, match in enumerate(upload_matches, 1):
            print(f"\n📦 上传配置 {i}:")
            lines = match.strip().split('\n')
            for line in lines:
                if 'name:' in line:
                    print(f"  名称: {line.split('name:')[1].strip()}")
                elif 'path:' in line:
                    print(f"  路径: {line.split('path:')[1].strip()}")
                elif 'uses:' in line and 'upload-artifact' in line:
                    print(f"  动作: {line.split('uses:')[1].strip()}")
    
    # 检查Gitee特定的配置问题
    print("\n🔍 检查可能的问题:")
    
    # 1. 检查路径配置
    if 'path: artifacts/' in content:
        print("✅ 使用artifacts/目录收集文件")
    else:
        print("⚠️  可能不是使用artifacts/目录")
    
    # 2. 检查是否上传了正确的文件
    apk_patterns = [
        r'path:.*\.apk',
        r'path:.*\*\.apk',
        r'path: artifacts/'
    ]
    
    found_apk_path = False
    for pattern in apk_patterns:
        if re.search(pattern, content):
            found_apk_path = True
            break
    
    if found_apk_path:
        print("✅ 配置了APK文件上传路径")
    else:
        print("⚠️  可能没有正确配置APK文件上传路径")
    
    # 3. 检查Gitee特定的问题
    print("\n🎯 Gitee流水线可能的问题:")
    print("1. Gitee可能将构建产物标记为'备份'而不是实际名称")
    print("2. Gitee的artifact命名可能与GitHub不同")
    print("3. 可能需要特定的Gitee Actions配置")
    
    return True

def check_apk_output_directories():
    """检查APK可能的输出目录"""
    print("\n" + "=" * 70)
    print("检查Flet APK输出目录结构")
    print("=" * 70)
    
    # Flet可能的APK输出路径
    possible_paths = [
        "build/apk/",
        "build/android/",
        "build/android/app/build/outputs/apk/",
        "build/android/app/build/outputs/bundle/",
        "build/app/outputs/flutter-apk/",
        "build/app/outputs/apk/",
        "build/outputs/apk/",
        "build/outputs/flutter-apk/",
        "android/app/build/outputs/apk/",
        "android/app/build/outputs/bundle/",
        "app/build/outputs/apk/",
        "app/build/outputs/flutter-apk/"
    ]
    
    print("\n📁 Flet APK可能的输出路径:")
    for path in possible_paths:
        if os.path.exists(path):
            print(f"✅ {path}")
            # 列出文件
            try:
                for root, dirs, files in os.walk(path):
                    for file in files:
                        if file.endswith('.apk'):
                            full_path = os.path.join(root, file)
                            size = os.path.getsize(full_path) / (1024*1024)  # MB
                            print(f"   📱 {file} ({size:.2f} MB)")
            except:
                pass
        else:
            print(f"❌ {path} (不存在)")
    
    return True

def create_gitee_specific_workflow():
    """创建Gitee专用工作流文件"""
    print("\n" + "=" * 70)
    print("创建Gitee专用工作流配置")
    print("=" * 70)
    
    gitee_workflow = """name: Build APK for Gitee

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
    
    - name: Accept Android licenses
      run: |
        yes | sdkmanager --licenses || true
        flutter doctor --android-licenses
    
    - name: Setup JDK
      uses: actions/setup-java@v4
      with:
        distribution: 'temurin'
        java-version: '17'
    
    - name: Build APK with Flet
      env:
        FLET_CLI_NO_RICH_OUTPUT: 1
        PYTHONIOENCODING: utf-8
      run: |
        echo "开始构建APK..."
        
        # 清理旧的构建
        rm -rf build/ || true
        
        # 构建APK
        python -m flet.cli build apk --verbose --project "WW2Assistant"
        
        echo "构建完成，搜索APK文件..."
        
        # 查找所有APK文件
        find . -name "*.apk" -type f | while read apk; do
          echo "找到APK: $apk"
          ls -lh "$apk"
        done
        
        # 创建明确的输出目录
        mkdir -p apk-output
        
        # 复制所有APK文件到输出目录
        find . -name "*.apk" -type f -exec cp {} apk-output/ \;
        
        echo "APK文件已收集到 apk-output/ 目录:"
        ls -la apk-output/
        
        # 如果没有找到APK，创建错误标记
        if [ ! -f "apk-output/*.apk" ]; then
          echo "错误: 未找到APK文件"
          echo "构建日志:" > apk-output/build-error.log
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
    
    - name: Upload build logs
      if: always()
      uses: actions/upload-artifact@v4
      with:
        name: Build-Logs
        path: |
          build/
          **/*.log
        retention-days: 7
"""
    
    # 创建Gitee专用工作流文件
    workflow_dir = ".github/workflows"
    workflow_file = os.path.join(workflow_dir, "build-apk-gitee.yml")
    
    os.makedirs(workflow_dir, exist_ok=True)
    
    with open(workflow_file, 'w', encoding='utf-8') as f:
        f.write(gitee_workflow)
    
    print(f"✅ 已创建Gitee专用工作流: {workflow_file}")
    print("\n🎯 这个工作流的改进:")
    print("1. 明确创建 apk-output/ 目录收集APK文件")
    print("2. 创建单独的ZIP文件: ww2-assistant-apk.zip")
    print("3. 上传多个构建产物:")
    print("   - WW2Assistant-APK: 完整的ZIP包")
    print("   - APK-Files: 单独的APK文件")
    print("   - Build-Logs: 构建日志")
    print("4. 明确的产物名称，避免被标记为'备份'")
    
    return workflow_file

def check_gitee_naming_convention():
    """检查Gitee的命名约定"""
    print("\n" + "=" * 70)
    print("Gitee构建产物命名约定")
    print("=" * 70)
    
    print("\n📝 Gitee流水线特点:")
    print("1. Gitee可能将构建产物自动分类")
    print("2. '备份'可能是默认分类名称")
    print("3. 需要明确的产物名称")
    
    print("\n💡 解决方案:")
    print("1. 使用明确的artifact名称，如 'WW2Assistant-APK'")
    print("2. 创建单独的ZIP文件而不是上传目录")
    print("3. 提供多个构建产物选项")
    print("4. 检查Gitee流水线设置")
    
    print("\n🔧 操作步骤:")
    print("1. 使用新创建的Gitee专用工作流")
    print("2. 提交并推送到Gitee")
    print("3. 在Gitee上手动触发构建")
    print("4. 检查构建产物名称")
    
    return True

def main():
    """主函数"""
    print("\n🎯 解决Gitee构建产物显示为'备份'的问题")
    
    # 分析当前工作流
    analyze_gitee_workflow()
    
    # 检查APK输出目录
    check_apk_output_directories()
    
    # 创建Gitee专用工作流
    new_workflow = create_gitee_specific_workflow()
    
    # 检查Gitee命名约定
    check_gitee_naming_convention()
    
    print("\n" + "=" * 70)
    print("✅ 解决方案总结")
    print("=" * 70)
    print("\n问题: Gitee将构建产物标记为'备份'")
    print("\n原因: Gitee可能对未明确命名的artifact使用默认分类")
    print("\n解决方案:")
    print(f"1. 已创建Gitee专用工作流: {new_workflow}")
    print("2. 这个工作流会:")
    print("   - 创建明确的ZIP文件: ww2-assistant-apk.zip")
    print("   - 使用明确的artifact名称: WW2Assistant-APK")
    print("   - 同时上传单独的APK文件")
    print("   - 上传构建日志用于调试")
    
    print("\n🚀 下一步操作:")
    print("1. 提交新工作流文件:")
    print("   git add .github/workflows/build-apk-gitee.yml")
    print("   git commit -m '添加Gitee专用工作流'")
    print("   git push gitee master")
    print("\n2. 在Gitee上:")
    print("   - 打开流水线页面")
    print("   - 选择'Build APK for Gitee'工作流")
    print("   - 手动触发构建")
    print("   - 等待完成后下载'WW2Assistant-APK'")
    
    print("\n📦 构建产物将包括:")
    print("• WW2Assistant-APK - 包含APK的ZIP文件")
    print("• APK-Files - 单独的APK文件")
    print("• Build-Logs - 构建日志（用于调试）")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())