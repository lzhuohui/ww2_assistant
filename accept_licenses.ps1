# 自动接受Android许可证的脚本
# 适用于Windows系统

Write-Host "=" -ForegroundColor Green -NoNewline
Write-Host " 自动接受Android许可证 " -ForegroundColor White -NoNewline
Write-Host "=" -ForegroundColor Green

# 设置Flutter路径
$flutterExe = "C:\flutter\flutter\bin\flutter.bat"

# 检查flutter.exe是否存在
if (-not (Test-Path $flutterExe)) {
    Write-Host "❌ Flutter可执行文件不存在: $flutterExe" -ForegroundColor Red
    exit 1
}

Write-Host "正在自动接受Android许可证..."
Write-Host "这可能需要几分钟时间..."

# 创建一个临时批处理文件来自动输入y
try {
    # 创建临时批处理文件
    $tempBatch = "$env:TEMP\accept_licenses.bat"
    $batchContent = @'
@echo off
REM 自动接受所有Android许可证

echo y | "C:\flutter\flutter\bin\flutter.bat" doctor --android-licenses
echo 许可证接受完成！
pause
'@
    
    Set-Content -Path $tempBatch -Value $batchContent -Encoding ASCII
    
    # 运行批处理文件
    Write-Host "运行自动许可证接受脚本..."
    Start-Process -FilePath "cmd.exe" -ArgumentList "/c $tempBatch" -Wait -NoNewWindow
    
    Write-Host "✅ 许可证接受脚本已执行" -ForegroundColor Green
    
    # 清理临时文件
    Remove-Item $tempBatch -Force -ErrorAction SilentlyContinue
    
} catch {
    Write-Host "❌ 执行过程中出现错误: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host "=" -ForegroundColor Green -NoNewline
Write-Host " 操作完成 " -ForegroundColor White -NoNewline
Write-Host "=" -ForegroundColor Green
Write-Host "现在可以运行 'python build_apk_full.py' 来构建APK了！"
