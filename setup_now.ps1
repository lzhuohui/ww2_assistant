# 立即设置环境并检查

Write-Host "🚀 立即设置构建环境" -ForegroundColor Cyan
Write-Host "="*50 -ForegroundColor Cyan
Write-Host ""

# 1. 设置Android SDK路径
$androidHome = "C:\Users\$env:USERNAME\AppData\Local\Android\Sdk"
if (Test-Path "$androidHome\platform-tools\adb.exe") {
    Write-Host "✅ 找到Android SDK: $androidHome" -ForegroundColor Green
    $env:ANDROID_HOME = $androidHome
    $env:Path = "$androidHome\platform-tools;$androidHome\tools;$env:Path"
    
    # 尝试设置JAVA_HOME（Android Studio自带Java）
    $javaPaths = @(
        "$androidHome\jre",
        "$androidHome\jbr",
        "C:\Program Files\Android\Android Studio\jbr",
        "C:\Program Files\Android\Android Studio\jre"
    )
    
    foreach ($path in $javaPaths) {
        if (Test-Path "$path\bin\java.exe") {
            $env:JAVA_HOME = $path
            $env:Path = "$path\bin;$env:Path"
            Write-Host "✅ 找到Java: $path" -ForegroundColor Green
            break
        }
    }
} else {
    Write-Host "❌ Android SDK未找到" -ForegroundColor Red
    Write-Host "  请确保Android Studio已正确安装" -ForegroundColor Yellow
}

# 2. 检查Flutter
Write-Host ""
Write-Host "检查Flutter安装..." -ForegroundColor Yellow
$flutterPath = "C:\flutter\bin\flutter.bat"
if (Test-Path $flutterPath) {
    Write-Host "✅ Flutter已安装: C:\flutter" -ForegroundColor Green
    $env:Path = "C:\flutter\bin;$env:Path"
    
    # 设置国内镜像
    $env:FLUTTER_STORAGE_BASE_URL = "https://storage.flutter-io.cn"
    $env:PUB_HOSTED_URL = "https://pub.flutter-io.cn"
    
    Write-Host "运行Flutter版本检查..." -ForegroundColor Cyan
    & $flutterPath --version
} else {
    Write-Host "❌ Flutter未安装" -ForegroundColor Red
    Write-Host ""
    Write-Host "📥 请下载Flutter SDK：" -ForegroundColor Yellow
    Write-Host "   1. 下载: https://storage.flutter-io.cn/flutter_infra_release/releases/stable/windows/flutter_windows_3.16.0-stable.zip" -ForegroundColor White
    Write-Host "   2. 解压到: C:\flutter" -ForegroundColor White
    Write-Host "   3. 重启命令行窗口" -ForegroundColor White
}

# 3. 检查当前环境
Write-Host ""
Write-Host "="*50 -ForegroundColor Cyan
Write-Host "当前环境状态：" -ForegroundColor Cyan
Write-Host "="*50 -ForegroundColor Cyan

# 检查Java
Write-Host "Java: " -NoNewline
try {
    $java = Get-Command java -ErrorAction Stop
    java -version 2>&1 | Select-Object -First 1
} catch {
    Write-Host "未找到" -ForegroundColor Red
}

# 检查Flutter
Write-Host "Flutter: " -NoNewline
try {
    $flutter = Get-Command flutter -ErrorAction Stop
    & $flutter.Source --version 2>&1 | Select-Object -First 1
} catch {
    Write-Host "未找到" -ForegroundColor Red
}

# 检查ADB
Write-Host "ADB: " -NoNewline
try {
    $adb = Get-Command adb -ErrorAction Stop
    & $adb.Source --version 2>&1 | Select-Object -First 1
} catch {
    Write-Host "未找到" -ForegroundColor Red
}

Write-Host ""
Write-Host "="*50 -ForegroundColor Cyan
Write-Host "下一步操作：" -ForegroundColor Yellow
Write-Host "="*50 -ForegroundColor Cyan

if (Test-Path $flutterPath) {
    Write-Host "✅ Flutter已安装，可以尝试构建APK" -ForegroundColor Green
    Write-Host ""
    Write-Host "运行以下命令构建APK：" -ForegroundColor White
    Write-Host "   python build_apk_simple.py" -ForegroundColor Green
} else {
    Write-Host "❌ 需要先安装Flutter SDK" -ForegroundColor Red
    Write-Host ""
    Write-Host "最简单的安装方法：" -ForegroundColor Yellow
    Write-Host "   1. 下载上面的ZIP文件" -ForegroundColor White
    Write-Host "   2. 解压到 C:\flutter" -ForegroundColor White
    Write-Host "   3. 运行这个脚本 again" -ForegroundColor White
}

Write-Host ""
Write-Host "按Enter键继续..."
Read-Host