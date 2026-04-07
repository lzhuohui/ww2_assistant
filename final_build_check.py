# -*- coding: utf-8 -*-
"""
最终构建检查
"""

import os
import sys
import time
from datetime import datetime
from pathlib import Path

def check_apk_build_result():
    """检查APK构建结果"""
    print("="*70)
    print("APK构建最终检查")
    print(f"检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    build_dir = Path("build")
    
    if not build_dir.exists():
        print("❌ 构建失败: build目录不存在")
        print("   构建可能尚未开始或已失败")
        return False
    
    # 检查APK文件
    apk_files = list(build_dir.rglob("*.apk"))
    
    if apk_files:
        print(f"🎉 APK构建成功!")
        print(f"   找到 {len(apk_files)} 个APK文件")
        print("\n生成的APK文件:")
        
        for apk in apk_files:
            size_mb = apk.stat().st_size / (1024 * 1024)
            rel_path = apk.relative_to(Path('.'))
            print(f"   📱 {rel_path} ({size_mb:.2f} MB)")
            
            # 检查是否是release版本
            if "release" in str(apk).lower():
                print(f"   ✅ Release版本")
            elif "debug" in str(apk).lower():
                print(f"   ⚠️  Debug版本")
        
        print("\n🎯 下一步操作:")
        print("1. 将APK文件传输到Android设备")
        print("2. 在设备设置中允许安装未知来源应用")
        print("3. 安装并测试应用")
        print("4. 如有问题，检查日志文件")
        
        return True
    
    # 如果没有APK文件，检查构建状态
    print("⏳ APK文件尚未生成，检查构建状态...")
    print()
    
    # 检查构建目录结构
    check_items = [
        ("build/.hash", "构建配置哈希", True),
        ("build/site-packages", "Python依赖包", True),
        ("build/flutter", "Flutter项目", True),
        ("build/flutter/android", "Android项目", True),
        ("build/flutter/android/app", "Android应用", True),
        ("build/flutter/android/app/build", "Android构建目录", False),
        ("build/flutter/android/app/build/outputs", "构建输出目录", False),
        ("build/apk", "APK输出目录", False),
    ]
    
    all_passed = True
    for path_str, desc, required in check_items:
        path = Path(path_str)
        if path.exists():
            if path.is_dir():
                item_count = len(list(path.iterdir()))
                print(f"✅ {desc}: 存在 ({item_count}个项目)")
            else:
                print(f"✅ {desc}: 存在")
        else:
            if required:
                print(f"❌ {desc}: 缺失 (必需)")
                all_passed = False
            else:
                print(f"⏳ {desc}: 尚未创建")
    
    # 计算构建目录大小
    total_size = 0
    file_count = 0
    for root, dirs, files in os.walk(build_dir):
        file_count += len(files)
        for file in files:
            try:
                total_size += os.path.getsize(os.path.join(root, file))
            except:
                pass
    
    print(f"\n📊 构建统计:")
    print(f"   目录大小: {total_size/(1024*1024):.2f} MB")
    print(f"   文件数量: {file_count}")
    
    # 检查是否有错误文件
    error_files = list(build_dir.rglob("*error*")) + list(build_dir.rglob("*fail*"))
    if error_files:
        print(f"\n⚠️  发现 {len(error_files)} 个可能包含错误的文件:")
        for err_file in error_files[:3]:  # 只显示前3个
            print(f"   • {err_file.relative_to(build_dir)}")
    
    # 分析构建状态
    if not all_passed:
        print("\n❌ 构建失败: 缺少必需目录")
        print("   建议重新运行: python -m flet.cli build apk --verbose")
        return False
    
    # 检查构建是否卡住
    build_time_file = build_dir / ".hash" / "package"
    if build_time_file.exists():
        file_age = time.time() - build_time_file.stat().st_mtime
        if file_age > 300:  # 5分钟没有更新
            print(f"\n⚠️  构建可能卡住")
            print(f"   最后更新: {file_age/60:.1f} 分钟前")
            print("   建议检查终端输出或重新构建")
    
    print("\n🔄 构建进行中...")
    print("   首次构建需要较长时间，请耐心等待")
    print("   通常需要15-30分钟完成")
    
    return None  # 表示仍在进行中

def main():
    """主函数"""
    result = check_apk_build_result()
    
    print("\n" + "="*70)
    print("建议:")
    
    if result is True:
        print("✅ 构建成功！APK文件已生成")
        print("   可以开始测试应用")
    elif result is False:
        print("❌ 构建失败")
        print("   请检查错误信息并重新构建")
    else:
        print("⏳ 构建仍在进行中")
        print("   继续等待或检查终端输出")
        print("   或运行监控: python simple_build_monitor.py")
    
    print("="*70)

if __name__ == "__main__":
    main()