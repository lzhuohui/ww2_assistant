#!/usr/bin/env python3
"""
快速测试Gitee流水线功能
"""

import os
import subprocess
import sys
from pathlib import Path

def print_step(step, description):
    """打印步骤信息"""
    print(f"\n{'='*60}")
    print(f"🔧 步骤 {step}: {description}")
    print(f"{'='*60}")

def run_command(cmd, check=True):
    """运行命令"""
    print(f"$ {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            if result.stdout.strip():
                print(f"✅ 成功\n{result.stdout}")
            else:
                print("✅ 成功")
        else:
            print(f"❌ 失败")
            if result.stderr:
                print(f"错误：{result.stderr}")
            if check:
                print("⚠️  继续执行...")
        return result.returncode == 0
    except Exception as e:
        print(f"❌ 执行出错：{e}")
        return False

def check_git_status():
    """检查Git状态"""
    print_step(1, "检查Git状态")
    
    if not Path(".git").exists():
        print("❌ 当前目录不是Git仓库")
        return False
    
    # 检查远程仓库
    print("\n📦 远程仓库配置：")
    run_command("git remote -v")
    
    # 检查是否有未提交的更改
    print("\n📝 Git状态：")
    run_command("git status --porcelain")
    
    return True

def check_workflow_files():
    """检查工作流文件"""
    print_step(2, "检查工作流文件")
    
    workflow_dir = Path(".github/workflows")
    if not workflow_dir.exists():
        print("❌ 工作流目录不存在")
        return False
    
    files = list(workflow_dir.glob("*.yml")) + list(workflow_dir.glob("*.yaml"))
    
    if not files:
        print("⚠️  工作流目录为空")
        return False
    
    print(f"✅ 找到 {len(files)} 个工作流文件：")
    for file in files:
        size = file.stat().st_size
        print(f"   📄 {file.name} ({size} 字节)")
        
        # 读取工作流名称
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                import re
                name_match = re.search(r'name:\s*["\']?(.+?)["\']?\n', content)
                if name_match:
                    print(f"      🔧 {name_match.group(1)}")
        except:
            pass
    
    return True

def test_gitee_push():
    """测试推送到Gitee"""
    print_step(3, "测试推送到Gitee")
    
    # 检查是否有gitee远程
    result = subprocess.run("git remote -v", shell=True, capture_output=True, text=True)
    if "gitee.com" not in result.stdout:
        print("❌ 未配置Gitee远程仓库")
        return False
    
    # 添加测试文件
    test_file = "test_pipeline.txt"
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(f"测试文件，用于验证Gitee流水线功能\n")
        f.write(f"生成时间：{subprocess.check_output('date', shell=True, text=True).strip()}\n")
    
    print(f"📝 创建测试文件：{test_file}")
    
    # 添加到Git
    run_command(f"git add {test_file}", check=False)
    
    # 提交
    run_command('git commit -m "test: Add test file for Gitee pipeline"', check=False)
    
    # 推送到Gitee
    print("\n🚀 推送到Gitee...")
    success = run_command("git push gitee master", check=False)
    
    if success:
        print("\n✅ 推送成功！")
        print("\n🔗 请访问：https://gitee.com/lzhuohui/ww2_assistant/pipelines")
        print("   查看流水线是否自动触发构建")
    else:
        print("\n⚠️  推送失败，但工作流文件已存在")
        print("   可以手动在Gitee页面触发构建")
    
    return True

def show_gitee_links():
    """显示Gitee相关链接"""
    print_step(4, "Gitee链接和下一步操作")
    
    print("""
🔗 重要链接：

1. **流水线主页**：
   https://gitee.com/lzhuohui/ww2_assistant/pipelines

2. **工作流列表**：
   https://gitee.com/lzhuohui/ww2_assistant/pipelines/list

3. **构建历史**：
   https://gitee.com/lzhuohui/ww2_assistant/pipelines?status=failed

4. **仓库设置**：
   https://gitee.com/lzhuohui/ww2_assistant/settings

🎯 下一步操作：

1. **立即访问流水线页面**（链接1）
2. **检查是否有以下内容**：
   - 顶部菜单有"流水线"标签
   - 能看到工作流列表
   - 能看到构建历史（#7、#6、#4等）
   - 有"运行流水线"按钮

3. **手动触发构建**：
   - 点击"运行流水线"
   - 选择"Build APK for Gitee"
   - 点击"运行"

4. **查看结果**：
   - 构建成功：下载APK
   - 构建失败：查看错误日志

🆘 如果遇到问题：

1. **看不到"流水线"菜单**：
   - 访问：https://gitee.com/features/pipelines
   - 点击"开通"或"立即使用"

2. **页面404或其他错误**：
   - 提供截图
   - 复制错误信息

3. **备用方案**：
   - 运行：python switch_to_github.py
   - 使用GitHub Actions
    """)

def cleanup():
    """清理测试文件"""
    print_step(5, "清理测试文件")
    
    test_file = "test_pipeline.txt"
    if Path(test_file).exists():
        # 撤销Git添加
        run_command(f"git reset HEAD {test_file}", check=False)
        run_command(f"git checkout -- {test_file}", check=False)
        
        # 删除文件
        Path(test_file).unlink(missing_ok=True)
        print(f"🗑️  已清理测试文件：{test_file}")

def main():
    """主函数"""
    print("🚀 Gitee流水线快速测试工具")
    print("="*60)
    
    try:
        # 检查Git状态
        if not check_git_status():
            print("\n❌ Git状态检查失败")
            return
        
        # 检查工作流文件
        if not check_workflow_files():
            print("\n⚠️  工作流文件检查失败，但可以继续")
        
        # 测试推送到Gitee
        test_gitee_push()
        
        # 显示Gitee链接
        show_gitee_links()
        
        # 清理
        cleanup()
        
        print("\n" + "="*60)
        print("🎉 测试完成！")
        print("="*60)
        print("\n📋 请立即访问Gitee流水线页面，然后告诉我：")
        print("1. 是否能访问流水线页面？")
        print("2. 看到了什么内容？")
        print("3. 是否有错误信息？")
        
    except KeyboardInterrupt:
        print("\n\n❌ 用户中断操作")
        cleanup()
    except Exception as e:
        print(f"\n❌ 程序出错：{e}")
        import traceback
        traceback.print_exc()
        cleanup()

if __name__ == "__main__":
    main()