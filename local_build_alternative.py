#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本地构建APK的替代方案
当Gitee流水线有问题时使用
"""

import os
import sys
import subprocess
import time
import zipfile
import shutil

def check_environment():
    """检查本地构建环境"""
    print("=" * 70)
    print("本地APK构建环境检查")
    print("=" * 70)
    
    requirements = {
        "Python": ["python", "--version"],
        "Pip": ["python", "-m", "pip", "--version"],
        "Flet": ["python", "-c", "import flet; print(f'Flet版本: {flet.__version__}')"],
        "Flutter": ["flutter", "--version"],
        "Android SDK": ["which", "adb"]  # 简单检查
    }
    
    print("\n🔧 检查必要的工具和环境:")
    
    all_ok = True
    for tool, cmd in requirements.items():
        try:
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                print(f"✅ {tool}: 已安装")
                if tool == "Flet":
                    print(f"   版本: {result.stdout.strip()}")
                elif tool == "Flutter":
                    # 只显示第一行版本信息
                    lines = result.stdout.strip().split('\n')
                    if lines:
                        print(f"   版本: {lines[0]}")
            else:
                print(f"❌ {tool}: 未安装或配置错误")
                all_ok = False
        except FileNotFoundError:
            print(f"❌ {tool}: 未找到命令")
            all_ok = False
        except Exception as e:
            print(f"⚠️  {tool}: 检查出错 - {e}")
            all_ok = False
    
    return all_ok

def build_apk_locally():
    """本地构建APK"""
    print("\n" + "=" * 70)
    print("开始本地构建APK")
    print("=" * 70)
    
    # 清理之前的构建
    if os.path.exists("build"):
        print("清理之前的构建目录...")
        try:
            shutil.rmtree("build")
            print("✅ 清理完成")
        except Exception as e:
            print(f"⚠️  清理失败: {e}")
    
    # 设置环境变量
    env = os.environ.copy()
    env['FLET_CLI_NO_RICH_OUTPUT'] = '1'
    env['PYTHONIOENCODING'] = 'utf-8'
    
    print("\n🚀 开始构建APK...")
    
    # 构建命令
    build_cmd = [
        "python", "-m", "flet.cli", 
        "build", "apk", 
        "--verbose", 
        "--project", "WW2Assistant"
    ]
    
    print(f"执行命令: {' '.join(build_cmd)}")
    print("这可能需要15-30分钟，请耐心等待...")
    print("-" * 50)
    
    try:
        # 执行构建
        process = subprocess.Popen(
            build_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding='utf-8',
            errors='ignore',
            env=env
        )
        
        # 实时输出
        for line in process.stdout:
            print(line, end='')
            sys.stdout.flush()
        
        # 等待完成
        returncode = process.wait()
        
        print("-" * 50)
        
        if returncode == 0:
            print("✅ APK构建成功！")
            
            # 查找APK文件
            print("\n🔍 查找生成的APK文件...")
            apk_files = []
            for root, dirs, files in os.walk("."):
                for file in files:
                    if file.endswith(".apk"):
                        apk_path = os.path.join(root, file)
                        apk_files.append(apk_path)
            
            if apk_files:
                print(f"找到 {len(apk_files)} 个APK文件:")
                for apk in apk_files:
                    size = os.path.getsize(apk)
                    size_mb = size / (1024 * 1024)
                    print(f"  📱 {apk} ({size_mb:.2f} MB)")
                
                # 复制到项目根目录
                print("\n📦 复制APK文件到项目根目录...")
                for apk in apk_files:
                    filename = os.path.basename(apk)
                    dest = os.path.join(".", filename)
                    shutil.copy2(apk, dest)
                    print(f"  复制: {filename}")
                
                # 创建ZIP包
                print("\n📦 创建ZIP包...")
                zip_filename = "ww2_assistant_apk.zip"
                with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for apk in apk_files:
                        arcname = os.path.basename(apk)
                        zipf.write(apk, arcname)
                        print(f"  添加到ZIP: {arcname}")
                
                zip_size = os.path.getsize(zip_filename)
                zip_size_mb = zip_size / (1024 * 1024)
                print(f"\n✅ ZIP包创建完成: {zip_filename} ({zip_size_mb:.2f} MB)")
                print(f"📁 位置: {os.path.abspath(zip_filename)}")
                
                return True, zip_filename, apk_files
            else:
                print("❌ 未找到APK文件")
                return False, None, []
        else:
            print(f"❌ APK构建失败，返回码: {returncode}")
            return False, None, []
            
    except KeyboardInterrupt:
        print("\n⏹️  构建被用户中断")
        return False, None, []
    except Exception as e:
        print(f"\n❌ 构建过程中出错: {e}")
        return False, None, []

def create_readme(apk_files, zip_file):
    """创建使用说明文档"""
    print("\n" + "=" * 70)
    print("创建使用说明文档")
    print("=" * 70)
    
    readme_content = f"""# WW2 Assistant APK 本地构建结果

