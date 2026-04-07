#!/usr/bin/env python3
"""
一键切换到GitHub Actions脚本
用于快速切换到GitHub进行APK构建
"""

import subprocess
import os
import sys
import time
from pathlib import Path

def run_command(cmd, desc=""):
    """运行命令并显示结果"""
    print(f"\n🔧 {desc}")
    print(f"$ {cmd}")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ 成功")
            if result.stdout.strip():
                print(result.stdout)
        else:
            print("❌ 失败")
            if result.stderr:
                print(f"错误信息：\n{result.stderr}")
            if result.stdout:
                print(f"输出：\n{result.stdout}")
                
        return result.returncode, result.stdout, result.stderr
        
    except Exception as e:
        print(f"❌ 执行命令出错：{e}")
        return 1, "", str(e)

def check_git_status():
    """检查Git状态"""
    print("\n" + "="*60)
    print("🔍 检查Git状态")
    print("="*60)
    
    # 检查是否为Git仓库
    if not Path(".git").exists():
        print("❌ 当前目录不是Git仓库")
        return False
    
    # 检查远程仓库
    code, out, err = run_command("git remote -v", "检查远程仓库")
    if code != 0:
        return False
    
    # 检查是否有未提交的更改
    code, out, err = run_command("git status --porcelain", "检查未提交的更改")
    if code != 0:
        return False
    
    if out.strip():
        print("\n⚠️  发现未提交的更改：")
        print(out)
        
        answer = input("\n❓ 是否提交这些更改？(y/n): ").strip().lower()
        if answer == 'y':
            # 添加所有更改
            run_command("git add .", "添加所有更改")
            
            # 提交更改
            commit_msg = input("请输入提交信息（默认：Update for GitHub Actions）: ").strip()
            if not commit_msg:
                commit_msg = "Update for GitHub Actions"
            
            code, out, err = run_command(f'git commit -m "{commit_msg}"', "提交更改")
            if code != 0:
                print("❌ 提交失败，请手动处理")
                return False
            print("✅ 更改已提交")
        else:
            print("❌ 请先提交或暂存更改")
            return False
    
    return True

def check_github_remote():
    """检查GitHub远程配置"""
    print("\n" + "="*60)
    print("🔗 检查GitHub远程配置")
    print("="*60)
    
    code, out, err = run_command("git remote -v", "查看远程仓库")
    
    if "github.com" in out.lower():
        print("✅ 检测到GitHub远程仓库")
        
        # 检查origin指向GitHub
        lines = out.split('\n')
        for line in lines:
            if "origin" in line and "github.com" in line:
                print(f"📦 GitHub远程：{line}")
                return True
    else:
        print("⚠️  未检测到GitHub远程仓库")
        
        # 添加GitHub远程
        print("\n📝 需要添加GitHub远程仓库")
        print("当前仓库：lzhuohui/ww2_assistant")
        
        answer = input("是否添加GitHub远程？(y/n): ").strip().lower()
        if answer == 'y':
            # 添加GitHub远程
            github_url = "https://github.com/lzhuohui/ww2_assistant.git"
            code, out, err = run_command(f'git remote add github {github_url}', "添加GitHub远程")
            
            if code == 0:
                print("✅ GitHub远程已添加")
                
                # 设置GitHub为默认推送目标
                run_command("git branch --set-upstream-to=github/master master", "设置上游分支")
                return True
            else:
                print("❌ 添加GitHub远程失败")
                return False
        else:
            print("❌ 请先配置GitHub远程仓库")
            return False
    
    return True

def push_to_github():
    """推送到GitHub"""
    print("\n" + "="*60)
    print("🚀 推送到GitHub")
    print("="*60)
    
    # 确认推送
    print("\n即将推送到：https://github.com/lzhuohui/ww2_assistant")
    answer = input("确认推送？(y/n): ").strip().lower()
    
    if answer != 'y':
        print("❌ 取消推送")
        return False
    
    # 执行推送
    print("\n📤 推送代码中...")
    code, out, err = run_command("git push origin master", "推送到GitHub")
    
    if code == 0:
        print("\n🎉 推送成功！")
        return True
    else:
        print("\n❌ 推送失败")
        return False

def check_workflow_files():
    """检查工作流文件"""
    print("\n" + "="*60)
    print("📁 检查工作流文件")
    print("="*60)
    
    workflow_dir = Path(".github/workflows")
    
    if not workflow_dir.exists():
        print("❌ 工作流目录不存在")
        return False
    
    files = list(workflow_dir.glob("*.yml")) + list(workflow_dir.glob("*.yaml"))
    
    if files:
        print(f"✅ 找到 {len(files)} 个工作流文件：")
        for file in files:
            print(f"   📄 {file.name}")
        return True
    else:
        print("⚠️  工作流目录为空")
        return True  # 仍然可以推送

def show_next_steps():
    """显示后续步骤"""
    print("\n" + "="*60)
    print("📋 后续步骤")
    print("="*60)
    
    print("""
1. 🔗 访问GitHub Actions页面：
   https://github.com/lzhuohui/ww2_assistant/actions

2. ⏱️  等待构建开始（通常1-2分钟）

3. 📱 查看构建进度：
   - 点击最新的"Build APK"工作流
   - 查看每个步骤的日志

4. 📥 下载APK文件：
   - 构建完成后，在"Artifacts"部分
   - 点击"WW2Assistant-APK"下载ZIP文件
   - 解压后得到APK文件

5. 🔧 如果构建失败：
   - 查看错误日志
   - 修改代码后重新推送
   - 或运行本地构建脚本

💡 提示：
- GitHub Actions对公开仓库完全免费
- 每次推送都会自动触发构建
- 可以手动触发构建（Workflow dispatch）
    """)

def main():
    """主函数"""
    print("🚀 GitHub Actions一键切换工具")
    print("="*60)
    
    # 检查当前目录
    current_dir = os.getcwd()
    print(f"📁 当前目录：{current_dir}")
    
    # 执行检查
    if not check_git_status():
        print("\n❌ Git状态检查失败，请先解决Git问题")
        return
    
    if not check_github_remote():
        print("\n❌ GitHub远程配置失败")
        return
    
    if not check_workflow_files():
        print("\n⚠️  工作流文件检查失败，但可以继续")
    
    # 推送到GitHub
    if push_to_github():
        # 显示后续步骤
        show_next_steps()
        
        # 提供快速链接
        print("\n🔗 快速链接：")
        print("   GitHub仓库：https://github.com/lzhuohui/ww2_assistant")
        print("   GitHub Actions：https://github.com/lzhuohui/ww2_assistant/actions")
        print("   GitHub设置：https://github.com/lzhuohui/ww2_assistant/settings/actions")
        
        # 询问是否要查看构建状态
        answer = input("\n❓ 是否要打开GitHub Actions页面？(y/n): ").strip().lower()
        if answer == 'y':
            import webbrowser
            webbrowser.open("https://github.com/lzhuohui/ww2_assistant/actions")
            print("✅ 已打开浏览器")
    else:
        print("\n❌ 切换到GitHub Actions失败")
        print("\n💡 备选方案：")
        print("   1. 手动运行：git push origin master")
        print("   2. 使用本地构建：python local_build_alternative.py")
        print("   3. 检查网络连接和Git配置")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ 用户中断操作")
    except Exception as e:
        print(f"\n❌ 程序出错：{e}")
        import traceback
        traceback.print_exc()