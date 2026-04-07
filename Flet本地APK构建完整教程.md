# 📱 Flet Python应用打包为Android APK完整教程

> 参考：CSDN文章《如何将Flet Python应用打包为Android APK》及其他相关资料

## 🎯 **核心要点**

根据你的需求（GitHub访问困难），**本地构建是最佳选择**。Flet打包APK依赖于完整的Flutter+Android开发环境，这是必须的前置条件。

## 📋 **环境要求清单**

### **必须安装（按顺序）：**
1. ✅ **Python 3.8+**（已安装）
2. ✅ **Flet 0.82.0**（已安装）
3. ⚠️ **Flutter SDK**（需要安装）
4. ⚠️ **Android SDK**（需要安装）
5. ⚠️ **JDK 11+**（需要安装）

## 🚀 **分步安装指南**

### **第1步：验证当前环境**
运行我创建的测试脚本：
```bash
cd "c:\Users\chmm1\Documents\二战风云"
python simple_build_test.py
```

### **第2步：安装Flutter SDK（国内镜像版）**

#### **方案A：使用官方源（可能需要VPN）**
```bash
# 1. 下载Flutter SDK
# 访问：https://flutter.dev/docs/get-started/install

# 2. 解压到 C:\flutter

# 3. 添加环境变量
# 系统变量 Path 添加：C:\flutter\bin

# 4. 验证安装
flutter --version
```

#### **方案B：使用国内镜像（推荐）**
```bash
# 1. 设置国内镜像环境变量（PowerShell）
$env:FLUTTER_STORAGE_BASE_URL = "https://storage.flutter-io.cn"
$env:PUB_HOSTED_URL = "https://pub.flutter-io.cn"

# 2. 下载Flutter SDK
# 访问：https://flutter.cn/community/china
# 或使用镜像下载：https://storage.flutter-io.cn/flutter_infra_release/releases/stable/windows/flutter_windows_3.16.0-stable.zip

# 3. 解压到 C:\flutter

# 4. 永久设置环境变量（系统属性 -> 高级 -> 环境变量）
# 新增系统变量：
# FLUTTER_STORAGE_BASE_URL = https://storage.flutter-io.cn
# PUB_HOSTED_URL = https://pub.flutter-io.cn
# Path 添加：C:\flutter\bin

# 5. 运行flutter doctor检查
flutter doctor
```

### **第3步：安装Android Studio和SDK**

#### **安装Android Studio**
1. **下载地址**：https://developer.android.com/studio
2. **安装时选择**：
   - Android SDK
   - Android SDK Platform
   - Android Virtual Device

#### **配置环境变量**
```bash
# 系统变量
ANDROID_HOME = C:\Users\你的用户名\AppData\Local\Android\Sdk
# 或 ANDROID_SDK_ROOT = C:\Users\你的用户名\AppData\Local\Android\Sdk

# Path添加
%ANDROID_HOME%\platform-tools
%ANDROID_HOME%\tools
%ANDROID_HOME%\tools\bin
```

#### **通过命令行安装SDK组件**
```bash
# 安装必要的Android SDK组件
sdkmanager "platform-tools" "platforms;android-33" "build-tools;33.0.0"

# 接受许可
flutter doctor --android-licenses
# 全部输入 y 确认
```

### **第4步：验证环境**
```bash
# 运行flutter doctor
flutter doctor

# 期望输出：
# [✓] Flutter (Channel stable, ...)
# [✓] Android toolchain - develop for Android devices
# [✓] Chrome - develop for the web
# [✓] Visual Studio - develop for Windows
# [✓] Connected device
# [✓] Network resources
```

## 🔧 **构建APK命令**

### **基本构建命令**
```bash
# 进入项目目录
cd "c:\Users\chmm1\Documents\二战风云"

# 构建APK
python -m flet.cli build apk --project "WW2Assistant" --verbose

# 或使用项目名称（根据你的main.py中的app名称）
python -m flet.cli build apk
```

### **带自定义参数的构建**
```bash
# 指定应用名称
python -m flet.cli build apk --name "二战风云助手"

# 指定包名
python -m flet.cli build apk --package "com.ww2.assistant"

# 指定版本
python -m flet.cli build apk --version "1.0.0"

# 指定图标
python -m flet.cli build apk --icon "assets/icon.png"

# 完整命令示例
python -m flet.cli build apk \
  --name "二战风云助手" \
  --package "com.ww2.assistant" \
  --version "1.0.0" \
  --verbose
```

## 📱 **构建配置文件**

### **创建`pubspec.yaml`（可选）**
```yaml
name: ww2_assistant
description: 二战风云游戏助手
version: 1.0.0
publish_to: 'none'

environment:
  sdk: '>=3.0.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter
  flet: ^0.82.0

flutter:
  uses-material-design: true
  assets:
    - assets/
```

### **创建`build.yaml`（可选）**
```yaml
# Flet构建配置
project:
  name: WW2Assistant
  description: 二战风云游戏助手
  version: 1.0.0
  organization: com.ww2
  
android:
  package: com.ww2.assistant
  min_sdk: 21
  target_sdk: 33
  
assets:
  - assets/
```

## 🛠️ **一键构建脚本**

### **完整构建脚本** `build_apk_full.py`
```python
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
            text=True,
            encoding='utf-8'
        )
        if result.returncode == 0:
            print("✅ 成功")
            if result.stdout.strip():
                print(f"输出: {result.stdout[:500]}...")
            return True, result.stdout
        else:
            print("❌ 失败")
            if result.stderr:
                print(f"错误: {result.stderr[:500]}")
            return False, result.stderr
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
    
    success, output = run_command(build_cmd)
    
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
    
    # 2. 运行flutter doctor
    print("\n2. 运行flutter doctor检查...")
    run_command("flutter doctor")
    
    # 3. 接受Android许可
    print("\n3. 接受Android许可...")
    print("   运行: flutter doctor --android-licenses")
    print("   输入 y 接受所有许可")
    
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

### 3. 接受许可
```
flutter doctor --android-licenses
# 全部输入 y
```

## 🏗️ 构建APK
```
python build_apk_full.py
```

## 🆘 故障排除
1. **Flutter doctor报错**：检查环境变量和网络
2. **许可问题**：运行 `flutter doctor --android-licenses`
3. **网络问题**：确保使用国内镜像
4. **SDK问题**：通过Android Studio安装必要的SDK组件

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
            
            response = input("\n❓ 是否尝试修复环境？(y/n): ").strip().lower()
            if response == 'y':
                setup_flutter_environment()
            
            print("\n📋 请先完成环境配置，然后重新运行此脚本")
            return
        
        # 2. 询问是否构建
        print("\n" + "="*60)
        print("✅ 环境检查通过！")
        print("="*60)
        
        response = input("\n❓ 是否开始构建APK？(y/n): ").strip().lower()
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