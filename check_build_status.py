# -*- coding: utf-8 -*-
"""
检查APK构建状态
"""

import os
import sys
import time
from datetime import datetime

def check_build_status():
    """检查构建状态"""
    print("="*60)
    print("APK构建状态检查")
    print(f"检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    build_dir = "build"
    if not os.path.exists(build_dir):
        print("❌ build目录不存在")
        print("   构建过程可能尚未开始或已失败")
        return False
    
    print(f"✅ build目录存在")
    
    # 检查关键目录和文件
    check_items = [
        ("build/.hash", "构建哈希目录"),
        ("build/site-packages", "Python依赖包目录"),
        ("build/flutter", "Flutter项目目录"),
        ("build/apk", "APK输出目录"),
        ("build/apk/release", "Release APK目录"),
        ("build/apk/debug", "Debug APK目录"),
    ]
    
    for path, desc in check_items:
        if os.path.exists(path):
            if os.path.isdir(path):
                item_count = len(os.listdir(path))
                print(f"✅ {path} ({desc}) - 包含 {item_count} 个项目")
            else:
                size = os.path.getsize(path) / 1024  # KB
                print(f"✅ {path} ({desc}) - 大小: {size:.1f} KB")
        else:
            print(f"⏳ {path} ({desc}) - 尚未创建")
    
    print("\n" + "="*60)
    print("检查APK文件:")
    
    # 搜索所有APK文件
    apk_files = []
    for root, dirs, files in os.walk(build_dir):
        for file in files:
            if file.endswith('.apk'):
                full_path = os.path.join(root, file)
                apk_files.append(full_path)
    
    if apk_files:
        print(f"✅ 找到 {len(apk_files)} 个APK文件:")
        for apk in apk_files:
            size = os.path.getsize(apk) / (1024 * 1024)  # MB
            relative_path = os.path.relpath(apk, build_dir)
            print(f"  • {relative_path} ({size:.2f} MB)")
    else:
        print("⏳ 尚未生成APK文件")
        print("\n构建过程可能还在进行中，这很正常:")
        print("1. 首次构建需要下载Flutter和Android SDK")
        print("2. 需要编译Flutter应用")
        print("3. 需要打包Python运行时和依赖")
        print("4. 整个过程可能需要10-30分钟")
    
    # 检查构建目录大小
    print("\n" + "="*60)
    print("构建目录统计:")
    
    total_size = 0
    total_files = 0
    total_dirs = 0
    
    for root, dirs, files in os.walk(build_dir):
        total_dirs += len(dirs)
        total_files += len(files)
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.exists(file_path):
                try:
                    total_size += os.path.getsize(file_path)
                except:
                    pass
    
    print(f"总目录数: {total_dirs}")
    print(f"总文件数: {total_files}")
    print(f"总大小: {total_size / (1024*1024):.2f} MB")
    
    # 检查是否有进行中的构建迹象
    print("\n" + "="*60)
    print("构建进程状态:")
    
    # 检查是否有锁定文件或临时文件
    lock_files = []
    temp_files = []
    
    for root, dirs, files in os.walk(build_dir):
        for file in files:
            if file.endswith('.lock') or file.endswith('.tmp') or file.endswith('.temp'):
                lock_files.append(os.path.join(root, file))
            if file.startswith('temp_') or file.startswith('tmp_'):
                temp_files.append(os.path.join(root, file))
    
    if lock_files:
        print(f"🔒 发现 {len(lock_files)} 个锁定文件 - 构建可能正在进行中")
    if temp_files:
        print(f"⏳ 发现 {len(temp_files)} 个临时文件 - 构建可能正在进行中")
    
    if not lock_files and not temp_files and not apk_files:
        print("ℹ️ 未发现进行中的构建迹象")
        print("   可能需要重新启动构建: flet build apk")
    
    print("\n" + "="*60)
    print("建议操作:")
    
    if apk_files:
        print("✅ APK已构建完成!")
        print("   1. 将APK文件传输到Android设备")
        print("   2. 允许安装未知来源应用")
        print("   3. 安装并测试")
    else:
        print("⏳ 构建进行中或尚未开始")
        print("   1. 等待构建完成 (首次构建需要10-30分钟)")
        print("   2. 检查终端输出获取进度")
        print("   3. 或重新运行: flet build apk --verbose")
    
    return bool(apk_files)

if __name__ == "__main__":
    if check_build_status():
        sys.exit(0)
    else:
        sys.exit(1)