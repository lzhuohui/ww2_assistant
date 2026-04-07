# Flutter SDK Installation Script for Windows
# For WW2 Assistant Project

Write-Host "=" -ForegroundColor Green -NoNewline
Write-Host " Flutter SDK Installation Script " -ForegroundColor White -NoNewline
Write-Host "=" -ForegroundColor Green
Write-Host "Installing Flutter SDK for WW2 Assistant project..."

# Set variables
$flutterVersion = "3.41.2"
$flutterZip = "flutter_windows_${flutterVersion}-stable.zip"
$flutterUrl = "https://storage.flutter-io.cn/flutter_infra_release/releases/stable/windows/${flutterZip}"
$installDir = "C:\flutter"
$flutterBin = "${installDir}\bin"

# Create installation directory
if (-not (Test-Path $installDir)) {
    Write-Host "Creating Flutter installation directory: $installDir"
    New-Item -ItemType Directory -Path $installDir -Force | Out-Null
}

# Download Flutter SDK
$zipPath = "${installDir}\${flutterZip}"
Write-Host "Downloading Flutter SDK ${flutterVersion}..."
Write-Host "Download URL: $flutterUrl"

try {
    Invoke-WebRequest -Uri $flutterUrl -OutFile $zipPath -ErrorAction Stop
    Write-Host "✅ Download completed!" -ForegroundColor Green
} catch {
    Write-Host "❌ Download failed: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Extract Flutter SDK
Write-Host "Extracting Flutter SDK..."
try {
    Expand-Archive -Path $zipPath -DestinationPath $installDir -Force
    Write-Host "✅ Extraction completed!" -ForegroundColor Green
} catch {
    Write-Host "❌ Extraction failed: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Clean up temporary files
Remove-Item $zipPath -Force -ErrorAction SilentlyContinue

# Check if Flutter is installed successfully
$flutterExe = "${flutterBin}\flutter.exe"
if (Test-Path $flutterExe) {
    Write-Host "✅ Flutter SDK installed successfully!" -ForegroundColor Green
    Write-Host "Flutter path: $flutterBin"
} else {
    Write-Host "❌ Flutter SDK installation failed, flutter.exe not found" -ForegroundColor Red
    exit 1
}

# Set environment variables
Write-Host "Setting environment variables..."

# Set FLUTTER_STORAGE_BASE_URL
[Environment]::SetEnvironmentVariable("FLUTTER_STORAGE_BASE_URL", "https://storage.flutter-io.cn", "User")

# Set PUB_HOSTED_URL
[Environment]::SetEnvironmentVariable("PUB_HOSTED_URL", "https://pub.flutter-io.cn", "User")

# Add Flutter to PATH environment variable
$currentPath = [Environment]::GetEnvironmentVariable("PATH", "User")
if (-not $currentPath.Contains($flutterBin)) {
    $newPath = "${currentPath};${flutterBin}"
    [Environment]::SetEnvironmentVariable("PATH", $newPath, "User")
    Write-Host "✅ Added Flutter to PATH environment variable" -ForegroundColor Green
} else {
    Write-Host "⚠️ Flutter is already in PATH environment variable" -ForegroundColor Yellow
}

# Verify environment variable settings
Write-Host "Verifying environment variable settings..."
Write-Host "FLUTTER_STORAGE_BASE_URL: $(Get-ChildItem Env:FLUTTER_STORAGE_BASE_URL)"
Write-Host "PUB_HOSTED_URL: $(Get-ChildItem Env:PUB_HOSTED_URL)"
Write-Host "PATH contains Flutter: $($env:PATH.Contains($flutterBin))"

# Test Flutter command
Write-Host "Testing Flutter command..."
try {
    # Reload environment variables
    $env:PATH = [Environment]::GetEnvironmentVariable("PATH", "User") + ";" + [Environment]::GetEnvironmentVariable("PATH", "Machine")
    $env:FLUTTER_STORAGE_BASE_URL = [Environment]::GetEnvironmentVariable("FLUTTER_STORAGE_BASE_URL", "User")
    $env:PUB_HOSTED_URL = [Environment]::GetEnvironmentVariable("PUB_HOSTED_URL", "User")
    
    # Test flutter --version
    $flutterVersionOutput = & "${flutterBin}\flutter.exe" --version
    Write-Host "✅ Flutter version information:"
    Write-Host $flutterVersionOutput
} catch {
    Write-Host "⚠️ Flutter command test failed, you may need to restart terminal" -ForegroundColor Yellow
    Write-Host "Error: $($_.Exception.Message)"
}

Write-Host "=" -ForegroundColor Green -NoNewline
Write-Host " Installation Completed " -ForegroundColor White -NoNewline
Write-Host "=" -ForegroundColor Green
Write-Host "📋 Next steps:"
Write-Host "1. Restart terminal or computer to apply environment variables"
Write-Host "2. Run 'flutter doctor' to check environment"
Write-Host "3. Run 'flutter doctor --android-licenses' to accept licenses"
Write-Host "4. Then run 'python build_apk_full.py' to build APK"
Write-Host ""
Write-Host "💡 Note: If you're using PowerShell, you may need to run this script as administrator"
