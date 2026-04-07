# -*- coding: utf-8 -*-
"""
简单构建监控
"""

import os
import time
from datetime import datetime
from pathlib import Path

def monitor_build():
    """监控构建进度"""
    print("="*60)
    print("APK构建监控")
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    build_dir = Path("build")
    apk_files = []
    
    try:
        while True:
            # 清屏并显示状态
            os.system('cls' if os.name == 'nt' else 'clear')
            
            print("="*60)
            print(f"APK构建监控 - {datetime.now().strftime('%H:%M:%S')}")
            print("="*60)
            
            if not build_dir.exists():
                print("❌ build目录不存在")
                print("构建可能尚未开始或已失败")
                time.sleep(5)
                continue
            
            # 计算目录大小
            total_size = 0
            file_count = 0
            dir_count = 0
            
            for root, dirs, files in os.walk(build_dir):
                dir_count += len(dirs)
                file_count += len(files)
                for file in files:
                    try:
                        total_size += os.path.getsize(os.path.join(root, file))
                    except:
                        pass
            
            print(f"📊 构建目录: {total_size/(1024*1024):.2f} MB")
            print(f"📁 包含: {dir_count}个目录, {file_count}个文件")
            
            # 检查关键目录
            print("\n📂 关键目录状态:")
            
            check_dirs = [
                ("build/.hash", "配置哈希"),
                ("build/site-packages", "Python依赖"),
                ("build/flutter", "Flutter项目"),
                ("build/flutter/android", "Android项目"),
                ("build/flutter/android/app", "Android应用"),
                ("build/apk", "APK输出"),
            ]
            
            for dir_path, desc in check_dirs:
                path = Path(dir_path)
                if path.exists():
                    if path.is_dir():
                        items = len(list(path.iterdir()))
                        print(f"   ✅ {desc}: {items}个项目")
                    else:
                        print(f"   ✅ {desc}: 文件存在")
                else:
                    print(f"   ⏳ {desc}: 等待中...")
            
            # 搜索APK文件
            apk_files = list(build_dir.rglob("*.apk"))
            if apk_files:
                print(f"\n🎉 找到 {len(apk_files)} 个APK文件:")
                for apk in apk_files:
                    size_mb = apk.stat().st_size / (1024 * 1024)
                    rel_path = apk.relative_to(build_dir)
                    print(f"   📱 {rel_path} ({size_mb:.2f} MB)")
                print("\n✅ APK构建完成!")
                break
            
            # 显示进度条（基于目录大小增长）
            print(f"\n⏱️  已运行: {int(time.time() - start_time)}秒")
            
            # 估计剩余时间（首次构建通常需要15-30分钟）
            if total_size < 50 * 1024 * 1024:  # 小于50MB
                print("🔄 构建初始化阶段... (可能需要10-20分钟)")
            elif total_size < 200 * 1024 * 1024:  # 小于200MB
                print("🔄 编译阶段... (可能需要5-15分钟)")
            else:
                print("🔄 打包阶段... (可能需要1-5分钟)")
            
            print("\n按Ctrl+C停止监控")
            time.sleep(10)  # 每10秒更新一次
            
    except KeyboardInterrupt:
        print("\n\n监控已停止")
        print(f"构建总时间: {int(time.time() - start_time)}秒")
        print(f"构建目录大小: {total_size/(1024*1024):.2f} MB")
        
        if apk_files:
            print("\n✅ APK文件已生成!")
        else:
            print("\n⏳ 构建可能仍在进行中")
            print("检查终端输出获取详细进度")

if __name__ == "__main__":
    start_time = time.time()
    monitor_build()