## 构建信息
- 构建时间: {time.strftime('%Y-%m-%d %H:%M:%S')}
- 构建方式: 本地构建
- 项目名称: WW2 Assistant

## 生成的文件

### APK文件:
"""
    
    for apk in apk_files:
        size = os.path.getsize(apk)
        size_mb = size / (1024 * 1024)
        readme_content += f"- `{os.path.basename(apk)}` ({size_mb:.2f} MB)\n"
    
    readme_content += f"""
### 打包文件:
- `{zip_file}` - 包含所有APK文件的ZIP包

## 安装说明

### 方法1: 直接安装APK
1. 将APK文件传输到Android设备
2. 在文件管理器中找到APK文件
3. 点击安装（可能需要开启"未知来源"安装权限）
4. 按照提示完成安装

### 方法2: 通过ADB安装
```bash
# 连接设备
adb devices

# 安装APK
adb install 文件名.apk

# 重新安装（如果已存在）
adb install -r 文件名.apk
```

### 方法3: 使用Android Studio
1. 打开Android Studio
2. 选择"Profile or Debug APK"
3. 选择生成的APK文件
4. 点击"运行"按钮

## 注意事项
1. 首次安装可能需要允许"未知来源"应用安装
2. 如果安装失败，请检查Android版本兼容性
3. 建议在Android 8.0及以上版本运行
4. 安装后可能需要授予相关权限

## 故障排除

### 安装失败
1. **存储空间不足**: 清理设备存储空间
2. **版本不兼容**: 确保Android版本符合要求
3. **签名问题**: 如果是调试版本，需要启用USB调试

### 运行崩溃
1. **权限问题**: 检查应用权限设置
2. **兼容性问题**: 尝试在其他设备上运行
3. **日志查看**: 使用`adb logcat`查看错误信息

## 支持
如有问题，请查看构建日志或联系开发者。
"""

    readme_file = "APK_BUILD_README.md"
    with open(readme_file, "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print(f"✅ 创建说明文档: {readme_file}")
    return readme_file

def main():
    """主函数"""
    print("\n" + "=" * 70)
    print("本地APK构建替代方案")
    print("=" * 70)
    print("\n当Gitee流水线有问题时，可以使用此脚本在本地构建APK。")
    print("这需要本地已安装Flutter和Android SDK。")
    
    # 检查环境
    if not check_environment():
        print("\n⚠️  环境检查失败，请先安装必要的工具:")
        print("1. Python 3.8+ 和 pip")
        print("2. Flet: pip install flet")
        print("3. Flutter: https://flutter.dev/docs/get-started/install")
        print("4. Android SDK 和 JDK")
        print("\n是否继续尝试构建？(y/n): ", end="")
        choice = input().strip().lower()
        if choice not in ['y', 'yes', '是']:
            print("退出构建")
            return 1
    
    print("\n是否开始本地构建APK？ (y/n): ", end="")
    try:
        choice = input().strip().lower()
    except:
        choice = 'y'  # 默认继续
    
    if choice not in ['y', 'yes', '是']:
        print("取消构建")
        return 0
    
    # 开始构建
    success, zip_file, apk_files = build_apk_locally()
    
    if success and zip_file:
        # 创建说明文档
        readme_file = create_readme(apk_files, zip_file)
        
        print("\n" + "=" * 70)
        print("🎉 本地构建完成！")
        print("=" * 70)
        print(f"\n📁 生成的文件:")
        print(f"1. ZIP包: {zip_file}")
        print(f"2. 说明文档: {readme_file}")
        
        for apk in apk_files:
            print(f"3. APK文件: {os.path.basename(apk)}")
        
        print("\n📱 安装方法:")
        print("1. 将ZIP包解压")
        print("2. 复制APK文件到Android设备")
        print("3. 在设备上安装APK")
        print(f"\n📖 详细说明请查看: {readme_file}")
        
        # 打开目录
        print("\n是否要打开文件所在目录？(y/n): ", end="")
        try:
            open_choice = input().strip().lower()
            if open_choice in ['y', 'yes', '是']:
                if sys.platform == "win32":
                    os.startfile(".")
                elif sys.platform == "darwin":
                    subprocess.run(["open", "."])
                else:
                    subprocess.run(["xdg-open", "."])
        except:
            pass
        
        return 0
    else:
        print("\n" + "=" * 70)
        print("❌ 构建失败")
        print("=" * 70)
        print("\n可能的原因:")
        print("1. Flutter环境未正确配置")
        print("2. Android SDK许可未接受")
        print("3. 网络问题导致依赖下载失败")
        print("4. 项目配置问题")
        print("\n💡 建议:")
        print("1. 运行: flutter doctor")
        print("2. 运行: flutter doctor --android-licenses")
        print("3. 检查网络连接")
        print("4. 查看详细错误日志")
        
        return 1

if __name__ == "__main__":
    sys.exit(main())