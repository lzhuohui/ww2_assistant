@echo off
echo ========================================
echo 一键环境检查
echo ========================================
echo.

echo 1. 检查Java...
where java >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Java已安装
    java -version 2>&1 | findstr "version"
) else (
    echo ❌ Java未找到
    echo   尝试查找Android Studio自带的Java...
    if exist "C:\Users\%USERNAME%\AppData\Local\Android\Sdk\jre\bin\java.exe" (
        echo   ✅ 找到: C:\Users\%USERNAME%\AppData\Local\Android\Sdk\jre\bin\java.exe
    ) else (
        echo   ❌ 未找到Java
    )
)

echo.
echo 2. 检查Flutter...
where flutter >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Flutter已安装
    flutter --version 2>&1 | findstr "Flutter"
) else (
    echo ❌ Flutter未找到
    echo   请下载: https://storage.flutter-io.cn/flutter_infra_release/releases/stable/windows/flutter_windows_3.16.0-stable.zip
    echo   解压到: C:\flutter
    echo   添加环境变量: C:\flutter\bin 到Path
)

echo.
echo 3. 检查Android SDK...
if not "%ANDROID_HOME%"=="" (
    echo ✅ ANDROID_HOME: %ANDROID_HOME%
) else (
    echo ❌ ANDROID_HOME未设置
    echo   应该设置为: C:\Users\%USERNAME%\AppData\Local\Android\Sdk
)

echo.
echo 4. 检查ADB...
where adb >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ ADB已安装
    adb --version 2>&1 | findstr "Android Debug Bridge"
) else (
    echo ❌ ADB未找到
)

echo.
echo ========================================
echo 解决方案：
echo ========================================
echo.
echo 如果Flutter显示未安装：
echo   1. 下载上面的链接
echo   2. 解压到 C:\flutter
echo   3. 设置环境变量（见上面）
echo.
echo 如果Java显示未安装：
echo   Android Studio自带Java，可能只是环境变量问题
echo   尝试运行: set JAVA_HOME=C:\Users\%USERNAME%\AppData\Local\Android\Sdk\jre
echo.
echo 安装完成后：
echo   1. 重启命令行窗口
echo   2. 运行: flutter doctor
echo   3. 运行: flutter doctor --android-licenses （全部输入y）
echo   4. 运行: python build_apk_simple.py
echo.
pause