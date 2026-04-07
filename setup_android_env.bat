@echo off
echo ========================================
echo 设置Android SDK环境变量
echo ========================================
echo.

echo 设置Android SDK路径：
set ANDROID_HOME=C:\Users\%USERNAME%\AppData\Local\Android\Sdk

echo.
echo 如果Android SDK安装在其他位置，请修改上面的路径
echo 常见的Android SDK安装位置：
echo   C:\Users\%USERNAME%\AppData\Local\Android\Sdk
echo   C:\Android\Sdk
echo   D:\Android\Sdk
echo.

echo 设置Path环境变量（仅当前窗口有效）：
set PATH=%ANDROID_HOME%\platform-tools;%ANDROID_HOME%\tools;%ANDROID_HOME%\tools\bin;%PATH%

echo.
echo 环境变量已设置：
echo ANDROID_HOME=%ANDROID_HOME%
echo.

echo 永久设置方法：
echo 1. 右键点击"此电脑" -> "属性"
echo 2. 点击"高级系统设置"
echo 3. 点击"环境变量"
echo 4. 在"系统变量"中点击"新建"
echo    变量名: ANDROID_HOME
echo    变量值: C:\Users\%USERNAME%\AppData\Local\Android\Sdk
echo 5. 编辑Path变量，添加：
echo     %%ANDROID_HOME%%\platform-tools
echo     %%ANDROID_HOME%%\tools
echo     %%ANDROID_HOME%%\tools\bin
echo.

echo 验证Android工具：
where adb
if %errorlevel% equ 0 (
    echo.
    echo ✅ ADB已找到
    adb --version
) else (
    echo.
    echo ❌ ADB未找到！
    echo 请确保：
    echo 1. 已安装Android Studio
    echo 2. 已通过SDK Manager安装Android SDK Platform-Tools
    echo 3. Android SDK路径正确
)

echo.
echo ========================================
echo 按任意键退出...
pause > nul