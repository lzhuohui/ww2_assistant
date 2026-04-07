# -*- coding: utf-8 -*-
"""
实时监控APK构建进度
"""

import os
import time
import threading
import subprocess
import sys
from datetime import datetime
from pathlib import Path

class BuildMonitor:
    def __init__(self, project_dir):
        self.project_dir = Path(project_dir)
        self.build_dir = self.project_dir / "build"
        self.apk_output_dir = self.build_dir / "apk" / "release"
        self.start_time = time.time()
        self.last_size = 0
        self.last_check_time = time.time()
        self.monitoring = True
        
    def check_apk_files(self):
        """检查APK文件"""
        apk_files = list(self.build_dir.rglob("*.apk"))
        return apk_files
    
    def get_build_size(self):
        """获取构建目录大小"""
        total_size = 0
        for path in self.build_dir.rglob("*"):
            if path.is_file():
                try:
                    total_size += path.stat().st_size
                except:
                    pass
        return total_size
    
    def check_build_progress(self):
        """检查构建进度"""
        # 检查APK文件
        apk_files = self.check_apk_files()
        if apk_files:
            print(f"✅ 找到APK文件: {len(apk_files)}个")
            for apk in apk_files[:3]:  # 只显示前3个
                size_mb = apk.stat().st_size / (1024 * 1024)
                rel_path = apk.relative_to(self.project_dir)
                print(f"   • {rel_path} ({size_mb:.2f} MB)")
            if len(apk_files) > 3:
                print(f"   ... 还有{len(apk_files)-3}个文件")
            return True
        
        # 检查目录增长
        current_size = self.get_build_size()
        elapsed = time.time() - self.last_check_time
        
        if elapsed >= 30:  # 每30秒报告一次
            size_growth = current_size - self.last_size
            growth_rate = size_growth / elapsed / 1024  # KB/s
            
            print(f"📊 构建目录: {current_size/(1024*1024):.1f} MB | "
                  f"增长率: {growth_rate:.1f} KB/s | "
                  f"运行时间: {int(time.time() - self.start_time)}s")
            
            self.last_size = current_size
            self.last_check_time = time.time()
        
        return False
    
    def check_flutter_project(self):
        """检查Flutter项目目录"""
        flutter_dir = self.build_dir / "flutter"
        if flutter_dir.exists():
            dirs_count = sum(1 for _ in flutter_dir.rglob("*") if _.is_dir())
            files_count = sum(1 for _ in flutter_dir.rglob("*") if _.is_file())
            return f"Flutter项目: {dirs_count}目录/{files_count}文件"
        return "Flutter项目: 尚未创建"
    
    def check_python_deps(self):
        """检查Python依赖包"""
        site_packages_dir = self.build_dir / "site-packages"
        if site_packages_dir.exists():
            arch_dirs = [d for d in site_packages_dir.iterdir() if d.is_dir()]
            return f"Python依赖: {len(arch_dirs)}个架构"
        return "Python依赖: 打包中..."
    
    def monitor(self):
        """主监控循环"""
        print("="*70)
        print("🔍 APK构建实时监控器")
        print(f"📅 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📁 项目目录: {self.project_dir}")
        print("="*70)
        print("\n监控说明:")
        print("• 首次构建需要下载Flutter、Android SDK和依赖包")
        print("• 构建过程可能需要10-30分钟")
        print("• 构建目录大小会逐渐增加")
        print("• APK文件生成在最后阶段")
        print("\n按Ctrl+C停止监控\n")
        
        try:
            while self.monitoring:
                # 显示状态信息
                print("\n" + "="*50)
                print(f"[{datetime.now().strftime('%H:%M:%S')}] 构建状态:")
                
                # 检查各个组件
                flutter_status = self.check_flutter_project()
                python_status = self.check_python_deps()
                
                print(f"  • {flutter_status}")
                print(f"  • {python_status}")
                
                # 检查APK文件
                if self.check_apk_files():
                    print("\n" + "="*70)
                    print("🎉 APK构建完成!")
                    print("="*70)
                    print("\n生成的APK文件:")
                    apk_files = self.check_apk_files()
                    for apk in apk_files:
                        size_mb = apk.stat().st_size / (1024 * 1024)
                        rel_path = apk.relative_to(self.project_dir)
                        print(f"  📱 {rel_path} ({size_mb:.2f} MB)")
                    
                    print("\n🎯 下一步:")
                    print("1. 将APK文件传输到Android设备")
                    print("2. 在设备设置中允许安装未知来源应用")
                    print("3. 安装并测试应用")
                    print("4. 如有问题，检查log文件")
                    
                    self.monitoring = False
                    break
                
                # 显示进度条（简单版本）
                elapsed_min = int((time.time() - self.start_time) / 60)
                elapsed_sec = int((time.time() - self.start_time) % 60)
                print(f"  ⏱️  已运行: {elapsed_min}分{elapsed_sec}秒")
                
                # 等待一段时间
                time.sleep(5)
                
        except KeyboardInterrupt:
            print("\n\n🔴 监控已停止")
            print("构建过程可能仍在后台继续...")
        except Exception as e:
            print(f"\n❌ 监控错误: {e}")
        
        if self.monitoring:
            print("\n" + "="*70)
            print("📊 最终状态:")
            print(f"总构建时间: {int(time.time() - self.start_time)}秒")
            print(f"构建目录大小: {self.get_build_size()/(1024*1024):.1f} MB")
            print("构建状态: 进行中/未完成")
            print("\n💡 建议:")
            print("• 检查终端输出获取详细构建日志")
            print("• 如果构建卡住，可能需要重启")
            print("• 确保网络连接正常（需要下载依赖）")

def main():
    """主函数"""
    project_dir = os.getcwd()
    monitor = BuildMonitor(project_dir)
    
    # 先检查是否已经有APK
    apk_files = monitor.check_apk_files()
    if apk_files:
        print("🎉 发现已存在的APK文件:")
        for apk in apk_files:
            size_mb = apk.stat().st_size / (1024 * 1024)
            print(f"  • {apk.relative_to(project_dir)} ({size_mb:.2f} MB)")
        print("\n无需重新构建，APK已存在！")
        return
    
    # 开始监控
    monitor.monitor()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n监控已取消")
    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)