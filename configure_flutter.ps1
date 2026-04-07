# Final Flutter SDK configuration script
# For WW2 Assistant Project

Write-Host "=" -ForegroundColor Green -NoNewline
Write-Host " Flutter SDK Final Configuration " -ForegroundColor White -NoNewline
Write-Host "=" -ForegroundColor Green

# Set variables
$flutterDir = "C:\flutter\flutter"
$flutterBin = "${flutterDir}\bin"
$flutterExe = "${flutterBin}\flutter.exe"

# Check if flutter.exe exists
if (Test-Path $flutterExe) {
    Write-Host "✅ Found flutter.exe at: $flutterExe" -ForegroundColor Green
} else {
    Write-Host "❌ flutter.exe not found at: $flutterExe" -ForegroundColor Red
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

# Test Flutter command
Write-Host "Testing Flutter command..."
try {
    # Reload environment variables
    $env:PATH = [Environment]::GetEnvironmentVariable("PATH", "User") + ";" + [Environment]::GetEnvironmentVariable("PATH", "Machine")
    $env:FLUTTER_STORAGE_BASE_URL = [Environment]::GetEnvironmentVariable("FLUTTER_STORAGE_BASE_URL", "User")
    $env:PUB_HOSTED_URL = [Environment]::GetEnvironmentVariable("PUB_HOSTED_URL", "User")
    
    # Test flutter --version
    Write-Host "Running: flutter --version"
    $flutterVersionOutput = & $flutterExe --version
    Write-Host "✅ Flutter version information:"
    Write-Host $flutterVersionOutput
} catch {
    Write-Host "⚠️ Flutter command test failed, you may need to restart terminal" -ForegroundColor Yellow
    Write-Host "Error: $($_.Exception.Message)"
}

Write-Host "=" -ForegroundColor Green -NoNewline
Write-Host " Configuration Completed " -ForegroundColor White -NoNewline
Write-Host "=" -ForegroundColor Green
Write-Host "📋 Next steps:"
Write-Host "1. Restart terminal or computer to apply environment variables"
Write-Host "2. Run 'flutter doctor' to check environment"
Write-Host "3. Run 'flutter doctor --android-licenses' to accept licenses"
Write-Host "4. Then run 'python build_apk_full.py' to build APK"
Write-Host ""
Write-Host "💡 Flutter SDK is now ready!"
