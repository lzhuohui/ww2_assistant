#!/usr/bin/env python3
"""
最简单的APK构建脚本
直接尝试构建，不进行环境检查
"""

import os
import sys
import subprocess
from pathlib import Path

def run_build():
    """运行构建"""
    print("🚀 开始构建APK...")
    print("="*50)
    
    # 检查main.py
    if not Path("main.py").exists():
        print("❌ 错误：未找到main.py文件")
        print("💡 请确保在项目根目录运行此脚本")
        return False
    
    print("📄 找到main.py，开始构建...")
    
    # 构建命令
    build_cmd = [
        sys.executable,
        "-m", "flet.cli",
        "build", "apk",
        "--project", "WW2Assistant",
        "--verbose"
    ]
    
    print(f"🔨 命令：{' '.join(build_cmd)}")
    print("⏳ 构建中，这可能需要几分钟...")
    print("="*50)
    
    try:
        # 运行构建命令
        result = subprocess.run(
            build_cmd,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        # 输出结果
        if result.stdout:
            print("📋 构建输出：")
            print(result.stdout)
        
        if result.returncode == 0:
            print("="*50)
            print("✅ APK构建成功！")
            
            # 查找APK文件
            apk_files = list(Path(".").glob("**/*.apk"))
            if apk_files:
                print("\n📱 找到APK文件：")
                for apk in apk_files:
                    size = apk.stat().st_size
                    print(f"   📄 {apk.name} ({size/1024/1024:.2f} MB)")
                    
                    # 创建输出目录
                    output_dir = Path("apk-output")
                    output_dir.mkdir(exist_ok=True)
                    
                    import shutil
                    target = output_dir / apk.name
                    shutil.copy2(apk, target)
                    print(f"      📦 已复制到: {target}")
                
                print(f"\n🎉 APK文件已保存在: {output_dir.absolute()}")
                return True
            else:
                print("⚠️  构建成功但未找到APK文件")
                # 检查常见位置
                search_paths = [
                    "build/app/outputs/flutter-apk/",
                    "build/app/outputs/apk/",
                    "build/",
                ]
                for path in search_paths:
                    if Path(path).exists():
                        print(f"📁 检查目录: {path}")
                        for apk in Path(path).glob("**/*.apk"):
                            print(f"   📄 {apk}")
                return False
        else:
            print("="*50)
            print("❌ APK构建失败")
            
            if result.stderr:
                print("\n📋 错误信息：")
                print(result.stderr)
            
            # 常见错误处理
            error_msg = result.stderr.lower() if result.stderr else ""
            
            if "flutter" in error_msg and "not found" in error_msg:
                print("\n💡 解决方案：")
                print("   1. 安装Flutter SDK：https://flutter.cn/community/china")
                print("   2. 解压到 C:\\flutter")
                print("   3. 添加环境变量 Path：C:\\flutter\\bin")
                print("   4. 重启命令行窗口")
            
            elif "android" in error_msg and "sdk" in error_msg:
                print("\n💡 解决方案：")
                print("   1. 安装Android Studio：https://developer.android.com/studio")
                print("   2. 通过SDK Manager安装Android SDK")
                print("   3. 设置环境变量 ANDROID_HOME")
            
            elif "license" in error_msg:
                print("\n💡 解决方案：")
                print("   运行命令：flutter doctor --android-licenses")
                print("   对所有问题输入 y")
            
            elif "connection" in error_msg or "network" in error_msg:
                print("\n💡 解决方案：")
                print("   设置国内镜像环境变量：")
                print("   set FLUTTER_STORAGE_BASE_URL=https://storage.flutter-io.cn")
                print("   set PUB_HOSTED_URL=https://pub.flutter-io.cn")
                print("   或运行 flutter_env.bat")
            
            return False
            
    except FileNotFoundError as e:
        print(f"❌ 命令未找到：{e}")
        print("\n💡 可能的原因：")
        print("   1. Python未正确安装")
        print("   2. Flet未安装，运行：pip install flet==0.82.0")
        print("   3. Flutter未安装或不在PATH中")
        return False
    
    except Exception as e:
        print(f"❌ 构建过程出错：{e}")
        return False

def main():
    """主函数"""
    print("📱 Flet APK简单构建工具")
    print("="*50)
    print("直接尝试构建，不进行环境检查")
    print("如果失败，请查看错误信息并解决问题")
    print("="*50)
    
    # 显示当前目录
    print(f"📁 当前目录：{os.getcwd()}")
    
    # 检查Python和Flet
    try:
        import flet
        print(f"✅ Flet版本：{flet.__version__}")
    except ImportError:
        print("❌ Flet未安装")
        install = input("是否安装Flet？(y/n): ").strip().lower()
        if install == 'y':
            subprocess.run([sys.executable, "-m", "pip", "install", "flet==0.82.0"])
        else:
            print("❌ 需要Flet才能构建APK")
            return
    
    # 运行构建
    success = run_build()
    
    if not success:
        print("\n" + "="*50)
        print("💡 建议操作：")
        print("   1. 运行 'python simple_build_test.py' 检查环境")
        print("   2. 运行 'python build_apk_full.py' 完整环境检查")
        print("   3. 查看 'Flet本地APK构建完整教程.md' 获取详细指南")
        print("   4. 运行 'flutter_env.bat' 设置国内镜像")
        print("="*50)
    
    print("\n按Enter键退出...")
    input()

if __name__ == "__main__":
    main()