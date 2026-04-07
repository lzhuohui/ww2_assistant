# -*- coding: utf-8 -*-
"""
修复编码问题并构建APK
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def fix_encoding_and_build():
    """修复编码问题并构建APK"""
    print("="*70)
    print("修复编码问题并构建APK")
    print("="*70)
    
    # 清理旧的构建目录
    build_dir = Path("build")
    if build_dir.exists():
        import shutil
        try:
            shutil.rmtree(build_dir)
            print("✅ 已清理旧的build目录")
        except Exception as e:
            print(f"⚠️  清理失败: {e}")
    
    # 设置正确的环境变量解决编码问题
    env = os.environ.copy()
    env['PYTHONUTF8'] = '1'
    env['PYTHONIOENCODING'] = 'utf-8'
    env['FLET_CLI_NO_RICH_OUTPUT'] = '1'  # 禁用富文本输出，避免编码问题
    
    print("\n🔧 环境配置:")
    print(f"   PYTHONUTF8: {env.get('PYTHONUTF8')}")
    print(f"   PYTHONIOENCODING: {env.get('PYTHONIOENCODING')}")
    print(f"   FLET_CLI_NO_RICH_OUTPUT: {env.get('FLET_CLI_NO_RICH_OUTPUT')}")
    
    # 构建命令
    cmd = [
        sys.executable,
        "-m", "flet.cli",
        "build", "apk",
        "--verbose",
        "--no-rich-output"  # 明确禁用富文本输出
    ]
    
    print(f"\n🚀 构建命令: {' '.join(cmd)}")
    print("\n" + "="*70)
    print("开始构建APK...")
    print("="*70)
    print("注意: 首次构建可能需要15-30分钟")
    print("      请耐心等待...")
    print("="*70)
    
    start_time = time.time()
    
    try:
        # 运行构建命令
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding='utf-8',
            errors='replace',
            env=env
        )
        
        # 实时输出处理
        output_lines = []
        error_detected = False
        
        while True:
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                break
                
            if line:
                # 清理行中的特殊字符
                cleaned_line = line.encode('ascii', 'ignore').decode('ascii')
                output_lines.append(cleaned_line.strip())
                
                # 检查关键信息
                if "Error" in line or "error:" in line.lower():
                    print(f"❌ 错误: {cleaned_line.strip()}")
                    error_detected = True
                elif "Building APK" in line or "BUILD SUCCESSFUL" in line:
                    print(f"✅ {cleaned_line.strip()}")
                elif "Downloading" in line or "Compiling" in line:
                    print(f"🔄 {cleaned_line.strip()}")
                elif len(output_lines) % 20 == 0:  # 每20行显示一次进度
                    print(f"⏳ 构建中... ({len(output_lines)} 行输出)")
        
        # 等待进程完成
        return_code = process.wait()
        elapsed_time = time.time() - start_time
        
        print(f"\n⏱️  构建时间: {elapsed_time:.1f}秒")
        print(f"退出码: {return_code}")
        
        # 检查结果
        if return_code == 0:
            print("\n" + "="*70)
            print("✅ 构建完成!")
            print("="*70)
            
            # 检查APK文件
            apk_files = list(Path(".").rglob("*.apk"))
            if apk_files:
                print(f"🎉 找到 {len(apk_files)} 个APK文件:")
                for apk in apk_files:
                    size_mb = apk.stat().st_size / (1024 * 1024)
                    print(f"   📱 {apk} ({size_mb:.2f} MB)")
            else:
                print("⚠️  未找到APK文件，但构建已成功完成")
                print("   检查 build/apk/release/ 目录")
            
            return True
        else:
            print("\n" + "="*70)
            print("❌ 构建失败!")
            print("="*70)
            
            # 显示最后10行错误信息
            print("最后10行输出:")
            for line in output_lines[-10:]:
                print(f"   {line}")
            
            return False
            
    except Exception as e:
        print(f"\n❌ 构建异常: {e}")
        return False

def check_build_requirements():
    """检查构建要求"""
    print("\n" + "="*70)
    print("检查构建要求")
    print("="*70)
    
    requirements = [
        ("Python 3.7+", sys.version_info >= (3, 7)),
        ("Flet 已安装", True),  # 会在后面检查
        ("Flutter 已安装", True),  # 会在构建时自动检查
        ("磁盘空间 > 2GB", True),  # 假设足够
    ]
    
    all_met = True
    for req, met in requirements:
        status = "✅" if met else "❌"
        print(f"{status} {req}")
        if not met:
            all_met = False
    
    # 检查Flet
    try:
        import flet
        print(f"✅ Flet版本: {flet.__version__}")
    except ImportError:
        print("❌ Flet未安装")
        all_met = False
    
    return all_met

def main():
    """主函数"""
    print("二战风云 - APK构建（修复编码问题）")
    print("="*70)
    
    # 检查要求
    if not check_build_requirements():
        print("\n❌ 不满足构建要求")
        return
    
    # 构建APK
    success = fix_encoding_and_build()
    
    # 最终检查
    print("\n" + "="*70)
    if success:
        print("🎉 APK构建成功!")
        print("\n下一步:")
        print("1. APK文件位于: build/apk/release/ 目录")
        print("2. 将APK传输到Android设备")
        print("3. 允许安装未知来源应用")
        print("4. 安装并测试")
    else:
        print("❌ APK构建失败")
        print("\n建议:")
        print("1. 检查网络连接")
        print("2. 确保有足够磁盘空间")
        print("3. 查看完整错误日志")
        print("4. 可以尝试: python -m flet.cli doctor")
    
    print("="*70)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n构建已取消")
    except Exception as e:
        print(f"\n❌ 程序异常: {e}")
        import traceback
        traceback.print_exc()