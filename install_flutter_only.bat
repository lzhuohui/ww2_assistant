@echo off
echo ========================================
echo Flutter SDK 极简安装脚本
echo 专门为已安装Android Studio的用户设计
echo ========================================
echo.

echo 步骤1：设置临时环境变量（使用国内镜像加速）
set FLUTTER_STORAGE_BASE_URL=https://storage.flutter-io.cn
set PUB_HOSTED_URL=https://pub.flutter-io.cn
echo ✅ 已设置国内镜像
echo.

echo 步骤2：下载Flutter SDK（稳定版）
echo 正在从国内镜像下载Flutter SDK...
echo 如果下载慢，可以手动下载：
echo https://storage.flutter-io.cn/flutter_infra_release/releases/stable/windows/flutter_windows_3.16.0-stable.zip
echo.

echo 请手动下载并解压到 C:\flutter
echo.
echo 手动操作步骤：
echo 1. 点击上方链接下载ZIP文件
echo 2. 解压到 C:\flutter
echo 3. 将 C:\flutter\bin 添加到系统Path环境变量
echo 4. 重启命令行窗口
echo.

echo 步骤3：验证Flutter安装
where flutter
if %errorlevel% equ 0 (
    echo.
    echo ✅ Flutter已安装
    flutter --version
) else (
    echo.
    echo ❌ Flutter未找到
    echo 请按上面步骤手动安装
)
echo.

echo 步骤4：设置Android SDK路径
echo 检查ANDROID_HOME环境变量...
if "%ANDROID_HOME%"=="" (
    echo ❌ ANDROID_HOME未设置
    echo 正在尝试自动设置...
    
    rem 常见Android SDK路径
    set "SDK_PATHS=C:\Users\%USERNAME%\AppData\Local\Android\Sdk;C:\Android\Sdk;D:\Android\Sdk"
    
    for %%i in (%SDK_PATHS%) do (
        if exist "%%i\platform-tools\adb.exe" (
            set ANDROID_HOME=%%i
            echo ✅ 找到Android SDK: %%i
            goto :found_sdk
        )
    )
    
    echo ❌ 未找到Android SDK
    echo 请手动设置ANDROID_HOME环境变量
    echo 通常路径: C:\Users\%USERNAME%\AppData\Local\Android\Sdk
    goto :end
) else (
    echo ✅ ANDROID_HOME已设置: %ANDROID_HOME%
)

:found_sdk
echo.
echo 步骤5：运行Flutter环境检查
if not "%ANDROID_HOME%"=="" (
    echo 设置ANDROID_HOME环境变量...
    set ANDROID_HOME=%ANDROID_HOME%
    set PATH=%ANDROID_HOME%\platform-tools;%ANDROID_HOME%\tools;%ANDROID_HOME%\tools\bin;%PATH%
)

where flutter
if %errorlevel% equ 0 (
    echo.
    echo 运行flutter doctor...
    flutter doctor
) else (
    echo.
    echo ⚠️ 请先安装Flutter SDK
)

:end
echo.
echo ========================================
echo 安装说明：
echo 1. 下载Flutter SDK并解压到 C:\flutter
echo 2. 添加环境变量 Path: C:\flutter\bin
echo 3. 设置ANDROID_HOME指向Android SDK路径
echo 4. 运行 flutter doctor --android-licenses 接受许可
echo 5. 运行 python build_apk_simple.py 构建APK
echo ========================================
echo.
pause