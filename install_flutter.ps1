# 下载并安装Flutter SDK的PowerShell脚本
# 适用于Windows系统

Write-Host "=" -ForegroundColor Green -NoNewline
Write-Host " Flutter SDK 安装脚本 " -ForegroundColor White -NoNewline
Write-Host "=" -ForegroundColor Green
Write-Host "正在为二战风云项目安装Flutter SDK..."

# 设置变量
$flutterVersion = "3.41.2"
$flutterZip = "flutter_windows_${flutterVersion}-stable.zip"
$flutterUrl = "https://storage.flutter-io.cn/flutter_infra_release/releases/stable/windows/${flutterZip}"
$installDir = "C:\flutter"
$flutterBin = "${installDir}\bin"

# 创建安装目录
if (-not (Test-Path $installDir)) {
    Write-Host "创建Flutter安装目录: $installDir"
    New-Item -ItemType Directory -Path $installDir -Force | Out-Null
}

# 下载Flutter SDK
$zipPath = "${installDir}\${flutterZip}"
Write-Host "正在下载Flutter SDK ${flutterVersion}..."
Write-Host "下载地址: $flutterUrl"

try {
    Invoke-WebRequest -Uri $flutterUrl -OutFile $zipPath -ErrorAction Stop
    Write-Host "✅ 下载完成!" -ForegroundColor Green
} catch {
    Write-Host "❌ 下载失败: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# 解压Flutter SDK
Write-Host "正在解压Flutter SDK..."
try {
    Expand-Archive -Path $zipPath -DestinationPath $installDir -Force
    Write-Host "✅ 解压完成!" -ForegroundColor Green
} catch {
    Write-Host "❌ 解压失败: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# 清理临时文件
Remove-Item $zipPath -Force -ErrorAction SilentlyContinue

# 检查Flutter是否安装成功
$flutterExe = "${flutterBin}\flutter.exe"
if (Test-Path $flutterExe) {
    Write-Host "✅ Flutter SDK 安装成功!" -ForegroundColor Green
    Write-Host "Flutter 路径: $flutterBin"
} else {
    Write-Host "❌ Flutter SDK 安装失败，未找到flutter.exe" -ForegroundColor Red
    exit 1
}

# 设置环境变量
Write-Host "正在设置环境变量..."

# 设置FLUTTER_STORAGE_BASE_URL
[Environment]::SetEnvironmentVariable("FLUTTER_STORAGE_BASE_URL", "https://storage.flutter-io.cn", "User")

# 设置PUB_HOSTED_URL
[Environment]::SetEnvironmentVariable("PUB_HOSTED_URL", "https://pub.flutter-io.cn", "User")

# 将Flutter添加到PATH环境变量
$currentPath = [Environment]::GetEnvironmentVariable("PATH", "User")
if (-not $currentPath.Contains($flutterBin)) {
    $newPath = "${currentPath};${flutterBin}"
    [Environment]::SetEnvironmentVariable("PATH", $newPath, "User")
    Write-Host "✅ 已将Flutter添加到PATH环境变量" -ForegroundColor Green
} else {
    Write-Host "⚠️ Flutter已在PATH环境变量中" -ForegroundColor Yellow
}

# 验证环境变量设置
Write-Host "验证环境变量设置..."
Write-Host "FLUTTER_STORAGE_BASE_URL: $(Get-ChildItem Env:FLUTTER_STORAGE_BASE_URL)"
Write-Host "PUB_HOSTED_URL: $(Get-ChildItem Env:PUB_HOSTED_URL)"
Write-Host "PATH包含Flutter: $($env:PATH.Contains($flutterBin))"

# 测试Flutter命令
Write-Host "正在测试Flutter命令..."
try {
    # 重新加载环境变量
    $env:PATH = [Environment]::GetEnvironmentVariable("PATH", "User") + ";" + [Environment]::GetEnvironmentVariable("PATH", "Machine")
    $env:FLUTTER_STORAGE_BASE_URL = [Environment]::GetEnvironmentVariable("FLUTTER_STORAGE_BASE_URL", "User")
    $env:PUB_HOSTED_URL = [Environment]::GetEnvironmentVariable("PUB_HOSTED_URL", "User")
    
    # 测试flutter --version
    $flutterVersionOutput = & "${flutterBin}\flutter.exe" --version
    Write-Host "✅ Flutter版本信息:"
    Write-Host $flutterVersionOutput
} catch {
    Write-Host "⚠️ 测试Flutter命令失败，可能需要重启终端" -ForegroundColor Yellow
    Write-Host "错误: $($_.Exception.Message)"
}

Write-Host "=" -ForegroundColor Green -NoNewline
Write-Host " 安装完成 " -ForegroundColor White -NoNewline
Write-Host "=" -ForegroundColor Green
Write-Host "📋 下一步操作:"
Write-Host "1. 重启终端或电脑以应用环境变量"
Write-Host "2. 运行 'flutter doctor' 检查环境"
Write-Host "3. 运行 'flutter doctor --android-licenses' 接受许可"
Write-Host "4. 然后运行 'python build_apk_full.py' 构建APK"
Write-Host ""
Write-Host "💡 提示: 如果你使用PowerShell，可能需要以管理员身份运行此脚本"
