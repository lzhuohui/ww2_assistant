#!/usr/bin/env python3
"""
Gitee流水线状态检查脚本
用于快速检查Gitee仓库设置和流水线功能
"""

import os
import subprocess
import sys
import json
from pathlib import Path

def print_header(title):
    """打印标题"""
    print("\n" + "=" * 60)
    print(f"🔍 {title}")
    print("=" * 60)

def check_git_remote():
    """检查Git远程仓库配置"""
    print_header("检查Git远程仓库配置")
    
    try:
        # 获取远程仓库URL
        result = subprocess.run(
            ["git", "remote", "-v"],
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        
        if result.returncode == 0:
            print("✅ Git远程仓库配置：")
            print(result.stdout)
            
            # 检查是否有gitee远程
            if "gitee.com" in result.stdout.lower():
                print("✅ 检测到Gitee远程仓库")
            else:
                print("⚠️  未检测到Gitee远程仓库")
                
            if "github.com" in result.stdout.lower():
                print("✅ 检测到GitHub远程仓库")
        else:
            print(f"❌ 获取Git远程仓库失败：{result.stderr}")
            
    except Exception as e:
        print(f"❌ 执行Git命令出错：{e}")

def check_workflow_files():
    """检查工作流文件"""
    print_header("检查工作流文件")
    
    workflow_dir = Path(".github/workflows")
    
    if workflow_dir.exists():
        print(f"✅ 工作流目录存在：{workflow_dir}")
        
        files = list(workflow_dir.glob("*.yml")) + list(workflow_dir.glob("*.yaml"))
        
        if files:
            print(f"📁 找到 {len(files)} 个工作流文件：")
            for file in files:
                print(f"   📄 {file.name}")
                
                # 读取文件内容概要
                try:
                    with open(file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # 提取工作流名称
                        import re
                        name_match = re.search(r'name:\s*["\']?(.+?)["\']?\n', content)
                        if name_match:
                            workflow_name = name_match.group(1)
                            print(f"      🔧 工作流名称：{workflow_name}")
                except Exception as e:
                    print(f"      ⚠️  读取文件失败：{e}")
        else:
            print("❌ 工作流目录为空")
    else:
        print("❌ 工作流目录不存在")

def check_requirements():
    """检查依赖文件"""
    print_header("检查依赖文件")
    
    required_files = [
        "requirements.txt",
        "main.py",
        ".gitignore"
    ]
    
    for file in required_files:
        path = Path(file)
        if path.exists():
            size = path.stat().st_size
            print(f"✅ {file} 存在 ({size} 字节)")
            
            # 读取requirements.txt内容
            if file == "requirements.txt":
                try:
                    with open(file, 'r', encoding='utf-8') as f:
                        deps = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                        print(f"   📦 依赖项：{len(deps)} 个")
                        for dep in deps[:5]:  # 只显示前5个
                            print(f"      - {dep}")
                        if len(deps) > 5:
                            print(f"      ... 还有 {len(deps)-5} 个")
                except Exception as e:
                    print(f"   ⚠️  读取失败：{e}")
        else:
            print(f"❌ {file} 不存在")

def check_python_environment():
    """检查Python环境"""
    print_header("检查Python环境")
    
    try:
        # 检查Python版本
        python_version = sys.version
        print(f"✅ Python版本：{python_version.split()[0]}")
        
        # 检查flet是否安装
        import importlib
        try:
            importlib.import_module('flet')
            print("✅ Flet库已安装")
        except ImportError:
            print("❌ Flet库未安装")
            
        # 检查pip list
        result = subprocess.run(
            [sys.executable, "-m", "pip", "list"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ pip包列表可用")
        else:
            print(f"❌ pip命令失败：{result.stderr}")
            
    except Exception as e:
        print(f"❌ 环境检查失败：{e}")

def check_gitee_api():
    """检查Gitee API访问（模拟）"""
    print_header("检查Gitee访问状态")
    
    gitee_urls = [
        "https://gitee.com/lzhuohui/ww2_assistant",
        "https://gitee.com/lzhuohui/ww2_assistant/actions",
        "https://gitee.com/lzhuohui/ww2_assistant/settings"
    ]
    
    print("📡 需要手动检查的Gitee链接：")
    for url in gitee_urls:
        print(f"   🌐 {url}")
    
    print("\n🔗 直接访问这些链接检查：")
    print("   1. 仓库主页：确认仓库存在")
    print("   2. Actions页面：确认流水线功能")
    print("   3. 设置页面：开启流水线功能")

def generate_report():
    """生成检查报告"""
    print_header("流水线功能检查报告")
    
    print("""
🚀 下一步操作指南：

1️⃣ **登录Gitee并检查**
   网址：https://gitee.com/lzhuohui/ww2_assistant
   - 确认已登录你的账号
   - 点击右上角"管理"进入设置
   - 找到"功能设置" → 开启"流水线"

2️⃣ **验证流水线**
   - 回到仓库主页
   - 查看顶部是否有"流水线"标签
   - 点击进入流水线页面
   - 查看构建历史

3️⃣ **手动触发构建**
   - 点击"运行流水线"
   - 选择"Build APK for Gitee"工作流
   - 等待构建完成

4️⃣ **检查结果**
   - 构建成功：下载APK文件
   - 构建失败：查看详细错误日志

5️⃣ **如果仍有问题**
   - 提供Gitee页面的截图
   - 复制错误日志
   - 或改用GitHub Actions
""")

def main():
    """主函数"""
    print("🚀 Gitee流水线功能诊断工具")
    print("=" * 60)
    
    # 检查当前目录
    current_dir = os.getcwd()
    print(f"📁 当前目录：{current_dir}")
    
    # 检查是否为Git仓库
    git_dir = Path(".git")
    if git_dir.exists():
        print("✅ 当前目录是Git仓库")
    else:
        print("❌ 当前目录不是Git仓库")
        print("⚠️  请确保在项目根目录运行此脚本")
        return
    
    # 执行各项检查
    check_git_remote()
    check_workflow_files()
    check_requirements()
    check_python_environment()
    check_gitee_api()
    generate_report()
    
    print_header("操作步骤总结")
    print("""
📋 立即执行的步骤：

1. 打开浏览器访问：https://gitee.com/lzhuohui/ww2_assistant/settings
2. 找到"功能设置" → 开启"流水线"
3. 保存设置
4. 访问：https://gitee.com/lzhuohui/ww2_assistant/actions
5. 查看流水线页面是否正常显示

🔧 备用方案：
如果Gitee流水线无法使用，可以：
1. 改回GitHub Actions
2. 使用本地构建脚本
3. 联系Gitee客服

💡 提示：
- 保存页面截图给我看
- 复制任何错误信息
- 告诉我你看到的具体情况
    """)

if __name__ == "__main__":
    main()