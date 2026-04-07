#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
诊断Flet APK构建路径问题
"""

import os
import subprocess
import sys

def run_flet_build_test():
    """运行Flet构建测试来查看实际输出路径"""
    print("=" * 60)
    print("诊断Flet APK构建路径问题")
    print("=" * 60)
    
    # 清理之前的构建
    if os.path.exists("build"):
        print("清理之前的构建目录...")
        import shutil
        shutil.rmtree("build")
    
    # 设置环境变量
    env = os.environ.copy()
    env['FLET_CLI_NO_RICH_OUTPUT'] = '1'
    env['PYTHONIOENCODING'] = 'utf-8'
    
    print("\n1. 运行Flet构建命令（仅显示路径信息）...")
    
    # 首先检查Flet版本和帮助信息
    print("\n检查Flet版本:")
    subprocess.run(["python", "-m", "flet.cli", "--version"], env=env)
    
    print("\n检查构建帮助:")
    subprocess.run(["python", "-m", "flet.cli", "build", "apk", "--help"], env=env)
    
    print("\n2. 模拟构建过程（不实际构建）...")
    
    # 创建一个简单的测试脚本来查找构建输出
    test_script = """
import os
import subprocess
import sys

# 测试命令
cmd = ["python", "-m", "flet.cli", "build", "apk", "--verbose", "--project", "WW2Assistant"]
print(f"将要执行的命令: {' '.join(cmd)}")

# 检查可能的输出目录
possible_dirs = [
    "build",
    "build/apk",
    "build/android",
    "android",
    "android/app/build",
    "dist",
    "outputs"
]

print("\\n检查现有的构建相关目录:")
for dir_path in possible_dirs:
    if os.path.exists(dir_path):
        print(f"  {dir_path}: 存在")
        # 列出内容
        try:
            for root, dirs, files in os.walk(dir_path):
                level = root.replace(dir_path, '').count(os.sep)
                indent = ' ' * 2 * level
                print(f'{indent}{os.path.basename(root)}/')
                subindent = ' ' * 2 * (level + 1)
                for file in files:
                    print(f'{subindent}{file}')
        except Exception as e:
            print(f"    无法遍历目录: {e}")
    else:
        print(f"  {dir_path}: 不存在")

print("\\nFlet构建APK可能的输出路径:")
print("1. build/apk/ - 默认输出目录")
print("2. build/android/ - 可能的位置")
print("3. android/app/build/outputs/apk/ - Android Studio风格")
print("4. 直接在build/目录下")
"""
    
    with open("test_build_path.py", "w", encoding="utf-8") as f:
        f.write(test_script)
    
    subprocess.run(["python", "test_build_path.py"], env=env)
    
    # 清理测试文件
    if os.path.exists("test_build_path.py"):
        os.remove("test_build_path.py")
    
    print("\n3. 检查项目结构...")
    
    # 检查main.py是否存在
    if os.path.exists("main.py"):
        print("✅ main.py存在")
        with open("main.py", "r", encoding="utf-8") as f:
            content = f.read()
            if "ft.run" in content or "flet.run" in content:
                print("✅ main.py包含flet.run调用")
            else:
                print("⚠️  main.py可能不是有效的Flet入口")
    else:
        print("❌ main.py不存在")
    
    # 检查requirements.txt
    if os.path.exists("requirements.txt"):
        print("✅ requirements.txt存在")
        with open("requirements.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
            flet_found = any("flet" in line.lower() for line in lines)
            if flet_found:
                print("✅ requirements.txt包含flet")
            else:
                print("⚠️  requirements.txt可能不包含flet")
    else:
        print("❌ requirements.txt不存在")
    
    print("\n4. 建议的解决方案:")
    print("A. 修改工作流文件，搜索所有可能的APK文件:")
    print("""
    - name: Find and upload APK
      if: success()
      run: |
        echo "搜索APK文件..."
        find . -name "*.apk" -type f | head -20
        echo "将所有APK文件打包..."
        mkdir -p artifacts
        find . -name "*.apk" -type f -exec cp {} artifacts/ \\;
        
    - name: Upload APK artifacts
      uses: actions/upload-artifact@v4
      with:
        name: ww2-assistant-apk
        path: artifacts/*.apk
        retention-days: 7
    """)
    
    print("\nB. 或者使用更通用的路径:")
    print("""
    - name: Upload all build artifacts
      if: success()
      uses: actions/upload-artifact@v4
      with:
        name: build-output
        path: build/
        retention-days: 7
    """)
    
    return True

def main():
    """主函数"""
    try:
        run_flet_build_test()
    except Exception as e:
        print(f"\n❌ 诊断过程中出错: {e}")
        return 1
    
    print("\n" + "=" * 60)
    print("诊断完成！")
    print("=" * 60)
    print("\n📋 总结建议:")
    print("1. Flet构建APK的输出路径可能不是标准的 build/apk/")
    print("2. 建议修改工作流文件，使用通配符搜索APK文件")
    print("3. 或者上传整个build目录作为构建产物")
    print("\n💡 下一步:")
    print("运行以下命令查看本地构建输出:")
    print("  python -m flet.cli build apk --verbose --project WW2Assistant")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())