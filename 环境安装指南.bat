@echo off
echo ========================================
echo Flet APK构建环境安装指南
echo ========================================
echo.

echo 检测到需要安装以下组件：
echo 1. ❌ Flutter SDK
echo 2. ❌ Java JDK
echo 3. ❌ Android SDK
echo.

echo 请按以下步骤操作：
echo.

echo ========================================
echo 步骤1：安装Flutter SDK
echo ========================================
echo.
echo 方法A：使用国内镜像（推荐）
echo 下载地址: https://flutter.cn/community/china
echo 或直接下载: https://storage.flutter-io.cn/flutter_infra_release/releases/stable/windows/flutter_windows_3.16.0-stable.zip
echo.
echo 安装步骤：
echo   1. 下载 flutter_windows_3.16.0-stable.zip
echo   2. 解压到 C:\flutter
echo   3. 将 C:\flutter\bin 添加到系统Path环境变量
echo   4. 设置国内镜像环境变量（可选但推荐）：
echo      FLUTTER_STORAGE_BASE_URL=https://storage.flutter-io.cn
echo      PUB_HOSTED_URL=https://pub.flutter-io.cn
echo.
pause

echo.
echo ========================================
echo 步骤2：安装Java JDK
echo ========================================
echo.
echo 下载地址: https://www.oracle.com/java/technologies/downloads/
echo 或使用OpenJDK: https://adoptium.net/temurin/releases/
echo.
echo 安装步骤：
echo   1. 下载JDK 11或更高版本
echo   2. 运行安装程序
echo   3. 设置JAVA_HOME环境变量指向JDK安装目录
echo   4. 将 %%JAVA_HOME%%\bin 添加到系统Path环境变量
echo.
pause

echo.
echo ========================================
echo 步骤3：安装Android Studio和SDK
echo ========================================
echo.
echo 下载地址: https://developer.android.com/studio
echo.
echo 安装步骤：
echo   1. 下载Android Studio安装程序
echo   2. 运行安装程序，选择以下组件：
echo      - Android SDK
echo      - Android SDK Platform
echo      - Android Virtual Device（可选）
echo   3. 安装完成后，打开Android Studio
echo   4. 点击 Configure -> SDK Manager
echo   5. 安装 Android SDK Platform 33 或更高版本
echo   6. 安装 Android SDK Build-Tools 33.0.0 或更高版本
echo   7. 设置环境变量：
echo      ANDROID_HOME = C:\Users\%USERNAME%\AppData\Local\Android\Sdk
echo.
pause

echo.
echo ========================================
echo 步骤4：验证安装
echo ========================================
echo.
echo 安装完成后，运行以下命令验证：
echo.
echo 1. 验证Java:
echo    java -version
echo.
echo 2. 验证Flutter:
echo    先运行: setup_flutter_env.bat
echo    然后运行: flutter --version
echo.
echo 3. 验证Android SDK:
echo    先运行: setup_android_env.bat
echo    然后运行: adb --version
echo.
echo 4. 完整环境检查:
echo    flutter doctor
echo.
pause

echo.
echo ========================================
echo 步骤5：接受Android许可
echo ========================================
echo.
echo 安装完成后，需要接受Android SDK许可：
echo   flutter doctor --android-licenses
echo   对所有问题输入 y 接受
echo.
pause

echo.
echo ========================================
echo 快速开始脚本
echo ========================================
echo.
echo 已创建以下脚本帮助你：
echo.
echo 1. setup_flutter_env.bat    - 设置Flutter国内镜像
echo 2. setup_android_env.bat    - 设置Android SDK环境变量
echo 3. verify_environment.bat   - 验证环境安装
echo 4. accept_licenses.bat      - 接受Android许可
echo.
echo 请按顺序运行这些脚本！
echo ========================================
pause