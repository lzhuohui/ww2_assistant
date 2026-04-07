#!/usr/bin/env python3
"""
极简构建测试脚本
用于快速测试基础环境
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_step(step, message):
    """打印步骤信息"""
    print(f"\n{'='*50}")
    print(f"🔧 步骤 {step}: {message}")
    print(f"{'='*50}")

def run_cmd(cmd, desc="", silent=False):
    """运行命令"""
    if desc and not silent:
        print(f"\n📝 {desc}")
    if not silent:
        print(f"$ {cmd}")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            if not silent:
                print("✅ 成功")
                if result.stdout.strip():
                    print(f"输出: {result.stdout.strip()}")
            return True, result.stdout
        else:
            if not silent:
                print("❌ 失败")
                if result.stderr:
                    print(f"错误: {result.stderr.strip()}")
            return False, result.stderr
    except Exception as e:
        if not silent:
            print(f"⚠️  命令执行异常: {e}")
        return False, str(e)

def main():
    """主函数"""
    print("🚀 极简构建环境测试")
    print("="*60)
    
    print_step(1, "检查Python环境")
    success, version = run_cmd(f'"{sys.executable}" --version', "Python版本")
    if not success:
        print("❌ Python环境检查失败")
        print("💡 请安装Python 3.8+：https://www.python.org/downloads/")
        return
    
    print_step(2, "检查pip")
    success, _ = run_cmd(f'"{sys.executable}" -m pip --version', "pip版本")
    if not success:
        print("❌ pip检查失败")
        print("💡 请确保pip已安装")
        return
    
    print_step(3, "检查Flet安装")
    try:
        import flet
        print(f"✅ Flet已安装，版本: {flet.__version__}")
    except ImportError:
        print("❌ Flet未安装")
        print("正在安装Flet...")
        success, _ = run_cmd(f'"{sys.executable}" -m pip install flet==0.82.0', "安装Flet")
        if not success:
            print("❌ Flet安装失败")
            return
    
    print_step(4, "检查项目结构")
    current_dir = Path.cwd()
    print(f"📁 当前目录: {current_dir}")
    
    # 检查必要文件
    required_files = ["main.py", "requirements.txt"]
    for file in required_files:
        if Path(file).exists():
            print(f"✅ 找到: {file}")
        else:
            print(f"❌ 未找到: {file}")
    
    # 检查main.py
    main_file = Path("main.py")
    if main_file.exists():
        size = main_file.stat().st_size
        print(f"📄 main.py大小: {size} 字节")
        
        # 读取前几行
        try:
            with open(main_file, 'r', encoding='utf-8') as f:
                first_lines = [next(f).strip() for _ in range(5)]
            print("📝 文件内容预览:")
            for i, line in enumerate(first_lines, 1):
                print(f"   {i}: {line}")
        except:
            print("⚠️  无法读取文件内容")
    else:
        print("❌ 未找到main.py，请在项目根目录运行此脚本")
        return
    
    print_step(5, "检查requirements.txt")
    req_file = Path("requirements.txt")
    if req_file.exists():
        with open(req_file, 'r', encoding='utf-8') as f:
            deps = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        print(f"📦 依赖项: {len(deps)} 个")
        for dep in deps[:10]:
            print(f"   - {dep}")
    else:
        print("📝 创建requirements.txt...")
        req_file.write_text("flet==0.82.0\n")
        print("✅ 已创建requirements.txt")
    
    print_step(6, "安装依赖")
    success, _ = run_cmd(f'"{sys.executable}" -m pip install -r requirements.txt', "安装依赖")
    if not success:
        print("⚠️  依赖安装失败，尝试单独安装...")
        run_cmd(f'"{sys.executable}" -m pip install flet==0.82.0', "安装Flet")
    
    print_step(7, "验证Flet功能")
    test_code = """
import flet as ft

def main(page: ft.Page):
    page.title = "测试应用"
    page.add(ft.Text("Flet测试应用运行正常！"))
    print("✅ Flet测试通过")

if __name__ == "__main__":
    ft.app(target=main)
"""
    
    test_file = Path("test_flet.py")
    test_file.write_text(test_code, encoding='utf-8')
    
    print("运行Flet测试...")
    success, output = run_cmd(f'"{sys.executable}" test_flet.py', "Flet功能测试")
    
    # 清理测试文件
    test_file.unlink(missing_ok=True)
    
    if success and "✅ Flet测试通过" in output:
        print("🎉 Flet功能正常！")
    else:
        print("⚠️  Flet测试失败，但可能仍可工作")
    
    print_step(8, "检查构建环境")
    print("🔍 检查Flutter...")
    flutter_found = False
    for cmd in ["flutter", "flutter.bat", r"C:\flutter\bin\flutter.bat"]:
        success, _ = run_cmd(f'{cmd} --version', f"检查{cmd}", silent=True)
        if success:
            flutter_found = True
            break
    
    if flutter_found:
        print("✅ Flutter已安装")
    else:
        print("❌ Flutter未安装")
        print("\n📥 需要安装Flutter SDK：")
        print("   1. 下载: https://flutter.dev/docs/get-started/install")
        print("   2. 解压到: C:\\flutter")
        print("   3. 添加环境变量Path: C:\\flutter\\bin")
        print("   4. 运行: flutter --version")
    
    print_step(9, "构建准备就绪检查")
    print("📋 环境检查结果:")
    
    checks = [
        ("Python 3.8+", True if "Python 3" in version else False),
        ("pip", success),
        ("Flet", True),
        ("项目文件", main_file.exists()),
        ("Flutter SDK", flutter_found),
    ]
    
    all_pass = True
    for check_name, check_result in checks:
        status = "✅" if check_result else "❌"
        print(f"   {status} {check_name}")
        if not check_result:
            all_pass = False
    
    if all_pass:
        print("\n🎉 所有检查通过！可以开始构建APK")
        print("\n🚀 运行构建命令:")
        print(f'   "{sys.executable}" -m flet.cli build apk --project "WW2Assistant" --verbose')
        
        response = input("\n❓ 是否立即开始构建APK？(y/n): ").strip().lower()
        if response == 'y':
            print("\n🔨 开始构建APK...")
            run_cmd(f'"{sys.executable}" -m flet.cli build apk --project "WW2Assistant" --verbose', "构建APK")
    else:
        print("\n⚠️  部分检查未通过")
        print("💡 请先解决上述问题，然后重新运行此脚本")
    
    print_step(10, "完成")
    print("📋 下一步操作:")
    print("   1. 安装缺失的组件（如Flutter）")
    print("   2. 运行: python local_apk_builder.py")
    print("   3. 或运行: python -m flet.cli build apk --project \"WW2Assistant\"")
    print("\n🆘 如果遇到问题，请提供:")
    print("   - 错误信息截图")
    print("   - 执行的命令")
    print("   - 系统环境信息")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 用户取消操作")
    except Exception as e:
        print(f"\n❌ 程序出错: {e}")
        import traceback
        traceback.print_exc()