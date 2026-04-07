#!/usr/bin/env python3
"""
本地APK构建脚本
无需复杂的CI/CD配置，直接在本地构建APK
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def check_python():
    """检查Python环境"""
    print("🔍 检查Python环境...")
    try:
        result = subprocess.run([sys.executable, "--version"], 
                              capture_output=True, text=True)
        print(f"✅ Python版本: {result.stdout.strip()}")
        return True
    except Exception as e:
        print(f"❌ Python检查失败: {e}")
        return False

def check_flet():
    """检查Flet安装"""
    print("\n🔍 检查Flet安装...")
    try:
        import flet
        print(f"✅ Flet版本: {flet.__version__}")
        return True
    except ImportError:
        print("❌ Flet未安装")
        return False

def install_flet():
    """安装Flet"""
    print("\n📦 安装Flet...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "flet==0.82.0", "--upgrade"],
                      check=True, capture_output=True, text=True)
        print("✅ Flet安装成功")
        return True
    except Exception as e:
        print(f"❌ Flet安装失败: {e}")
        return False

def check_flutter():
    """检查Flutter环境"""
    print("\n🔍 检查Flutter环境...")
    try:
        # 尝试查找Flutter
        flutter_paths = [
            "flutter",
            "flutter.bat",
            os.path.expanduser("~/flutter/bin/flutter"),
            "C:\\flutter\\bin\\flutter.bat",
            "/usr/local/flutter/bin/flutter"
        ]
        
        for flutter_cmd in flutter_paths:
            try:
                result = subprocess.run([flutter_cmd, "--version"], 
                                      capture_output=True, text=True, shell=True)
                if result.returncode == 0:
                    # 提取版本信息
                    for line in result.stdout.split('\n'):
                        if "Flutter" in line:
                            print(f"✅ {line.strip()}")
                    return True
            except:
                continue
        
        print("⚠️  Flutter未找到，需要安装Flutter SDK")
        print("\n📥 请从以下地址下载Flutter SDK：")
        print("   https://flutter.dev/docs/get-started/install")
        print("\n📋 安装步骤：")
        print("   1. 下载Flutter SDK")
        print("   2. 解压到合适位置")
        print("   3. 将flutter/bin添加到PATH环境变量")
        print("   4. 运行 'flutter doctor' 检查安装")
        return False
        
    except Exception as e:
        print(f"❌ Flutter检查失败: {e}")
        return False

def check_android_sdk():
    """检查Android SDK"""
    print("\n🔍 检查Android SDK...")
    
    # 检查环境变量
    android_home = os.environ.get('ANDROID_HOME') or os.environ.get('ANDROID_SDK_ROOT')
    if android_home:
        print(f"✅ ANDROID_HOME: {android_home}")
        
        # 检查sdkmanager
        sdkmanager_path = os.path.join(android_home, 'cmdline-tools', 'latest', 'bin', 'sdkmanager')
        if os.path.exists(sdkmanager_path) or os.path.exists(sdkmanager_path + '.bat'):
            print("✅ Android SDK工具已安装")
            return True
        else:
            print("⚠️  Android SDK工具未找到")
    else:
        print("⚠️  ANDROID_HOME未设置")
    
    print("\n📥 请安装Android Studio或Android SDK：")
    print("   1. 下载Android Studio：https://developer.android.com/studio")
    print("   2. 安装时选择Android SDK组件")
    print("   3. 设置ANDROID_HOME环境变量")
    print("   4. 运行 'flutter doctor --android-licenses' 接受许可")
    
    return False

def build_apk():
    """构建APK"""
    print("\n🚀 开始构建APK...")
    
    try:
        # 检查主文件
        main_file = Path("main.py")
        if not main_file.exists():
            print("❌ 未找到main.py文件")
            print("   请在项目根目录运行此脚本")
            return False
        
        print(f"✅ 找到主文件: {main_file}")
        
        # 构建APK
        print("\n🔨 运行Flet构建命令...")
        cmd = [sys.executable, "-m", "flet.cli", "build", "apk", "--project", "WW2Assistant", "--verbose"]
        
        print(f"📝 命令: {' '.join(cmd)}")
        print("⏳ 构建中，这可能需要几分钟...")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ APK构建成功！")
            
            # 查找APK文件
            apk_files = list(Path(".").glob("**/*.apk"))
            if apk_files:
                print("\n📱 找到APK文件：")
                for apk in apk_files:
                    size = apk.stat().st_size
                    print(f"   📄 {apk} ({size/1024/1024:.2f} MB)")
                
                # 复制到output目录
                output_dir = Path("apk-output")
                output_dir.mkdir(exist_ok=True)
                
                for apk in apk_files:
                    target = output_dir / apk.name
                    import shutil
                    shutil.copy2(apk, target)
                    print(f"   📦 已复制到: {target}")
                
                print(f"\n🎉 APK文件已保存在: {output_dir.absolute()}")
                return True
            else:
                print("⚠️  构建成功但未找到APK文件")
                print("   检查build/目录：")
                build_dir = Path("build")
                if build_dir.exists():
                    for file in build_dir.rglob("*"):
                        print(f"      {file}")
                return False
        else:
            print("❌ APK构建失败")
            print("错误输出：")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ 构建过程出错: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_requirements():
    """检查requirements.txt"""
    print("\n🔍 检查依赖文件...")
    req_file = Path("requirements.txt")
    if req_file.exists():
        print(f"✅ 找到requirements.txt")
        with open(req_file, 'r', encoding='utf-8') as f:
            deps = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            print(f"   依赖项数量: {len(deps)}")
            for dep in deps[:5]:  # 只显示前5个
                print(f"     - {dep}")
            if len(deps) > 5:
                print(f"     ... 还有 {len(deps)-5} 个")
    else:
        print("⚠️  未找到requirements.txt")
        print("   创建中...")
        req_file.write_text("flet==0.82.0\n")
        print("✅ 已创建requirements.txt")

def main():
    """主函数"""
    print("=" * 60)
    print("📱 本地APK构建工具")
    print("=" * 60)
    
    # 检查当前目录
    current_dir = os.getcwd()
    print(f"📁 当前目录: {current_dir}")
    
    try:
        # 检查Python
        if not check_python():
            print("\n❌ 请先安装Python 3.8+")
            print("   下载地址: https://www.python.org/downloads/")
            return
        
        # 检查/安装Flet
        if not check_flet():
            if not install_flet():
                print("\n❌ Flet安装失败，请手动安装:")
                print("   pip install flet==0.82.0")
                return
        
        # 检查Flutter（警告但不阻止）
        check_flutter()
        
        # 检查Android SDK（警告但不阻止）
        check_android_sdk()
        
        # 检查依赖文件
        check_requirements()
        
        print("\n" + "=" * 60)
        print("⚙️  环境检查完成")
        print("=" * 60)
        
        # 询问是否继续
        response = input("\n❓ 是否开始构建APK？(y/n): ").strip().lower()
        if response != 'y':
            print("👋 已取消构建")
            return
        
        # 构建APK
        if build_apk():
            print("\n" + "=" * 60)
            print("🎉 APK构建完成！")
            print("=" * 60)
            print("\n📋 下一步操作：")
            print("   1. 将APK文件复制到手机")
            print("   2. 在手机上安装APK")
            print("   3. 测试应用功能")
            
            # 打开输出目录
            output_dir = Path("apk-output")
            if output_dir.exists():
                print(f"\n📁 APK文件位置: {output_dir.absolute()}")
                try:
                    if platform.system() == "Windows":
                        os.startfile(output_dir.absolute())
                    elif platform.system() == "Darwin":
                        subprocess.run(["open", output_dir.absolute()])
                    elif platform.system() == "Linux":
                        subprocess.run(["xdg-open", output_dir.absolute()])
                except:
                    pass
        else:
            print("\n" + "=" * 60)
            print("❌ APK构建失败")
            print("=" * 60)
            print("\n💡 解决方法：")
            print("   1. 确保已安装Flutter SDK")
            print("   2. 确保已安装Android SDK")
            print("   3. 运行 'flutter doctor' 检查环境")
            print("   4. 运行 'flutter doctor --android-licenses' 接受许可")
            
    except KeyboardInterrupt:
        print("\n\n👋 用户取消操作")
    except Exception as e:
        print(f"\n❌ 程序出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()