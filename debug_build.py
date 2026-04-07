# -*- coding: utf-8 -*-
"""
调试构建问题
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def check_build_environment():
    """检查构建环境"""
    print("="*60)
    print("检查构建环境")
    print("="*60)
    
    # 检查虚拟环境
    venv_path = Path("venv_new")
    if not venv_path.exists():
        print("❌ 虚拟环境不存在: venv_new")
        return False
    print("✅ 虚拟环境存在")
    
    # 检查Flet是否安装
    try:
        result = subprocess.run(
            [sys.executable, "-m", "flet", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print(f"✅ Flet已安装: {result.stdout.strip()}")
        else:
            print(f"❌ Flet检查失败: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Flet检查异常: {e}")
        return False
    
    # 检查Flutter
    flutter_paths = [
        Path("C:/Users/chmm1/flutter/3.41.4/bin/flutter.bat"),
        Path("C:/Users/chmm1/flutter/bin/flutter.bat"),
        Path("C:/flutter/bin/flutter.bat"),
    ]
    
    flutter_found = False
    for flutter_path in flutter_paths:
        if flutter_path.exists():
            print(f"✅ Flutter找到: {flutter_path}")
            flutter_found = True
            break
    
    if not flutter_found:
        print("⚠️  Flutter未找到，构建可能会自动下载")
    
    return True

def check_build_logs():
    """检查构建日志"""
    print("\n" + "="*60)
    print("检查构建日志")
    print("="*60)
    
    build_dir = Path("build")
    if not build_dir.exists():
        print("❌ build目录不存在")
        return
    
    # 查找任何日志文件
    log_files = list(build_dir.rglob("*.log")) + list(build_dir.rglob("*.txt"))
    
    if log_files:
        print(f"✅ 找到 {len(log_files)} 个日志文件")
        for log_file in log_files[:5]:  # 只显示前5个
            size_kb = log_file.stat().st_size / 1024
            print(f"  • {log_file.relative_to(build_dir)} ({size_kb:.1f} KB)")
            
            # 读取最后几行
            try:
                with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                    if lines:
                        print(f"    最后内容: {lines[-1].strip()}")
            except:
                pass
    else:
        print("⚠️  未找到日志文件")
    
    # 检查是否有错误文件
    error_files = list(build_dir.rglob("*error*"))
    if error_files:
        print(f"\n⚠️  找到 {len(error_files)} 个可能包含错误的文件:")
        for err_file in error_files:
            print(f"  • {err_file.relative_to(build_dir)}")

def check_build_steps():
    """检查构建步骤状态"""
    print("\n" + "="*60)
    print("检查构建步骤状态")
    print("="*60)
    
    build_dir = Path("build")
    if not build_dir.exists():
        print("❌ 构建尚未开始")
        return
    
    steps = [
        ("build/.hash", "构建配置哈希", True),
        ("build/site-packages", "Python依赖包", True),
        ("build/flutter", "Flutter项目", True),
        ("build/flutter/android", "Android项目", False),
        ("build/flutter/android/app", "Android应用", False),
        ("build/apk", "APK输出目录", False),
    ]
    
    for path_str, description, required in steps:
        path = Path(path_str)
        if path.exists():
            if path.is_dir():
                item_count = len(list(path.iterdir()))
                print(f"✅ {description}: 存在 ({item_count}个项目)")
            else:
                print(f"✅ {description}: 存在")
        else:
            if required:
                print(f"⏳ {description}: 缺失 (必需)")
            else:
                print(f"⏳ {description}: 尚未创建")

def check_processes():
    """检查相关进程"""
    print("\n" + "="*60)
    print("检查构建相关进程")
    print("="*60)
    
    try:
        import psutil
        
        build_processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                cmdline = ' '.join(proc.info['cmdline'] or [])
                name = proc.info['name'] or ''
                
                # 检查是否包含构建相关关键词
                keywords = ['flutter', 'flet', 'gradle', 'java', 'dart']
                if any(keyword in cmdline.lower() or keyword in name.lower() for keyword in keywords):
                    build_processes.append(proc)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        if build_processes:
            print(f"✅ 找到 {len(build_processes)} 个构建相关进程:")
            for proc in build_processes:
                try:
                    cmdline = ' '.join(proc.info['cmdline'] or [])
                    print(f"  • PID {proc.pid}: {proc.info['name']}")
                    # 显示简短命令
                    if len(cmdline) > 100:
                        print(f"    命令: {cmdline[:100]}...")
                    else:
                        print(f"    命令: {cmdline}")
                except:
                    print(f"  • PID {proc.pid}: {proc.info['name']}")
        else:
            print("⚠️  未找到构建相关进程")
            
    except ImportError:
        print("ℹ️  安装psutil以查看进程详情: pip install psutil")
    
    print("\n" + "="*60)
    print("构建状态总结")
    print("="*60)
    
    # 总结
    has_apk = any(Path("build").rglob("*.apk"))
    has_flutter = Path("build/flutter").exists()
    has_site_packages = Path("build/site-packages").exists()
    has_hash = Path("build/.hash").exists()
    
    if has_apk:
        print("🎉 APK构建完成！")
        apk_files = list(Path("build").rglob("*.apk"))
        for apk in apk_files:
            size_mb = apk.stat().st_size / (1024 * 1024)
            print(f"  📱 {apk.relative_to(Path('.'))} ({size_mb:.2f} MB)")
    elif has_flutter:
        print("🔄 构建进行中 (Flutter项目已创建)")
        print("   预计还需5-15分钟")
    elif has_site_packages and has_hash:
        print("⏳ 构建初始化阶段")
        print("   正在准备Python依赖")
        print("   预计还需10-20分钟")
    elif has_hash:
        print("⏳ 构建刚开始")
        print("   正在初始化构建环境")
        print("   预计还需15-30分钟")
    else:
        print("❓ 构建状态未知")
        print("   可能需要重新启动构建")

def main():
    """主函数"""
    print("二战风云 - APK构建调试工具")
    print("="*60)
    
    if not check_build_environment():
        print("\n❌ 构建环境检查失败")
        print("请确保:")
        print("1. 虚拟环境已激活")
        print("2. Flet已安装: pip install flet")
        print("3. Flutter已安装或可自动下载")
        return
    
    check_build_logs()
    check_build_steps()
    check_processes()
    
    print("\n" + "="*60)
    print("建议操作:")
    print("="*60)
    
    # 基于当前状态给出建议
    has_apk = any(Path("build").rglob("*.apk"))
    
    if has_apk:
        print("✅ 构建已完成")
        print("   运行: python monitor_build_progress.py 查看APK文件")
    else:
        print("🔄 构建进行中")
        print("   耐心等待，首次构建需要较长时间")
        print("   或检查终端输出: flet build apk --verbose")
        print("   如需重新构建: 删除build目录后重新运行")

if __name__ == "__main__":
    main()