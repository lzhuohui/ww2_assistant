@echo off

echo =====================================
echo Flutter SDK 环境变量设置
set "FLUTTER_HOME=C:\flutter\flutter"
set "FLUTTER_BIN=%FLUTTER_HOME%\bin"

echo 设置 FLUTTER_HOME=%FLUTTER_HOME%
echo 设置 FLUTTER_STORAGE_BASE_URL=https://storage.flutter-io.cn
echo 设置 PUB_HOSTED_URL=https://pub.flutter-io.cn

:: 设置用户环境变量
setx FLUTTER_HOME "%FLUTTER_HOME%"
setx FLUTTER_STORAGE_BASE_URL "https://storage.flutter-io.cn"
setx PUB_HOSTED_URL "https://pub.flutter-io.cn"

:: 检查PATH环境变量是否已包含Flutter
echo 检查PATH环境变量...
for /f "tokens=*" %%a in ('reg query "HKCU\Environment" /v PATH ^| findstr "PATH"') do set "CURRENT_PATH=%%a"

:: 提取实际的PATH值
set "CURRENT_PATH=%CURRENT_PATH:*REG_SZ    =%"

:: 检查Flutter是否在PATH中
if not "%CURRENT_PATH%" == "%CURRENT_PATH:%FLUTTER_BIN%=%" (
    echo Flutter已经在PATH环境变量中
) else (
    echo 将Flutter添加到PATH环境变量...
    setx PATH "%CURRENT_PATH%;%FLUTTER_BIN%"
)

echo =====================================
echo 环境变量设置完成！
echo =====================================
echo 下一步操作：
echo 1. 重启终端或电脑以应用环境变量
echo 2. 运行 'flutter doctor' 检查环境
echo 3. 运行 'flutter doctor --android-licenses' 接受许可
echo 4. 然后运行 'python build_apk_full.py' 构建APK
echo =====================================

:: 测试Flutter命令
echo 测试Flutter命令...
"%FLUTTER_BIN%\flutter.bat" --version

echo =====================================
echo Flutter SDK 安装完成！
echo =====================================
pause
