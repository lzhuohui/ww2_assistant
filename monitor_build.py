# -*- coding: utf-8 -*-
"""
监控APK构建进度
"""

import os
import time
import subprocess
import sys
import threading
from datetime import datetime

def check_build_progress():
    """检查构建进度"""
    print("="*60)
    print("APK构建监控器")
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    # 检查build目录中的变化
    build_dir = "build"
    apk_output_dir = "build/apk/release"
    
    print("监控构建进度...")
    print("按Ctrl+C停止监控")
    print("-"*60)
    
    start_time = time.time()
    last_check = start_time
    check_interval = 10  # 每10秒检查一次
    
    try:
        while True:
            current_time = time.time()
            elapsed = current_time - start_time
            
            # 每10秒输出一次状态
            if current_time - last_check >= check_interval:
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 构建已运行: {int(elapsed)}秒")
                
                # 检查目录变化
                if os.path.exists(build_dir):
                    print(f"  📁 build目录存在")
                    
                    # 检查APK输出目录
                    if os.path.exists(apk_output_dir):
                        print(f"  📁 APK输出目录存在: {apk_output_dir}")
                        
                        # 检查是否有APK文件
                        apk_files = []
                        for root, dirs, files in os.walk(apk_output_dir):
                            for file in files:
                                if file.endswith('.apk'):
                                    apk_files.append(os.path.join(root, file))
                        
                        if apk_files:
                            print(f"  ✅ 找到 {len(apk_files)} 个APK文件:")
                            for apk in apk_files:
                                size = os.path.getsize(apk) / (1024 * 1024)  # MB
                                print(f"    • {os.path.basename(apk)} ({size:.1f} MB)")
                            print("\n🎉 APK构建完成!")
                            return True
                    else:
                        print(f"  🔄 APK输出目录尚未创建，构建进行中...")
                        
                    # 检查build目录大小
                    total_size = 0
                    for dirpath, dirnames, filenames in os.walk(build_dir):
                        for f in filenames:
                            fp = os.path.join(dirpath, f)
                            if os.path.exists(fp):
                                total_size += os.path.getsize(fp)
                    
                    print(f"  📊 build目录大小: {total_size / (1024*1024):.1f} MB")
                else:
                    print(f"  🔄 build目录尚未创建，正在初始化...")
                
                last_check = current_time
            
            # 检查构建进程是否还在运行
            build_process_running = False
            try:
                # 简单检查是否有flutter或gradle进程
                import psutil
                for proc in psutil.process_iter(['name']):
                    if any(name in proc.info['name'].lower() for name in ['flutter', 'gradle', 'java']):
                        build_process_running = True
                        break
            except ImportError:
                # 如果没有psutil，跳过进程检查
                pass
            
            if not build_process_running and elapsed > 60:
                print("\n⚠️ 警告: 未检测到构建进程，但构建可能仍在继续")
            
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\n监控已停止")
        return False
    except Exception as e:
        print(f"\n❌ 监控错误: {e}")
        return False

def check_system_resources():
    """检查系统资源"""
    print("\n" + "="*60)
    print("系统资源检查")
    print("="*60)
    
    try:
        import psutil
        
        # CPU使用率
        cpu_percent = psutil.cpu_percent(interval=1)
        print(f"CPU使用率: {cpu_percent}%")
        
        # 内存使用
        memory = psutil.virtual_memory()
        print(f"内存使用: {memory.percent}% ({memory.used//(1024*1024)}MB / {memory.total//(1024*1024)}MB)")
        
        # 磁盘空间
        disk = psutil.disk_usage('.')
        print(f"磁盘空间: {disk.percent}% ({disk.free//(1024*1024*1024)}GB 可用)")
        
    except ImportError:
        print("安装psutil以查看系统资源详情: pip install psutil")
    except Exception as e:
        print(f"资源检查错误: {e}")

if __name__ == "__main__":
    print("二战风云 - APK构建进度监控")
    print("="*60)
    
    # 检查系统资源
    check_system_resources()
    
    # 开始监控
    success = check_build_progress()
    
    if success:
        print("\n" + "="*60)
        print("✅ APK构建成功完成!")
        print("="*60)
        print("生成的APK文件位于: build/apk/release/app-release.apk")
        print("\n下一步:")
        print("1. 将APK文件传输到Android设备")
        print("2. 在设备设置中允许安装未知来源应用")
        print("3. 安装并测试应用")
        print("4. 如有问题，检查log文件: build/logs/")
    else:
        print("\n" + "="*60)
        print("⏸️ 构建过程监控已停止")
        print("="*60)
        print("构建可能仍在后台运行...")
        print("\n手动检查构建状态:")
        print("1. 查看终端输出")
        print("2. 检查build目录中的文件")
        print("3. 运行: flet build apk --verbose 查看详细日志")