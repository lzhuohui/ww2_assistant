#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速本地构建测试
在不依赖Gitee的情况下测试项目是否可以构建
"""

import os
import sys
import subprocess
import shutil

def check_basic_requirements():
    """检查基本要求"""
    print("=" * 70)
    print("快速本地构建测试")
    print("=" * 70)
    
    print("\n🔍 检查基本要求...")
    
    # 检查必要文件
    required_files = [
        ("main.py", "Flet应用入口"),
        ("requirements.txt", "依赖文件"),
        ("设置界面/层级1_主入口/主入口.py", "主界面")
    ]
    
    missing = []
    for file_path, description in required_files:
        if os.path.exists(file_path):
            print(f"✅ {description}: {file_path}")
        else:
            print(f"❌ {description}: {file_path} (缺失)")
            missing.append(file_path)
    
    if missing:
        print(f"\n⚠️  缺失 {len(missing)} 个必要文件:")
        for file in missing:
            print(f"  • {file}")
        return False
    
    # 检查main.py内容
    try:
        with open("main.py", "r", encoding="utf-8") as f:
            content = f.read()
            if "ft.run" in content or "flet.run" in content:
                print("✅ main.py 包含有效的Flet入口")
            else:
                print("⚠️  main.py 可能不是有效的Flet入口")
    except Exception as e:
        print(f"❌ 无法读取main.py: {e}")
        return False
    
    return True

def test_flet_installation():
    """测试Flet安装"""
    print("\n🔧 测试Flet安装...")
    
    try:
        # 检查Python
        result = subprocess.run(["python", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Python: {result.stdout.strip()}")
        else:
            print("❌ Python未安装或不可用")
            return False
        
        # 检查pip
        result = subprocess.run(["python", "-m", "pip", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ pip可用")
        else:
            print("❌ pip不可用")
            return False
        
        # 检查Flet
        result = subprocess.run(
            ["python", "-c", "import flet; print(f'Flet版本: {flet.__version__}')"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            print(f"✅ {result.stdout.strip()}")
            return True
        else:
            print("❌ Flet未安装，尝试安装...")
            
            # 尝试安装Flet
            print("正在安装flet==0.82.0...")
            result = subprocess.run(
                ["python", "-m", "pip", "install", "flet==0.82.0"],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                print("✅ Flet安装成功")
                return True
            else:
                print(f"❌ Flet安装失败: {result.stderr}")
                return False
                
    except Exception as e:
        print(f"❌ 检查过程中出错: {e}")
        return False

def simulate_build():
    """模拟构建过程"""
    print("\n🚀 模拟构建过程...")
    
    # 清理之前的构建
    if os.path.exists("build"):
        try:
            shutil.rmtree("build")
            print("✅ 清理了之前的build目录")
        except Exception as e:
            print(f"⚠️  无法清理build目录: {e}")
    
    # 检查Flet CLI
    print("\n1. 检查Flet CLI...")
    try:
        result = subprocess.run(
            ["python", "-m", "flet.cli", "--version"],
            capture_output=True, text=True, encoding='utf-8', errors='ignore'
        )
        if result.returncode == 0:
            print(f"✅ Flet CLI: {result.stdout.strip()}")
        else:
            print(f"❌ Flet CLI检查失败: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Flet CLI检查出错: {e}")
        return False
    
    # 尝试构建（仅检查，不实际构建）
    print("\n2. 检查构建命令...")
    print("命令: python -m flet.cli build apk --project WW2Assistant")
    
    # 只运行--help查看选项
    print("\n3. 查看构建选项...")
    try:
        result = subprocess.run(
            ["python", "-m", "flet.cli", "build", "apk", "--help"],
            capture_output=True, text=True, encoding='utf-8', errors='ignore',
            timeout=30
        )
        if result.returncode == 0:
            print("✅ Flet构建命令可用")
            # 提取关键信息
            lines = result.stdout.split('\n')
            for line in lines[:10]:  # 只显示前10行
                if line.strip():
                    print(f"   {line}")
        else:
            print(f"❌ 无法获取帮助信息: {result.stderr}")
    except subprocess.TimeoutExpired:
        print("⚠️  命令超时，但可能仍在运行")
    except Exception as e:
        print(f"❌ 检查构建选项出错: {e}")
    
    return True

def check_project_structure_for_build():
    """检查项目结构是否适合构建"""
    print("\n📁 检查项目结构...")
    
    # 检查Flet相关文件
    flet_files = []
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        if 'import flet' in content or 'import flet as ft' in content:
                            flet_files.append(filepath)
                except:
                    pass
    
    if flet_files:
        print(f"✅ 找到 {len(flet_files)} 个Flet相关文件")
        print("示例文件:")
        for file in flet_files[:5]:  # 只显示前5个
            print(f"  • {file}")
    else:
        print("⚠️  未找到明显的Flet相关文件")
    
    # 检查requirements.txt
    if os.path.exists("requirements.txt"):
        print("\n📦 检查requirements.txt...")
        try:
            with open("requirements.txt", 'r', encoding='utf-8') as f:
                lines = f.readlines()
                flet_found = False
                for line in lines:
                    if 'flet' in line.lower():
                        flet_found = True
                        print(f"✅ 找到Flet依赖: {line.strip()}")
                        break
                if not flet_found:
                    print("⚠️  requirements.txt中未找到flet依赖")
        except Exception as e:
            print(f"❌ 无法读取requirements.txt: {e}")
    
    return True

def create_minimal_build_script():
    """创建最小化构建脚本"""
    print("\n🔧 创建最小化构建脚本...")
    
    script_content = """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    script_content += '''
"""
最小化Flet构建测试脚本
用于在本地测试Flet APK构建
"""

import os
import sys
import subprocess
import shutil

def main():
    """主函数"""
    print("最小化Flet构建测试")
    print("=" * 50)
    
    # 1. 检查基本环境
    print("\\n1. 检查Python环境...")
    try:
        result = subprocess.run(["python", "--version"], capture_output=True, text=True)
        print(f"   Python: {result.stdout.strip()}")
    except:
        print("   ❌ Python不可用")
        return 1
    
    # 2. 检查Flet
    print("\\n2. 检查Flet...")
    try:
        result = subprocess.run(
            ["python", "-c", "import flet; print(f'Flet版本: {flet.__version__}')"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            print(f"   ✅ {result.stdout.strip()}")
        else:
            print("   ❌ Flet未安装，尝试安装...")
            result = subprocess.run(
                ["pip", "install", "flet==0.82.0"],
                capture_output=True, text=True
            )
            if result.returncode != 0:
                print("   ❌ Flet安装失败")
                return 1
    except:
        print("   ❌ Flet检查失败")
        return 1
    
    # 3. 检查main.py
    print("\\n3. 检查main.py...")
    if not os.path.exists("main.py"):
        print("   ❌ main.py不存在")
        return 1
    
    with open("main.py", "r", encoding="utf-8") as f:
        content = f.read()
        if "ft.run" in content or "flet.run" in content:
            print("   ✅ main.py包含Flet运行入口")
        else:
            print("   ⚠️  main.py可能不是有效的Flet入口")
    
    # 4. 尝试构建（简化版）
    print("\\n4. 尝试构建...")
    print("   注意: 完整构建需要Flutter和Android SDK")
    print("   这里只测试基本命令...")
    
    try:
        # 只检查构建命令是否可用
        result = subprocess.run(
            ["python", "-m", "flet.cli", "build", "apk", "--help"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            print("   ✅ Flet构建命令可用")
            print("\\n构建命令选项:")
            for line in result.stdout.split('\\n')[:5]:
                if line.strip():
                    print(f"   {line}")
        else:
            print(f"   ❌ 构建命令检查失败: {result.stderr[:200]}")
    except subprocess.TimeoutExpired:
        print("   ⚠️  命令超时")
    except Exception as e:
        print(f"   ❌ 构建测试出错: {e}")
    
    print("\\n" + "=" * 50)
    print("✅ 基本环境检查完成")
    print("\\n💡 下一步:")
    print("1. 如果需要完整构建，请安装Flutter和Android SDK")
    print("2. 或使用Gitee/GitHub Actions进行云端构建")
    print("3. 或使用在线Flet构建服务")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
'''
    
    script_file = "minimal_build_test.py"
    with open(script_file, "w", encoding="utf-8") as f:
        f.write(script_content)
    
    print(f"✅ 已创建最小化构建测试脚本: {script_file}")
    print("\n使用方法:")
    print(f"  python {script_file}")
    
    return script_file

