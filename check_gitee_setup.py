#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查Gitee仓库设置问题
解决构建失败#7的常见配置问题
"""

import os
import sys
import json
import webbrowser

def check_gitee_repository_settings():
    """检查Gitee仓库可能的问题设置"""
    print("=" * 80)
    print("Gitee仓库设置检查指南")
    print("=" * 80)
    
    print("\n🎯 构建失败 #7 可能的原因分析:")
    print("提交: '修复Gitee工作流的APK文件检查逻辑'")
    print("时间: 2026-04-07 10:07:55")
    print("状态: 失败")
    
    print("\n🔍 Gitee仓库设置常见问题:")
    print("1. 流水线功能未开启")
    print("2. 构建环境配置问题")
    print("3. 权限不足")
    print("4. 工作流文件语法错误")
    print("5. 依赖下载失败")
    print("6. Android SDK许可问题")
    
    return True

def check_workflow_syntax():
    """检查工作流文件语法"""
    print("\n" + "=" * 80)
    print("工作流文件语法检查")
    print("=" * 80)
    
    workflow_file = ".github/workflows/build-apk-gitee.yml"
    
    if not os.path.exists(workflow_file):
        print(f"❌ 工作流文件不存在: {workflow_file}")
        return False
    
    print(f"✅ 工作流文件存在: {workflow_file}")
    
    # 检查基本语法
    with open(workflow_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    issues = []
    
    # 检查YAML基本结构
    if 'name:' not in content:
        issues.append("缺少 'name:' 字段")
    if 'on:' not in content:
        issues.append("缺少 'on:' 触发器配置")
    if 'jobs:' not in content:
        issues.append("缺少 'jobs:' 配置")
    if 'runs-on:' not in content:
        issues.append("缺少 'runs-on:' 运行环境配置")
    
    # 检查关键步骤
    required_steps = [
        'actions/checkout',
        'actions/setup-python',
        'subosito/flutter-action',
        'actions/setup-java'
    ]
    
    for step in required_steps:
        if step not in content:
            issues.append(f"缺少步骤: {step}")
    
    if issues:
        print("⚠️  发现可能的问题:")
        for issue in issues:
            print(f"   • {issue}")
        return False
    else:
        print("✅ 工作流文件基本语法正确")
        return True

def check_project_structure():
    """检查项目结构"""
    print("\n" + "=" * 80)
    print("项目结构检查")
    print("=" * 80)
    
    required_files = [
        ("main.py", "Flet应用主入口"),
        ("requirements.txt", "Python依赖文件"),
        (".github/workflows/build-apk-gitee.yml", "Gitee工作流"),
        ("设置界面/层级1_主入口/主入口.py", "主界面文件")
    ]
    
    missing_files = []
    
    for file_path, description in required_files:
        if os.path.exists(file_path):
            print(f"✅ {description}: {file_path}")
        else:
            print(f"❌ {description}: {file_path} (缺失)")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n⚠️  缺失 {len(missing_files)} 个必要文件")
        return False
    
    # 检查main.py内容
    try:
        with open("main.py", "r", encoding="utf-8") as f:
            main_content = f.read()
            if "ft.run" in main_content or "flet.run" in main_content:
                print("✅ main.py 包含Flet运行入口")
            else:
                print("⚠️  main.py 可能不是有效的Flet入口")
                return False
    except:
        print("❌ 无法读取main.py")
        return False
    
    return True

def gitee_settings_checklist():
    """Gitee仓库设置检查清单"""
    print("\n" + "=" * 80)
    print("Gitee仓库设置检查清单")
    print("=" * 80)
    
    print("\n📋 请按顺序检查以下设置:")
    
    checklist = [
        {
            "步骤": "1. 流水线功能开启",
            "操作": "访问: https://gitee.com/lzhuohui/ww2_assistant/settings",
            "检查点": "功能设置 → 流水线 → 开启",
            "重要性": "🔴 必须"
        },
        {
            "步骤": "2. 查看构建日志",
            "操作": "访问: https://gitee.com/lzhuohui/ww2_assistant/pipelines",
            "检查点": "点击失败的任务(#7) → 查看详细日志",
            "重要性": "🔴 必须"
        },
        {
            "步骤": "3. 检查工作流文件",
            "操作": "仓库 → .github/workflows/build-apk-gitee.yml",
            "检查点": "确认文件存在且内容正确",
            "重要性": "🟡 重要"
        },
        {
            "步骤": "4. 查看构建环境",
            "操作": "构建日志中的'Set up job'部分",
            "检查点": "Ubuntu环境、Python版本等",
            "重要性": "🟡 重要"
        },
        {
            "步骤": "5. 检查错误信息",
            "操作": "构建日志中的红色错误信息",
            "检查点": "具体的失败原因",
            "重要性": "🔴 必须"
        },
        {
            "步骤": "6. 重新触发构建",
            "操作": "流水线页面 → '运行流水线'",
            "检查点": "选择master分支，点击运行",
            "重要性": "🟢 最后一步"
        }
    ]
    
    for item in checklist:
        print(f"\n{item['步骤']}")
        print(f"  操作: {item['操作']}")
        print(f"  检查点: {item['检查点']}")
        print(f"  重要性: {item['重要性']}")
    
    return checklist

def common_gitee_issues():
    """常见Gitee问题及解决方案"""
    print("\n" + "=" * 80)
    print("常见Gitee流水线问题及解决方案")
    print("=" * 80)
    
    issues = [
        {
            "问题": "流水线功能未开启",
            "症状": "无法看到流水线页面或无法触发构建",
            "解决": "仓库设置 → 功能设置 → 开启流水线"
        },
        {
            "问题": "Android SDK许可问题",
            "症状": "'flutter doctor --android-licenses' 失败",
            "解决": "工作流中已添加自动接受许可，但如果失败可能需要手动配置"
        },
        {
            "问题": "Flet版本不兼容",
            "症状": "构建过程中Flet相关错误",
            "解决": "确保使用 flet==0.82.0"
        },
        {
            "问题": "Flutter环境问题",
            "症状": "Flutter命令失败或版本不对",
            "解决": "工作流指定了 flutter-version: '3.19.5'"
        },
        {
            "问题": "Python环境问题",
            "症状": "Python包安装失败",
            "解决": "工作流使用 python-version: '3.11'"
        },
        {
            "问题": "网络问题",
            "症状": "依赖下载超时或失败",
            "解决": "重试构建或使用镜像源"
        },
        {
            "问题": "权限问题",
            "症状": "文件操作权限错误",
            "解决": "检查工作流中的文件路径和权限"
        }
    ]
    
    print("\n🔧 常见问题列表:")
    for i, issue in enumerate(issues, 1):
        print(f"\n{i}. {issue['问题']}")
        print(f"   症状: {issue['症状']}")
        print(f"   解决: {issue['解决']}")
    
    return issues

def provide_quick_fixes():
    """提供快速修复方案"""
    print("\n" + "=" * 80)
    print("快速修复方案")
    print("=" * 80)
    
    print("\n🚀 方案A: 简化工作流（推荐）")
    print("1. 使用更简单的工作流文件")
    print("2. 减少依赖和步骤")
    print("3. 更容易调试")
    
    print("\n🚀 方案B: 本地构建测试")
    print("1. 在本地运行构建测试")
    print("2. 确认项目可以构建")
    print("3. 排除环境问题")
    
    print("\n🚀 方案C: 查看详细日志")
    print("1. 访问构建详情页面")
    print("2. 查看每一步的输出")
    print("3. 复制错误信息给我分析")
    
    print("\n🚀 方案D: 创建调试工作流")
    print("1. 创建只输出环境信息的工作流")
    print("2. 逐步添加构建步骤")
    print("3. 定位具体失败点")
    
    return [
        "简化工作流",
        "本地测试", 
        "查看日志",
        "逐步调试"
    ]

def create_simplified_workflow_now():
    """立即创建简化版工作流"""
    print("\n" + "=" * 80)
    print("立即创建简化版工作流")
    print("=" * 80)
    
    simple_workflow = """name: Simple APK Build

