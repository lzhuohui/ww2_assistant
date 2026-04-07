# -*- coding: utf-8 -*-
"""
检查APK构建路径
"""

import os
import sys

def check_apk_paths():
    """检查APK可能输出的路径"""
    print("APK输出路径检查")
    print("="*60)
    
    # 可能的APK输出路径
    possible_paths = [
        "build/apk/release/app-release.apk",
        "build/apk/debug/app-debug.apk",
        "build/android/app/outputs/apk/release/app-release.apk",
        "build/android/app/outputs/apk/debug/app-debug.apk",
        "build/android/app/release/app-release.apk",
        "build/android/app/debug/app-debug.apk",
        "build/android/release/app-release.apk",
        "build/android/debug/app-debug.apk",
        "build/outputs/apk/release/app-release.apk",
        "build/outputs/apk/debug/app-debug.apk",
    ]
    
    print("可能的APK输出路径:")
    for path in possible_paths:
        if os.path.exists(path):
            size = os.path.getsize(path) / (1024 * 1024)  # MB
            print(f"✅ 存在: {path} ({size:.2f} MB)")
        else:
            print(f"❌ 不存在: {path}")
    
    print("\n" + "="*60)
    print("检查Flet默认构建目录结构:")
    
    # 检查build目录结构
    build_dir = "build"
    if os.path.exists(build_dir):
        print(f"📁 build目录存在")
        for root, dirs, files in os.walk(build_dir):
            level = root.replace(build_dir, '').count(os.sep)
            indent = ' ' * 2 * level
            print(f"{indent}{os.path.basename(root)}/")
            subindent = ' ' * 2 * (level + 1)
            for file in files:
                if file.endswith('.apk'):
                    print(f"{subindent}🔍 {file} (APK文件)")
                elif file.endswith('.aab'):
                    print(f"{subindent}🔍 {file} (AAB文件)")
                elif file.endswith('.ipa'):
                    print(f"{subindent}🔍 {file} (iOS应用文件)")
    else:
        print("📁 build目录不存在")
    
    print("\n" + "="*60)
    print("Flet APK构建说明:")
    print("1. 默认APK输出路径: build/apk/release/app-release.apk")
    print("2. 使用命令: flet build apk")
    print("3. 可以指定输出目录: flet build apk -o ./output")
    print("4. 构建过程需要安装Flutter和Android SDK")
    print("5. 构建时间通常需要10-30分钟")
    
    print("\n" + "="*60)
    print("当前项目状态:")
    
    # 检查关键文件
    required_files = [
        ("main.py", "应用入口点"),
        ("flet.yaml", "Flet配置文件"),
        ("requirements.txt", "Python依赖"),
        ("build/flutter/pubspec.yaml", "Flutter项目配置"),
        ("build/flutter/android/app/build.gradle.kts", "Android构建配置"),
    ]
    
    for file, desc in required_files:
        if os.path.exists(file):
            print(f"✅ {file} ({desc})")
        else:
            print(f"❌ {file} ({desc}) - 文件不存在")

if __name__ == "__main__":
    check_apk_paths()