def main():
    """主函数"""
    print("\n🔧 Gitee构建失败诊断工具")
    print("构建ID: #7")
    print("状态: 失败")
    print("时间: 2026-04-07 10:07:55")
    
    # 检查基本要求
    if not check_basic_requirements():
        print("\n❌ 基本要求检查失败")
        return 1
    
    # 测试Flet安装
    if not test_flet_installation():
        print("\n❌ Flet安装检查失败")
        return 1
    
    # 检查项目结构
    check_project_structure_for_build()
    
    # 模拟构建
    if not simulate_build():
        print("\n⚠️  模拟构建发现潜在问题")
    
    # 创建最小化构建脚本
    script_file = create_minimal_build_script()
    
    print("\n" + "=" * 70)
    print("🎯 诊断完成")
    print("=" * 70)
    
    print("\n📋 发现的问题:")
    print("1. Gitee构建失败 #7")
    print("2. 需要检查具体错误日志")
    print("3. 可能需要调整Gitee设置")
    
    print("\n🚀 建议的解决方案:")
    print("1. 首先运行最小化测试:")
    print(f"   python {script_file}")
    print("\n2. 检查Gitee构建日志:")
    print("   访问: https://gitee.com/lzhuohui/ww2_assistant/pipelines")
    print("   点击失败的任务(#7)，查看详细错误")
    print("\n3. 运行调试工作流:")
    print("   在Gitee选择 'Simple APK Build' 工作流")
    print("   手动触发，查看每一步的输出")
    
    print("\n4. 如果Gitee仍然失败:")
    print("   • 检查流水线功能是否开启")
    print("   • 检查网络连接")
    print("   • 使用本地构建: python local_build_alternative.py")
    
    print("\n" + "=" * 70)
    print("💡 立即操作:")
    print("1. 查看Gitee构建 #7 的详细错误日志")
    print("2. 把错误信息复制给我")
    print("3. 我可以提供针对性的修复方案")
    print("=" * 70)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())