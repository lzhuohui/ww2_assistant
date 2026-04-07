@echo off
echo ========================================
echo 环境验证脚本
echo ========================================
echo.

echo 1. 验证Java安装...
where java
if %errorlevel% equ 0 (
    echo ✅ Java已安装
    java -version
) else (
    echo ❌ Java未安装
    echo 请安装Java JDK 11+
    echo 下载地址: https://www.oracle.com/java/technologies/downloads/
)
echo.

echo 2. 设置Flutter环境...
call setup_flutter_env.bat
echo.

echo 3. 验证Flutter安装...
where flutter
if %errorlevel% equ 0 (
    echo ✅ Flutter已安装
    flutter --version
) else (
    echo ❌ Flutter未安装
    echo 请安装Flutter SDK：
    echo 1. 下载: https://flutter.cn/community/china
    echo 2. 解压到 C:\flutter
    echo 3. 将 C:\flutter\bin 添加到Path
)
echo.

echo 4. 设置Android环境...
call setup_android_env.bat
echo.

echo 5. 验证Android SDK安装...
where adb
if %errorlevel% equ 0 (
    echo ✅ Android SDK工具已安装
    adb --version
) else (
    echo ❌ Android SDK工具未找到
    echo 请安装Android Studio和SDK
    echo 下载地址: https://developer.android.com/studio
)
echo.

echo 6. 运行Flutter环境检查...
flutter doctor
echo.

echo ========================================
echo 环境验证完成！
echo ========================================
echo.
echo 如果所有检查都通过✅，就可以开始构建APK了！
echo 运行以下命令构建APK：
echo   python build_apk_simple.py
echo 或
echo   python build_apk_full.py
echo.
pause