on:
  workflow_dispatch:  # 仅手动触发

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
    
    - name: Debug - Show environment
      run: |
        echo "=== 环境信息 ==="
        uname -a
        python --version
        pip --version
        echo "当前目录:"
        pwd
        ls -la
        echo "main.py前20行:"
        head -20 main.py || echo "main.py不存在"
        echo "requirements.txt内容:"
        cat requirements.txt || echo "requirements.txt不存在"
    
    - name: Setup Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install flet==0.82.0
    
    - name: Try Flet build
      run: |
        echo "=== 尝试Flet构建 ==="
        python -m flet.cli --version
        echo "尝试构建..."
        python -m flet.cli build apk --project "WW2Assistant" --verbose || {
          echo "构建失败，显示错误"
          exit 1
        }
        echo "构建成功！"
    
    - name: Find APK files
      if: success()
      run: |
        echo "=== 查找APK文件 ==="
        find . -name "*.apk" -type f 2>/dev/null || echo "未找到APK文件"
        echo "build目录内容:"
        find build -type f 2>/dev/null || echo "build目录不存在"
    
    - name: Upload debug info
      if: always()
      uses: actions/upload-artifact@v4
      with:
        name: Debug-Info
        path: |
          **/*.log
          **/build/
        retention-days: 7
"""
    
    # 创建简化版工作流
    workflow_dir = ".github/workflows"
    workflow_file = os.path.join(workflow_dir, "debug-build.yml")
    
    os.makedirs(workflow_dir, exist_ok=True)
    
    with open(workflow_file, 'w', encoding='utf-8') as f:
        f.write(simple_workflow)
    
    print(f"✅ 已创建调试工作流: {workflow_file}")
    print("\n🎯 这个工作流的特点:")
    print("1. 仅手动触发，不会自动运行")
    print("2. 显示详细的环境信息")
    print("3. 尝试简单的Flet构建")
    print("4. 上传调试信息")
    print("5. 更容易定位问题")
    
    return workflow_file

def main():
    """主函数"""
    print("\n🔧 Gitee构建失败 #7 诊断工具")
    print("构建详情: 失败#7 修复Gitee工作流的APK文件检查逻辑")
    print("时间: 2026-04-07 10:07:55")
    
    # 检查项目结构
    check_project_structure()
    
    # 检查工作流语法
    check_workflow_syntax()
    
    # Gitee设置检查清单
    checklist = gitee_settings_checklist()
    
    # 常见问题
    common_gitee_issues()
    
    # 快速修复方案
    fixes = provide_quick_fixes()
    
    # 创建简化工作流
    debug_file = create_simplified_workflow_now()
    
    print("\n" + "=" * 80)
    print("🎯 立即操作建议")
    print("=" * 80)
    
    print("\n1. 首先检查Gitee设置:")
    print("   访问: https://gitee.com/lzhuohui/ww2_assistant/settings")
    print("   确认流水线功能已开启")
    
    print("\n2. 查看构建 #7 的详细日志:")
    print("   访问: https://gitee.com/lzhuohui/ww2_assistant/pipelines")
    print("   点击失败的任务(#7)")
    print("   复制错误信息给我")
    
    print("\n3. 提交并推送调试工作流:")
    print(f"   git add {debug_file}")
    print("   git commit -m '添加调试工作流'")
    print("   git push gitee master")
    
    print("\n4. 运行调试工作流:")
    print("   在Gitee流水线页面")
    print("   选择 'Simple APK Build' 工作流")
    print("   手动触发运行")
    
    print("\n5. 查看调试输出:")
    print("   查看每一步的环境信息和错误")
    
    print("\n" + "=" * 80)
    print("💡 最可能的问题:")
    print("1. Gitee流水线功能未开启 ❓")
    print("2. Android SDK许可问题 ⚠️")
    print("3. 网络依赖下载失败 🌐")
    print("4. 工作流语法错误 📝")
    print("=" * 80)
    
    print("\n📞 下一步:")
    print("请先检查Gitee仓库设置和构建 #7 的详细日志")
    print("然后把错误信息发给我，我可以提供具体修复方案")
    
    # 询问是否打开设置页面
    print("\n是否要打开Gitee设置页面? (y/n): ", end="")
    try:
        choice = input().strip().lower()
        if choice in ['y', 'yes', '是']:
            webbrowser.open("https://gitee.com/lzhuohui/ww2_assistant/settings")
            webbrowser.open("https://gitee.com/lzhuohui/ww2_assistant/pipelines")
    except:
        pass
    
    return 0

if __name__ == "__main__":
    sys.exit(main())