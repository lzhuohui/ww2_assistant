# Flutter SDK 自动安装脚本
# 适用于已安装Android Studio的用户

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Flutter SDK 自动安装脚本" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查是否以管理员权限运行
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "⚠️  建议以管理员权限运行此脚本" -ForegroundColor Yellow
    Write-Host "   右键点击 -> 以管理员身份运行" -ForegroundColor Yellow
    Write-Host ""
}

# 步骤1：检查当前环境
Write-Host "步骤1：检查当前环境..." -ForegroundColor Yellow

# 检查Flutter是否已安装
$flutterCmd = Get-Command flutter -ErrorAction SilentlyContinue
if ($flutterCmd) {
    Write-Host "✅ Flutter已安装" -ForegroundColor Green
    flutter --version
    exit 0
} else {
    Write-Host "❌ Flutter未安装" -ForegroundColor Red
}

# 检查Android SDK路径
$androidHome = $env:ANDROID_HOME
if (-not $androidHome) {
    $androidHome = $env:ANDROID_SDK_ROOT
}

if ($androidHome) {
    Write-Host "✅ 找到Android SDK: $androidHome" -ForegroundColor Green
} else {
    # 尝试自动查找Android SDK
    $commonPaths = @(
        "$env:USERPROFILE\AppData\Local\Android\Sdk",
        "C:\Android\Sdk",
        "D:\Android\Sdk",
        "C:\Program Files\Android\Sdk"
    )
    
    foreach ($path in $commonPaths) {
        if (Test-Path "$path\platform-tools\adb.exe") {
            $androidHome = $path
            Write-Host "✅ 自动找到Android SDK: $androidHome" -ForegroundColor Green
            break
        }
    }
    
    if (-not $androidHome) {
        Write-Host "❌ 未找到Android SDK" -ForegroundColor Red
        Write-Host "   请确保Android Studio已正确安装" -ForegroundColor Yellow
    }
}

# 步骤2：下载Flutter SDK
Write-Host ""
Write-Host "步骤2：下载Flutter SDK..." -ForegroundColor Yellow

$flutterUrl = "https://storage.flutter-io.cn/flutter_infra_release/releases/stable/windows/flutter_windows_3.16.0-stable.zip"
$downloadPath = "$env:TEMP\flutter_windows_3.16.0-stable.zip"
$installPath = "C:\flutter"

Write-Host "下载地址: $flutterUrl" -ForegroundColor Cyan
Write-Host "下载到: $downloadPath" -ForegroundColor Cyan
Write-Host "安装到: $installPath" -ForegroundColor Cyan

# 询问用户是否下载
$choice = Read-Host "是否自动下载Flutter SDK？(y/n)"
if ($choice -eq 'y') {
    try {
        Write-Host "开始下载Flutter SDK (约1.5GB)..." -ForegroundColor Yellow
        Write-Host "这可能需要几分钟，请耐心等待..." -ForegroundColor Yellow
        
        # 使用WebClient下载
        $webClient = New-Object System.Net.WebClient
        $webClient.DownloadFile($flutterUrl, $downloadPath)
        
        Write-Host "✅ 下载完成" -ForegroundColor Green
        
        # 解压
        Write-Host "解压到 $installPath..." -ForegroundColor Yellow
        if (Test-Path $installPath) {
            Remove-Item $installPath -Recurse -Force -ErrorAction SilentlyContinue
        }
        
        Add-Type -AssemblyName System.IO.Compression.FileSystem
        [System.IO.Compression.ZipFile]::ExtractToDirectory($downloadPath, $installPath)
        
        Write-Host "✅ 解压完成" -ForegroundColor Green
        
        # 清理临时文件
        Remove-Item $downloadPath -ErrorAction SilentlyContinue
        
    } catch {
        Write-Host "❌ 下载失败: $_" -ForegroundColor Red
        Write-Host "请手动下载并解压到 C:\flutter" -ForegroundColor Yellow
    }
} else {
    Write-Host "请手动下载并解压到 C:\flutter" -ForegroundColor Yellow
}

# 步骤3：设置环境变量
Write-Host ""
Write-Host "步骤3：设置环境变量..." -ForegroundColor Yellow

if (Test-Path $installPath) {
    # 设置用户环境变量
    $userPath = [Environment]::GetEnvironmentVariable("Path", "User")
    $flutterBin = "$installPath\bin"
    
    if ($userPath -notlike "*$flutterBin*") {
        [Environment]::SetEnvironmentVariable("Path", "$userPath;$flutterBin", "User")
        Write-Host "✅ 已添加Flutter到用户Path环境变量" -ForegroundColor Green
    }
    
    # 设置Flutter镜像环境变量
    [Environment]::SetEnvironmentVariable("FLUTTER_STORAGE_BASE_URL", "https://storage.flutter-io.cn", "User")
    [Environment]::SetEnvironmentVariable("PUB_HOSTED_URL", "https://pub.flutter-io.cn", "User")
    
    Write-Host "✅ 已设置Flutter国内镜像" -ForegroundColor Green
    
    if ($androidHome) {
        [Environment]::SetEnvironmentVariable("ANDROID_HOME", $androidHome, "User")
        Write-Host "✅ 已设置ANDROID_HOME: $androidHome" -ForegroundColor Green
    }
    
    Write-Host "环境变量将在下次启动命令行时生效" -ForegroundColor Yellow
    Write-Host "要立即生效，请重启命令行窗口" -ForegroundColor Yellow
} else {
    Write-Host "❌ Flutter SDK未找到，请先安装" -ForegroundColor Red
}

# 步骤4：验证安装
Write-Host ""
Write-Host "步骤4：验证安装..." -ForegroundColor Yellow

if (Test-Path "$installPath\bin\flutter.bat") {
    # 设置临时环境变量
    $env:Path = "$installPath\bin;$env:Path"
    $env:FLUTTER_STORAGE_BASE_URL = "https://storage.flutter-io.cn"
    $env:PUB_HOSTED_URL = "https://pub.flutter-io.cn"
    
    if ($androidHome) {
        $env:ANDROID_HOME = $androidHome
        $env:Path = "$androidHome\platform-tools;$androidHome\tools;$androidHome\tools\bin;$env:Path"
    }
    
    Write-Host "运行flutter --version..." -ForegroundColor Cyan
    & "$installPath\bin\flutter.bat" --version
    
    Write-Host ""
    Write-Host "运行flutter doctor..." -ForegroundColor Cyan
    & "$installPath\bin\flutter.bat" doctor
    
    Write-Host ""
    Write-Host "重要：运行以下命令接受Android许可：" -ForegroundColor Yellow
    Write-Host "flutter doctor --android-licenses" -ForegroundColor White
    Write-Host "对所有问题输入 y" -ForegroundColor White
} else {
    Write-Host "❌ Flutter SDK未正确安装" -ForegroundColor Red
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "安装完成！" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "下一步操作：" -ForegroundColor Yellow
Write-Host "1. 重启命令行窗口" -ForegroundColor White
Write-Host "2. 运行: flutter doctor --android-licenses" -ForegroundColor White
Write-Host "3. 运行: python build_apk_simple.py" -ForegroundColor White
Write-Host ""
Write-Host "按Enter键退出..."
Read-Host