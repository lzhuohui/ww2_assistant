#!/usr/bin/env python3
"""
Flet APK一键构建脚本
"""

import os
import sys
import subprocess
import platform
from pathlib import Path
import shutil

def run_command(cmd, cwd=None, shell=True):
    """运行命令并返回结果"""
    print(f"$ {cmd}")
    try:
        result = subprocess.run(
            cmd, 
            shell=shell, 
            cwd=cwd,
            capture_output=True, 
            text=False  # 不使用文本模式，获取原始字节
        )
        
        # 尝试解码输出
        def decode_output(output):
            if output:
                try:
                    return output.decode('utf-8')
                except UnicodeDecodeError:
                    try:
                        return output.decode('gbk')
                    except UnicodeDecodeError:
                        return output.decode('latin-1', errors='ignore')
            return ""
        
        stdout = decode_output(result.stdout)
        stderr = decode_output(result.stderr)
        
        if result.returncode == 0:
            print("✅ 成功")
            if stdout.strip():
                print(f"输出: {stdout[:500]}...")
            return True, stdout
        else:
            print("❌ 失败")
            if stderr:
                print(f"错误: {stderr[:500]}")
            return False, stderr
    except Exception as e:
        print(f"⚠️ 命令执行异常: {e}")
        return False, str(e)

def check_environment():
    """检查环境"""
    print("="*60)
    print("🔍 环境检查")
    print("="*60)
    
    checks = []
    
    # 1. 检查Python
    print("\n1. 检查Python...")
    success, output = run_command(f'"{sys.executable}" --version')
    checks.append(("Python 3.8+", success))
    
    # 2. 检查Flet
    print("\n2. 检查Flet...")
    try:
        import flet
        print(f"✅ Flet版本: {flet.__version__}")
        checks.append(("Flet", True))
    except ImportError:
        print("❌ Flet未安装")
        print("正在安装Flet...")
        success, _ = run_command(f'"{sys.executable}" -m pip install flet==0.82.0')
        checks.append(("Flet", success))
    
    # 3. 检查Flutter
    print("\n3. 检查Flutter...")
    flutter_paths = [
        "flutter",
        "flutter.bat",
        r"C:\flutter\flutter\bin\flutter.bat",  # 修正Flutter路径
        r"C:\flutter\bin\flutter.bat",
        r"C:\src\flutter\bin\flutter.bat"
    ]
    flutter_found = False
    for flutter_cmd in flutter_paths:
        success, output = run_command(f'{flutter_cmd} --version', shell=True)
        if success:
            flutter_found = True
            # 提取版本信息
            for line in output.split('\n'):
                if "Flutter" in line:
                    print(f"✅ {line.strip()}")
            break
    
    if not flutter_found:
        print("❌ Flutter未安装或不在PATH中")
        print("\n📥 请安装Flutter SDK：")
        print("   1. 下载: https://flutter.cn/community/china")
        print("   2. 解压到: C:\\flutter")
        print("   3. 添加环境变量Path: C:\\flutter\\bin")
        print("   4. 设置国内镜像：")
        print("      FLUTTER_STORAGE_BASE_URL=https://storage.flutter-io.cn")
        print("      PUB_HOSTED_URL=https://pub.flutter-io.cn")
    
    checks.append(("Flutter SDK", flutter_found))
    
    # 4. 检查Android SDK
    print("\n4. 检查Android SDK...")
    android_home = os.environ.get('ANDROID_HOME') or os.environ.get('ANDROID_SDK_ROOT')
    if not android_home:
        # 尝试常见的Android SDK路径
        common_android_paths = [
            r"C:\Users\chmm1\AppData\Local\Android\Sdk",
            r"C:\Android\Sdk",
            r"D:\Android\Sdk"
        ]
        for path in common_android_paths:
            if os.path.exists(path):
                android_home = path
                print(f"✅ 自动找到Android SDK: {android_home}")
                # 设置环境变量
                os.environ['ANDROID_HOME'] = android_home
                break
    
    if android_home:
        print(f"✅ ANDROID_HOME: {android_home}")
        # 检查adb
        adb_path = os.path.join(android_home, 'platform-tools', 'adb')
        if os.path.exists(adb_path) or os.path.exists(adb_path + '.exe'):
            print("✅ Android工具已安装")
            checks.append(("Android SDK", True))
        else:
            print("⚠️  Android工具未找到")
            checks.append(("Android SDK", False))
    else:
        print("❌ ANDROID_HOME未设置")
        print("\n📥 请安装Android Studio：")
        print("   1. 下载: https://developer.android.com/studio")
        print("   2. 安装时选择Android SDK")
        print("   3. 设置环境变量ANDROID_HOME")
        checks.append(("Android SDK", False))
    
    # 5. 检查JDK
    print("\n5. 检查Java JDK...")
    success, output = run_command("java -version")
    if success:
        print("✅ Java已安装")
        checks.append(("Java JDK", True))
    else:
        # 尝试从Android Studio查找Java
        java_paths = [
            r"C:\Program Files\Android\Android Studio\jbr\bin\java.exe",
            r"C:\Program Files\Android\Android Studio\jre\bin\java.exe",
            r"C:\Program Files (x86)\Android\Android Studio\jbr\bin\java.exe",
            r"C:\Program Files (x86)\Android\Android Studio\jre\bin\java.exe"
        ]
        java_found = False
        for java_path in java_paths:
            if os.path.exists(java_path):
                java_found = True
                print(f"✅ 自动找到Java: {java_path}")
                # 设置JAVA_HOME环境变量
                java_home = os.path.dirname(os.path.dirname(java_path))
                os.environ['JAVA_HOME'] = java_home
                os.environ['PATH'] = f"{os.environ['PATH']};{os.path.dirname(java_path)}"
                break
        
        if java_found:
            checks.append(("Java JDK", True))
        else:
            print("❌ Java未安装")
            print("\n📥 请安装Java JDK 11+：")
            print("   1. 下载: https://www.oracle.com/java/technologies/downloads/")
            print("   2. 或使用OpenJDK: https://adoptium.net/")
            checks.append(("Java JDK", False))
    
    # 显示检查结果
    print("\n" + "="*60)
    print("📋 环境检查结果")
    print("="*60)
    
    all_pass = True
    for check_name, check_result in checks:
        status = "✅" if check_result else "❌"
        print(f"   {status} {check_name}")
        if not check_result:
            all_pass = False
    
    return all_pass

