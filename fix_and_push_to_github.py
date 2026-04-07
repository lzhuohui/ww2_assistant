#!/usr/bin/env python3
"""
一键修复并推送到GitHub Actions
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(cmd, desc=""):
    """运行命令"""
    print(f"\n🔧 {desc}")
    print(f"$ {cmd}")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8', errors='ignore')
        
        if result.returncode == 0:
            print("✅ 成功")
            if result.stdout and result.stdout.strip():
                print(f"输出：{result.stdout.strip()}")
            return True, result.stdout
        else:
            print("❌ 失败")
            if result.stderr:
                print(f"错误：{result.stderr.strip()}")
            return False, result.stderr
    except Exception as e:
        print(f"❌ 执行出错：{e}")
        return False, str(e)

def check_git_status():
    """检查Git状态"""
    print("\n" + "="*60)
    print("🔍 检查Git状态")
    print("="*60)
    
    # 检查当前分支
    success, output = run_command("git branch --show-current", "检查当前分支")
    if success:
        print(f"当前分支：{output.strip()}")
    
    # 检查状态
    success, output = run_command("git status --porcelain", "检查未提交的更改")
    
    changes = []
    if output.strip():
        lines = output.strip().split('\n')
        print(f"发现 {len(lines)} 个未提交的更改：")
        for line in lines:
            print(f"  {line}")
            changes.append(line)
    
    return len(changes) > 0

def commit_changes():
    """提交更改"""
    print("\n" + "="*60)
    print("💾 提交更改")
    print("="*60)
    
    # 添加所有更改
    success, _ = run_command("git add .", "添加所有更改")
    if not success:
        return False
    
    # 提交
    commit_msg = "fix: Update for GitHub Actions build"
    success, output = run_command(f'git commit -m "{commit_msg}"', "提交更改")
    
    return success

def push_to_github():
    """推送到GitHub"""
    print("\n" + "="*60)
    print("🚀 推送到GitHub")
    print("="*60)
    
    # 检查GitHub远程
    success, output = run_command("git remote -v", "检查远程仓库")
    
    if "github.com" not in output.lower():
        print("❌ 未检测到GitHub远程仓库")
        print("正在添加GitHub远程...")
        
        github_url = "https://github.com/lzhuohui/ww2_assistant.git"
        success, _ = run_command(f'git remote add github {github_url}', "添加GitHub远程")
        if not success:
            return False
    
    # 推送
    print("\n📤 推送到GitHub...")
    success, output = run_command("git push origin master", "推送到GitHub")
    
    if success:
        print("\n🎉 推送成功！")
        return True
    else:
        # 尝试使用github别名
        print("尝试使用github别名推送...")
        success, output = run_command("git push github master", "推送到GitHub(github别名)")
        return success

def check_workflow_files():
    """检查工作流文件"""
    print("\n" + "="*60)
    print("📁 检查工作流文件")
    print("="*60)
    
    workflow_dir = Path(".github/workflows")
    
    if not workflow_dir.exists():
        print("❌ 工作流目录不存在，创建中...")
        workflow_dir.mkdir(parents=True, exist_ok=True)
    
    files = list(workflow_dir.glob("*.yml")) + list(workflow_dir.glob("*.yaml"))
    
    if files:
        print(f"✅ 找到 {len(files)} 个工作流文件：")
        for file in files:
            size = file.stat().st_size
            print(f"  📄 {file.name} ({size} 字节)")
    else:
        print("❌ 工作流目录为空")
        
        # 创建简单的工作流文件
        simple_workflow = """name: Build APK

on:
  push:
    branches: [ main, master ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
        pip install flet==0.82.0
    
    - name: Build APK
      run: |
        python -m flet.cli build apk --project "WW2Assistant" --verbose
        
    - name: Upload APK
      uses: actions/upload-artifact@v4
      with:
        name: WW2Assistant-APK
        path: build/apk/*.apk
        retention-days: 5"""
        
        workflow_file = workflow_dir / "build-apk.yml"
        workflow_file.write_text(simple_workflow, encoding='utf-8')
        print(f"✅ 已创建工作流文件：{workflow_file}")
    
    return True

def show_next_steps():
    """显示后续步骤"""
    print("\n" + "="*60)
    print("📋 下一步操作")
    print("="*60)
    
    print("""
🎯 请按以下步骤操作：

1. 🔗 访问GitHub Actions页面：
   https://github.com/lzhuohui/ww2_assistant/actions

2. ⏱️ 等待构建开始（1-2分钟内）：
   - 应该能看到"Build APK"工作流
   - 点击进入查看详情

3. 📱 查看构建进度：
   - 每个步骤都会有日志输出
   - 绿色表示成功，红色表示失败

4. 📥 下载APK文件：
   - 构建完成后，在"Artifacts"部分
   - 点击"WW2Assistant-APK"下载ZIP
   - 解压得到APK文件

5. 🔧 如果构建失败：
   - 查看错误日志
   - 告诉我错误信息
   - 我会帮你修复

💡 提示：
- GitHub Actions对公开仓库完全免费
- 每次推送都会自动触发构建
- 可以在页面手动触发构建（Workflow dispatch）
    """)
    
    print("\n🔗 重要链接：")
    print("   GitHub仓库：https://github.com/lzhuohui/ww2_assistant")
    print("   GitHub Actions：https://github.com/lzhuohui/ww2_assistant/actions")
    print("   GitHub设置：https://github.com/lzhuohui/ww2_assistant/settings/actions")

def main():
    """主函数"""
    print("🚀 GitHub Actions一键配置工具")
    print("="*60)
    
    try:
        # 检查当前目录
        current_dir = os.getcwd()
        print(f"📁 当前目录：{current_dir}")
        
        # 检查Git仓库
        if not Path(".git").exists():
            print("❌ 当前目录不是Git仓库")
            return
        
        # 检查工作流文件
        check_workflow_files()
        
        # 检查Git状态
        has_changes = check_git_status()
        
        if has_changes:
            # 提交更改
            if not commit_changes():
                print("❌ 提交更改失败")
                return
        else:
            print("✅ 没有未提交的更改")
        
        # 推送到GitHub
        if push_to_github():
            # 显示后续步骤
            show_next_steps()
            
            # 询问是否打开GitHub
            answer = input("\n❓ 是否要打开GitHub Actions页面？(y/n): ").strip().lower()
            if answer == 'y':
                import webbrowser
                webbrowser.open("https://github.com/lzhuohui/ww2_assistant/actions")
                print("✅ 已打开浏览器")
        else:
            print("\n❌ 推送到GitHub失败")
            print("\n💡 备用方案：")
            print("   1. 手动推送：git push origin master")
            print("   2. 检查网络连接")
            print("   3. 确认GitHub仓库权限")
            
    except KeyboardInterrupt:
        print("\n\n❌ 用户中断操作")
    except Exception as e:
        print(f"\n❌ 程序出错：{e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()