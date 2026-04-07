@echo off
echo ========================================
echo Flutter安装验证脚本
echo ========================================
echo.

echo 步骤1：检查Flutter是否在Path中
where flutter >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Flutter命令找到
) else (
    echo ❌ Flutter命令未找到
    echo   请检查：
    echo   1. 是否解压到 C:\flutter
    echo   2. 是否添加了 C:\flutter\bin 到Path
    echo   3. 是否重启了命令行窗口
    goto :end
)

echo.
echo 步骤2：检查Flutter版本
flutter --version
if %errorlevel% neq 0 (
    echo ❌ Flutter版本检查失败
    goto :end
)

echo.
echo 步骤3：检查环境变量
echo FLUTTER_STORAGE_BASE_URL=%FLUTTER_STORAGE_BASE_URL%
echo PUB_HOSTED_URL=%PUB_HOSTED_URL%
echo ANDROID_HOME=%ANDROID_HOME%

echo.
echo 步骤4：运行flutter doctor（这可能需要一些时间）
flutter doctor

echo.
echo 步骤5：检查Android许可
echo 如果需要，运行：flutter doctor --android-licenses
echo 对所有问题输入 y

echo.
echo ========================================
echo 如果所有检查都通过✅，可以开始构建APK：
echo.
echo cd "C:\Users\chmm1\Documents\二战风云"
echo python build_apk_simple.py
echo ========================================

:end
echo.
pause