def build_apk():
    """构建APK"""
    print("\n" + "="*60)
    print("🔨 开始构建APK")
    print("="*60)
    
    # 检查main.py
    main_file = Path("main.py")
    if not main_file.exists():
        print("❌ 未找到main.py文件")
        return False
    
    print(f"📄 主文件: {main_file.absolute()}")
    
    # 创建assets目录（如果不存在）
    assets_dir = Path("assets")
    if not assets_dir.exists():
        assets_dir.mkdir(exist_ok=True)
        print("📁 创建assets目录")
    
    # 检查requirements.txt
    req_file = Path("requirements.txt")
    if not req_file.exists():
        print("📝 创建requirements.txt...")
        req_file.write_text("flet==0.82.0\n", encoding='utf-8')
    
    # 构建命令
    build_cmd = [
        sys.executable, 
        "-m", "flet.cli", 
        "build", "apk",
        "--project", "WW2Assistant",
        "--verbose"
    ]
    
    print(f"\n🚀 构建命令: {' '.join(build_cmd)}")
    print("⏳ 构建中，这可能需要5-15分钟...")
    
    success, output = run_command(' '.join(build_cmd))
    
    if success:
        # 查找APK文件
        apk_files = list(Path(".").glob("**/*.apk"))
        if apk_files:
            print("\n🎉 APK构建成功！")
            print("\n📱 生成的APK文件：")
            
            # 创建输出目录
            output_dir = Path("apk-output")
            output_dir.mkdir(exist_ok=True)
            
            for apk in apk_files:
                size_mb = apk.stat().st_size / 1024 / 1024
                print(f"   📄 {apk.name} ({size_mb:.2f} MB)")
                
                # 复制到输出目录
                target = output_dir / apk.name
                shutil.copy2(apk, target)
                print(f"      → 已复制到: {target}")
            
            print(f"\n📁 所有APK文件已保存到: {output_dir.absolute()}")
            
            # 在文件管理器中打开目录
            try:
                if platform.system() == "Windows":
                    os.startfile(output_dir.absolute())
                elif platform.system() == "Darwin":
                    subprocess.run(["open", output_dir.absolute()])
                elif platform.system() == "Linux":
                    subprocess.run(["xdg-open", output_dir.absolute()])
            except:
                pass
            
            return True
        else:
            print("⚠️  构建成功但未找到APK文件")
            # 检查build目录
            build_dir = Path("build")
            if build_dir.exists():
                print("   检查build目录：")
                for file in build_dir.rglob("*"):
                    if file.is_file():
                        print(f"      {file.relative_to(build_dir)}")
            return False
    else:
        print("\n❌ APK构建失败")
        print("\n💡 常见问题解决：")
        print("   1. 运行 'flutter doctor' 检查环境")
        print("   2. 运行 'flutter doctor --android-licenses' 接受许可")
        print("   3. 确保Android SDK已正确安装")
        print("   4. 检查网络连接")
        return False

