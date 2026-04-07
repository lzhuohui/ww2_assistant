# -*- coding: utf-8 -*-
"""
修复APK构建问题并重新构建
"""

import os
import sys
import shutil
import subprocess
import time
from pathlib import Path

def clean_build_directory():
    """清理构建目录"""
    print("="*60)
    print("清理构建目录")
    print("="*60)
    
    build_dir = Path("build")
    if build_dir.exists():
        try:
            shutil.rmtree(build_dir)
            print("✅ 已清理build目录")
        except Exception as e:
            print(f"❌ 清理失败: {e}")
            return False
    else:
        print("ℹ️  build目录不存在，无需清理")
    
    return True

def check_flet_cli():
    """检查Flet CLI是否可用"""
    print("\n" + "="*60)
    print("检查Flet CLI")
    print("="*60)
    
    try:
        result = subprocess.run(
            [sys.executable, "-m", "flet.cli", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print(f"✅ Flet CLI可用: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Flet CLI检查失败: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Flet CLI检查异常: {e}")
        return False

def get_main_script():
    """获取主脚本文件"""
    print("\n" + "="*60)
    print("查找主脚本文件")
    print("="*60)
    
    # 尝试找到主入口文件
    main_scripts = [
        Path("设置界面/层级1_主入口/主入口.py"),
        Path("主入口.py"),
        Path("main.py"),
        Path("app.py")
    ]
    
    for script in main_scripts:
        if script.exists():
            print(f"✅ 找到主脚本: {script}")
            return script
    
    print("❌ 未找到主脚本文件")
    return None

def build_apk_with_fix():
    """使用修复方法构建APK"""
    print("\n" + "="*60)
    print("开始构建APK（使用修复方法）")
    print("="*60)
    
    # 获取主脚本
    main_script = get_main_script()
    if not main_script:
        return False
    
    # 构建命令
    # 明确指定应用名称和主脚本
    app_name = "WW2Assistant"
    main_script_str = str(main_script)
    
    print(f"应用名称: {app_name}")
    print(f"主脚本: {main_script_str}")
    print("\n构建命令: python -m flet.cli build apk --name WW2Assistant")
    
    try:
        # 运行构建命令
        print("\n" + "="*60)
        print("开始构建...")
        print("="*60)
        
        # 设置环境变量避免编码问题
        env = os.environ.copy()
        env['PYTHONUTF8'] = '1'
        env['PYTHONIOENCODING'] = 'utf-8'
        
        # 运行构建
        process = subprocess.Popen(
            [sys.executable, "-m", "flet.cli", "build", "apk", "--name", "WW2Assistant"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding='utf-8',
            errors='replace',
            env=env
        )
        
        # 实时输出
        print("构建输出:")
        print("-" * 40)
        
        line_count = 0
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                line_count += 1
                if line_count <= 100:  # 只显示前100行，避免过多输出
                    print(output.strip())
                elif line_count == 101:
                    print("... (输出已截断，构建仍在继续) ...")
            
            # 每10行检查一次构建状态
            if line_count % 10 == 0:
                if Path("build/apk").exists():
                    print("\n✅ APK目录已创建")
                    apk_files = list(Path("build").rglob("*.apk"))
                    if apk_files:
                        print(f"🎉 找到 {len(apk_files)} 个APK文件")
                        return True
        
        # 等待进程完成
        return_code = process.wait()
        
        if return_code == 0:
            print("\n" + "="*60)
            print("✅ 构建成功完成!")
            return True
        else:
            print(f"\n❌ 构建失败，退出码: {return_code}")
            return False
            
    except Exception as e:
        print(f"\n❌ 构建异常: {e}")
        return False

def check_build_result():
    """检查构建结果"""
    print("\n" + "="*60)
    print("检查构建结果")
    print("="*60)
    
    build_dir = Path("build")
    if not build_dir.exists():
        print("❌ build目录不存在")
        return False
    
    # 检查APK文件
    apk_files = list(build_dir.rglob("*.apk"))
    
    if apk_files:
        print(f"🎉 构建成功! 找到 {len(apk_files)} 个APK文件:")
        for apk in apk_files:
            size_mb = apk.stat().st_size / (1024 * 1024)
            print(f"   📱 {apk.relative_to(Path('.'))} ({size_mb:.2f} MB)")
        return True
    else:
        print("⏳ 未找到APK文件")
        
        # 检查构建状态
        check_dirs = [
            ("build/.hash", "配置哈希"),
            ("build/site-packages", "Python依赖"),
            ("build/flutter", "Flutter项目"),
            ("build/flutter/android/app/build", "Android构建"),
            ("build/apk", "APK输出"),
        ]
        
        for dir_path, desc in check_dirs:
            path = Path(dir_path)
            if path.exists():
                if path.is_dir():
                    items = len(list(path.iterdir()))
                    print(f"   ✅ {desc}: {items}个项目")
                else:
                    print(f"   ✅ {desc}: 存在")
            else:
                print(f"   ⏳ {desc}: 缺失")
        
        return False

def main():
    """主函数"""
    print("二战风云 - APK构建修复工具")
    print("="*60)
    
    # 1. 清理旧的构建目录
    if not clean_build_directory():
        print("❌ 清理失败，无法继续")
        return
    
    # 2. 检查Flet CLI
    if not check_flet_cli():
        print("❌ Flet CLI检查失败，无法继续")
        return
    
    # 3. 构建APK
    start_time = time.time()
    success = build_apk_with_fix()
    elapsed_time = time.time() - start_time
    
    print(f"\n⏱️  构建时间: {elapsed_time:.1f}秒")
    
    # 4. 检查结果
    if success:
        print("\n" + "="*60)
        print("✅ APK构建成功!")
        print("="*60)
        
        if check_build_result():
            print("\n🎯 下一步:")
            print("1. 将APK文件传输到Android设备")
            print("2. 在设备设置中允许安装未知来源应用")
            print("3. 安装并测试应用")
            print("4. APK文件位于: build/apk/release/")
        else:
            print("\n⚠️  构建似乎成功，但未找到APK文件")
            print("   请检查构建目录获取更多信息")
    else:
        print("\n" + "="*60)
        print("❌ APK构建失败")
        print("="*60)
        
        print("\n🔧 故障排除建议:")
        print("1. 检查网络连接（需要下载Flutter和Android SDK）")
        print("2. 确保有足够的磁盘空间")
        print("3. 尝试手动运行: python -m flet.cli build apk --verbose")
        print("4. 查看详细错误信息")
        
        # 尝试获取更多错误信息
        print("\n📋 最后检查:")
        check_build_result()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n构建已取消")
    except Exception as e:
        print(f"\n❌ 程序异常: {e}")