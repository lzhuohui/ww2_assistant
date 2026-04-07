#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查Gitee仓库访问状态
"""

import requests
import webbrowser
import sys
import os
from urllib.parse import urljoin

def check_gitee_repo():
    """检查Gitee仓库是否可访问"""
    print("=" * 60)
    print("检查Gitee仓库访问状态")
    print("=" * 60)
    
    repo_url = "https://gitee.com/lzhuohui/ww2_assistant"
    actions_url = "https://gitee.com/lzhuohui/ww2_assistant/actions"
    
    print(f"\n📊 仓库信息:")
    print(f"用户名: lzhuohui")
    print(f"仓库名: ww2_assistant")
    print(f"仓库URL: {repo_url}")
    print(f"Actions URL: {actions_url}")
    
    print(f"\n🔍 检查仓库是否存在...")
    try:
        # 尝试访问仓库主页
        response = requests.get(repo_url, timeout=10)
        if response.status_code == 200:
            print(f"✅ 仓库可访问 (状态码: {response.status_code})")
            
            # 检查页面内容
            if "二战风云" in response.text:
                print("✅ 仓库内容包含'二战风云'项目")
            else:
                print("⚠️  仓库内容中未找到'二战风云'关键词")
                
            # 检查Actions页面
            print(f"\n🔍 检查Actions页面...")
            actions_response = requests.get(actions_url, timeout=10)
            if actions_response.status_code == 200:
                print(f"✅ Actions页面可访问 (状态码: {actions_response.status_code})")
                
                if "workflows" in actions_response.text.lower() or "流水线" in actions_response.text:
                    print("✅ Actions/流水线功能可用")
                else:
                    print("⚠️  Actions页面可能未显示工作流")
            else:
                print(f"❌ Actions页面访问失败 (状态码: {actions_response.status_code})")
                print("提示: Gitee需要开启Actions功能")
                
        elif response.status_code == 404:
            print(f"❌ 仓库不存在 (404)")
            print("可能的原因:")
            print("1. 仓库名错误")
            print("2. 仓库未公开")
            print("3. 需要登录才能访问")
        else:
            print(f"⚠️  仓库访问异常 (状态码: {response.status_code})")
            
    except requests.exceptions.ConnectionError:
        print("❌ 网络连接失败")
        print("请检查网络连接或尝试使用代理")
    except requests.exceptions.Timeout:
        print("❌ 请求超时")
    except Exception as e:
        print(f"❌ 检查过程中出错: {e}")
    
    return repo_url, actions_url

def open_gitee_pages(repo_url, actions_url):
    """打开Gitee页面"""
    print(f"\n🌐 打开浏览器...")
    
    # 尝试打开仓库主页
    try:
        print(f"1. 打开仓库主页: {repo_url}")
        webbrowser.open(repo_url)
    except Exception as e:
        print(f"打开仓库主页失败: {e}")
    
    # 尝试打开Actions页面
    try:
        print(f"2. 打开Actions页面: {actions_url}")
        webbrowser.open(actions_url)
    except Exception as e:
        print(f"打开Actions页面失败: {e}")

def check_local_config():
    """检查本地Git配置"""
    print(f"\n📁 本地配置检查:")
    
    # 检查工作流文件是否存在
    workflow_file = ".github/workflows/build-apk.yml"
    if os.path.exists(workflow_file):
        print(f"✅ GitHub Actions工作流文件存在: {workflow_file}")
        
        # 读取文件内容
        with open(workflow_file, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = len(content.split('\n'))
            print(f"   文件大小: {lines} 行")
            
            # 检查关键内容
            if "Build APK" in content:
                print("   ✅ 包含'Build APK'工作流")
            if "ubuntu-latest" in content:
                print("   ✅ 使用Ubuntu最新版环境")
            if "flet==0.82.0" in content:
                print("   ✅ 指定了Flet版本")
    else:
        print(f"❌ 工作流文件不存在: {workflow_file}")
    
    # 检查Git状态
    print(f"\n🔧 Git状态:")
    try:
        import subprocess
        result = subprocess.run(
            ['git', 'status', '--porcelain'],
            capture_output=True, 
            text=True,
            cwd=os.getcwd()
        )
        if result.returncode == 0:
            changes = result.stdout.strip()
            if changes:
                print(f"⚠️  有未提交的更改:")
                print(changes[:200])  # 只显示前200个字符
            else:
                print("✅ 所有更改已提交")
        else:
            print(f"Git状态检查失败: {result.stderr}")
    except Exception as e:
        print(f"Git状态检查出错: {e}")

def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("Gitee仓库访问检查工具")
    print("=" * 60)
    
    # 检查本地配置
    check_local_config()
    
    # 检查Gitee访问
    repo_url, actions_url = check_gitee_repo()
    
    print(f"\n🎯 操作指南:")
    print("1. 如果仓库存在且可访问:")
    print("   - 打开浏览器访问上面的URL")
    print("   - 点击'Actions'或'流水线'标签")
    print("   - 手动触发'Build APK'工作流")
    
    print(f"\n2. 如果仓库不存在或无法访问:")
    print("   - 请确保你在Gitee上已登录")
    print("   - 检查仓库名是否正确: lzhuohui/ww2_assistant")
    print("   - 可能需要手动创建仓库")
    
    print(f"\n3. 如果Actions不可用:")
    print("   - Gitee可能需要手动开启CI/CD功能")
    print("   - 在仓库设置中开启'流水线'功能")
    
    # 询问是否打开浏览器
    print(f"\n是否要打开浏览器访问Gitee页面？ (y/n): ", end="")
    try:
        choice = input().strip().lower()
        if choice in ['y', 'yes', '是']:
            open_gitee_pages(repo_url, actions_url)
    except:
        pass  # 如果input不可用，继续执行
    
    print(f"\n✅ 检查完成!")
    return 0

if __name__ == "__main__":
    sys.exit(main())