def setup_flutter_environment():
    """设置Flutter环境"""
    print("\n" + "="*60)
    print("⚙️  设置Flutter环境")
    print("="*60)
    
    # 1. 设置国内镜像
    print("\n1. 设置国内镜像...")
    env_file = Path("flutter_env.bat")
    env_content = """@echo off
echo 设置Flutter国内镜像环境变量
set FLUTTER_STORAGE_BASE_URL=https://storage.flutter-io.cn
set PUB_HOSTED_URL=https://pub.flutter-io.cn
echo 环境变量已设置
"""
    env_file.write_text(env_content, encoding='utf-8')
    print(f"✅ 创建环境变量脚本: {env_file}")
    print("💡 运行此脚本设置临时环境变量")
    
    # 2. 运行flutter doctor
    print("\n2. 运行flutter doctor检查...")
    run_command("flutter doctor")
    
    return True

def create_quick_start_guide():
    """创建快速开始指南"""
    guide = """# 🚀 Flet APK构建快速开始

## 📋 环境检查
运行以下命令检查环境：
```
python simple_build_test.py
```

## 🔧 环境安装（如果缺失）

### 1. 安装Flutter SDK
1. 下载Flutter SDK：https://flutter.cn/community/china
2. 解压到 C:\\flutter
3. 设置环境变量：
   - 系统变量 Path 添加：C:\\flutter\\bin
   - 新建系统变量：
     - FLUTTER_STORAGE_BASE_URL = https://storage.flutter-io.cn
     - PUB_HOSTED_URL = https://pub.flutter-io.cn

### 2. 安装Android Studio
1. 下载：https://developer.android.com/studio
2. 安装时选择Android SDK
3. 设置环境变量：
   - ANDROID_HOME = C:\\Users\\你的用户名\\AppData\\Local\\Android\\Sdk

### 3. 安装Java JDK
1. 下载：https://www.oracle.com/java/technologies/downloads/
2. 或使用OpenJDK：https://adoptium.net/

### 4. 接受许可
```
flutter doctor --android-licenses
# 全部输入 y
```

## 🏗️ 构建APK
```
python build_apk_full.py
```

## 🆘 故障排除

### 常见问题1：Flutter命令找不到
```
解决方案：
1. 确保Flutter SDK已解压到 C:\\flutter
2. 将 C:\\flutter\\bin 添加到系统Path环境变量
3. 重启命令行窗口
```

### 常见问题2：Android SDK问题
```
解决方案：
1. 打开Android Studio
2. 点击 Configure -> SDK Manager
3. 安装 Android SDK Platform
4. 安装 Android SDK Build-Tools
```

### 常见问题3：许可问题
```
解决方案：
1. 运行：flutter doctor --android-licenses
2. 对所有问题输入 y
```

### 常见问题4：网络问题
```
解决方案：
1. 设置国内镜像环境变量
2. 运行 flutter_env.bat
3. 重新运行构建
```

## 📞 帮助
如果遇到问题，请提供：
- `flutter doctor` 输出
- 错误信息截图
- 操作系统版本
"""
    
    guide_file = Path("快速开始指南.txt")
    guide_file.write_text(guide, encoding='utf-8')
    print(f"📝 创建快速开始指南: {guide_file}")

def main():
    """主函数"""
    print("="*60)
    print("📱 Flet APK一键构建工具")
    print("="*60)
    
    # 检查当前目录
    current_dir = os.getcwd()
    print(f"📁 当前目录: {current_dir}")
    
    try:
        # 1. 环境检查
        env_ok = check_environment()
        
        if not env_ok:
            print("\n⚠️  环境检查未通过")
            print("💡 请按照上面的提示安装缺失的组件")
            create_quick_start_guide()
            
            response = input("\n❓ 是否尝试设置Flutter环境？(y/n): ").strip().lower()
            if response == 'y':
                setup_flutter_environment()
            
            print("\n📋 请先完成环境配置，然后重新运行此脚本")
            return
        
        # 2. 询问是否构建
        print("\n" + "="*60)
        print("✅ 环境检查通过！")
        print("="*60)
        
        response = 'y'  # 自动继续构建
        if response != 'y':
            print("👋 已取消构建")
            return
        
        # 3. 构建APK
        if build_apk():
            print("\n" + "="*60)
            print("🎉 APK构建完成！")
            print("="*60)
            print("\n📱 下一步：")
            print("   1. 将apk-output目录中的APK文件复制到手机")
            print("   2. 在手机上安装APK")
            print("   3. 测试应用功能")
        else:
            print("\n" + "="*60)
            print("❌ 构建失败")
            print("="*60)
            create_quick_start_guide()
    
    except KeyboardInterrupt:
        print("\n\n👋 用户取消操作")
    except Exception as e:
        print(f"\n❌ 程序出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()