# Flet APK构建环境验证脚本（PowerShell版本）

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "环境验证脚本" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 1. 验证Java安装
Write-Host "1. 验证Java安装..." -ForegroundColor Yellow
$javaCmd = Get-Command java -ErrorAction SilentlyContinue
if ($javaCmd) {
    Write-Host "✅ Java已安装" -ForegroundColor Green
    java -version
} else {
    Write-Host "❌ Java未安装" -ForegroundColor Red
    Write-Host "请安装Java JDK 11+" -ForegroundColor Yellow
    Write-Host "下载地址: https://www.oracle.com/java/technologies/downloads/" -ForegroundColor Yellow
}
Write-Host ""

# 2. 验证Flutter安装
Write-Host "2. 验证Flutter安装..." -ForegroundColor Yellow
$flutterCmd = Get-Command flutter -ErrorAction SilentlyContinue
if ($flutterCmd) {
    Write-Host "✅ Flutter已安装" -ForegroundColor Green
    # 设置国内镜像
    $env:FLUTTER_STORAGE_BASE_URL = "https://storage.flutter-io.cn"
    $env:PUB_HOSTED_URL = "https://pub.flutter-io.cn"
    flutter --version
} else {
    Write-Host "❌ Flutter未安装" -ForegroundColor Red
    Write-Host "请安装Flutter SDK：" -ForegroundColor Yellow
    Write-Host "1. 下载: https://flutter.cn/community/china" -ForegroundColor Yellow
    Write-Host "2. 解压到 C:\flutter" -ForegroundColor Yellow
    Write-Host "3. 将 C:\flutter\bin 添加到Path" -ForegroundColor Yellow
    Write-Host "4. 设置国内镜像环境变量：" -ForegroundColor Yellow
    Write-Host "   FLUTTER_STORAGE_BASE_URL=https://storage.flutter-io.cn" -ForegroundColor Yellow
    Write-Host "   PUB_HOSTED_URL=https://pub.flutter-io.cn" -ForegroundColor Yellow
}
Write-Host ""

# 3. 验证Android SDK安装
Write-Host "3. 验证Android SDK安装..." -ForegroundColor Yellow
$androidHome = $env:ANDROID_HOME
if (-not $androidHome) {
    $androidHome = $env:ANDROID_SDK_ROOT
}

if ($androidHome) {
    Write-Host "✅ ANDROID_HOME: $androidHome" -ForegroundColor Green
    
    # 检查adb
    $adbPath = Join-Path $androidHome "platform-tools\adb.exe"
    if (Test-Path $adbPath) {
        Write-Host "✅ Android SDK工具已安装" -ForegroundColor Green
        & $adbPath --version
    } else {
        Write-Host "❌ Android SDK工具未找到" -ForegroundColor Red
        Write-Host "请通过Android Studio安装Android SDK Platform-Tools" -ForegroundColor Yellow
    }
} else {
    Write-Host "❌ ANDROID_HOME未设置" -ForegroundColor Red
    Write-Host "请安装Android Studio和SDK" -ForegroundColor Yellow
    Write-Host "下载地址: https://developer.android.com/studio" -ForegroundColor Yellow
    Write-Host "安装后设置环境变量: ANDROID_HOME = C:\Users\$env:USERNAME\AppData\Local\Android\Sdk" -ForegroundColor Yellow
}
Write-Host ""

# 4. 运行Flutter环境检查
Write-Host "4. 运行Flutter环境检查..." -ForegroundColor Yellow
if ($flutterCmd) {
    # 设置国内镜像
    $env:FLUTTER_STORAGE_BASE_URL = "https://storage.flutter-io.cn"
    $env:PUB_HOSTED_URL = "https://pub.flutter-io.cn"
    
    Write-Host "运行flutter doctor..." -ForegroundColor Cyan
    flutter doctor
} else {
    Write-Host "⚠️ Flutter未安装，跳过环境检查" -ForegroundColor Yellow
}
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "环境验证完成！" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if ($javaCmd -and $flutterCmd -and $androidHome) {
    Write-Host "🎉 所有检查都通过！可以开始构建APK了！" -ForegroundColor Green
    Write-Host ""
    Write-Host "运行以下命令构建APK：" -ForegroundColor Yellow
    Write-Host "  python build_apk_simple.py" -ForegroundColor White
    Write-Host "或" -ForegroundColor Yellow
    Write-Host "  python build_apk_full.py" -ForegroundColor White
} else {
    Write-Host "⚠️  部分环境未安装完成" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "请先安装缺失的组件：" -ForegroundColor Yellow
    if (-not $javaCmd) {
        Write-Host "  - Java JDK" -ForegroundColor Red
    }
    if (-not $flutterCmd) {
        Write-Host "  - Flutter SDK" -ForegroundColor Red
    }
    if (-not $androidHome) {
        Write-Host "  - Android SDK" -ForegroundColor Red
    }
    Write-Host ""
    Write-Host "查看 download_links.html 获取下载链接" -ForegroundColor Yellow
    Write-Host "运行 环境安装指南.bat 获取安装说明" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "按任意键退出..."
pause