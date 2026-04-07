# -*- coding: utf-8 -*-
"""
APK构建脚本
用于构建二战风云辅助工具的Android APK
"""

import os
import sys
import subprocess
import time

def check_dependencies():
    """检查所有必需的依赖"""
    print("="*60)
    print("检查APK构建依赖")
    print("="*60)
    
    dependencies = [
        ("flet", "flet==0.82.0"),
        ("PyYAML", "PyYAML>=6.0"),
        ("cryptography", "cryptography>=42.0.0"),
        ("pypinyin", "pypinyin>=0.51.0"),
    ]
    
    all_ok = True
    for dep, expected in dependencies:
        try:
            if dep == "flet":
                import flet
                version = flet.__version__
            elif dep == "PyYAML":
                import yaml
                version = yaml.__version__
            elif dep == "cryptography":
                import cryptography
                version = cryptography.__version__
            elif dep == "pypinyin":
                import pypinyin
                version = pypinyin.__version__
            
            print(f"✅ {dep}: 版本 {version}")
        except ImportError as e:
            print(f"❌ {dep}: 未安装 ({e})")
            all_ok = False
    
    print("\n" + "="*60)
    return all_ok

def check_project_structure():
    """检查项目结构"""
    print("检查项目结构...")
    
    required_files = [
        "requirements.txt",
        "flet.yaml",
        "main.py",
        "build/flutter/pubspec.yaml",
        "build/flutter/android/app/build.gradle.kts",
        "build/flutter/android/app/src/main/AndroidManifest.xml",
    ]
    
    all_ok = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} 不存在")
            all_ok = False
    
    print("\n" + "="*60)
    return all_ok

def build_apk():
    """构建APK"""
    print("="*60)
    print("开始构建APK")
    print("="*60)
    
    try:
        # 检查是否在虚拟环境中
        if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            print("⚠️ 警告：建议在虚拟环境中构建APK")
            print("   当前目录: " + os.getcwd())
            print("   Python路径: " + sys.executable)
        
        # 执行flet build apk命令
        print("执行: flet build apk")
        print("这可能需要几分钟时间...")
        
        start_time = time.time()
        
        # 使用subprocess运行命令
        result = subprocess.run(
            ["flet", "build", "apk"],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        
        elapsed_time = time.time() - start_time
        
        print("\n" + "="*60)
        print(f"构建完成，耗时: {elapsed_time:.1f}秒")
        print("="*60)
        
        if result.returncode == 0:
            print("✅ APK构建成功!")
            print(f"输出: {result.stdout}")
            
            # 检查生成的APK文件
            apk_path = "build/apk/release/app-release.apk"
            if os.path.exists(apk_path):
                apk_size = os.path.getsize(apk_path) / (1024 * 1024)  # MB
                print(f"✅ APK文件已生成: {apk_path}")
                print(f"   APK大小: {apk_size:.2f} MB")
            else:
                # 尝试其他可能的路径
                import glob
                apk_files = glob.glob("build/**/*.apk", recursive=True)
                if apk_files:
                    for apk_file in apk_files:
                        size = os.path.getsize(apk_file) / (1024 * 1024)
                        print(f"✅ 找到APK文件: {apk_file}")
                        print(f"   APK大小: {size:.2f} MB")
                else:
                    print("⚠️ 未找到APK文件，请检查build目录")
        else:
            print("❌ APK构建失败!")
            print(f"返回码: {result.returncode}")
            print(f"错误输出:\n{result.stderr}")
            print(f"标准输出:\n{result.stdout}")
            
    except Exception as e:
        print(f"❌ 构建过程中出现异常: {e}")
        print("="*60)
        return False
    
    print("\n" + "="*60)
    return True

def main():
    """主函数"""
    print("二战风云辅助工具 - APK构建脚本")
    print("="*60)
    
    # 检查依赖
    if not check_dependencies():
        print("❌ 依赖检查失败，请先安装缺失的依赖包")
        print("   运行: pip install -r requirements.txt")
        return
    
    # 检查项目结构
    if not check_project_structure():
        print("❌ 项目结构不完整")
        return
    
    # 询问是否继续构建
    print("\n" + "="*60)
    print("准备构建APK")
    print("="*60)
    
    response = input("是否开始构建APK? (y/n): ").strip().lower()
    if response not in ['y', 'yes', '是']:
        print("取消构建")
        return
    
    # 开始构建
    build_apk()
    
    print("\n" + "="*60)
    print("APK构建流程完成")
    print("="*60)
    print("下一步:")
    print("1. 将生成的APK文件传输到Android设备")
    print("2. 在设备上安装APK（可能需要允许安装未知来源应用）")
    print("3. 运行应用测试功能")
    print("="*60)

if __name__ == "__main__":
    main()