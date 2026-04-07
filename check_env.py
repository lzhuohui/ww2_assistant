#!/usr/bin/env python3
"""
环境检查脚本 - Python版本
"""

import os
import sys
import subprocess
import platform

def run_cmd(cmd):
    """运行命令"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8')
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def print_status(name, success):
    """打印状态"""
    if success:
        print(f"✅ {name}")
    else:
        print(f"❌ {name}")

def main():
    """主函数"""
    print("="*60)
    print("🔍 环境检查")
    print("="*60)
    
    checks = []
    
    # 1. 检查Python
    print("\n1. 检查Python...")
    success, stdout, stderr = run_cmd(f'"{sys.executable}" --version')
    if success:
        print(f"✅ Python: {stdout.strip()}")
    else:
        print("❌ Python未正确安装")
    checks.append(("Python", success))
    
    # 2. 检查Flet
    print("\n2. 检查Flet...")
    try:
        import flet
        print(f"✅ Flet版本: {flet.__version__}")
        checks.append(("Flet", True))
    except ImportError:
        print("❌ Flet未安装")
        checks.append(("Flet", False))
    
    # 3. 检查Java
    print("\n3. 检查Java JDK...")
    success, stdout, stderr = run_cmd("java -version")
    if success:
        # 提取Java版本
        for line in stdout.split('\n'):
            if "version" in line.lower():
                print(f"✅ Java: {line.strip()}")
                break
    else:
        print("❌ Java未安装")
        print("   下载地址: https://www.oracle.com/java/technologies/downloads/")
        print("   或 OpenJDK: https://adoptium.net/")
    checks.append(("Java JDK", success))
    
    # 4. 检查Flutter
    print("\n4. 检查Flutter SDK...")
    success, stdout, stderr = run_cmd("flutter --version")
    if not success:
        # 尝试其他路径
        flutter_paths = [
            r"C:\flutter\bin\flutter.bat",
            r"C:\src\flutter\bin\flutter.bat",
            "flutter.bat",
            "flutter"
        ]
        for path in flutter_paths:
            success, stdout, stderr = run_cmd(f'"{path}" --version')
            if success:
                break
    
    if success:
        # 提取Flutter版本
        for line in stdout.split('\n'):
            if "Flutter" in line:
                print(f"✅ {line.strip()}")
                break
    else:
        print("❌ Flutter未安装")
        print("   下载地址: https://flutter.cn/community/china")
        print("   安装步骤:")
        print("   1. 解压到 C:\\flutter")
        print("   2. 添加环境变量 Path: C:\\flutter\\bin")
        print("   3. 设置国内镜像:")
        print("      FLUTTER_STORAGE_BASE_URL=https://storage.flutter-io.cn")
        print("      PUB_HOSTED_URL=https://pub.flutter-io.cn")
    checks.append(("Flutter SDK", success))
    
    # 5. 检查Android SDK
    print("\n5. 检查Android SDK...")
    android_home = os.environ.get('ANDROID_HOME') or os.environ.get('ANDROID_SDK_ROOT')
    if android_home:
        print(f"✅ ANDROID_HOME: {android_home}")
        # 检查adb
        adb_path = os.path.join(android_home, 'platform-tools', 'adb')
        if os.path.exists(adb_path) or os.path.exists(adb_path + '.exe'):
            print("✅ Android SDK工具已安装")
            success, stdout, stderr = run_cmd("adb --version")
            if success:
                for line in stdout.split('\n'):
                    if "Android Debug Bridge" in line:
                        print(f"✅ {line.strip()}")
                        break
            checks.append(("Android SDK", True))
        else:
            print("⚠️  Android SDK工具未找到")
            checks.append(("Android SDK", False))
    else:
        print("❌ ANDROID_HOME未设置")
        print("   下载Android Studio: https://developer.android.com/studio")
        print("   安装后设置环境变量:")
        print("   ANDROID_HOME = C:\\Users\\你的用户名\\AppData\\Local\\Android\\Sdk")
        checks.append(("Android SDK", False))
    
    # 6. 运行flutter doctor（如果Flutter已安装）
    if checks[3][1]:  # Flutter检查通过
        print("\n6. 运行flutter doctor检查...")
        # 设置国内镜像
        os.environ['FLUTTER_STORAGE_BASE_URL'] = 'https://storage.flutter-io.cn'
        os.environ['PUB_HOSTED_URL'] = 'https://pub.flutter-io.cn'
        
        success, stdout, stderr = run_cmd("flutter doctor")
        if success:
            print("✅ Flutter环境检查完成")
            # 显示关键信息
            for line in stdout.split('\n'):
                if any(keyword in line.lower() for keyword in ['[✓]', '[×]', '[!]', 'doctor', 'android', 'java', 'visual', 'chrome']):
                    print(f"   {line.strip()}")
        else:
            print("⚠️  Flutter doctor检查失败")
    
    # 总结
    print("\n" + "="*60)
    print("📋 检查结果")
    print("="*60)
    
    all_pass = True
    for check_name, check_result in checks:
        status = "✅" if check_result else "❌"
        print(f"   {status} {check_name}")
        if not check_result:
            all_pass = False
    
    print("\n" + "="*60)
    if all_pass:
        print("🎉 所有环境检查通过！可以开始构建APK")
        print("\n运行以下命令构建APK：")
        print("  python build_apk_simple.py")
        print("或")
        print("  python build_apk_full.py")
    else:
        print("⚠️  部分环境未安装完成")
        print("\n请先安装缺失的组件：")
        for check_name, check_result in checks:
            if not check_result:
                print(f"  - {check_name}")
        
        print("\n查看 download_links.html 获取下载链接")
        print("运行 环境安装指南.bat 获取安装说明")
    
    print("\n按Enter键退出...")
    input()

if __name__ == "__main__":
    main()